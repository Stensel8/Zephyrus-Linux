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

The working setup uses PEAP/MSCHAPv2 with CA validation via the system trust store and `domain-suffix-match` — the modern replacement for the deprecated `altsubject-matches` that breaks on Fedora 43.

### Connection settings

| Setting | Value |
|---------|-------|
| Security | WPA & WPA2 Enterprise |
| Authentication | Protected EAP (PEAP) |
| PEAP version | Automatic |
| Inner authentication | MSCHAPv2 |
| CA certificate | System CA bundle (`/etc/pki/tls/certs/ca-bundle.crt`) |
| Domain validation | `domain-suffix-match: saxion.net` |
| Identity | `user@institution.tld` |

{{< callout type="info" >}}
This configuration validates the RADIUS server certificate using the system CA trust store and `domain-suffix-match`. This is more secure than the "Do not validate" approach on Android, and equivalent to what Windows does after you accept the certificate on first connection.
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
4. Create a PEAP/MSCHAPv2 connection profile with CA validation via the system trust store
5. Try to activate the connection

The default domain suffix is `saxion.net`. For other institutions, pass `--domain your-institution.tld`.

{{< callout type="info" >}}
After the script finishes, it activates the connection automatically — you should be connected within a few seconds. If your credentials or the RADIUS server certificate are incorrect, NetworkManager may show a GUI prompt asking you to re-enter your credentials.
{{< /callout >}}

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
  802-1x.password "your-password" \
  802-1x.ca-cert /etc/pki/tls/certs/ca-bundle.crt \
  802-1x.domain-suffix-match "saxion.net"
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
| **CA certificate** | USERTrust RSA → GEANT OV RSA CA 4 (embedded) | System CA bundle (`/etc/pki/tls/certs/ca-bundle.crt`) |
| **Server validation** | `altsubject-matches: DNS:ise.infra.saxion.net` (deprecated) | `domain-suffix-match: saxion.net` |
| **`password-flags`** | `1` (agent-owned — requires secret agent like GNOME Keyring) | `0` (stored in connection file) |
| **Result on Fedora 43** | Hangs during TLS handshake | Connects immediately |

### How the official script connects

The official CAT installer does three things that cause problems on modern Fedora:

1. **Embeds a CA certificate chain** (USERTrust RSA root + GEANT OV RSA CA 4 intermediate) and tells NetworkManager to validate the RADIUS server against it.

2. **Sets `altsubject-matches`** to `DNS:ise.infra.saxion.net`. This property still exists in NetworkManager, but `domain-suffix-match` has been the recommended replacement since NM 1.8 (2017). On Fedora 43 with NM 1.50+, the combination of CA validation with `altsubject-matches` causes the TLS handshake to stall — no error, no timeout, just infinite loading.

3. **Sets `password-flags` to `1`** (agent-owned), meaning NetworkManager expects a secret agent (e.g. GNOME Keyring) to supply the password at connection time instead of reading it from the connection file. Without an active, unlocked keyring agent this can cause additional problems.

### How this script connects

This script fixes all three issues:

- **System CA bundle** instead of an embedded certificate chain — NetworkManager validates the RADIUS server certificate against the system trust store, which includes USERTrust RSA.
- **`domain-suffix-match`** instead of the deprecated `altsubject-matches` — verifies that the server certificate matches `saxion.net` (configurable via `--domain`) without triggering the TLS handshake bug.
- **`password-flags` set to `0`** — the password is stored directly in the connection file so NetworkManager can connect without depending on an external secret agent.

This is more secure than what Android and Windows do by default:

- **Windows** prompts "Do you trust this certificate?" on first connection — clicking OK accepts it. This script validates automatically.
- **Android** — institutional setup guides (including Saxion's own) tell users to set certificate validation to "Do not validate". This script does validate.

The institution's RADIUS server (`ise.infra.saxion.net`, Cisco ISE) works fine. The problem was purely client-side: the deprecated `altsubject-matches` property stalling the TLS handshake.

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
