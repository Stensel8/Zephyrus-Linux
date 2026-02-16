---
title: "eduroam Network Installation"
weight: 23
---

The official eduroam installers and community scripts don't work on Fedora 43 (NetworkManager 1.50+). The connection just hangs during the TLS handshake — no error, no timeout, nothing. This guide explains why and gives you a setup that actually works.

## What doesn't work

I tried every tool I could find. None of them resulted in a working connection on Fedora 43:

{{% details title="cat.eduroam.org installer (official)" closed="true" %}}
The Python installer from [cat.eduroam.org](https://cat.eduroam.org/) creates a connection profile, but it never actually connects — it hangs during the TLS handshake. You can download it yourself from [cat.eduroam.org](https://cat.eduroam.org/) and try, but on Fedora 43 it won't work. See [Technical comparison](#technical-comparison) below for why.

![cat.eduroam.org download portal for Saxion](/images/eduroam-cat-portal.png)
{{% /details %}}

{{% details title="geteduroam Linux app (official)" closed="true" %}}
The [geteduroam Linux app](https://github.com/geteduroam/linux-app) (CLI and GUI RPM) has the same problem: it connects forever without ever succeeding.
{{% /details %}}

{{% details title="easyroam-linux (community)" closed="true" %}}
[easyroam-linux](https://github.com/jahtz/easyroam-linux) by jahtz didn't work either.
{{% /details %}}

{{% details title="UvA/HvA Linux eduroam guide" closed="true" %}}
The guide at [linux.datanose.nl](https://linux.datanose.nl/linux/eduroam/) (UvA/HvA) also didn't result in a working connection.
{{% /details %}}

## What does work

The working setup uses PEAP/MSCHAPv2 without CA certificate validation — the same way Android and Windows actually connect to eduroam in practice.

### Connection settings

| Setting | Value |
|---------|-------|
| Security | WPA & WPA2 Enterprise |
| Authentication | Protected EAP (PEAP) |
| PEAP version | Automatic |
| Inner authentication | MSCHAPv2 |
| CA certificate | None |
| Identity | `user@institution.tld` |

{{< callout type="warning" >}}
This configuration does **not** validate the server's CA certificate. This matches how Android and Windows behave and avoids the validation issues that break the official tools. Be aware of the security trade-off.
{{< /callout >}}

### Automated setup (recommended)

A Python script automates the whole `nmcli` connection setup:

```bash
curl -LO https://zephyrus-linux.stentijhuis.nl/scripts/eduroam-linux.py
python eduroam-linux.py
```

The script will:
1. Check that NetworkManager (`nmcli`) is available
2. Remove any existing eduroam connection profile
3. Ask for your credentials (username + password)
4. Create a PEAP/MSCHAPv2 connection profile without CA certificate validation
5. Try to activate the connection

If everything goes well, you should see something like this:

![eduroam installer showing installation successful](/images/eduroam-installer-success.png)

**Source:** [eduroam-linux.py](/scripts/eduroam-linux.py)

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
  802-1x.password "your-password"
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

![GNOME Settings eduroam Security tab](/images/eduroam-gnome-settings.png)

### Removal

```bash
nmcli connection delete eduroam
```

## Technical comparison

The official CAT installer (from [cat.eduroam.org](https://cat.eduroam.org/)) and this script differ in three key ways:

| | Official CAT script | This script |
|---|---|---|
| **CA certificate** | USERTrust RSA → GEANT OV RSA CA 4 (embedded) | None |
| **Server validation** | `altsubject-matches: DNS:ise.infra.saxion.net` | None |
| **`password-flags`** | `1` (agent-owned — requires secret agent like GNOME Keyring) | `0` (stored in connection file) |
| **Result on Fedora 43** | Hangs during TLS handshake | Connects immediately |

### How the official script connects

The official CAT installer does three things that cause problems on modern Fedora:

1. **Embeds a CA certificate chain** (USERTrust RSA root + GEANT OV RSA CA 4 intermediate) and tells NetworkManager to validate the RADIUS server against it.

2. **Sets `altsubject-matches`** to `DNS:ise.infra.saxion.net`. This property still exists in NetworkManager, but `domain-suffix-match` has been the recommended replacement since NM 1.8 (2017). On Fedora 43 with NM 1.50+, the combination of CA validation with `altsubject-matches` causes the TLS handshake to stall — no error, no timeout, just infinite loading.

3. **Sets `password-flags` to `1`** (agent-owned), meaning NetworkManager expects a secret agent (e.g. GNOME Keyring) to supply the password at connection time instead of reading it from the connection file. Without an active, unlocked keyring agent this can cause additional problems.

### How this script connects

This script removes all three of those settings:

- **No CA certificate** — NetworkManager skips server certificate validation and goes straight to the PEAP tunnel.
- **No `altsubject-matches`** — avoids the broken validation path entirely.
- **`password-flags` set to `0`** — the password is stored directly in the connection file so NetworkManager can connect without depending on an external secret agent.

This is functionally the same as what Android and Windows do:

- **Windows** prompts "Do you trust this certificate?" on first connection — clicking OK skips further validation.
- **Android** — institutional setup guides (including Saxion's own) tell users to set certificate validation to "Do not validate".

The institution's RADIUS server (`ise.infra.saxion.net`, Cisco ISE) works fine. The problem is purely client-side.

### Password storage

{{< callout type="warning" >}}
Your eduroam password is stored in **plaintext** in the NetworkManager connection file:

```bash
sudo cat /etc/NetworkManager/system-connections/eduroam.nmconnection
```

The file is only readable by root (`chmod 600`). Keep this in mind if you give someone `sudo` access or copy system backups externally.
{{< /callout >}}

{{< callout type="info" >}}
This script was written by Sten Tijhuis ([Stensel8](https://github.com/Stensel8)) based on studying how eduroam connects on Android and Windows, and comparing the official CAT installer against what modern NetworkManager versions support. It is not affiliated with or endorsed by any institution or the eduroam consortium.
{{< /callout >}}
