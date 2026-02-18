---
title: "Getting Started"
weight: 2
---

This is my personal setup log for the ROG Zephyrus G16 running Fedora Linux. I'm not a software engineer or developer — I'm just someone who switched to Linux and ran into a lot of things that didn't work out of the box. I figured I'd write it all down so others don't have to go through the same trial and error I did.

If something here helps you, great. If you run into something I haven't covered, feel free to reach out — I'm happy to think along. I don't always have the answer, but I'll do my best.

The steps below are roughly in the order I set things up after a fresh Fedora 43 install.

{{% steps %}}

### Brave browser — RPM with Wayland workarounds

I use Brave as my main browser. I started with the Flatpak version but switched to the native RPM for better system integration. There's a catch though: Brave 1.82+ has three crash bugs on GNOME Wayland that need workarounds before it's actually stable. I don't fully understand why these crashes happen — they seem to involve GPU drivers and Wayland protocols that are apparently not playing well together — but the fixes below work for me.

- **RPM (native):** Better performance and system integration. This is what I use.
- **Flatpak:** Might work better in some situations, but it feels a bit more isolated and slightly slower.

**RPM Installation**

{{< callout type="warning" >}}
On Fedora with GNOME + Wayland, Brave 1.82+ has three known crash bugs that require workarounds. The first two are applied via the desktop entry; the third requires a setting in `brave://flags`.
{{< /callout >}}

```bash
sudo dnf install dnf-plugins-core
sudo dnf config-manager addrepo --from-repofile=https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo
sudo dnf install brave-browser
```

![Brave install instructions](/images/brave-install.avif)

**Workarounds 1 & 2: patch the desktop entry**

Copy the system desktop entry to your user directory so it doesn't get overwritten by updates:
```bash
sudo cp /usr/share/applications/brave-browser.desktop ~/.local/share/applications/
```

Patch all three `Exec=` lines with both flags:
```bash
sed -i \
  's|Exec=/usr/bin/brave-browser-stable %U|Exec=/usr/bin/brave-browser-stable --disable-features=WaylandWpColorManagerV1 --ozone-platform=x11 %U|' \
  ~/.local/share/applications/brave-browser.desktop

sed -i \
  's|Exec=/usr/bin/brave-browser-stable$|Exec=/usr/bin/brave-browser-stable --disable-features=WaylandWpColorManagerV1 --ozone-platform=x11|' \
  ~/.local/share/applications/brave-browser.desktop

sed -i \
  's|Exec=/usr/bin/brave-browser-stable --incognito$|Exec=/usr/bin/brave-browser-stable --incognito --disable-features=WaylandWpColorManagerV1 --ozone-platform=x11|' \
  ~/.local/share/applications/brave-browser.desktop
```

Verify it worked — you should see exactly three `Exec=` lines:
```bash
grep "^Exec" ~/.local/share/applications/brave-browser.desktop
```

**What these flags actually do (as far as I understand it):**

`--disable-features=WaylandWpColorManagerV1` — Brave 1.82+ introduced some Wayland color management extension that apparently conflicts with the AMD amdgpu driver on Fedora + GNOME Wayland. Without this flag, Brave triggers GPU ring timeouts that crash the entire GNOME Shell session. I have no idea why a browser color management feature would take down the whole desktop, but here we are.

`--ozone-platform=x11` — This forces Brave to run via XWayland instead of native Wayland. It fixes a hard crash that happens when you try to open a Bitwarden attachment download. Apparently Brave tries to do something with a Wayland protocol in a way that's not valid, and it immediately crashes. Running via XWayland sidesteps the whole thing. You lose some native Wayland features like fractional scaling, but the browser actually stays open, which feels like a reasonable trade.

{{< callout type="info" >}}
Always launch Brave from the GNOME dock or app launcher — not from the terminal. When you launch it from a terminal inside a Wayland session, the terminal's environment overrides the `--ozone-platform=x11` flag and Brave falls back to native Wayland, bringing all the crashes back.
{{< /callout >}}

**Third workaround: disable hardware video decode in `brave://flags`**

{{< callout type="warning" >}}
Hardware video decode still causes crashes even with the two flags above. As long as the AMD VCN decoder is active, GNOME Shell crashes with SIGABRT (`g_assertion_message_expr`) — reproducible during Picture-in-Picture video and intensive video activity. See [gnome-shell issue #9056](https://gitlab.gnome.org/GNOME/gnome-shell/-/issues/9056) and [Fedora bugzilla #2440608](https://bugzilla.redhat.com/show_bug.cgi?id=2440608). Hardware video decode is **not yet stable** on the AMD Radeon 890M with GNOME Wayland. I don't understand why a browser's video decode can crash the whole session manager, but disabling it solves it.
{{< /callout >}}

Go to `brave://flags` and disable:

- **Hardware-accelerated video decode** → `Disabled`

![Brave flags — hardware video decode disabled](/images/brave-flags.avif)

Video now decodes in software. You lose hardware acceleration for video, but the session stays stable. After this, `brave://gpu` will show:

- `Video Decode: Software only. Hardware acceleration disabled`
- `Video Encode: Software only. Hardware acceleration disabled`

Brave://gpu config — video decode set to software (stable):

![Brave hardware acceleration config](/images/brave-gpu-config.avif)

**Flatpak Installation**

If the RPM version gives you trouble, the Flatpak is worth trying:

```bash
flatpak install flathub com.brave.Browser
```

![Brave Flatpak in Flathub](/images/brave-flathub.avif)

### Setting the hostname

Nothing special here — just set the hostname via System Settings so the machine has a proper name on the network.

![Set hostname](/images/system-info.avif)

### GNOME window buttons — adding minimize & maximize back

By default, GNOME 49 only shows the close button. I personally want minimize and maximize visible too — it's one of those small things that bugged me coming from Windows. One command fixes it:

```bash
gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:minimize,maximize,close'
```

![Example of how the new GNOME windows look](/images/window-controls.avif)

### Bitwarden desktop (Flathub)

I use Bitwarden for password management. The desktop app is available via Flathub and works well.

![Bitwarden desktop app in Flathub](/images/bitwarden-flathub.avif)

### Signal Messenger (Flathub)

Signal is my main messaging app. Officially it's only supported on Debian/Ubuntu, but the Flatpak version works perfectly fine on Fedora. It's Electron-based, so performance is decent.

![Signal Messenger app in Flathub](/images/signal-flathub.avif)

### Git & GitHub CLI

Git comes pre-installed on Fedora. If for some reason it's not there, or if you also want the GitHub CLI (`gh`):

```bash
sudo dnf install git gh
```

### Proton Mail (Flathub)

I use Proton Mail as my email provider. The desktop app is a wrapper around the web app rather than a native client. For web-based mail that's fine by me — it works, and it lives in the app launcher like any other app.

![Proton Mail app in Flathub](/images/protonmail-flathub.avif)

### Visual Studio Code

I install VS Code via the official RPM repo and Microsoft GPG key, as described in the [official instructions](https://code.visualstudio.com/docs/setup/linux):

```bash
# Import Microsoft GPG key and add repo
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc

echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\nautorefresh=1\ntype=rpm-md\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null

# Update repo cache
dnf check-update

# Install VS Code
sudo dnf install code
```

{{< callout type="warning" >}}
On kernel 6.18.x, VS Code hardware acceleration can trigger an amdgpu page fault. Disable hardware acceleration. See the [NVIDIA Driver Installation Guide]({{< relref "/docs/nvidia-driver-installation" >}}).
{{< /callout >}}

### Kleopatra & GPG commit signing

I sign my Git commits and tags with a GPG key. It's one of those things I set up once and then never think about again. Kleopatra makes generating and managing keys straightforward via a GUI instead of having to figure out the GPG command line.

After installing VS Code and Git, install Kleopatra and create your keys there. Then configure Git to use them:

```bash
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg
```

To find your key ID:
```bash
gpg --list-secret-keys --keyid-format=long
```
Use the ID from the `sec` line (e.g., `rsa4096/YOUR_GPG_KEY_ID`).

### Tidal Hi-Fi (Electron)

There's no official Tidal client for Linux. [Tidal Hi-Fi](https://github.com/Mastermindzh/tidal-hifi) by Rick van Lieshout is a community-made Electron wrapper around the Tidal web player, with Hi-Fi and Max quality support. It's not official, but it works well and is available via Flathub.

![Tidal Hi-Fi in the Flathub store](/images/tidal-hifi-flathub.avif)

### NVIDIA GPU drivers

The G16 has an RTX 4060 alongside the AMD iGPU. The open-source Nouveau driver doesn't perform well on modern NVIDIA hardware, so proprietary drivers are needed for anything graphics-intensive.

{{< callout type="info" >}}
Full installation guide: [NVIDIA Driver Installation Guide]({{< relref "/docs/nvidia-driver-installation" >}})
{{< /callout >}}

**What I ended up with:**
- NVIDIA driver 580.119.02 via RPM Fusion
- MOK enrollment for Secure Boot
- A kernel parameter workaround for an AMD GPU crash with external monitors

After this, the GPU works correctly on Wayland with CUDA 13.0 support.

### Bottles — running Windows software

[Bottles](https://usebottles.com/) lets you run Windows software via Wine. Install it from Flathub — the RPM packages in Fedora's repos are deprecated and ship much older versions. Make sure you get version 61 or newer.

- Open GNOME Software Center
- Search for "Bottles"
- Select the **Flathub** source (not Fedora Linux / RPM)
- Click Install

For anything that doesn't work under Wine — like Microsoft 365 — I use a Windows VM instead.

![Bottles in the Flathub store](/images/bottles-flathub.avif)

### Archi (ArchiMate modeling tool)

I use [Archi](https://www.archimatetool.com/) for ArchiMate modeling. It's free and open-source, but the Linux package is just a portable archive — no installer, no `.deb`, no `.rpm`. To make it show up properly in GNOME with an icon, you have to place the files yourself and create a desktop entry manually.

![Archi download page — Linux version with Wayland note](/images/archi-download.avif)

{{< callout type="info" >}}
Archi's download page warns about possible UI issues on Wayland. In my experience it runs fine on GNOME 49 Wayland — no issues so far.
{{< /callout >}}

```bash
# Download and extract in one flow
cd /tmp
curl -L https://github.com/archimatetool/archi.io/releases/download/5.7.0/Archi-Linux64-5.7.0.tgz | tar -xz

# Move to /opt
sudo mv Archi-Linux64-5.7.0/Archi /opt/

# Cleanup
rm -rf Archi-Linux64-5.7.0
cd ~

# Create symlink so you can run 'archi' from the terminal
sudo ln -s /opt/Archi/Archi /usr/local/bin/archi
```

Create a desktop entry so Archi shows up in GNOME:
```bash
sudo nano /usr/share/applications/archi.desktop
```

```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Archi
Comment=ArchiMate Modelling Tool
Exec=/opt/Archi/Archi
Icon=/opt/Archi/plugins/com.archimatetool.editor_5.7.0.202509230807/img/app-128.png
Terminal=false
Categories=Development;IDE;
StartupWMClass=Archi
```

After saving, Archi appears in the GNOME app launcher:

![Archi in the GNOME application launcher](/images/archi-launcher.avif)

![Archi running on Wayland with GNOME 49](/images/archi-running.avif)

### Windows 11 VM with virt-manager (KVM/QEMU)

Some things just don't run on Linux — Microsoft 365 being the obvious one. For those cases I have a Windows 11 VM running via KVM/QEMU.

{{< callout type="info" >}}
Full setup guide: [Windows 11 VM Setup Guide]({{< relref "/docs/vm-setup" >}})
{{< /callout >}}

**My setup:**
- Windows 11 Enterprise, Q35 chipset, UEFI Secure Boot, emulated TPM 2.0
- virt-manager with KVM/QEMU, host-passthrough CPU, 8 GB RAM, 8 cores
- VirtIO disk (writeback cache, threaded I/O, TRIM/discard), VirtIO network
- SPICE display with GL acceleration via AMD iGPU
- Hyper-V enlightenments for better Windows performance
- VirtIO Guest Tools and SPICE Guest Tools inside the VM

### Steam

I game on this machine too, so Steam is a must. It needs the RPM Fusion nonfree repo. The [official Fedora gaming documentation](https://docs.fedoraproject.org/en-US/gaming/proton/) is worth a read for the latest instructions.

**Enable RPM Fusion repositories (free + nonfree):**
```bash
sudo dnf install \
  https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y
```

**Enable the Cisco OpenH264 repository:**
```bash
sudo dnf config-manager setopt fedora-cisco-openh264.enabled=1
```

**Install Steam:**
```bash
sudo dnf install steam -y
```

![Steam in GNOME Software — installed via rpmfusion-nonfree-steam](/images/steam-gnome-software.avif)

Reboot after installing. Steam includes Proton out of the box, which lets you run a lot of Windows games on Linux. You can pick specific Proton versions per game via Steam Settings > Compatibility.

{{< callout type="info" >}}
If Steam won't launch, try running it from the terminal with:
```bash
__GL_CONSTANT_FRAME_RATE_HINT=3 steam
```
{{< /callout >}}

### Solaar for Logitech devices

[Solaar](https://github.com/pwr-Solaar/Solaar) manages Logitech keyboards, mice, and other peripherals connected via Unifying, Lightspeed, Nano receiver, USB, or Bluetooth. Install it from Flathub — the Fedora RPM version is outdated. You want version 1.1.19 or newer.

- Open GNOME Software Center
- Search for "Solaar"
- Select the **Flathub** source (not Fedora Linux / RPM)
- Click Install

![Solaar in GNOME Software — select the Flathub version](/images/solaar-flathub.avif)

It runs in the system tray and shows battery notifications for your devices. You can also configure DPI, polling rate, and buttons from there.

![Solaar about screen — version 1.1.19](/images/solaar-about.avif)

### GNOME keyboard shortcuts — making it feel more like Windows

Coming from Windows, some things feel off without the right shortcuts. These are the ones I set up to make the transition smoother.

**Built-in shortcuts (via Settings > Keyboard > Keyboard Shortcuts):**

| # | Action | Shortcut | Category |
|---|--------|----------|----------|
| 1 | Show desktop (hide all windows) | `Super+D` | Navigation |
| 2 | Take a screenshot interactively | `Shift+Super+S` | Screenshots |
| 3 | Open Settings | `Super+I` | System |

**Custom shortcut (via Settings > Keyboard > Keyboard Shortcuts > Custom Shortcuts):**

| # | Action | Command | Shortcut |
|---|--------|---------|----------|
| 4 | Open file manager | `nautilus` | `Super+E` |

GNOME doesn't have a built-in shortcut for the file manager, so this one needs to be created manually.

### Touchpad scroll speed — no native GNOME setting (yet)

This one frustrated me. As of GNOME 49 and Fedora 43, there is simply **no native setting** for touchpad scroll speed anywhere in the Settings panel. KDE Plasma has had this for years. There are merge requests open in [mutter](https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/1840) and [GNOME Control Center](https://gitlab.gnome.org/GNOME/gnome-control-center/-/merge_requests/991) to add it, but they've been sitting there for years and it's unclear when or if they'll ship. See the [GNOME Discourse thread](https://discourse.gnome.org/t/adding-scroll-speed-setting-in-gnome/25893) if you're curious about the discussion.

In the meantime, [libinput-config](https://github.com/lz42/libinput-config) by lz42 is a third-party workaround that intercepts libinput events and applies a scroll multiplier. It's not elegant, but it works.

**Install (one-time):**

```bash
# 1. Install dependencies
sudo dnf install -y meson ninja-build libinput-devel git

# 2. Clone libinput-config
git clone https://github.com/lz42/libinput-config.git
cd libinput-config

# 3. Build
meson setup build
ninja -C build

# 4. Install system-wide
sudo ninja -C build install

# 5. Cleanup (optional)
cd ..
rm -rf libinput-config
```

**Configuration for slower touchpad scroll:**

```bash
sudo tee /etc/libinput.conf >/dev/null << 'EOF'
# libinput-config configuration
override-compositor=enabled

# Make touchpad scroll slower (lower = slower)
# Default: 1.0, tested value: 0.25
scroll-factor=0.25

# Keep mouse wheel behavior normal
discrete-scroll-factor=1.0
EOF
```

Log out and back in (or reboot), then adjust `scroll-factor` to your liking.

**Rollback:**

```bash
sudo rm /etc/libinput.conf
```

### eduroam (university Wi-Fi)

Getting eduroam to work on Linux was genuinely painful. The official installers didn't work, community tools failed, and it took me a while to land on a setup that actually connects reliably. A manual PEAP/MSCHAPv2 configuration via nmcli ended up being the solution.

{{< callout type="info" >}}
Full setup guide: [eduroam Network Installation]({{< relref "/docs/eduroam-network-installation" >}})
{{< /callout >}}

**What worked for me:**
- PEAP / MSCHAPv2 with CA validation via the system trust store
- `domain-suffix-match` instead of the deprecated `altsubject-matches`
- An automated Python script or manual nmcli command

### GDM autologin after LUKS

After unlocking the disk with my LUKS password at boot, I didn't want to type a second password to log in. This skips the GDM login screen so the desktop loads immediately after the disk unlock.

{{< callout type="info" >}}
Full setup guide: [GDM Autologin Guide]({{< relref "/docs/autologin" >}})
{{< /callout >}}

**Setup:**
- Edit `/etc/gdm/custom.conf`
- Set `AutomaticLoginEnable=True` and `AutomaticLogin=sten` under `[daemon]`
- Reboot

{{% /steps %}}
