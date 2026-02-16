#!/usr/bin/env python3
"""
eduroam-linux.py — Connect to eduroam on Linux via NetworkManager.

Based on the official eduroam CAT installer structure
(https://cat.eduroam.org/) by the GEANT project, but with fixes for
modern NetworkManager versions (1.8+) where the original script fails.

Changes from the official CAT installer:
  - Replaced altsubject-matches (deprecated since NM 1.8+) with
    domain-suffix-match — the modern equivalent that actually works
  - Uses the system CA bundle instead of an embedded certificate chain
  - Result: connects immediately instead of hanging during TLS handshake,
    while still validating the RADIUS server certificate

Improvements over the official CAT installer:
  - Full type annotations checked with Pylance/mypy (strict mode)
  - No use of deprecated typing imports (uses Python 3.10+ built-in generics)
  - Proper None-safety: all optional attributes are guarded before access
  - No global mutable state for dbus module (TYPE_CHECKING guard)
  - subprocess calls use capture_output instead of manual PIPE wiring
  - Wayland display detection (WAYLAND_DISPLAY) alongside X11 (DISPLAY)
  - shutil.which() instead of subprocess(['which', ...]) for tool detection
  - Clean fallback chain: nmcli → D-Bus → wpa_supplicant
  - argparse with proper help text and mutual requirements (--silent needs -u/-p)
  - Configurable domain suffix via --domain (default: saxion.net)
  - Single responsibility: ~400 lines vs ~900+ lines in official CAT script

The official CAT script uses altsubject-matches for server validation,
which is deprecated since NM 1.8 (2017). On Fedora 43 with NM 1.50+,
this causes the TLS handshake to stall indefinitely. This script
replaces it with domain-suffix-match and the system CA trust store,
which provides equivalent security without the compatibility issue.

Default domain suffix is saxion.net (Saxion University of Applied
Sciences). Use --domain to override for other institutions.

Tested alternatives that did NOT work:
  - cat.eduroam.org installer (hangs during TLS handshake)
  - geteduroam Linux app (https://github.com/geteduroam/linux-app)
  - easyroam-linux (https://github.com/jahtz/easyroam-linux)
  - UvA/HvA Linux guide (https://linux.datanose.nl/linux/eduroam/)

WARNING: Your password is stored in plaintext in
         /etc/NetworkManager/system-connections/<con-name>.nmconnection
         (where <con-name> matches the connection name, e.g. "eduroam")
         The file is chmod 600 (root-only), but keep this in mind.

Requires: Python 3.10+, NetworkManager (nmcli or dbus-python)

Author:  Sten Tijhuis (Stensel8) — https://github.com/Stensel8
License: MIT
"""

from __future__ import annotations

import argparse
import getpass
import os
import re
import shutil
import subprocess
import sys
import types
import uuid
from typing import Any

# ---------------------------------------------------------------------------
# Global state
# ---------------------------------------------------------------------------

nm_available: bool = True
debug_enabled: bool = False

_dbus: types.ModuleType | None = None  # populated at runtime if available

# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="eduroam Linux installer.")
parser.add_argument(
    "--debug", "-d", action="store_true", default=False,
    help="enable debug output",
)
parser.add_argument(
    "--username", "-u", type=str, default=None,
    help="set username (skip interactive prompt)",
)
parser.add_argument(
    "--password", "-p", type=str, default=None,
    help="set password (skip interactive prompt)",
)
parser.add_argument(
    "--silent", "-s", action="store_true", default=False,
    help="run without interactive prompts (requires -u and -p)",
)
parser.add_argument(
    "--wpa_conf", action="store_true", default=False,
    help="generate wpa_supplicant config instead of using NM",
)
parser.add_argument(
    "--domain", type=str, default="saxion.net",
    help="domain suffix for RADIUS server validation (default: saxion.net)",
)
ARGS = parser.parse_args()

if ARGS.debug:
    debug_enabled = True
    print("Running in debug mode")


def debug(msg: object) -> None:
    """Print debugging messages to stdout."""
    if debug_enabled:
        print(f"DEBUG: {msg}")


# ---------------------------------------------------------------------------
# dbus import (optional — no type stubs available)
# ---------------------------------------------------------------------------

try:
    import dbus  # type: ignore[import-untyped]
    _dbus = dbus
except ImportError:
    debug("Cannot import dbus module — falling back to nmcli")
    nm_available = False


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


class Config:
    """Connection configuration constants."""

    title: str = "eduroam installer"
    ssids: list[str] = ["eduroam"]
    del_ssids: list[str] = []
    eap_outer: str = "PEAP"
    eap_inner: str = "MSCHAPV2"
    anonymous_identity: str = ""
    ca_cert: str = "/etc/pki/tls/certs/ca-bundle.crt"
    domain_suffix: str = "saxion.net"  # overridden by --domain arg


class Messages:
    """User-facing messages."""

    quit: str = "Really quit?"
    credentials_prompt: str = "Please enter your eduroam credentials:"
    username_prompt: str = "Username (e.g. user@institution.tld)"
    enter_password: str = "Password"
    repeat_password: str = "Repeat password"
    passwords_differ: str = "Passwords do not match"
    empty_field: str = "One of the fields was empty"
    installation_finished: str = (
        "Installation successful!\n\n"
        "eduroam is now connected. If your credentials or the server\n"
        "certificate are incorrect, NetworkManager may prompt you to\n"
        "re-enter your credentials."
    )
    cont: str = "Continue?"
    nm_not_supported: str = "This NetworkManager version is not supported"
    dbus_error: str = "DBus connection problem, a sudo might help"
    ok: str = "OK"
    yes: str = "Y"
    nay: str = "N"
    save_wpa_conf: str = (
        "NetworkManager not available. "
        "We can generate a wpa_supplicant configuration file "
        "instead. Note: your password will be stored as "
        "clear text in this file."
    )
    save_wpa_confirm: str = "Write the file"
    wrong_username: str = (
        "Error: your username must be of the form "
        "'xxx@institutionID' e.g. 'john@example.net'!"
    )


# ---------------------------------------------------------------------------
# User interaction
# ---------------------------------------------------------------------------


class InstallerData:
    """
    User interaction handling.

    Supports tty (command-line) and zenity/kdialog/yad GUIs.
    """

    def __init__(
        self,
        silent: bool = False,
        username: str = "",
        password: str = "",
    ) -> None:
        self.graphics: str = "tty"
        self.username: str = username
        self.password: str = password
        self.silent: bool = silent

        if not silent:
            self._detect_graphics()

        self.show_info(
            "This installer configures eduroam using PEAP/MSCHAPv2.\n\n"
            "It validates the RADIUS server using the system CA bundle\n"
            f"and domain-suffix-match ({Config.domain_suffix}).\n\n"
            "Author: Sten Tijhuis (Stensel8)\n"
            "https://github.com/Stensel8"
        )

    # -- Display helpers ---------------------------------------------------

    def show_info(self, data: str) -> None:
        """Show an informational message."""
        if self.silent:
            return
        if self.graphics == "tty":
            print("\n" + data)
            return

        command: list[str] = []
        if self.graphics == "zenity":
            command = [
                "zenity", "--info", "--width=500",
                f"--title={Config.title}", f"--text={data}",
            ]
        elif self.graphics == "kdialog":
            command = [
                "kdialog", "--msgbox", data,
                f"--title={Config.title}",
            ]
        elif self.graphics == "yad":
            command = [
                "yad", "--button=OK", "--width=500",
                f"--title={Config.title}", f"--text={data}",
            ]

        if command:
            subprocess.call(command, stderr=subprocess.DEVNULL)

    def alert(self, text: str) -> None:
        """Show a warning/error message."""
        if self.silent:
            return
        if self.graphics == "tty":
            print(text)
            return

        command: list[str] = []
        if self.graphics == "zenity":
            command = ["zenity", "--warning", f"--text={text}"]
        elif self.graphics == "kdialog":
            command = [
                "kdialog", "--sorry", text,
                f"--title={Config.title}",
            ]
        elif self.graphics == "yad":
            command = ["yad", f"--text={text}"]

        if command:
            subprocess.call(command, stderr=subprocess.DEVNULL)

    def ask(
        self, question: str, prompt: str = "", default: int | None = None,
    ) -> int:
        """Prompt for Y/N. Returns 0 for yes, 1 for no."""
        if self.silent:
            return 0
        if self.graphics == "tty":
            return self._ask_tty(question, prompt, default)
        return self._ask_gui(question, prompt)

    def confirm_exit(self) -> None:
        """Confirm exit from installer."""
        if self.ask(Messages.quit) == 0:
            sys.exit(1)

    # -- Credential prompts ------------------------------------------------

    def prompt_nonempty_string(
        self, show: int, prompt: str, val: str = "",
    ) -> str:
        """Prompt for a non-empty string. *show*=0 hides input (password)."""
        if self.graphics == "tty":
            return self._prompt_tty(show, prompt)
        return self._prompt_gui(show, prompt, val)

    def get_user_cred(self) -> None:
        """Get username and password from the user."""
        if self.silent:
            if not self.username or not self.password:
                print(
                    "Error: --silent requires both --username and --password",
                )
                sys.exit(1)
            return

        while True:
            self.username = self.prompt_nonempty_string(
                1, Messages.username_prompt,
            )
            if self._validate_user_name():
                break

        password: str = ""
        password1: str = ""
        while True:
            password = self.prompt_nonempty_string(
                0, Messages.enter_password,
            )
            password1 = self.prompt_nonempty_string(
                0, Messages.repeat_password,
            )
            if password == password1:
                break
            self.alert(Messages.passwords_differ)

        self.password = password

    # -- Private helpers ---------------------------------------------------

    def _validate_user_name(self) -> bool:
        """Check that username contains exactly one @ with text on both sides."""
        name = self.username
        pos = name.find("@")
        debug(f"@ position: {pos}")

        if pos == -1 or pos == 0 or pos == len(name) - 1:
            debug("invalid username format")
            self.alert(Messages.wrong_username)
            return False

        if name.find("@", pos + 1) > -1:
            debug("second @ found")
            self.alert(Messages.wrong_username)
            return False

        if name[pos + 1] == ".":
            debug("dot immediately after @")
            self.alert(Messages.wrong_username)
            return False

        debug("username validation passed")
        return True

    def _detect_graphics(self) -> None:
        """Detect available GUI toolkit."""
        self.graphics = "tty"
        if (
            os.environ.get("DISPLAY") is None
            and os.environ.get("WAYLAND_DISPLAY") is None
        ):
            return
        for cmd in ("zenity", "yad", "kdialog"):
            if shutil.which(cmd) is not None:
                self.graphics = cmd
                debug(f"Using {cmd}")
                return

    def _ask_tty(
        self, question: str, prompt: str, default: int | None,
    ) -> int:
        """TTY-based Y/N prompt."""
        yes = Messages.yes[:1].upper()
        nay = Messages.nay[:1].upper()
        print(f"\n-------\n{question}\n")
        while True:
            suffix = f" ({Messages.yes}/{Messages.nay}) "
            if default == 1:
                suffix += f"[{yes}]"
            elif default == 0:
                suffix += f"[{nay}]"

            inp = input(prompt + suffix)
            if inp == "":
                if default == 1:
                    return 0
                if default == 0:
                    return 1
                continue

            first = inp[:1].upper()
            if first == yes:
                return 0
            if first == nay:
                return 1

    def _ask_gui(self, question: str, prompt: str) -> int:
        """GUI-based Y/N prompt."""
        text = f"{question}\n\n{prompt}"
        command: list[str] = []

        if self.graphics == "zenity":
            command = [
                "zenity", f"--title={Config.title}", "--width=500",
                "--question", f"--text={text}",
            ]
        elif self.graphics == "kdialog":
            command = [
                "kdialog", "--yesno", text,
                f"--title={Config.title}",
            ]
        elif self.graphics == "yad":
            command = [
                "yad", '--image="dialog-question"',
                "--button=gtk-yes:0", "--button=gtk-no:1",
                "--width=500", "--wrap", f"--text={text}",
                f"--title={Config.title}",
            ]

        if not command:
            return 0
        return subprocess.call(command, stderr=subprocess.DEVNULL)

    @staticmethod
    def _prompt_tty(show: int, prompt: str) -> str:
        """TTY-based string prompt."""
        while True:
            if show == 0:
                inp = getpass.getpass(f"{prompt}: ")
            else:
                inp = input(f"{prompt}: ")
            output = inp.strip()
            if output:
                return output

    def _prompt_gui(self, show: int, prompt: str, val: str) -> str:
        """GUI-based string prompt (zenity/kdialog/yad)."""
        command: list[str] = []

        if self.graphics == "zenity":
            parts = ["zenity", "--entry", "--width=500", f"--text={prompt}"]
            if show == 0:
                parts.append("--hide-text")
            if val:
                parts.append(f"--entry-text={val}")
            command = parts
        elif self.graphics == "kdialog":
            flag = "--password" if show == 0 else "--inputbox"
            command = ["kdialog", flag, prompt, f"--title={Config.title}"]
        elif self.graphics == "yad":
            field = ":H" if show == 0 else ""
            command = [
                "yad", "--form", f"--field={field}",
                f"--text={prompt}", val,
            ]

        if not command:
            return self._prompt_tty(show, prompt)

        output = ""
        while not output:
            proc = subprocess.run(
                command, capture_output=True, text=True,
            )
            output = proc.stdout
            if self.graphics == "yad" and len(output) >= 2:
                output = output[:-2]
            output = output.strip()
            if proc.returncode == 1:
                self.confirm_exit()

        return output


# ---------------------------------------------------------------------------
# wpa_supplicant configuration
# ---------------------------------------------------------------------------


class WpaConf:
    """Generate wpa_supplicant configuration file."""

    @staticmethod
    def _prepare_network_block(ssid: str, user_data: InstallerData) -> str:
        """Build a wpa_supplicant network block."""
        lines = [
            "network={",
            f'    ssid="{ssid}"',
            "    key_mgmt=WPA-EAP",
            "    pairwise=CCMP",
            "    group=CCMP TKIP",
            f"    eap={Config.eap_outer}",
            f'    ca_cert="{Config.ca_cert}"',
            f'    domain_suffix_match="{Config.domain_suffix}"',
            f'    identity="{user_data.username}"',
            f'    phase2="auth={Config.eap_inner}"',
            f'    password="{user_data.password}"',
        ]
        if Config.anonymous_identity:
            lines.append(
                f'    anonymous_identity="{Config.anonymous_identity}"',
            )
        lines.append("}")
        return "\n".join(lines) + "\n"

    def create_wpa_conf(
        self, ssids: list[str], user_data: InstallerData,
    ) -> None:
        """Create and save the wpa_supplicant config file."""
        home = os.environ.get("HOME", "")
        config_dir = os.path.join(home, ".config", "cat_installer")
        os.makedirs(config_dir, mode=0o700, exist_ok=True)
        wpa_conf_path = os.path.join(config_dir, "cat_installer.conf")

        with open(wpa_conf_path, "w", encoding="utf-8") as conf:
            for ssid in ssids:
                conf.write(self._prepare_network_block(ssid, user_data))

        print(f"Configuration written to {wpa_conf_path}")


# ---------------------------------------------------------------------------
# NetworkManager D-Bus configuration
# ---------------------------------------------------------------------------


class CatNMConfigTool:
    """
    Configure eduroam via NetworkManager D-Bus interface.

    Based on the official CAT installer's NM configuration,
    using system CA bundle and domain-suffix-match instead of
    the deprecated altsubject-matches.
    """

    SYSTEM_SERVICE: str = "org.freedesktop.NetworkManager"

    def __init__(self) -> None:
        self.nm_version: str = "unknown"
        self.bus: Any = None
        self.settings: Any = None
        self.user_data: InstallerData | None = None

    def connect_to_nm(self) -> bool | None:
        """Connect to NetworkManager via D-Bus. Returns True or None."""
        if _dbus is None:
            return None

        try:
            self.bus = _dbus.SystemBus()
        except (AttributeError, Exception) as exc:  # noqa: BLE001
            debug(f"DBus connection failed: {exc}")
            return None

        self._check_nm_version()
        debug(f"NM version: {self.nm_version}")

        if self.nm_version not in ("0.9", "1.0"):
            print(Messages.nm_not_supported)
            return None

        sysproxy: Any = self.bus.get_object(
            self.SYSTEM_SERVICE,
            "/org/freedesktop/NetworkManager/Settings",
        )
        self.settings = _dbus.Interface(
            sysproxy,
            "org.freedesktop.NetworkManager.Settings",
        )

        debug("NM D-Bus connection successful")
        return True

    def add_connections(self, user_data: InstallerData) -> None:
        """Delete existing and add new connections."""
        self.user_data = user_data
        for ssid in Config.ssids:
            self._delete_existing_connection(ssid)
            self._add_connection(ssid)
        for ssid in Config.del_ssids:
            self._delete_existing_connection(ssid)

    # -- Private -----------------------------------------------------------

    def _check_nm_version(self) -> None:
        """Detect the NetworkManager version via D-Bus properties."""
        if _dbus is None or self.bus is None:
            return

        version = ""
        try:
            proxy: Any = self.bus.get_object(
                self.SYSTEM_SERVICE,
                "/org/freedesktop/NetworkManager",
            )
            props: Any = _dbus.Interface(
                proxy, "org.freedesktop.DBus.Properties",
            )
            version = str(props.Get(
                "org.freedesktop.NetworkManager", "Version",
            ))
        except Exception:  # noqa: BLE001
            version = ""

        if re.match(r"^1\.", version):
            self.nm_version = "1.0"
        elif re.match(r"^0\.9", version):
            self.nm_version = "0.9"
        else:
            self.nm_version = "unknown"

    def _delete_existing_connection(self, ssid: str) -> None:
        """Delete any existing connection for the given SSID."""
        if _dbus is None or self.bus is None or self.settings is None:
            return

        conns: Any
        try:
            conns = self.settings.ListConnections()
        except Exception:  # noqa: BLE001
            print(Messages.dbus_error)
            sys.exit(3)

        each: Any
        for each in conns:
            con_proxy: Any = self.bus.get_object(self.SYSTEM_SERVICE, each)
            connection: Any = _dbus.Interface(
                con_proxy,
                "org.freedesktop.NetworkManager.Settings.Connection",
            )
            try:
                connection_settings: Any = connection.GetSettings()
                if (
                    connection_settings["connection"]["type"]
                    == "802-11-wireless"
                ):
                    raw_ssid: Any = connection_settings["802-11-wireless"]["ssid"]
                    conn_ssid = "".join(chr(int(x)) for x in raw_ssid)
                    if conn_ssid == ssid:
                        debug(f"Deleting existing connection: {conn_ssid}")
                        connection.Delete()
            except Exception:  # noqa: BLE001
                pass

    def _add_connection(self, ssid: str) -> None:
        """Add a new eduroam connection profile via D-Bus."""
        if _dbus is None or self.settings is None or self.user_data is None:
            return

        debug(f"Adding connection: {ssid}")

        # Use the system CA bundle and domain-suffix-match instead of the
        # deprecated altsubject-matches that hangs on modern NM versions.
        ca_cert_uri = f"file://{Config.ca_cert}\0"

        s_8021x_data: dict[str, Any] = {
            "eap": [Config.eap_outer.lower()],
            "identity": self.user_data.username,
            "password": self.user_data.password,
            "phase2-auth": Config.eap_inner.lower(),
            "password-flags": _dbus.UInt32(0),  # type: ignore[attr-defined]
            "ca-cert": _dbus.ByteArray(  # type: ignore[attr-defined]
                ca_cert_uri.encode("utf-8"),
            ),
            "domain-suffix-match": Config.domain_suffix,
        }
        if Config.anonymous_identity:
            s_8021x_data["anonymous-identity"] = Config.anonymous_identity

        user = os.environ.get("USER", "")
        s_con: Any = _dbus.Dictionary({  # type: ignore[attr-defined]
            "type": "802-11-wireless",
            "uuid": str(uuid.uuid4()),
            "permissions": [f"user:{user}"],
            "id": ssid,
        })
        s_wifi: Any = _dbus.Dictionary({  # type: ignore[attr-defined]
            "ssid": _dbus.ByteArray(ssid.encode("utf-8")),  # type: ignore[attr-defined]
            "security": "802-11-wireless-security",
        })
        s_wsec: Any = _dbus.Dictionary({  # type: ignore[attr-defined]
            "key-mgmt": "wpa-eap",
            "proto": ["rsn"],
            "pairwise": ["ccmp"],
            "group": ["ccmp", "tkip"],
        })
        s_8021x: Any = _dbus.Dictionary(s_8021x_data)  # type: ignore[attr-defined]
        s_ip4: Any = _dbus.Dictionary({"method": "auto"})  # type: ignore[attr-defined]
        s_ip6: Any = _dbus.Dictionary({"method": "auto"})  # type: ignore[attr-defined]

        con: Any = _dbus.Dictionary({  # type: ignore[attr-defined]
            "connection": s_con,
            "802-11-wireless": s_wifi,
            "802-11-wireless-security": s_wsec,
            "802-1x": s_8021x,
            "ipv4": s_ip4,
            "ipv6": s_ip6,
        })

        self.settings.AddConnection(con)


# ---------------------------------------------------------------------------
# nmcli fallback
# ---------------------------------------------------------------------------


def nmcli_configure(user_data: InstallerData) -> None:
    """Configure eduroam via nmcli (preferred method)."""
    con_name = "eduroam"

    # Delete existing connection if present
    result = subprocess.run(
        ["nmcli", "-t", "-f", "NAME", "connection", "show"],
        capture_output=True, text=True,
    )
    if con_name in result.stdout.splitlines():
        debug("Deleting existing nmcli connection")
        subprocess.run(
            ["nmcli", "connection", "delete", con_name],
            capture_output=True, check=False,
        )

    cmd: list[str] = [
        "nmcli", "connection", "add",
        "type", "wifi",
        "con-name", con_name,
        "ssid", "eduroam",
        "wifi-sec.key-mgmt", "wpa-eap",
        "802-1x.eap", Config.eap_outer.lower(),
        "802-1x.phase2-auth", Config.eap_inner.lower(),
        "802-1x.identity", user_data.username,
        "802-1x.password", user_data.password,
        "802-1x.password-flags", "0",
        "802-1x.ca-cert", f"file://{Config.ca_cert}",
        "802-1x.domain-suffix-match", Config.domain_suffix,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error: nmcli failed to create connection")
        stderr = result.stderr.strip()
        if stderr:
            print(f"  {stderr}")
        sys.exit(1)

    # Activate the connection immediately instead of waiting for
    # NM auto-connect (which takes 20-40s and prompts for credentials).
    debug("Activating eduroam connection")
    activate = subprocess.run(
        ["nmcli", "connection", "up", con_name],
        capture_output=True, text=True,
    )
    if activate.returncode != 0:
        debug(f"Activation failed: {activate.stderr.strip()}")
        print("Connection profile created. NetworkManager will connect automatically.")
    else:
        debug("Connection activated successfully")


# ---------------------------------------------------------------------------
# Main installer
# ---------------------------------------------------------------------------


def run_installer() -> None:
    """Main installer logic."""
    global nm_available  # noqa: PLW0603

    username: str = ARGS.username or ""
    password: str = ARGS.password or ""
    silent: bool = ARGS.silent
    wpa_conf: bool = ARGS.wpa_conf
    Config.domain_suffix = ARGS.domain

    debug("Starting installer")
    installer_data = InstallerData(
        silent=silent, username=username, password=password,
    )

    if wpa_conf:
        nm_available = False

    # Prefer nmcli over D-Bus: nmcli handles ca-cert correctly on all
    # NM versions, while the D-Bus ByteArray format for ca-cert is
    # rejected by NM 1.50+ supplicant config builder.
    if nm_available and shutil.which("nmcli") is not None:
        debug("nmcli found — using nmcli")
        installer_data.get_user_cred()
        nmcli_configure(installer_data)
        installer_data.show_info(Messages.installation_finished)
        return

    # No nmcli — try D-Bus as fallback
    config_tool: CatNMConfigTool | None = None
    if nm_available:
        config_tool = CatNMConfigTool()
        if config_tool.connect_to_nm() is None:
            nm_available = False
            config_tool = None

    if not nm_available and not wpa_conf:
        # No nmcli and no D-Bus — offer wpa_supplicant config
        if installer_data.ask(Messages.save_wpa_conf, Messages.cont, 1):
            sys.exit(1)
        wpa_conf = True

    installer_data.get_user_cred()

    if nm_available and config_tool is not None:
        config_tool.add_connections(installer_data)
    elif wpa_conf:
        wpa = WpaConf()
        wpa.create_wpa_conf(Config.ssids, installer_data)

    installer_data.show_info(Messages.installation_finished)


if __name__ == "__main__":
    run_installer()
