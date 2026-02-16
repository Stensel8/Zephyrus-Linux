---
title: "Aan de slag"
weight: 2
---

Complete setup-handleiding voor de ROG Zephyrus G16 op Fedora Linux. Volg de stappen op volgorde om van een verse Fedora 43-installatie naar een volledig geconfigureerd systeem te gaan.

{{% steps %}}

### Brave browser installeren (Flathub)

Ik heb Brave geïnstalleerd via Flathub. De officiële `.sh` script versie van Brave's website crashte regelmatig en wilde soms niet meer openen. De Flatpak versie werkt stabiel.

**Installatie:**
- Open GNOME Software Center
- Zoek naar "Brave"
- Klik op Installeren

![Brave Browser in de Flathub store](/images/brave-flathub.png)

### Hostname instellen

Stel de hostnaam in via de systeeminstellingen naar de gewenste naam.

![Hostname instellen](/images/system-info.png)

### GNOME vensterknoppen configureren

Ik heb de venster-knoppen in GNOME 49 aangepast om minimize, maximize en close knoppen te tonen. Standaard toont GNOME alleen de close knop.

![Een voorbeeld van hoe de nieuwe GNOME vensters eruit zien](/images/window-controls.png)

**Configuratie:**
```bash
gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:minimize,maximize,close'
```

Dit zorgt ervoor dat alle drie de vensterknoppen (minimize, maximize/zoom, en close) zichtbaar zijn in de titelbalk van applicaties, vergelijkbaar met andere desktop-omgevingen.

### Bitwarden desktop (Flathub)

Installeer de Bitwarden desktop-app via Flathub.

![Bitwarden desktop app in Flathub](/images/bitwarden-flathub.png)

### Signal Messenger (Flathub)

Signal Messenger geïnstalleerd via Flathub. Mijn voorkeurs-app voor messaging. Officieel is Signal alleen voor Debian/Ubuntu, maar de Flatpak versie werkt prima op Fedora. Signal is gebouwd op Electron, dus biedt goede prestaties.

![Signal Messenger app in de Flathub store](/images/signal-flathub.png)

### Git installeren

Git is nodig om met repositories te werken en commits te doen. Op Fedora wordt Git standaard meegeïnstalleerd als onderdeel van het systeem. Mocht het om wat voor reden dan ook niet geïnstalleerd zijn, dan kan het handmatig met:

```bash
sudo dnf install git
```

### Proton Mail (Flathub wrapper)

Proton Mail geïnstalleerd via Flathub. Dit is een wrapper. Sommige apps zijn wrappers en geen officiële native apps, maar voor webgebaseerde mail-apps vind ik dat acceptabel.

![Proton Mail app in Flathub](/images/protonmail-flathub.png)

### Visual Studio Code installeren

Installeer Visual Studio Code volgens de [officiële instructies](https://code.visualstudio.com/docs/setup/linux).

Op Fedora gebruik je de RPM-repo en Microsoft GPG key:

```bash
# Microsoft GPG key importeren en repo toevoegen
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc

echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\nautorefresh=1\ntype=rpm-md\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo > /dev/null

# Repo cache updaten
dnf check-update

# VS Code installeren
sudo dnf install code
```

{{< callout type="warning" >}}
Op kernel 6.18.x kan hardware acceleration in VS Code een amdgpu page fault veroorzaken. Zet hardware acceleration uit. Zie de [NVIDIA Driver Installatie]({{< relref "/docs/nvidia-driver-installation" >}}).
{{< /callout >}}

### Kleopatra & git commit signing

Na het installeren van VS Code en Git, installeer `kleopatra` en maak je GPG-keys aan via de GUI. Daarna configureer je Git om commits en tags te ondertekenen.

**Eenmalige setup:**
```bash
git config --global user.name "JOUW_NAAM"
git config --global user.email "JOUW_EMAIL"
git config --global user.signingkey JOUW_GPG_KEY_ID
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg
```

**Vind je GPG key ID:**
```bash
gpg --list-secret-keys --keyid-format=long
```
Gebruik de key ID van de `sec` regel (bijv. `rsa4096/JOUW_GPG_KEY_ID`).

### Tidal Hi-Fi (Electron)

Er is geen officiële Tidal-client voor Linux. [Tidal Hi-Fi](https://github.com/Mastermindzh/tidal-hifi) van Rick van Lieshout (Mastermindzh) is een community Electron-client die de Tidal webplayer wrapt met Hi-Fi en Max kwaliteit ondersteuning. Installeer via Flathub.

![Tidal Hi-Fi in de Flathub store](/images/tidal-hifi-flathub.png)

### NVIDIA GPU drivers installeren

De RTX 4060 heeft proprietary NVIDIA drivers nodig voor goede prestaties. Nouveau (open-source) werkt slecht voor moderne GPU's.

{{< callout type="info" >}}
Volledige installatie handleiding: [NVIDIA Driver Installatie]({{< relref "/docs/nvidia-driver-installation" >}})
{{< /callout >}}

**Samenvatting:**
- Installeer NVIDIA driver 580.119.02 via RPM Fusion
- MOK enrollment voor Secure Boot
- Kernel parameter voor AMD GPU crash fix (externe monitors)

Na installatie werkt de GPU correct met Wayland en CUDA 13.0 support.

### Bottles installeren (Flathub)

[Bottles](https://usebottles.com/) laat je Windows software draaien op Linux via Wine. Installeer via Flathub — de RPM-pakketten uit Fedora's repos zijn verouderd en bevatten oudere versies. Zorg dat je minimaal versie 61 hebt.

**Installatie:**
- Open GNOME Software Center
- Zoek naar "Bottles"
- Selecteer de **Flathub** bron (niet Fedora Linux / RPM)
- Klik op Installeren

Voor Microsoft 365 is een Windows VM nodig.

![Bottles in de Flathub store](/images/bottles-flathub.png)

![Bottles application window](/images/bottles-install.png)

### Archi installeren (ArchiMate modelleertool)

[Archi](https://www.archimatetool.com/) is een gratis, open-source tool voor het maken van ArchiMate modellen. Download het van de [officiële downloadpagina](https://www.archimatetool.com/download/).

![Archi downloadpagina — Linux versie met Wayland opmerking](/images/archi-download.png)

Het Linux-pakket is een portable archief — er is geen installer, `.deb` of `.rpm`. Om Archi als een gewone applicatie met icoon in GNOME te laten verschijnen, moet je de bestanden zelf verplaatsen en een desktop entry aanmaken.

{{< callout type="info" >}}
De downloadpagina van Archi waarschuwt voor mogelijke UI-problemen op Wayland. In mijn ervaring werkt Archi prima op Wayland met GNOME 49 — tot nu toe geen problemen.
{{< /callout >}}

**Installatie:**
```bash
# Download en extract in één flow
cd /tmp
curl -L https://github.com/archimatetool/archi.io/releases/download/5.7.0/Archi-Linux64-5.7.0.tgz | tar -xz

# Move naar /opt
sudo mv Archi-Linux64-5.7.0/Archi /opt/

# Cleanup
rm -rf Archi-Linux64-5.7.0
cd ~

# Symlink zodat je 'archi' kunt starten vanuit de terminal
sudo ln -s /opt/Archi/Archi /usr/local/bin/archi
```

**Desktop entry aanmaken zodat Archi in GNOME verschijnt:**
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

Na het opslaan van de desktop entry verschijnt Archi in de GNOME applicatie launcher:

![Archi in de GNOME applicatie launcher](/images/archi-launcher.png)

![Archi draaiend op Wayland met GNOME 49](/images/archi-running.png)

### Windows 11 VM opzetten met virt-manager (KVM/QEMU)

Voor apps die niet onder Wine/Bottles draaien (zoals Microsoft 365) kun je een Windows 11 VM opzetten.

{{< callout type="info" >}}
Volledige setup guide: [Windows 11 VM Setup Guide]({{< relref "/docs/vm-setup" >}})
{{< /callout >}}

**Samenvatting:**
- Windows 11 Enterprise met Q35 chipset, UEFI Secure Boot en geëmuleerde TPM 2.0
- virt-manager met KVM/QEMU, host-passthrough CPU, 8 GB RAM, 8 cores
- VirtIO disk (writeback cache, threaded I/O, TRIM/discard), VirtIO netwerk
- SPICE display met GL-acceleratie via AMD iGPU
- Hyper-V enlightenments voor geoptimaliseerde Windows-prestaties
- VirtIO Guest Tools en SPICE Guest Tools vereist in de VM

### Steam installeren voor gaming

Steam vereist de RPM Fusion nonfree repository. Volg de [officiële Fedora gaming documentatie](https://docs.fedoraproject.org/en-US/gaming/proton/) voor de meest recente instructies.

**RPM Fusion repositories activeren (free + nonfree):**
```bash
sudo dnf install \
  https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm \
  https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y
```

**Cisco OpenH264 repository inschakelen:**
```bash
sudo dnf config-manager setopt fedora-cisco-openh264.enabled=1
```

**Steam installeren:**
```bash
sudo dnf install steam -y
```

![Steam in GNOME Software — geïnstalleerd via rpmfusion-nonfree-steam](/images/steam-gnome-software.png)

Herstart na installatie. Steam bevat standaard Proton, waarmee je veel Windows-games op Linux kunt draaien. Je kunt specifieke Proton-versies per game selecteren via Steam Settings > Compatibility.

{{< callout type="info" >}}
Als Steam niet wil starten, probeer dan vanuit de terminal:
```bash
__GL_CONSTANT_FRAME_RATE_HINT=3 steam
```
{{< /callout >}}

### Solaar installeren voor Logitech apparaten

[Solaar](https://github.com/pwr-Solaar/Solaar) beheert Logitech toetsenborden, muizen en trackpads die verbinden via Unifying, Lightspeed, Nano receiver, USB-kabel of Bluetooth. Installeer via Flathub — het Fedora RPM-pakket is verouderd en bevat een oudere versie. Zorg dat je minimaal versie 1.1.19 hebt.

**Installatie:**
- Open GNOME Software Center
- Zoek naar "Solaar"
- Selecteer de **Flathub** bron (niet Fedora Linux / RPM)
- Klik op Installeren

![Solaar in GNOME Software — selecteer de Flathub versie](/images/solaar-flathub.png)

**Functies:**
- Batterijniveau monitoren van Logitech-apparaten
- Configureren van DPI, polling rate, en knoppen
- Beheer van meerdere apparaten op één Unifying-ontvanger
- Ondersteuning voor zowel Unifying als Bluetooth-apparaten

Solaar draait als een systray-applicatie en toont notificaties wanneer de batterij van een apparaat bijna leeg is.

### GNOME sneltoetsen instellen (Windows-stijl)

Om de overgang van Windows soepeler te maken, stel je sneltoetsen in die vergelijkbaar zijn met Windows.

**Ingebouwde sneltoetsen (via Settings > Keyboard > Keyboard Shortcuts):**

| # | Actie | Sneltoets | Categorie |
|---|-------|-----------|-----------|
| 1 | Desktop tonen (alle vensters verbergen) | `Super+D` | Navigation |
| 2 | Screenshot interactief maken | `Shift+Super+S` | Screenshots |
| 3 | Instellingen openen | `Super+I` | System |

**Custom shortcut (via Settings > Keyboard > Keyboard Shortcuts > Custom Shortcuts):**

| # | Actie | Commando | Sneltoets |
|---|-------|----------|-----------|
| 4 | Bestandsbeheer openen | `nautilus` | `Super+E` |

De custom shortcut voor de bestandsbeheerder moet handmatig worden aangemaakt omdat GNOME hier geen standaard sneltoets voor heeft.

### Touchpad scroll speed aanpassen (optioneel)

Op GNOME 49 en Fedora 43 is er **geen native instelling** voor touchpad scroll snelheid. Het GNOME instellingenpaneel biedt dit simpelweg niet aan — in tegenstelling tot KDE Plasma, dat dit al jaren heeft. Er zijn [merge requests in mutter](https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/1840) en [GNOME Control Center](https://gitlab.gnome.org/GNOME/gnome-control-center/-/merge_requests/991) om dit toe te voegen, maar deze staan al jaren open en het is onduidelijk of ze in GNOME 50 (verwacht met Fedora 44) worden meegeleverd. Zie de [GNOME Discourse discussie](https://discourse.gnome.org/t/adding-scroll-speed-setting-in-gnome/25893) voor context.

In de tussentijd is [libinput-config](https://github.com/lz42/libinput-config) van lz42 een third-party workaround die libinput events onderschept en een scroll multiplier toepast.

**Installatie (éénmalig):**

```bash
# 1. Dependencies installeren
sudo dnf install -y meson ninja-build libinput-devel git

# 2. libinput-config clonen
git clone https://github.com/lz42/libinput-config.git
cd libinput-config

# 3. Bouwen
meson setup build
ninja -C build

# 4. Installeren in het systeem
sudo ninja -C build install

# 5. Opruimen (optioneel)
cd ..
rm -rf libinput-config
```

**Configuratie voor langzamere touchpad scroll:**

```bash
sudo tee /etc/libinput.conf >/dev/null << 'EOF'
# libinput-config configuration
override-compositor=enabled

# Maak touchpad-scroll trager (lager = trager)
# Standaard: 1.0, geteste waarde: 0.25
scroll-factor=0.25

# Laat muiswieltjes normaal gedrag houden
discrete-scroll-factor=1.0
EOF
```

Log uit en weer in (of reboot) en pas `scroll-factor` aan naar voorkeur.

**Rollback:**

```bash
sudo rm /etc/libinput.conf
```

### GDM autologin na LUKS

Sla het GDM inlogscherm over na LUKS ontgrendeling. Na het invoeren van je schijfwachtwoord bij het opstarten laadt het bureaublad direct.

{{< callout type="info" >}}
Volledige handleiding: [GDM Autologin Handleiding]({{< relref "/docs/autologin" >}})
{{< /callout >}}

**Samenvatting:**
- Bewerk `/etc/gdm/custom.conf`
- Stel `AutomaticLoginEnable=True` en `AutomaticLogin=sten` in onder `[daemon]`
- Herstart

{{% /steps %}}
