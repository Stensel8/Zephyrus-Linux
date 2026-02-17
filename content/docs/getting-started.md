---
title: "Getting Started"
weight: 2
---

Complete setup guide for the ROG Zephyrus G16 on Fedora Linux. Follow the steps in order to go from a fresh Fedora 43 installation to a fully configured system.

{{% steps %}}

### Install Brave browser (Flathub)

I installed Brave via Flathub. The official `.sh` script version from Brave's website crashed regularly and sometimes refused to open. The Flatpak version is stable.

**Installation:**
- Open GNOME Software Center
- Search for "Brave"
- Click Install

![Brave Browser in the Flathub store](/images/brave-flathub.avif)

### Set hostname

Set the hostname in the system settings to the desired name.

![Set hostname](/images/system-info.avif)

### Configure GNOME window buttons

I configured the window buttons in GNOME 49 to show minimize, maximize, and close buttons. By default, GNOME only shows the close button.

![Example of how the new GNOME windows look](/images/window-controls.avif)

**Configuration:**
```bash
gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:minimize,maximize,close'
```

This ensures that all three window buttons (minimize, maximize/zoom, and close) are visible in the title bar of applications, similar to other desktop environments.

### Bitwarden desktop (Flathub)

Install the Bitwarden desktop app via Flathub.

![Bitwarden desktop app in Flathub](/images/bitwarden-flathub.avif)

### Signal Messenger (Flathub)

Signal Messenger installed via Flathub. My preferred messaging app. Officially, Signal is only for Debian/Ubuntu, but the Flatpak version works great on Fedora. Signal is built on Electron, so it offers good performance.

![Signal Messenger app in Flathub](/images/signal-flathub.avif)

### Install Git

Git is needed to work with repositories and make commits. On Fedora, Git comes pre-installed as part of the system. If for some reason it's not installed, you can install it manually with:

```bash
sudo dnf install git gh
```

### Proton Mail (Flathub)

Proton Mail installed via Flathub. This is a wrapper. Some apps are wrappers and not official native apps, but for web-based mail apps I find that acceptable.

![Proton Mail app in Flathub](/images/protonmail-flathub.avif)

### Install Visual Studio Code

Install Visual Studio Code according to the [official instructions](https://code.visualstudio.com/docs/setup/linux).

On Fedora, use the RPM repo and Microsoft GPG key:

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

### Kleopatra & git commit signing

After installing VS Code and Git, install `kleopatra` and create your GPG keys via the GUI. Then configure Git to sign commits and tags.

**One-time setup:**
```bash
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg
```

**Find your GPG key ID:**
```bash
gpg --list-secret-keys --keyid-format=long
```
Use the key ID from the `sec` line (e.g., `rsa4096/YOUR_GPG_KEY_ID`).

### Tidal Hi-Fi (Electron)

There is no official Tidal client for Linux. [Tidal Hi-Fi](https://github.com/Mastermindzh/tidal-hifi) by Rick van Lieshout (Mastermindzh) is a community Electron client that wraps the Tidal web player with Hi-Fi and Max quality support. Install it via Flathub.

![Tidal Hi-Fi in the Flathub store](/images/tidal-hifi-flathub.avif)

### Install NVIDIA GPU drivers

The RTX 4060 requires proprietary NVIDIA drivers for good performance. Nouveau (open-source) performs poorly on modern GPUs.

{{< callout type="info" >}}
Full installation guide: [NVIDIA Driver Installation Guide]({{< relref "/docs/nvidia-driver-installation" >}})
{{< /callout >}}

**Summary:**
- Install NVIDIA driver 580.119.02 via RPM Fusion
- MOK enrollment for Secure Boot
- Kernel parameter for AMD GPU crash fix (external monitors)

After installation, the GPU works correctly with Wayland and CUDA 13.0 support.

### Install Bottles (Flathub)

[Bottles](https://usebottles.com/) lets you run Windows software on Linux via Wine. Install it via Flathub — the RPM packages from Fedora's repos are deprecated and ship older versions. Make sure you're on version 61 or newer.

**Installation:**
- Open GNOME Software Center
- Search for "Bottles"
- Select the **Flathub** source (not Fedora Linux / RPM)
- Click Install

For Microsoft 365, use a Windows VM instead.

![Bottles in the Flathub store](/images/bottles-flathub.avif)

### Install Archi (ArchiMate modeling tool)

[Archi](https://www.archimatetool.com/) is a free, open-source tool for creating ArchiMate models. Download it from the [official download page](https://www.archimatetool.com/download/).

![Archi download page — Linux version with Wayland note](/images/archi-download.avif)

The Linux package is a portable archive — there is no installer, `.deb`, or `.rpm`. To have Archi appear as a proper application with an icon in GNOME, you need to move the files yourself and create a desktop entry.

{{< callout type="info" >}}
Archi's download page warns about possible UI issues on Wayland. In my experience, Archi works fine on Wayland with GNOME 49 — no issues so far.
{{< /callout >}}

**Installation:**
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

**Create a desktop entry so Archi shows up in GNOME:**
```bash
sudo nano /usr/share/applications/archi.desktop
```

**Desktop entry content:**
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

After saving the desktop entry, Archi appears in the GNOME application launcher:

![Archi in the GNOME application launcher](/images/archi-launcher.avif)

![Archi running on Wayland with GNOME 49](/images/archi-running.avif)

### Set up Windows 11 VM with virt-manager (KVM/QEMU)

For apps that don't run under Wine/Bottles (like Microsoft 365), set up a Windows 11 VM.

{{< callout type="info" >}}
Full setup guide: [Windows 11 VM Setup Guide]({{< relref "/docs/vm-setup" >}})
{{< /callout >}}

**Summary:**
- Windows 11 Enterprise with Q35 chipset, UEFI Secure Boot, and emulated TPM 2.0
- virt-manager with KVM/QEMU, host-passthrough CPU, 8 GB RAM, 8 cores
- VirtIO disk (writeback cache, threaded I/O, TRIM/discard), VirtIO network
- SPICE display with GL acceleration via AMD iGPU
- Hyper-V enlightenments for optimized Windows performance
- VirtIO Guest Tools and SPICE Guest Tools required inside the VM

### Install Steam for gaming

Steam requires the RPM Fusion nonfree repository. Follow the [official Fedora gaming documentation](https://docs.fedoraproject.org/en-US/gaming/proton/) for the most up-to-date instructions.

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

Reboot after installation. Steam includes Proton by default, which allows you to run many Windows games on Linux. You can select specific Proton versions per game via Steam Settings > Compatibility.

{{< callout type="info" >}}
If Steam won't launch, try running from the terminal with:
```bash
__GL_CONSTANT_FRAME_RATE_HINT=3 steam
```
{{< /callout >}}

### Install Solaar for Logitech devices

[Solaar](https://github.com/pwr-Solaar/Solaar) manages Logitech keyboards, mice, and trackpads that connect via Unifying, Lightspeed, Nano receiver, USB cable, or Bluetooth. Install it via Flathub — the Fedora RPM package is outdated and ships an older version. Make sure you're on version 1.1.19 or newer.

**Installation:**
- Open GNOME Software Center
- Search for "Solaar"
- Select the **Flathub** source (not Fedora Linux / RPM)
- Click Install

![Solaar in GNOME Software — select the Flathub version](/images/solaar-flathub.avif)

**Features:**
- Monitor battery levels of Logitech devices
- Configure DPI, polling rate, and buttons
- Manage multiple devices on one Unifying receiver
- Support for both Unifying and Bluetooth devices

![Solaar about screen — version 1.1.19](/images/solaar-about.avif)

Solaar runs as a system tray application and shows notifications when a device's battery is running low.

### Set up GNOME keyboard shortcuts (Windows-style)

To make the transition from Windows smoother, set up keyboard shortcuts that mimic Windows.

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

The custom shortcut for the file manager needs to be created manually because GNOME doesn't have a default shortcut for this.

### Adjust touchpad scroll speed (optional)

As of GNOME 49 and Fedora 43, there is **no native setting** for touchpad scroll speed. GNOME's Settings panel simply doesn't offer it — unlike KDE Plasma, which has had this for years. There are [merge requests pending in mutter](https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/1840) and [GNOME Control Center](https://gitlab.gnome.org/GNOME/gnome-control-center/-/merge_requests/991) to add this, but they've been open for years and it's unclear if they'll ship in GNOME 50 (expected with Fedora 44). See the [GNOME Discourse discussion](https://discourse.gnome.org/t/adding-scroll-speed-setting-in-gnome/25893) for context.

In the meantime, [libinput-config](https://github.com/lz42/libinput-config) by lz42 is a third-party workaround that intercepts libinput events and applies a scroll multiplier.

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

Log out and back in (or reboot) and adjust `scroll-factor` as needed.

**Rollback:**

```bash
sudo rm /etc/libinput.conf
```

### Connect to eduroam (university Wi-Fi)

eduroam on Linux can be tricky — the official installers and community tools often fail. A custom PEAP/MSCHAPv2 setup via nmcli works reliably.

{{< callout type="info" >}}
Full setup guide: [eduroam Network Installation]({{< relref "/docs/eduroam-network-installation" >}})
{{< /callout >}}

**Summary:**
- PEAP / MSCHAPv2 with CA validation via the system trust store
- `domain-suffix-match` instead of the deprecated `altsubject-matches`
- Automated Python script or manual nmcli command

### GDM autologin after LUKS

Skip the GDM login screen after LUKS unlock. After entering your disk password at boot, the desktop loads immediately.

{{< callout type="info" >}}
Full setup guide: [GDM Autologin Guide]({{< relref "/docs/autologin" >}})
{{< /callout >}}

**Summary:**
- Edit `/etc/gdm/custom.conf`
- Set `AutomaticLoginEnable=True` and `AutomaticLogin=sten` under `[daemon]`
- Reboot

{{% /steps %}}
