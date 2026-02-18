---
title: "Aan de slag"
weight: 2
---

Dit is mijn persoonlijke setup-log voor de ROG Zephyrus G16 op Fedora Linux. Ik ben geen software-engineer of developer — ik ben gewoon iemand die overgestapt is naar Linux en daarna tegen van alles aan liep wat niet meteen werkte. Ik heb alles opgeschreven zodat anderen niet hetzelfde hoeven uit te zoeken als ik.

Als iets hier je helpt: mooi. Loop je ergens tegenaan wat ik niet behandeld heb, laat het gerust weten — ik denk graag mee. Ik heb niet altijd het antwoord, maar ik doe mijn best.

De stappen hieronder zijn in grote lijnen de volgorde waarop ik dingen heb opgezet na een schone Fedora 43-installatie.

{{% steps %}}

### Brave browser — RPM met Wayland-workarounds

Brave is mijn standaardbrowser. Ik begon met de Flatpak-versie maar ben overgestapt naar de native RPM — mensen op Reddit zeggen dat de RPM-versie nativer aanvoelt en betere prestaties en efficiëntie biedt. Er is alleen een addertje: Brave 1.82+ heeft twee crashbugs op GNOME Wayland die je moet oplossen voordat het écht stabiel is. Ik snap niet helemaal waarom die crashes plaatsvinden — het gaat om GPU-drivers en Wayland-protocollen die blijkbaar niet goed samenwerken — maar de onderstaande fixes werken voor mij.

- **RPM (native):** Nativer gevoel, betere prestaties en efficiëntie. Dit gebruik ik.
- **Flatpak:** Kan in sommige situaties beter werken, maar voelt wat meer geïsoleerd en iets trager.

**RPM Installatie**

{{< callout type="warning" >}}
Op Fedora met GNOME + Wayland heeft Brave 1.82+ twee bekende crashbugs waarvoor workarounds nodig zijn. De eerste wordt via de desktop entry toegepast; de tweede vereist een instelling in `brave://flags`.
{{< /callout >}}

```bash
sudo dnf install dnf-plugins-core
sudo dnf config-manager addrepo --from-repofile=https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo
sudo dnf install brave-browser
```

![Brave installatie-instructies](/images/brave-install.avif)

**Workaround 1: de desktop entry patchen**

Kopieer de systeem-desktop entry naar je gebruikersmap zodat hij niet wordt overschreven bij updates:
```bash
sudo cp /usr/share/applications/brave-browser.desktop ~/.local/share/applications/
```

Patch alle drie de `Exec=` regels met de flag:
```bash
sed -i \
  's|Exec=/usr/bin/brave-browser-stable %U|Exec=/usr/bin/brave-browser-stable --disable-features=WaylandWpColorManagerV1 %U|' \
  ~/.local/share/applications/brave-browser.desktop

sed -i \
  's|Exec=/usr/bin/brave-browser-stable$|Exec=/usr/bin/brave-browser-stable --disable-features=WaylandWpColorManagerV1|' \
  ~/.local/share/applications/brave-browser.desktop

sed -i \
  's|Exec=/usr/bin/brave-browser-stable --incognito$|Exec=/usr/bin/brave-browser-stable --incognito --disable-features=WaylandWpColorManagerV1|' \
  ~/.local/share/applications/brave-browser.desktop
```

Controleer of het gelukt is — je zou exact drie `Exec=` regels moeten zien:
```bash
grep "^Exec" ~/.local/share/applications/brave-browser.desktop
```

**Wat deze flag doet (voor zover ik het begrijp):**

`--disable-features=WaylandWpColorManagerV1` — Brave 1.82+ introduceerde een Wayland color management extensie die blijkbaar conflicteert met de AMD amdgpu-driver op Fedora + GNOME Wayland. Zonder deze flag veroorzaakt Brave GPU ring timeouts die de volledige GNOME Shell-sessie laten crashen. Ik heb geen idee waarom een browser-kleurbeheerfunctie het hele bureaublad kan neerhalen, maar hier zijn we dan.

**Een noot over `--ozone-platform=x11`:** Ik heb deze flag geprobeerd als workaround voor een crash bij het openen of downloaden van Bitwarden-bijlagen — Brave doet dan iets met een Wayland-protocol op een manier die niet geldig is en crasht direct. Via XWayland omzeil je dat. Maar het bleek een erger probleem te veroorzaken: gnome-shell crashte met `SIGABRT` (`g_assertion_message_expr` in `meta_window_unmanage`), getriggerd tijdens Picture-in-Picture video terwijl Brave via XWayland draaide — dezelfde onderliggende mutter-crash als gedocumenteerd in [gnome-mutter issue #4625](https://gitlab.gnome.org/GNOME/mutter/-/issues/4625) en [Fedora bugzilla #2440608](https://bugzilla.redhat.com/show_bug.cgi?id=2440608). Die crash slaat de hele bureaublad-sessie neer en vereist een harde herstart. De flag is weg. Brave draait nu op native Wayland. De Bitwarden-bijlage-crash bestaat nog steeds, maar een Brave-crash is te verkiezen boven het verliezen van de hele sessie.

**Tweede workaround: hardware video decode uitschakelen in `brave://flags`**

{{< callout type="warning" >}}
Hardware video decode veroorzaakt nog steeds crashes, ook met de flag hierboven. Zolang de AMD VCN decoder actief is, crasht GNOME Shell met een SIGABRT (`g_assertion_message_expr`) — reproduceerbaar bij Picture-in-Picture video en bij intensief videobeheer. Zie [gnome-mutter issue #4625](https://gitlab.gnome.org/GNOME/mutter/-/issues/4625) en [Fedora bugzilla #2440608](https://bugzilla.redhat.com/show_bug.cgi?id=2440608). Hardware video decode is **nog niet stabiel** op de AMD Radeon 890M met GNOME Wayland.
{{< /callout >}}

Ga naar `brave://flags` en schakel uit:

- **Hardware-accelerated video decode** → `Disabled`

![Brave flags — hardware video decode uitgeschakeld](/images/brave-flags.avif)

Video wordt nu via software gedecodeerd. Je verliest hardware-versnelling voor video, maar de sessie blijft stabiel. In `brave://gpu` staat daarna:

- `Video Decode: Software only. Hardware acceleration disabled`
- `Video Encode: Software only. Hardware acceleration disabled`

Brave://gpu config — video decode op software (stabiel):

![Brave hardware acceleration config](/images/brave-gpu-config.avif)

**Flatpak Installatie**

Geeft de RPM-versie je problemen, dan is de Flatpak het proberen waard:

```bash
flatpak install flathub com.brave.Browser
```

![Brave Flatpak in Flathub](/images/brave-flathub.avif)

### Hostname instellen

Niets bijzonders — gewoon de hostname instellen via Systeeminstellingen zodat de machine een fatsoenlijke naam heeft op het netwerk.

![Hostname instellen](/images/system-info.avif)

### GNOME-vensterknoppen — minimize en maximize terug

Standaard toont GNOME 49 alleen de sluitknop. Ik wil minimize en maximize ook zichtbaar — één van die kleine dingetjes die me stoorde na jaren Windows. Eén commando lost het op:

```bash
gsettings set org.gnome.desktop.wm.preferences button-layout 'appmenu:minimize,maximize,close'
```

![Voorbeeld van hoe de nieuwe GNOME-vensters eruitzien](/images/window-controls.avif)

### Bitwarden desktop (Flathub)

Ik gebruik Bitwarden voor wachtwoordbeheer. De desktop-app is beschikbaar via Flathub en werkt goed.

![Bitwarden desktop app in Flathub](/images/bitwarden-flathub.avif)

### Signal Messenger (Flathub)

Signal is mijn belangrijkste berichtenapp. Officieel wordt alleen Debian/Ubuntu ondersteund, maar de Flatpak-versie werkt prima op Fedora. Het is gebaseerd op Electron, dus de prestaties zijn redelijk.

![Signal Messenger app in Flathub](/images/signal-flathub.avif)

### Git & GitHub CLI

Git wordt standaard meegeleverd op Fedora. Als het om wat voor reden dan ook niet geïnstalleerd is, of als je ook de GitHub CLI (`gh`) wilt:

```bash
sudo dnf install git gh
```

### Proton Mail (Flathub)

Ik gebruik Proton Mail als e-mailprovider. De desktop-app is een wrapper rondom de webapp, geen echte native client. Voor webgebaseerde mail is dat prima voor mij — hij werkt, en hij zit gewoon in de app launcher zoals elke andere app.

![Proton Mail app in Flathub](/images/protonmail-flathub.avif)

### Visual Studio Code

Ik installeer VS Code via de officiële RPM-repo en Microsoft GPG key, zoals beschreven in de [officiële instructies](https://code.visualstudio.com/docs/setup/linux):

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
Op kernel 6.18.x kan hardware acceleration in VS Code een amdgpu page fault veroorzaken waardoor het systeem bevriest. Zet hardware acceleration uit. Zie de [NVIDIA Driver Installatie]({{< relref "/docs/nvidia-driver-installation" >}}).
{{< /callout >}}

### Kleopatra & GPG commit signing

Ik onderteken mijn Git commits en tags met een GPG-sleutel. Eenmalig instellen, daarna denk je er nooit meer aan. Kleopatra maakt het aanmaken en beheren van sleutels makkelijk via een GUI, zonder dat je de GPG-commandoregel hoeft uit te zoeken.

Na het installeren van VS Code en Git, installeer Kleopatra en maak je sleutels daarin aan. Daarna Git configureren:

```bash
git config --global user.name "JOUW_NAAM"
git config --global user.email "JOUW_EMAIL"
git config --global user.signingkey JOUW_GPG_KEY_ID
git config --global commit.gpgsign true
git config --global tag.gpgsign true
git config --global gpg.program gpg
```

Je sleutel-ID vinden:
```bash
gpg --list-secret-keys --keyid-format=long
```
Gebruik de ID van de `sec` regel (bijv. `rsa4096/JOUW_GPG_KEY_ID`).

### Tidal Hi-Fi (Electron)

Er is geen officiële Tidal-client voor Linux. [Tidal Hi-Fi](https://github.com/Mastermindzh/tidal-hifi) van Rick van Lieshout is een community-Electron-wrapper rondom de Tidal-webapp, met Hi-Fi en Max kwaliteitsondersteuning. Niet officieel, maar werkt goed en staat op Flathub.

![Tidal Hi-Fi in de Flathub store](/images/tidal-hifi-flathub.avif)

### NVIDIA GPU drivers

De G16 heeft een RTX 4060 naast de AMD iGPU. De open-source Nouveau driver werkt slecht op moderne NVIDIA-hardware, dus proprietary drivers zijn nodig voor alles wat graphics-intensief is.

{{< callout type="info" >}}
Volledige installatie-handleiding: [NVIDIA Driver Installatie]({{< relref "/docs/nvidia-driver-installation" >}})
{{< /callout >}}

**Waar ik op uitkwam:**
- NVIDIA driver 580.119.02 via RPM Fusion
- MOK enrollment voor Secure Boot
- Een kernel parameter-workaround voor een AMD GPU-crash met externe monitoren

Daarna werkt de GPU correct op Wayland met CUDA 13.0-ondersteuning.

### Bottles — Windows-software draaien

[Bottles](https://usebottles.com/) laat je Windows-software draaien via Wine. Installeer het via Flathub — de RPM-pakketten in Fedora's repos zijn verouderd en bevatten veel oudere versies. Zorg dat je versie 61 of nieuwer hebt.

- Open GNOME Software Center
- Zoek naar "Bottles"
- Selecteer de **Flathub** bron (niet Fedora Linux / RPM)
- Klik op Installeren

Voor wat niet werkt onder Wine — zoals Microsoft 365 — gebruik ik een Windows VM.

![Bottles in de Flathub store](/images/bottles-flathub.avif)

### Archi (ArchiMate-modelleertool)

Ik gebruik [Archi](https://www.archimatetool.com/) voor ArchiMate-modellering. Gratis en open-source, maar het Linux-pakket is een portable archief — geen installer, geen `.deb`, geen `.rpm`. Om het netjes in GNOME te laten verschijnen met een icoon, moet je de bestanden zelf plaatsen en een desktop entry handmatig aanmaken.

![Archi downloadpagina — Linux versie met Wayland-opmerking](/images/archi-download.avif)

{{< callout type="info" >}}
De downloadpagina van Archi waarschuwt voor mogelijke UI-problemen op Wayland. In mijn ervaring werkt hij prima op GNOME 49 Wayland — tot nu toe geen problemen.
{{< /callout >}}

```bash
# Download en extraheer in één keer
cd /tmp
curl -L https://github.com/archimatetool/archi.io/releases/download/5.7.0/Archi-Linux64-5.7.0.tgz | tar -xz

# Verplaats naar /opt
sudo mv Archi-Linux64-5.7.0/Archi /opt/

# Opruimen
rm -rf Archi-Linux64-5.7.0
cd ~

# Symlink zodat je 'archi' kunt starten vanuit de terminal
sudo ln -s /opt/Archi/Archi /usr/local/bin/archi
```

Desktop entry aanmaken zodat Archi in GNOME verschijnt:
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

Na het opslaan verschijnt Archi in de GNOME-app launcher:

![Archi in de GNOME-app launcher](/images/archi-launcher.avif)

![Archi draaiend op Wayland met GNOME 49](/images/archi-running.avif)

### Windows 11 VM met virt-manager (KVM/QEMU)

Sommige dingen draaien gewoon niet op Linux — Microsoft 365 is het meest voor de hand liggende voorbeeld. Daarvoor heb ik een Windows 11 VM draaien via KVM/QEMU.

{{< callout type="info" >}}
Volledige setup-handleiding: [Windows 11 VM Setup Guide]({{< relref "/docs/vm-setup" >}})
{{< /callout >}}

**Mijn setup:**
- Windows 11 Enterprise, Q35 chipset, UEFI Secure Boot, geëmuleerde TPM 2.0
- virt-manager met KVM/QEMU, host-passthrough CPU, 8 GB RAM, 8 cores
- VirtIO disk (writeback cache, threaded I/O, TRIM/discard), VirtIO netwerk
- SPICE display met GL-acceleratie via AMD iGPU
- Hyper-V enlightenments voor betere Windows-prestaties
- VirtIO Guest Tools en SPICE Guest Tools in de VM

### Steam

Ik game ook op deze machine, dus Steam is een must. Dat heeft de RPM Fusion nonfree repo nodig. De [officiële Fedora gaming documentatie](https://docs.fedoraproject.org/en-US/gaming/proton/) is de moeite waard voor de meest actuele instructies.

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

![Steam in GNOME Software — geïnstalleerd via rpmfusion-nonfree-steam](/images/steam-gnome-software.avif)

Herstart na installatie. Steam bevat Proton standaard, waarmee je veel Windows-games op Linux kunt draaien. Per game kun je een specifieke Proton-versie kiezen via Steam Settings > Compatibility.

{{< callout type="info" >}}
Als Steam niet wil starten, probeer het dan vanuit de terminal:
```bash
__GL_CONSTANT_FRAME_RATE_HINT=3 steam
```
{{< /callout >}}

### Solaar voor Logitech-apparaten

[Solaar](https://github.com/pwr-Solaar/Solaar) beheert Logitech-toetsenborden, muizen en andere randapparatuur via Unifying, Lightspeed, Nano receiver, USB of Bluetooth. Installeer het via Flathub — de Fedora RPM-versie is verouderd. Je wilt versie 1.1.19 of nieuwer.

- Open GNOME Software Center
- Zoek naar "Solaar"
- Selecteer de **Flathub** bron (niet Fedora Linux / RPM)
- Klik op Installeren

![Solaar in GNOME Software — selecteer de Flathub-versie](/images/solaar-flathub.avif)

Het draait in het systray en toont batterijnotificaties voor je apparaten. Je kunt er ook DPI, polling rate en knoppen mee configureren.

![Solaar about screen — version 1.1.19](/images/solaar-about.avif)

### GNOME-sneltoetsen — meer als Windows

Als je vanuit Windows komt, voelt een paar dingen meteen anders zonder de juiste sneltoetsen. Dit zijn de sneltoetsen die ik heb ingesteld om de overstap soepeler te laten lopen.

**Ingebouwde sneltoetsen (via Settings > Keyboard > Keyboard Shortcuts):**

| # | Actie | Sneltoets | Categorie |
|---|-------|-----------|-----------|
| 1 | Desktop tonen (alle vensters verbergen) | `Super+D` | Navigation |
| 2 | Interactieve screenshot | `Shift+Super+S` | Screenshots |
| 3 | Instellingen openen | `Super+I` | System |

**Custom shortcut (via Settings > Keyboard > Keyboard Shortcuts > Custom Shortcuts):**

| # | Actie | Commando | Sneltoets |
|---|-------|----------|-----------|
| 4 | Bestandsbeheer openen | `nautilus` | `Super+E` |

GNOME heeft standaard geen sneltoets voor de bestandsbeheerder, dus die moet je handmatig aanmaken.

### Touchpad-scrollsnelheid — geen native GNOME-instelling (nog niet)

Dit frustreerde me. GNOME 49 en Fedora 43 bieden simpelweg **geen instelling** voor touchpad-scrollsnelheid. KDE Plasma heeft dat al jaren. Er zijn merge requests open in [mutter](https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/1840) en [GNOME Control Center](https://gitlab.gnome.org/GNOME/gnome-control-center/-/merge_requests/991) om het toe te voegen, maar die staan al jaren open en het is onduidelijk wanneer het er ooit van komt. Zie de [GNOME Discourse-discussie](https://discourse.gnome.org/t/adding-scroll-speed-setting-in-gnome/25893) als je nieuwsgierig bent.

In de tussentijd is [libinput-config](https://github.com/lz42/libinput-config) van lz42 een third-party workaround die libinput events onderschept en een scrollmultiplicator toepast. Niet elegant, maar het werkt.

**Installatie (eenmalig):**

```bash
# 1. Dependencies installeren
sudo dnf install -y meson ninja-build libinput-devel git

# 2. libinput-config clonen
git clone https://github.com/lz42/libinput-config.git
cd libinput-config

# 3. Bouwen
meson setup build
ninja -C build

# 4. Systeembreed installeren
sudo ninja -C build install

# 5. Opruimen (optioneel)
cd ..
rm -rf libinput-config
```

**Configuratie voor langzamere touchpad-scroll:**

```bash
sudo tee /etc/libinput.conf >/dev/null << 'EOF'
# libinput-config configuration
override-compositor=enabled

# Touchpad-scroll langzamer (lager = langzamer)
# Standaard: 1.0, geteste waarde: 0.25
scroll-factor=0.25

# Muiswiel normaal houden
discrete-scroll-factor=1.0
EOF
```

Uitloggen en weer inloggen (of reboot), dan `scroll-factor` aanpassen naar voorkeur.

**Terugdraaien:**

```bash
sudo rm /etc/libinput.conf
```

### eduroam (universiteits-wifi)

eduroam werkend krijgen op Linux was echt gedoe. De officiële installers werkten niet, community-tools ook niet, en het kostte me een tijdje voordat ik een setup had die betrouwbaar verbindt. Een handmatige PEAP/MSCHAPv2-configuratie via nmcli bleek de oplossing.

{{< callout type="info" >}}
Volledige handleiding: [eduroam Netwerkinstallatie]({{< relref "/docs/eduroam-network-installation" >}})
{{< /callout >}}

**Wat bij mij werkte:**
- PEAP / MSCHAPv2 met CA-validatie via de systeem-truststore
- `domain-suffix-match` in plaats van het verouderde `altsubject-matches`
- Een geautomatiseerd Python-script of handmatig nmcli-commando

### GDM autologin na LUKS

Na het invoeren van mijn LUKS-wachtwoord bij het opstarten wilde ik niet nog een keer een wachtwoord invoeren om in te loggen. Dit slaat het GDM-inlogscherm over zodat het bureaublad direct laadt na de schijfontsluiting.

{{< callout type="info" >}}
Volledige handleiding: [GDM Autologin]({{< relref "/docs/autologin" >}})
{{< /callout >}}

**Setup:**
- Bewerk `/etc/gdm/custom.conf`
- Stel `AutomaticLoginEnable=True` en `AutomaticLogin=sten` in onder `[daemon]`
- Herstart

{{% /steps %}}
