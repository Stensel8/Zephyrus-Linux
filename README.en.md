# Zephyrus-Linux

🇺🇸 English | [🇳🇱 Nederlands](README.md)

My way of getting the ROG Zephyrus G16 GA605WV (2024) to work properly under Fedora after ditching Windows. Complete repo for running Linux on this gaming laptop the way I want it.

## Initial Setup

Here are the first installation and setup steps I performed. Click on a step to see the details.

<details>
<summary><strong>Step 1:</strong> Install Brave browser (Flathub)</summary>

I installed Brave via Flathub. The official `.sh` script version from Brave's website crashed regularly and sometimes refused to open. The Flatpak version works stable.

Installation via Flathub (Software Center) or command line:
```bash
flatpak install flathub com.brave.Browser
```

Then I adjusted the settings to my preference.
</details>

<details>
<summary><strong>Step 2:</strong> Set hostname</summary>

I set the hostname in the system settings to the desired name.
</details>

<details>
<summary><strong>Step 3:</strong> Bitwarden desktop (Flathub)</summary>

I installed the Bitwarden desktop app via Flathub.
</details>

<details>
<summary><strong>Step 4:</strong> Signal Messenger (Flathub)</summary>

Signal Messenger installed via Flathub — my preferred messaging app.
</details>

<details>
<summary><strong>Step 5:</strong> Install Git</summary>

Git installed so I can work with repositories and make commits (otherwise I couldn't have created this repo).
</details>

<details>
<summary><strong>Step 6:</strong> Proton Mail (Flathub wrapper)</summary>

Proton Mail installed via Flathub. This is a wrapper – some apps are wrappers and not official native apps, but for web-based mail apps I find that acceptable.
</details>

<details>
<summary><strong>Step 7:</strong> Install Visual Studio Code</summary>

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
</details>

<details>
<summary><strong>Step 8:</strong> Kleopatra & git commit signing</summary>

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
<summary><strong>Step 9:</strong> Tidal Hifi (Electron)</summary>

I eventually installed the Tidal Hifi Electron app from: https://github.com/Mastermindzh/tidal-hifi/releases/tag/6.1.0

I use this app for my music; there is no official Linux client, so the community Electron version works great for hi-res playback.
</details>

<details>
<summary><strong>Step 10:</strong> Install NVIDIA GPU drivers</summary>

The RTX 4060 requires proprietary NVIDIA drivers for good performance. Nouveau (open-source) performs poorly on modern GPUs.

Full installation guide: [NVIDIA Driver Installation Guide](NVIDIA_DRIVER_INSTALLATION.md)

**Summary:**
- Install NVIDIA driver 580.119.02 via RPM Fusion
- MOK enrollment for Secure Boot
- Kernel parameter for AMD GPU crash fix (external monitors)

After installation, the GPU works correctly with Wayland and CUDA 13.0 support.
</details>

<details>
<summary><strong>Step 11:</strong> Install Bottles (Flathub)</summary>

I installed Bottles via Flathub. Bottles is a Windows compatibility layer based on Wine that allows you to run Windows applications and games on Linux.

Installation via Flathub (Software Center) or command line:
```bash
flatpak install flathub com.usebottles.bottles
```

Bottles makes it easy to create isolated Windows environments (bottles) for different applications. This works well for games like Fortnite or World of Tanks.

**Note:** Microsoft 365 apps (Word, Excel, PowerPoint) unfortunately don't run well under Bottles/Wine. For these, you'll need to set up a full Windows VM with virt-manager.

![Bottles application window showing bottle creation process with status messages: Generating bottle configuration, The Wine config is being updated, Wine config updated, Setting Windows version, Apply CMD default settings, and Enabling font smoothing. A Cancel Creation button is visible at the bottom.](image.png)
</details>

<details>
<summary><strong>Step 12:</strong> Install Archi (ArchiMate modeling tool)</summary>

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
<summary><strong>Step 13:</strong> Set up Windows 11 VM with virt-manager (KVM/QEMU)</summary>

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
<summary><strong>Step 14:</strong> Install Steam for gaming</summary>

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

> **⚠️ IMPORTANT:** Reboot your system after installation, otherwise you'll get crashes on first Steam launch.
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
