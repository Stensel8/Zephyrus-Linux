# Zephyrus-Linux

🇺🇸 English | [🇳🇱 Nederlands](README.md)

My way of getting the ROG Zephyrus G16 GA605WV (2024) to work properly under Fedora after ditching Windows. Complete repo for running Linux on this gaming laptop the way I want it.

## Installation & Configuration

Complete setup guide for the ROG Zephyrus G16 on Fedora Linux. Click on a section to see the details.

<details>
<summary><strong>1.</strong> Install Brave browser (Flathub)</summary>

I installed Brave via Flathub. The official `.sh` script version from Brave's website crashed regularly and sometimes refused to open. The Flatpak version works stable.

**Installation:**
- Open GNOME Software Center
- Search for "Brave"
- Click Install
</details>

<details>
<summary><strong>2.</strong> Set hostname</summary>

I set the hostname in the system settings to the desired name.
</details>

<details>
<summary><strong>3.</strong> Configure GNOME window buttons</summary>

I configured the window buttons in GNOME 49 to show minimize, maximize, and close buttons. By default, GNOME only shows the close button.

**Configuration:**
```bash
gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:minimize,maximize,close'
```

This ensures that all three window buttons (minimize, maximize/zoom, and close) are visible in the title bar of applications, similar to other desktop environments.
</details>

<details>
<summary><strong>4.</strong> Bitwarden desktop (Flathub)</summary>

I installed the Bitwarden desktop app via Flathub.
</details>

<details>
<summary><strong>5.</strong> Signal Messenger (Flathub)</summary>

Signal Messenger installed via Flathub — my preferred messaging app.
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

Proton Mail installed via Flathub. This is a wrapper – some apps are wrappers and not official native apps, but for web-based mail apps I find that acceptable.
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

> **Known issue:** On kernel 6.18.x, the amdgpu driver has a bug where VS Code with hardware acceleration can trigger a page fault on the AMD Radeon 890M iGPU, causing a complete system crash. This will be addressed by kernel developers in the future, but for now hardware acceleration needs to be disabled. See the [NVIDIA Driver Installation Guide](NVIDIA_DRIVER_INSTALLATION.md) for the full workaround.
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

Full installation guide: [NVIDIA Driver Installation Guide](NVIDIA_DRIVER_INSTALLATION.md)

**Summary:**
- Install NVIDIA driver 580.119.02 via RPM Fusion
- MOK enrollment for Secure Boot
- Kernel parameter for AMD GPU crash fix (external monitors)

After installation, the GPU works correctly with Wayland and CUDA 13.0 support.
</details>

<details>
<summary><strong>12.</strong> Install Bottles (Flathub)</summary>

I installed Bottles via Flathub. Bottles is a Windows compatibility layer based on Wine that allows you to run Windows applications and games on Linux.

**Installation:**
- Open GNOME Software Center
- Search for "Bottles"
- Click Install

Bottles makes it easy to create isolated Windows environments (bottles) for different applications. This works well for games like Fortnite or World of Tanks.

**Note:**Microsoft 365 apps (Word, Excel, PowerPoint) unfortunately don't run well under Bottles/Wine. For these, you'll need to set up a full Windows VM with virt-manager.

![Bottles application window showing bottle creation process with status messages: Generating bottle configuration, The Wine config is being updated, Wine config updated, Setting Windows version, Apply CMD default settings, and Enabling font smoothing. A Cancel Creation button is visible at the bottom.](image.png)
</details>

<details>
<summary><strong>13.</strong> Install Archi (ArchiMate modeling tool)</summary>

I installed Archi, an open-source ArchiMate modeling tool that I need for my studies. This is useful for anyone working with enterprise architecture.

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

**Usage:**
- Start via app menu: search "Archi" (may take a few minutes to appear, or just reboot)
- Start via terminal: `archi`

**Notes:**
- App is installed in `/opt/Archi/` and runs fully standalone
- For updates: download new version, repeat the installation steps
- Icon path needs to be adjusted in the desktop entry when updating versions
- You can delete the `.tgz` file from Downloads once installation is complete
</details>

<details>
<summary><strong>14.</strong> Set up Windows 11 VM with virt-manager (KVM/QEMU)</summary>

For school programs that don't run under Wine/Bottles (like Microsoft 365), you can set up a high-performance Windows 11 virtual machine. With the right configuration, you get near-native performance.

Full setup guide: [VM Setup Guide](VM_SETUP.md)

**Summary:**
- Windows 11 IoT Enterprise LTSC (no bloatware, no mandatory TPM/Secure Boot)
- virt-manager with KVM/QEMU virtualization
- VirtIO drivers for optimal disk, network, and GPU performance
- CPU pinning and hugepages for near-native performance
- SPICE for seamless clipboard and file sharing

This setup is ideal for those who want to use Linux as their daily system but occasionally need Windows applications for school or work.
</details>

<details>
<summary><strong>15.</strong> Install Steam for gaming</summary>

Steam is the largest gaming platform for Linux and essential for running both native Linux games and Windows games via Proton.

**RPM Fusion Method (Recommended):**

The most straightforward way to install Steam on Fedora is via RPM Fusion, which hosts the Steam package due to licensing restrictions in Fedora's default repositories.

**Enable RPM Fusion repositories:**
```bash
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

**Install Steam:**
```bash
sudo dnf install steam
```

> **IMPORTANT:** Reboot your system after installation, otherwise you'll get crashes on first Steam launch.
> ```bash
> sudo reboot
> ```

**Launch Steam:**
- Via terminal: `steam`
- Via Applications menu: search "Steam"

The first launch will update Steam and prompt you to login or create an account.

**Enable Proton for Windows games:**
Go to Steam > Settings > Steam Play and enable Proton to run Windows games on Linux. This makes a large portion of the Steam catalog available, even games without native Linux support.
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

**Why this fix is needed:**

GNOME on Wayland has **no native way** to adjust touchpad scroll speed. You can only adjust pointer speed in Settings, not scroll speed. This is a [frequently requested feature](https://discourse.gnome.org/t/add-touchpad-scroll-sensitivity-adjustment-feature/18097/23) that the GNOME community has been discussing. This functionality may arrive in GNOME 50, but until then, there's no official solution.

The default scroll sensitivity on Fedora's touchpad is often way too high and feels unnatural. This workaround solves that problem.

**How this workaround works:**

`libinput-config` uses **LD_PRELOAD** to intercept libinput calls and read a configuration file (`/etc/libinput.conf`). It sits between libinput and your compositor (GNOME) and adjusts scroll values before they reach your applications. This means:
- It does **not** replace your system libinput
- It works as an "intermediary layer" that modifies scroll events
- System-wide effect across all applications

> **Warning:** This is a third-party workaround ([libinput-config](https://github.com/lz42/libinput-config)), not an official GNOME/Fedora feature. Use at your own risk. Test scroll behavior after system updates to ensure it still works as expected.

**Installation (one-time):**

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

**After installation:**
- Log out and back in (or reboot)
- Test the scroll speed
- Adjust `scroll-factor` to your preference:
  - `0.1` = very slow
  - `0.2` = just a bit too slow, especially in GNOME itself (feels fine in Brave)
  - `0.25` = my sweet spot (recommended, tested on ROG Zephyrus G16)
  - `0.3` = decent, but still a bit too fast
  - `0.5` = speed halved, but still fairly fast
  - `1.0` = default (way too fast)

**Adjust scroll speed later:**

If `0.25` is still too fast or too slow, adjust the value:

```bash
# Edit the config
sudo nano /etc/libinput.conf

# Adjust scroll-factor as desired (try 0.15 or 0.25)
# Save with Ctrl+O, Enter, Ctrl+X
# Log out and back in (or reboot)
```

**Or set a new value in one command:**

```bash
# Example: set scroll-factor to 0.15
sudo tee /etc/libinput.conf >/dev/null << 'EOF'
# libinput-config configuration
override-compositor=enabled
scroll-factor=0.15
discrete-scroll-factor=1.0
EOF

# Then log out and back in
```

**Rollback (revert everything):**

```bash
# 1. Disable config
sudo rm /etc/libinput.conf

# 2. Log out and back in

# 3. (Optional) Uninstall libinput-config
# This requires you still have the original build directory:
cd libinput-config
sudo ninja -C build uninstall
```

**Risks:**
- Third-party project (not officially supported)
- May break with major GNOME/Fedora updates
- Input debugging becomes slightly more complex

**Alternative: scroll-related flags in Brave:**

Brave has several experimental flags that let you tweak scroll behavior without system-wide tools. Navigate to `brave://flags` in the address bar to find them.

| Flag | Description |
|------|-------------|
| `brave://flags/#middle-button-autoscroll` | Auto-scroll using the middle mouse button |
| `brave://flags/#brave-change-active-tab-on-scroll-event` | Switch active tab by scrolling on the tab bar |
| `brave://flags/#smooth-scrolling` | Enable or disable smooth scrolling |
| `brave://flags/#fluent-overlay-scrollbars` | Modern overlay scrollbars (Fluent-style) |

Many more flags are available. Use `Ctrl+F` on the `brave://flags` page to search for specific settings.
</details>
