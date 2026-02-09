# Zephyrus-Linux

🇺🇸 English | [🇳🇱 Nederlands](README.md)

My way of getting the ROG Zephyrus G16 GA605WV (2024) to work properly under Fedora after ditching Windows. Complete repo for running Linux on this gaming laptop the way I want it.

## Initial Setup

Here are the first installation and setup steps I performed. Click on a step to see the details.

<details>
<summary><strong>Step 1:</strong> Install Brave browser</summary>

I installed and configured Brave the way I like it:

```bash
curl -fsS https://dl.brave.com/install.sh | sh
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
