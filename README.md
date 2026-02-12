# Zephyrus-Linux

English | [Nederlands](README.nl.md)

> **Disclaimer:** This is an independent personal project documenting my own research and findings while setting up Fedora 43 on the ASUS ROG Zephyrus G16 GA605WV (2024). I am not affiliated with, endorsed by, or acting on behalf of Microsoft, Windows, ASUS, ROG, G-Helper, or any other company or project mentioned herein. This repository shares my personal configuration and troubleshooting notes. No stability guarantees are provided. Your mileage may vary.

---

## tl;dr

In 2026 I moved this Zephyrus G16 to Fedora 43. It is not perfect, but stability is close to Windows 11 Pro and I prefer the control.

This repo documents the steps, tweaks, and workarounds I use and I keep it updated as Fedora and drivers change.

---

## Installation & Configuration

Complete setup guide for the ROG Zephyrus G16 on Fedora Linux. Click on a section to see the details.

<details>
<summary><strong>1.</strong> Install Brave browser (Flathub)</summary>

I installed Brave via Flathub. The official `.sh` script version from Brave's website crashed regularly and sometimes refused to open. The Flatpak version works stable.

**Installation:**
- Open GNOME Software Center
- Search for "Brave"
- Click Install

![Brave Browser in the Flathub store](/assets/images/brave-flathub.png){width="400px"}
</details>

<details>
<summary><strong>2.</strong> Set hostname</summary>

I set the hostname in the system settings to the desired name.

![Set hostname](/assets/images/system-info.png)
</details>

<details>
<summary><strong>3.</strong> Configure GNOME window buttons</summary>

I configured the window buttons in GNOME 49 to show minimize, maximize, and close buttons. By default, GNOME only shows the close button.

![Example of how the new GNOME windows look](/assets/images/window-controls.png)

**Configuration:**
```bash
gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:minimize,maximize,close'
```

This ensures that all three window buttons (minimize, maximize/zoom, and close) are visible in the title bar of applications, similar to other desktop environments.
</details>

<details>
<summary><strong>4.</strong> Bitwarden desktop (Flathub)</summary>

I installed the Bitwarden desktop app via Flathub.

![alt text](assets/images/bitwarden-flathub.png)
</details>

<details>
<summary><strong>5.</strong> Signal Messenger (Flathub)</summary>

Signal Messenger installed via Flathub. My preferred messaging app. Officially, Signal is only for Debian/Ubuntu, but the Flatpak version works great on Fedora. Signal is built on Electron, so it offers good performance.

![alt text](assets/images/signal-flathub.png)
</details>

<details>
<summary><strong>6.</strong> Install Git</summary>

Git is needed to work with repositories and make commits (otherwise I couldn't have created this repo). On Fedora, Git comes pre-installed as part of the system. If for some reason it's not installed, you can install it manually with:

```bash
sudo dnf install git
```
</details>

<details>
<summary><strong>7.</strong> Proton Mail (Flathub wrapper)</summary>

Proton Mail installed via Flathub. This is a wrapper. Some apps are wrappers and not official native apps, but for web-based mail apps I find that acceptable.

![alt text](assets/images/protonmail-flathub.png)
</details>

<details>
<summary><strong>8.</strong> Install Visual Studio Code</summary>

I installed Visual Studio Code according to the official instructions: https://code.visualstudio.com/docs/setup/linux

On Fedora I used the RPM repo and Microsoft GPG key. Commands I used:

```bash
# Import Microsoft GPG key and add repo
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc

echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\nautorefresh=1\ntype=rpm-md\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null

# Update repo cache
dnf check-update

# Install VS Code
sudo dnf install code
```

> **Known issue:** On kernel 6.18.x, VS Code hardware acceleration can trigger an amdgpu page fault. Disable hardware acceleration. See the [NVIDIA Driver Installation Guide](nvidia-driver-installation.md).
</details>

<details>
<summary><strong>9.</strong> Kleopatra & git commit signing</summary>

After installing VS Code and Git, I installed `kleopatra` and created my GPG keys via the GUI. Then I configured Git to sign commits and tags.

**ONE-TIME SETUP:**
```bash
git config --global user.name "Sten Tijhuis"
git config --global user.email "102481635+Stensel8@users.noreply.github.com"
git config --global user.signingkey 8E3B0360FED269E75261AC73D13D72C854C880F3
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg
```

This ensures that my commits are automatically signed with my GPG key.
</details>

<details>
<summary><strong>10.</strong> Tidal Hifi (Electron)</summary>

I eventually installed the Tidal Hifi Electron app from: https://github.com/Mastermindzh/tidal-hifi/releases/tag/6.1.0

I use this app for my music; there is no official Linux client, so the community Electron version works great for hi-res playback.
</details>

<details>
<summary><strong>11.</strong> Install NVIDIA GPU drivers</summary>

The RTX 4060 requires proprietary NVIDIA drivers for good performance. Nouveau (open-source) performs poorly on modern GPUs.

Full installation guide: [NVIDIA Driver Installation Guide](nvidia-driver-installation.md)

**Summary:**
- Install NVIDIA driver 580.119.02 via RPM Fusion
- MOK enrollment for Secure Boot
- Kernel parameter for AMD GPU crash fix (external monitors)

After installation, the GPU works correctly with Wayland and CUDA 13.0 support.
</details>

<details>
<summary><strong>12.</strong> Install Bottles (Flathub)</summary>

Run Windows apps via Wine.

**Installation:**
- Open GNOME Software Center
- Search for "Bottles"
- Click Install

For Microsoft 365, use a Windows VM.

![Bottles application window showing bottle creation process with status messages: Generating bottle configuration, The Wine config is being updated, Wine config updated, Setting Windows version, Apply CMD default settings, and Enabling font smoothing. A Cancel Creation button is visible at the bottom.](assets/images/bottles-install.png)
</details>

<details>
<summary><strong>13.</strong> Install Archi (ArchiMate modeling tool)</summary>

Open-source ArchiMate tool.

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

# Create symlink to PATH
sudo ln -s /opt/Archi/Archi /usr/local/bin/archi
```

**Create desktop entry:**
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
</details>

<details>
<summary><strong>14.</strong> Set up Windows 11 VM with virt-manager (KVM/QEMU)</summary>

For apps that don't run under Wine/Bottles (like Microsoft 365), set up a Windows 11 VM.

Full setup guide: [VM Setup Guide](vm-setup.md)

**Summary:**
- Windows 11 IoT Enterprise LTSC
- virt-manager with KVM/QEMU
- VirtIO drivers and SPICE
</details>

<details>
<summary><strong>15.</strong> Install Steam for gaming</summary>

Install Steam via RPM Fusion.

**Enable RPM Fusion repositories:**
```bash
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

**Install Steam:**
```bash
sudo dnf install steam
```

Reboot after installation:
```bash
sudo reboot
```
</details>

<details>
<summary><strong>16.</strong> Install Solaar for Logitech devices</summary>

I installed Solaar to manage my Logitech devices. With Solaar, you can configure and monitor Logitech devices that use the Unifying USB receiver or Bluetooth. For example, you can check the battery level of your Logitech devices.

**Installation via DNF:**
```bash
sudo dnf install solaar
```

**Usage:**
- Start via Applications menu: search "Solaar"
- Via terminal: `solaar`

**Features:**
- Monitor battery levels of Logitech devices
- Configure DPI, polling rate, and buttons
- Manage multiple devices on one Unifying receiver
- Support for both Unifying and Bluetooth devices

Solaar runs as a system tray application and shows notifications when a device's battery is running low.
</details>

<details>
<summary><strong>17.</strong> Set up GNOME keyboard shortcuts (Windows-style)</summary>

To make the transition from Windows smoother, I set up a few keyboard shortcuts that mimic the Windows shortcuts I was used to.

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

The custom shortcut for the file manager needs to be created manually because GNOME doesn't have a default shortcut for this. Go to Settings > Keyboard > Keyboard Shortcuts > Custom Shortcuts and click "Add Shortcut" to add it.
</details>

<details>
<summary><strong>18.</strong> Adjust touchpad scroll speed (optional)</summary>

GNOME on Wayland has no scroll-speed setting. Workaround: [libinput-config](https://github.com/lz42/libinput-config) (third-party).

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

**Adjust scroll speed later:**

```bash
# Edit the config
sudo nano /etc/libinput.conf

# Adjust scroll-factor as desired
# Save with Ctrl+O, Enter, Ctrl+X
# Log out and back in (or reboot)
```

**Rollback:**

```bash
sudo rm /etc/libinput.conf
```
</details>
