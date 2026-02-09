# Zephyrus-Linux

🇳🇱 Nederlands | [🇺🇸 English](README.en.md)

Mijn manier om de ROG Zephyrus G16 GA605WV (2024) goed werkend te krijgen onder Fedora na het verlaten van Microslop Windows. Complete repo voor het draaien van Linux op deze gaming laptop op de manier zoals ik het wil.

## Eerste dingen

Hier zijn de eerste installatie- en setup-stappen die ik gedaan heb. Klik op een stap om de details te zien.

<details>
<summary><strong>Stap 1:</strong> Brave browser installeren (Flathub)</summary>

Ik heb Brave geïnstalleerd via Flathub. De officiële `.sh` script versie van Brave's website crashte regelmatig en wilde soms niet meer openen. De Flatpak versie werkt stabiel.

Installatie via Flathub (Software Center) of command line:
```bash
flatpak install flathub com.brave.Browser
```

Daarna heb ik de instellingen aangepast naar mijn voorkeur.
</details>

<details>
<summary><strong>Stap 2:</strong> Hostname instellen</summary>

Ik heb de hostnaam in de systeeminstellingen gezet naar de gewenste naam.
</details>

<details>
<summary><strong>Stap 3:</strong> Bitwarden desktop (Flathub)</summary>

Ik heb de Bitwarden desktop-app geïnstalleerd via Flathub.
</details>

<details>
<summary><strong>Stap 4:</strong> Signal Messenger (Flathub)</summary>

Signal Messenger geïnstalleerd via Flathub — mijn voorkeurs-app voor messaging.
</details>

<details>
<summary><strong>Stap 5:</strong> Git installeren</summary>

Git geïnstalleerd zodat ik met repositories kan werken en commits kan doen (anders had ik deze repo niet kunnen aanmaken).
</details>

<details>
<summary><strong>Stap 6:</strong> Proton Mail (Flathub wrapper)</summary>

Proton Mail geïnstalleerd via Flathub. Dit is een wrapper – sommige apps zijn wrappers en geen officiële native apps, maar voor webgebaseerde mail-apps vind ik dat acceptabel.
</details>

<details>
<summary><strong>Stap 7:</strong> Visual Studio Code installeren</summary>

Ik heb Visual Studio Code geïnstalleerd volgens de officiële instructies: https://code.visualstudio.com/docs/setup/linux

Op Fedora gebruikte ik de RPM-repo en Microsoft GPG key. Commands die ik gebruikte:

```bash
# Microsoft GPG key importeren en repo toevoegen
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc

echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\nautorefresh=1\ntype=rpm-md\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null

# Repo cache updaten
dnf check-update

# VS Code installeren
sudo dnf install code
```
</details>

<details>
<summary><strong>Stap 8:</strong> Kleopatra & git commit signing</summary>

Na het installeren van VS Code en Git heb ik `kleopatra` geïnstalleerd en via de GUI mijn GPG-keys aangemaakt. Daarna heb ik Git geconfigureerd om commits en tags te ondertekenen.

**EENMALIGE SETUP:**
```bash
git config --global user.name "Sten Tijhuis"
git config --global user.email "102481635+Stensel8@users.noreply.github.com"
git config --global user.signingkey 8E3B0360FED269E75261AC73D13D72C854C880F3
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg
```

Dit zorgt ervoor dat mijn commits automatisch met mijn GPG-key gesigneerd worden.
</details>

<details>
<summary><strong>Stap 9:</strong> Tidal Hifi (Electron)</summary>

Ik heb uiteindelijk de Tidal Hifi Electron-app geïnstalleerd van: https://github.com/Mastermindzh/tidal-hifi/releases/tag/6.1.0

Ik gebruik deze app voor mijn muziek; er is geen officiële Linux-client, dus de community Electron-versie werkt prima voor hi-res afspelen.
</details>

<details>
<summary><strong>Stap 10:</strong> NVIDIA GPU drivers installeren</summary>

De RTX 4060 heeft proprietary NVIDIA drivers nodig voor goede prestaties. Nouveau (open-source) werkt slecht voor moderne GPU's.

Volledige installatie handleiding: [NVIDIA Driver Installation Guide](NVIDIA_DRIVER_INSTALLATION.nl.md)

**Samenvatting:**
- Installeer NVIDIA driver 580.119.02 via RPM Fusion
- MOK enrollment voor Secure Boot
- Kernel parameter voor AMD GPU crash fix (externe monitors)

Na installatie werkt de GPU correct met Wayland en CUDA 13.0 support.
</details>

<details>
<summary><strong>Stap 11:</strong> Bottles installeren (Flathub)</summary>

Ik heb Bottles geïnstalleerd via Flathub. Bottles is een Windows compatibility layer gebaseerd op Wine waarmee je Windows-applicaties kunt draaien op Linux. Dit is vooral handig voor veelgebruikte Windows-apps zoals Microsoft 365 (Word, Excel, PowerPoint) en andere Windows-only software die je op Linux wilt blijven gebruiken.

Installatie via Flathub (Software Center) of command line:
```bash
flatpak install flathub com.usebottles.bottles
```

Bottles maakt het eenvoudig om geïsoleerde Windows-omgevingen (bottles) te creëren voor verschillende applicaties, met ondersteuning voor zowel gaming als productivity software.
![Bottles application window showing bottle creation process with status messages: Generating bottle configuration, The Wine config is being updated, Wine config updated, Setting Windows version, Apply CMD default settings, and Enabling font smoothing. A Cancel Creation button is visible at the bottom.](image.png)
</details>
