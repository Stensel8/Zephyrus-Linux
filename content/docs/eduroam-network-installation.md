---
title: "eduroam Network Installation"
weight: 23
---


Some users may encounter issues connecting to eduroam on modern Linux systems with NetworkManager 1.50+ (tested on Fedora 43), where the connection hangs during the TLS handshake. This guide explains the technical background and provides a setup that works reliably on recent Linux distributions.

## What doesn't work


Several available tools and installers may not work out-of-the-box on the latest Linux distributions due to changes in NetworkManager. Below is a summary of common options and their behavior on Fedora 43:


{{% details title="cat.eduroam.org installer (official)" closed="true" %}}
The Python installer from [cat.eduroam.org](https://cat.eduroam.org/) provides a graphical interface and creates a connection profile. On some recent Linux distributions (such as Fedora 43), the connection may hang during the TLS handshake due to changes in NetworkManager. See [Technical comparison](#technical-comparison) below for more details.

![cat.eduroam.org download portal for Saxion](/images/eduroam-cat-portal.avif)
{{% /details %}}

{{% details title="geteduroam Linux app (official)" closed="true" %}}

The [geteduroam Linux app](https://github.com/geteduroam/linux-app) (CLI and GUI RPM) may also experience connection issues on some recent distributions.
{{% /details %}}

{{% details title="easyroam-linux (community)" closed="true" %}}
[easyroam-linux](https://github.com/jahtz/easyroam-linux) by jahtz may not work on all distributions.
{{% /details %}}

{{% details title="UvA/HvA Linux eduroam guide" closed="true" %}}
The guide at [linux.datanose.nl](https://linux.datanose.nl/linux/eduroam/) (UvA/HvA) may not result in a working connection on all recent systems.
{{% /details %}}

## What does work

The working setup uses PEAP/MSCHAPv2 with CA validation via the system trust store and `domain-suffix-match` — the modern replacement for the deprecated `altsubject-matches` that breaks on Fedora 43.

**Requirements:**
- Python 3.10+
- NetworkManager 1.8+ (`nmcli`)

### Connection settings

| Setting | Value |
|---------|-------|
| Security | WPA & WPA2 Enterprise |
| Authentication | Protected EAP (PEAP) |
| PEAP version | Automatic |
| Inner authentication | MSCHAPv2 |
| CA certificate | System CA bundle (`/etc/pki/tls/certs/ca-bundle.crt`) |
| Domain validation | `domain-suffix-match: ise.infra.saxion.net` |
| Phase2 domain validation | `phase2-domain-suffix-match: ise.infra.saxion.net` |
| Anonymous identity | `anonymous@saxion.nl` |
| Identity | `user@institution.tld` |

{{< callout type="info" >}}
This configuration validates the RADIUS server certificate using the system CA trust store and both `domain-suffix-match` and `phase2-domain-suffix-match` for `ise.infra.saxion.net`. The anonymous identity (`anonymous@saxion.nl`) protects your username during the initial handshake. This is a preferred method for Linux users who want a secure and automated setup. Android and Windows have their own official workflows, which may differ in certificate validation details.
{{< /callout >}}

### Automated setup (recommended)

A modern Python script with GUI support automates the whole `nmcli` connection setup for Saxion:

```bash
curl -LO https://zephyrus-linux.stentijhuis.nl/scripts/saxion-eduroam.py
python3 saxion-eduroam.py
```

The script will:
1. Detect available GUI tools (zenity, kdialog, or yad) or fall back to terminal input
2. Check that NetworkManager (`nmcli`) is available
3. Remove any existing eduroam connection profile
4. Show a friendly GUI dialog for entering your credentials (username + password)
5. Create a PEAP/MSCHAPv2 connection profile with:
   - CA validation via the system trust store
   - Domain validation against `ise.infra.saxion.net`
   - Phase2 domain suffix matching
   - Anonymous identity (`anonymous@saxion.nl`)
6. Automatically activate the connection

This script is **Saxion-specific** and validates against Saxion's RADIUS server domain (`ise.infra.saxion.net`). For other institutions, download the official CAT script from [cat.eduroam.org](https://cat.eduroam.org/) and adapt the server domain and realm.

{{< callout type="info" >}}
After the script finishes, it activates the connection automatically — you should be connected within a few seconds. If your credentials or the RADIUS server certificate are incorrect, NetworkManager may show a GUI prompt asking you to re-enter your credentials.
{{< /callout >}}

{{< callout type="warning" >}}
You are downloading and running a script from the internet. If you want to be extra safe, verify the script source (or its checksum) before running it.
{{< /callout >}}

If everything goes well, you should see something like this:

![eduroam installer showing installation successful](/images/eduroam-installer-success.avif)

**Source:** [saxion-eduroam.py](/scripts/saxion-eduroam.py)

### Manual setup via nmcli

```bash
nmcli connection add \
  type wifi \
  con-name "eduroam" \
  ssid "eduroam" \
  wifi-sec.key-mgmt wpa-eap \
  802-1x.eap peap \
  802-1x.phase2-auth mschapv2 \
  802-1x.identity "user@institution.tld" \
  802-1x.password "your-password" \
  802-1x.anonymous-identity "anonymous@saxion.nl" \
  802-1x.ca-cert file:///etc/pki/tls/certs/ca-bundle.crt \
  802-1x.domain-suffix-match "ise.infra.saxion.net" \
  802-1x.phase2-domain-suffix-match "ise.infra.saxion.net"
```

Then connect:

```bash
nmcli connection up eduroam
```

### Manual setup via GNOME Settings

1. Open **Settings → Wi-Fi**
2. Select **eduroam**
3. Go to the **Security** tab and fill in the settings from the table above
4. Enter your institutional credentials
5. Click **Apply**

Here's what the Security tab should look like:

![GNOME Settings eduroam Security tab](/images/eduroam-gnome-settings.avif)

### Removal

```bash
nmcli connection delete eduroam
```

## Technical comparison

The official CAT installer (from [cat.eduroam.org](https://cat.eduroam.org/)) and this script differ in three key ways:

| | Official CAT script | This script |
|---|---|---|
| **CA certificate** | USERTrust RSA → GEANT OV RSA CA 4 (embedded) | System CA bundle (`/etc/pki/tls/certs/ca-bundle.crt`) |
| **Server validation** | `altsubject-matches: DNS:ise.infra.saxion.net` (deprecated) | `domain-suffix-match: ise.infra.saxion.net` + phase2 |
| **Anonymous identity** | Not set | `anonymous@saxion.nl` |
| **`password-flags`** | `1` (agent-owned — requires secret agent like GNOME Keyring) | `1` (agent-owned — password stored securely in GNOME Keyring, not in connection file) |
| **User interface** | GUI and terminal dialogs | GUI support (zenity/kdialog/yad) + terminal fallback |
| **Result on modern NM (1.50+)** | Hangs during TLS handshake | Connects immediately |

### How the official script connects


The official CAT installer uses a configuration that may not be fully compatible with the latest NetworkManager versions on some Linux distributions:

1. **Embeds a CA certificate chain** (USERTrust RSA root + GEANT OV RSA CA 4 intermediate) and tells NetworkManager to validate the RADIUS server against it.

2. **Sets `altsubject-matches`** to `DNS:ise.infra.saxion.net`. This property still exists in NetworkManager, but `domain-suffix-match` has been the recommended replacement since NM 1.8 (2017). On some recent systems, the combination of CA validation with `altsubject-matches` may cause the TLS handshake to stall.

3. **Sets `password-flags` to `1`** (agent-owned), meaning NetworkManager expects a secret agent (e.g. GNOME Keyring) to supply the password at connection time instead of reading it from the connection file. Without an active, unlocked keyring agent this can cause additional problems.

### How this script connects


This script adapts the configuration for modern Linux and adds some features:

- **System CA bundle** — NetworkManager validates the RADIUS server certificate against the system trust store, which includes USERTrust RSA.
- **`domain-suffix-match` and `phase2-domain-suffix-match`** — uses the modern recommended properties for server validation.
- **Anonymous identity** — protects your username during the initial RADIUS handshake by sending `anonymous@saxion.nl` first.
- **`password-flags` set to `1`** — the password is stored securely in your GNOME Keyring (or compatible secret agent), not in the connection file.
- **GUI support** — automatically detects and uses zenity, kdialog, or yad for a user-friendly installation experience, with terminal fallback.


This method is designed for modern Linux systems and may offer a more seamless experience on recent distributions. Android and Windows have their own official workflows, which may differ in certificate validation details. This script is intended as a preferred method for Linux users who want a secure and automated setup.


### Password storage

{{< callout type="info" >}}
Your eduroam password is **not stored in plaintext** on disk. Instead, it is securely stored in your GNOME Keyring (or compatible secret agent). NetworkManager retrieves the password from the keyring at connection time, so even users with root access cannot simply read it from a file. You may be prompted to unlock your keyring when connecting to eduroam.
{{< /callout >}}

{{< callout type="info" >}}
This script was written by Sten Tijhuis ([Stensel8](https://github.com/Stensel8)) based on studying how eduroam connects on Android and Windows, and comparing the official CAT installer against what modern NetworkManager versions support. It is not affiliated with or endorsed by any institution or the eduroam consortium.
{{< /callout >}}

### Additional Notes on Compatibility

While the Saxion-specific script is optimized for modern Linux systems and provides a streamlined setup process, it is important to note that the official Eduroam script includes legacy support for older systems. This may be beneficial for users running outdated distributions or environments where modern tools like `domain-suffix-match` are not supported.

### Debugging Features

The official Eduroam script includes a `--debug` flag for verbose output and detailed error handling. In contrast, the Saxion-specific script has minimal debugging support. Users requiring extensive debugging capabilities may prefer the official script.
