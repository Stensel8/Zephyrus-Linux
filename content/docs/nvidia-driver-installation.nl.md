---
title: "NVIDIA Driver Installatie"
weight: 11
---

De G16 heeft een NVIDIA RTX 4060 naast de AMD iGPU. De open-source Nouveau driver werkt niet goed op moderne NVIDIA-hardware, dus proprietary drivers zijn nodig. Ze werkend krijgen op Fedora met Secure Boot ingeschakeld kost een paar stappen — dit is wat bij mij werkte. Ik liep ook tegen meerdere crashes en lockups aan na de installatie die wat tijd kostten om op te sporen, dus die heb ik ook gedocumenteerd.

**Driver die ik gebruik:**
- Versie: 580.119.02
- Bron: RPM Fusion
- Installatiemethode: akmod (automatisch kernel module rebuilding)


## Vereisten

### Systeem Verificatie

{{% details title="Check kernel versie" closed="true" %}}

Vereist: Kernel 6.18+ voor Ryzen AI 9 HX 370 ondersteuning.

```bash
uname -r
```

{{% /details %}}

{{% details title="Check Secure Boot status" closed="true" %}}

```bash
mokutil --sb-state
```

{{% /details %}}

### Waarom Proprietary Driver

De open-source Nouveau driver heeft slechte prestaties op moderne NVIDIA GPU's. De proprietary driver is vereist voor:
- Gaming en graphics-intensieve applicaties
- CUDA workloads
- Goede Wayland ondersteuning (beschikbaar sinds driver 555+)


## Installatiestappen

{{% steps %}}

### Repository problemen oplossen

Bij checksum errors tijdens `dnf update`, clean de cache:

```bash
sudo dnf clean all
sudo dnf makecache
```

### RPM Fusion repositories toevoegen

RPM Fusion biedt NVIDIA drivers voor Fedora. NVIDIA's officiële CUDA repository ondersteunt Fedora 43 nog niet.

```bash
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y
```

### Systeem updaten

```bash
sudo dnf update -y
```

Wacht tot update voltooid is.

### Driver versie verifiëren

Check beschikbare NVIDIA driver versie:

```bash
dnf info akmod-nvidia
```

Controleer dat de versie overeenkomt met de huidige release voor Fedora 43.

### NVIDIA driver installeren

Installeer driver met CUDA ondersteuning:

```bash
sudo dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda -y
```

Dit installeert de driver, CUDA libraries en build dependencies (ongeveer 1 GB).
- `akmod-nvidia` - Automatische kernel module builder
- `xorg-x11-drv-nvidia` - NVIDIA driver (ondersteunt X11 en Wayland)
- `xorg-x11-drv-nvidia-cuda` - CUDA libraries
- Build dependencies (gcc, kernel-devel, etc.)

### Kernel modules bouwen

Forceer akmod om NVIDIA kernel modules te bouwen:

```bash
sudo akmods --force
```

Dit proces kan 5-10 minuten duren.

### Kernel modules verifiëren

Check dat kernel modules gebouwd zijn:

```bash
ls /lib/modules/$(uname -r)/extra/nvidia/
```

Alle vijf kernel modules moeten aanwezig zijn.

### Eerste reboot en GNOME Software checken

```bash
sudo reboot
```

Na reboot, open GNOME Software en noteer de MOK enrollment code. De driver is nog niet actief.

### MOK enrollment bij volgende boot

Reboot opnieuw:

```bash
sudo reboot
```

Tijdens boot verschijnt het MOK Management scherm (blauw scherm):
1. Selecteer "Enroll MOK"
2. Selecteer "Continue"
3. Selecteer "Yes"
4. Voer de MOK enrollment code in van GNOME Software
5. Reboot

Het systeem boot normaal na MOK enrollment.

### Modules rebuilden na MOK enrollment

Na MOK enrollment, rebuild de kernel modules. Ze worden nu gesigneerd met de enrolled key.

```bash
sudo akmods --force --rebuild
```

### Definitieve reboot

```bash
sudo reboot
```

De NVIDIA driver laadt nu correct. GNOME Software toont de driver als geïnstalleerd (niet pending).

### NVIDIA power management services activeren

Activeer NVIDIA power services voor beter suspend/resume gedrag:

```bash
sudo systemctl enable nvidia-hibernate.service nvidia-suspend.service nvidia-resume.service
```

**Wat deze services doen:**
- `nvidia-hibernate.service` - Slaat GPU state correct op voor hibernation
- `nvidia-suspend.service` - Beheert GPU state tijdens system suspend
- `nvidia-resume.service` - Herstelt GPU state na resume

Deze services voorkomen GPU state problemen na suspend/resume cycli.

**Belangrijk: `nvidia-powerd` niet activeren — permanent masken**

De `nvidia-powerd.service` beheert NVIDIA Dynamic Boost, waarmee extra wattage (~5-15W) van de CPU naar de GPU geschoven wordt tijdens zware GPU-belasting. Hoewel nuttig op Intel-gebaseerde laptops, conflicteert het met AMD ATPX power management op de Zephyrus G16 en veroorzaakt soft lockups en "GPU has fallen off the bus" fouten.

Op deze laptop wordt GPU-vermogensbeheer geregeld via ATPX (AMD-gestuurd via ACPI). De NVIDIA suspend/hibernate/resume services en `supergfxctl` beheren power states correct zonder `nvidia-powerd`.

**Wat je verliest door het uit te zetten:** Minimaal — een paar FPS minder bij zware GPU workloads. De ~5-15W Dynamic Boost is de instabiliteit niet waard op AMD ATPX hardware.

**Uitschakelen en permanent masken:**
```bash
sudo systemctl disable nvidia-powerd.service
sudo systemctl stop nvidia-powerd.service
sudo systemctl mask nvidia-powerd.service
```

Masken maakt een symlink naar `/dev/null`, waardoor geen enkel proces — ook geen NVIDIA driver updates via `dnf` — de service opnieuw kan activeren.

**Als je het later opnieuw wilt proberen** (bijv. na een kernel- of driver-update die het ATPX-conflict mogelijk verhelpt):
```bash
sudo systemctl unmask nvidia-powerd.service
sudo systemctl enable --now nvidia-powerd.service
```

**Referentie:**
- [NVIDIA Power Management Documentatie](https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/powermanagement.html)

{{% /steps %}}

## Verificatie Na Installatie

{{% steps %}}

### Verifieer NVIDIA driver

Na reboot, check driver status:

```bash
nvidia-smi
```

Je ziet de NVIDIA driver- en CUDA-versies in de output.

### Verifieer Wayland sessie

Bevestig dat Wayland draait (niet X11):

```bash
echo $XDG_SESSION_TYPE
```

### Check geladen kernel modules

```bash
lsmod | grep nvidia
```

De NVIDIA modules zijn geladen en de driver is functioneel.

### Verifieer in GNOME Software

Open GNOME Software (witte tas icoon):
- Ga naar "Installed"
- Zoek "NVIDIA Linux Graphics Driver"
- Status moet "Installed" zijn (niet "Pending")
- "Uninstall" knop is zichtbaar

Dit bevestigt dat het systeem de driver erkent als correct geïnstalleerd.

{{% /steps %}}


## Performance Optimalisaties

{{% details title="Kernel parameters voor verbeterde performance en stabiliteit" closed="true" %}}

Het toevoegen van bepaalde kernel parameters kan de NVIDIA driver performance verbeteren, vooral voor Wayland sessies en dual-GPU setups.

**Stap 1: Voeg aanbevolen kernel parameters toe**

```bash
sudo grubby --update-kernel=ALL --args="rd.driver.blacklist=nouveau modprobe.blacklist=nouveau nvidia-drm.modeset=1 nvidia-drm.fbdev=1 nvidia.NVreg_PreserveVideoMemoryAllocations=1"
```

**Stap 2: Verifieer dat parameters toegevoegd zijn**

```bash
sudo grubby --info=ALL | grep args
```

Verwachte output moet de toegevoegde kernel parameters bevatten.

**Stap 3: Reboot om wijzigingen toe te passen**

```bash
sudo reboot
```

**Wat deze parameters doen:**

- `rd.driver.blacklist=nouveau` - Voorkomt dat de open-source Nouveau driver laadt tijdens early boot (initramfs)
- `modprobe.blacklist=nouveau` - Voorkomt dat Nouveau laadt na boot
- `nvidia-drm.modeset=1` - Schakelt NVIDIA kernel mode setting in voor betere Wayland ondersteuning en performance
- `nvidia-drm.fbdev=1` - Laat NVIDIA zijn framebuffer via het kernel DRM framework lopen in plaats van een generiek framebuffer. Verbetert de handoff tussen console en Wayland/GNOME en voorkomt race conditions bij suspend/resume op hybrid GPU laptops
- `nvidia.NVreg_PreserveVideoMemoryAllocations=1` - Behoudt VRAM-allocaties tijdens suspend/resume in plaats van ze vrij te geven en opnieuw op te bouwen. Voorkomt corrupte VRAM na resume, wat soft lockups kan veroorzaken

**Waarom Nouveau blacklisten:**
- De proprietary NVIDIA driver en Nouveau kunnen niet samen bestaan
- Blacklisting voorkomt conflicten en zorgt ervoor dat de proprietary driver altijd gebruikt wordt
- Als de NVIDIA driver faalt, kun je deze parameters verwijderen uit GRUB om terug te vallen op Nouveau

**Voordelen:**
- Betere Wayland performance en stabiliteit
- Voorkomt driver conflicten tijdens boot
- Verbeterde externe monitor ondersteuning
- Stabielere suspend/resume cycli op hybrid GPU setups
- Soepelere graphics performance in het algemeen

**Opmerking:** Deze parameters zijn optioneel maar aanbevolen voor optimale performance.

**Grafische boot splash opnieuw inschakelen:**

Fedora gebruikt `rhgb` (Red Hat Graphical Boot) en `quiet` om een Plymouth splash scherm te tonen tijdens het booten in plaats van scrollende kernel tekst. Als je deze hebt verwijderd tijdens het debuggen van NVIDIA- of boot-problemen, voeg ze opnieuw toe:

```bash
sudo grubby --update-kernel=ALL --args="rhgb quiet"
```

Het standaard Plymouth-thema (`bgrt`) toont het ASUS/BIOS fabrikantlogo. Om in de toekomst boot-problemen te debuggen, kun je ze tijdelijk verwijderen:

```bash
sudo grubby --update-kernel=ALL --remove-args="rhgb quiet"
```

**Referenties:**
- [NVIDIA Driver Modesetting - Arch Wiki](https://wiki.archlinux.org/title/NVIDIA)
- [Understanding nvidia-drm.modeset=1 - NVIDIA Developer Forums](https://forums.developer.nvidia.com/t/understanding-nvidia-drm-modeset-1-nvidia-linux-driver-modesetting/204068)
- [NVIDIA Power Management Documentatie](https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/powermanagement.html)

{{% /details %}}


## ICC Kleurprofielen

{{% details title="ASUS GameVisual kleurprofielen installeren voor Sharp LQ160R1JW02 panel" closed="true" %}}

De GA605WV wordt geleverd met een Sharp LQ160R1JW02 16" 2560x1600 240Hz display. ASUS kalibreert elk paneel in de fabriek en levert kleurprofielen via hun ASUS System Control Interface. Op Windows worden deze automatisch toegepast door Armoury Crate/GameVisual. Op Linux moeten we deze handmatig installeren.

Deze kleurprofielen zijn verkregen door een combinatie van reverse engineering en het uit elkaar trekken van ASUS Windows driver packages. Door de structuur van de ASUS CDN en de inhoud van de driver ZIP-bestanden te analyseren, zijn alle factory-gekalibreerde kleurprofielen voor dit specifieke paneel gevonden. De ICC metadata is vervolgens aangepast zodat de profielen direct met leesbare namen verschijnen in GNOME Color Management.

**Installeer de kleurprofielen:**

De ICC kleurprofielen staan in de [`/icc-profiles/`](https://github.com/Stensel8/Zephyrus-Linux/tree/main/static/icc-profiles) map van deze repository. Clone de repository of download de profielen handmatig en kopieer ze naar `~/.local/share/icc`:

```bash
mkdir -p ~/.local/share/icc

# Als je de repository al hebt gecloned:
cp /icc-profiles/*.icm ~/.local/share/icc/

# Of download de specifieke profielen die je nodig hebt uit de repository
```

**Activeer Native profiel in GNOME:**

1. Open **Instellingen** → **Color Management**
2. Selecteer **Built-In Screen**
3. Klik **Add Profile**
4. Selecteer **Native**
5. Klik **Add**

**Opmerking:** Als GNOME Settings de oude technische namen toont (bijv. "ASUS GA605WV 1002 104D158E CMDEF" in plaats van "Native"), sluit Settings af en heropen, of log uit/in om de color cache te verversen.

**Beschikbare kleurprofielen:**

| GNOME Naam | Bestand | Beschrijving |
|---|---|---|
| **Native** | `GA605WV_1002_104D158E_CMDEF.icm` | **Aanbevolen** - Factory-gekalibreerd voor Sharp LQ160R1JW02 panel, beste kleurnauwkeurigheid |
| DCI-P3 | `ASUS_DCIP3.icm` | Verzadigde DCI-P3 kleuren voor gaming/media (Vivid mode) |
| Display P3 | `ASUS_DisplayP3.icm` | Display P3 colorspace voor Apple-compatibele workflows |
| sRGB | `ASUS_sRGB.icm` | sRGB standaard voor web/foto werk |

**Aanbeveling:**

Gebruik **Native** voor de beste kleurnauwkeurigheid. Dit profiel bevat factory-kalibratie die specifiek is voor het Sharp LQ160R1JW02 panel in deze laptop. De andere profielen (DCI-P3, Display P3, sRGB) zijn generieke kleurruimten zonder panel-specifieke correcties.

**Opmerking:** Het `_1002_` in de bestandsnaam verwijst naar de AMD iGPU (Vendor ID 0x1002), die het interne eDP display aanstuurt op deze hybrid GPU laptop.

**Achtergrond:**

De profielen zijn gevonden door analyse van ASUS Windows driver packages. De ASUS CDN URL structuur:
```
https://dlcdn-rogboxbu1.asus.com/pub/ASUS/APService/Gaming/SYS/ROGS/{id}-{code}-{hash}.zip
```

Voor de GA605WV is dit: `20016-BWVQPK-01624c1cdd5a3c05252bad472fab1240.zip`

De profielen bevatten factory color corrections die specifiek zijn voor het Sharp LQ160R1JW02 panel (Panel ID: 104D158E) dat in dit model laptop wordt gebruikt.

**Technische Details:**

De profielen in deze repository zijn al voorbewerkt met aangepaste ICC metadata 'desc' tags, zodat ze direct met leesbare namen verschijnen in GNOME Color Management. Voor gebruikers die geïnteresseerd zijn in hoe deze modificaties werken, kun je zelf vergelijkbare ICC 'desc' tag manipulatie implementeren met Python's PIL/ImageCms.

{{% /details %}}


## Bekende Problemen

{{% details title="Systeem crasht met externe monitoren (AMD GPU PSR bug)" closed="true" %}}

**Probleem:**
Systeem bevriest of crasht bij gebruik van externe monitoren via Thunderbolt/USB-C, vooral bij het (ont)koppelen van displays. Logs tonen AMD GPU errors:
```
amdgpu 0000:66:00.0: amdgpu: MES failed to respond to msg=RESET
amdgpu 0000:66:00.0: amdgpu: Ring gfx_0.0.0 reset failed
amdgpu 0000:66:00.0: amdgpu: GPU reset begin!
```

**Oorzaak:**
Deze laptop heeft dual GPUs (AMD Radeon 890M integrated + NVIDIA RTX 4060 discrete). De PSR (Panel Self Refresh) feature van de AMD GPU heeft een bug die crashes veroorzaakt met externe Thunderbolt monitoren.

**Oplossing:**
Disable AMD PSR door een kernel parameter toe te voegen:

```bash
sudo grubby --update-kernel=ALL --args="amdgpu.dcdebugmask=0x600"
```

Verifieer dat het toegevoegd is:
```bash
sudo grubby --info=ALL | grep args
```

Reboot:
```bash
sudo reboot
```

**Wat dit doet:**
- `amdgpu.dcdebugmask=0x600` schakelt PSR (Panel Self Refresh) uit op de AMD GPU
- PSR is een power-saving feature waarbij het display zichzelf refresht zonder GPU betrokkenheid
- De PSR implementatie heeft bugs met Thunderbolt/USB-C externe monitoren

**Trade-offs:**
- Pro: Stabiel systeem met externe monitoren
- Con: Iets hoger stroomverbruik (PSR uitgeschakeld)

**Verificatie:**
Monitor voor AMD GPU errors tijdens gebruik van externe displays:
```bash
sudo journalctl -f -k | grep -i amdgpu
```

Als er geen `amdgpu: [drm] *ERROR*` berichten verschijnen, werkt de fix.

**Referentie:**
- [Fedora Discussion: Zephyrus G16 External Monitor Crashes](https://discussion.fedoraproject.org/t/asus-zephyrus-g16-with-nvidia-and-external-monitor-crashes-every-few-minutes/147175)

{{% /details %}}

{{% details title="VS Code crasht systeem (AMD GPU page fault - Kernel 6.18.x bug)" closed="true" %}}

**Wat speelt er:**
Systeem bevriest volledig tijdens VS Code gebruik. Kernel 6.18.x/6.19.x hebben kritieke amdgpu driver bugs. VS Code hardware acceleratie triggert AMD Radeon 890M page fault → volledige freeze.

**Fix:**
Voeg toe aan `~/.config/Code/User/settings.json`:
```json
{
    "disable-hardware-acceleration": true
}
```

**Vervolg:**
Herstart VS Code. Systeem blijft nu stabiel, VS Code iets langzamer maar prima bruikbaar.

**Bronnen:**
- [VS Code Issue #238088](https://github.com/microsoft/vscode/issues/238088)
- [Framework: Critical amdgpu bugs kernel 6.18.x](https://community.frame.work/t/attn-critical-bugs-in-amdgpu-driver-included-with-kernel-6-18-x-6-19-x/79221)

{{% /details %}}

{{% details title="Brave Browser crasht systeem (AMD GPU page fault - Kernel 6.18.x bug)" closed="true" %}}

**Wat speelt er:**
Systeem bevriest of crasht tijdens Brave Browser gebruik, zelfs bij minimale workload (enkele tabs). Dit is hetzelfde onderliggende probleem als de VS Code crash: Chromium-gebaseerde applicaties met hardware acceleratie triggeren AMD Radeon 890M page faults op kernel 6.18.x/6.19.x.

Typische crash sequence in logs:
```
amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:2)
amdgpu: Faulty UTCL2 client ID: SQC (data)
amdgpu: ring gfx_0.0.0 timeout, signaled seq=302899, emitted seq=302901
amdgpu: GPU reset begin!
```

Na GPU reset crasht gnome-shell (Signal 6 ABRT) omdat het een context reset detecteert.

**Fix:**
Open Brave Browser en ga naar `brave://settings/system`. Zet **"Use hardware acceleration when available"** uit.

Alternatief via terminal:
```bash
sed -i 's/"hardware_acceleration_mode_previous":true/"hardware_acceleration_mode_previous":false/' ~/.config/BraveSoftware/Brave-Browser/Local\ State
```

Of start Brave met de `--disable-gpu` flag:
```bash
brave-browser-stable --disable-gpu
```

**Vervolg:**
Herstart Brave. Verifieer via `brave://gpu` dat GPU acceleration uitgeschakeld is. Systeem blijft nu stabiel, Brave is iets langzamer bij zware pagina's maar prima bruikbaar.

**Achtergrond:**
Brave, VS Code, en andere Chromium-gebaseerde applicaties (Chrome, Edge, Electron apps) gebruiken GPU shader compilatie via Mesa. Op kernel 6.18.x heeft de amdgpu driver een bug in de Shader Queue Controller (SQC) memory access, waardoor page faults ontstaan die een volledige GPU reset triggeren. De fix is hardware acceleratie uitschakelen per applicatie totdat een kernel/Mesa update het probleem verhelpt.

**Bronnen:**
- [Framework: Critical amdgpu bugs kernel 6.18.x](https://community.frame.work/t/attn-critical-bugs-in-amdgpu-driver-included-with-kernel-6-18-x-6-19-x/79221)

{{% /details %}}

{{% details title="NVIDIA soft lockup bij minimale GPU load (hybrid GPU power management)" closed="true" %}}

**Wat speelt er:**
Systeem bevriest met een NVIDIA soft lockup, zelfs zonder actief GPU gebruik. Kernel logs tonen:
```
watchdog: BUG: soft lockup - CPU#23 stuck for 62s!
NVRM: Xid (PCI:0000:65:00): 79, pid=<...>, GPU has fallen off the bus
```

Dit kan optreden door een combinatie van factoren op hybrid GPU laptops:
- `nvidia-powerd` conflicteert met AMD ATPX power management
- NVIDIA dGPU power state transitions falen
- Corrupte VRAM na suspend/resume cycli

**Extra symptoom: Reboot hangt (zwart scherm, backlights blijven aan)**

Het systeem lijkt af te sluiten maar voltooit de hardware reset niet — het scherm wordt zwart maar toetsenbord- en schermverlichting blijven aan. Dit gebeurt wanneer `nvidia-powerd` interfereert met ACPI power state transitions tijdens shutdown/reboot.

**Oorzaak: `supergfxd` start `nvidia-powerd` achter je rug om**

Zelfs wanneer `nvidia-powerd` is uitgeschakeld via `systemctl disable`, roept `supergfxd` (de GPU switching daemon van asusctl) direct `systemctl start nvidia-powerd.service` aan tijdens GPU mode switches. Dit omzeilt de disabled status en activeert het conflict met ATPX opnieuw.

**Hoe dit is gediagnosticeerd:**

De logs van de vastgelopen boot tonen dat `supergfxd` nvidia-powerd opstartte:
```bash
journalctl -b -1 --no-pager | grep -iE "nvidia.*powerd|supergfxd"
```

Bewijsmateriaal:
```
supergfxd: [DEBUG supergfxctl] Did CommandArgs { inner: ["start", "nvidia-powerd.service"] }
nvidia-powerd: ERROR! Client (presumably SBIOS) has requested to disable Dynamic Boost DC controller
```

De SBIOS-fout bevestigt dat de firmware Dynamic Boost weigerde, maar `nvidia-powerd` draaide al en interfereerde met power state management. De shutdown-sequentie controleren:

```bash
journalctl -b -1 --reverse | head -20
```

Toont dat de hardware watchdog niet kon stoppen, wat bevestigt dat de ACPI reboot nooit voltooid is:
```
watchdog: watchdog0: watchdog did not stop!
```

**Fix:**

1. Disable en **mask** `nvidia-powerd` (masken is essentieel — `disable` alleen is niet genoeg omdat `supergfxd` het omzeilt):
```bash
sudo systemctl disable nvidia-powerd.service
sudo systemctl stop nvidia-powerd.service
sudo systemctl mask nvidia-powerd.service
```

2. Voeg kernel parameters toe voor stabielere NVIDIA power management:
```bash
sudo grubby --update-kernel=ALL --args="nvidia-drm.fbdev=1 nvidia.NVreg_PreserveVideoMemoryAllocations=1"
```

3. Reboot:
```bash
sudo reboot
```

**Vervolg:**
Systeem is stabieler na deze wijzigingen. De NVIDIA dGPU wordt nog steeds correct beheerd via ATPX (AMD-gestuurde power switching) zonder dat `nvidia-powerd` interfereert. De mask maakt een symlink naar `/dev/null`, waardoor geen enkel proces — inclusief `supergfxd` en NVIDIA driver updates — de service opnieuw kan activeren.

**Achtergrond:**
Op laptops met AMD iGPU + NVIDIA dGPU regelt het ATPX framework (via ACPI) welke GPU actief is. `nvidia-powerd` probeert zelfstandig power decisions te maken, wat conflicteert met ATPX. De `NVreg_PreserveVideoMemoryAllocations=1` parameter voorkomt dat VRAM verloren gaat tijdens power transitions, en `nvidia-drm.fbdev=1` zorgt voor een schonere framebuffer handoff.

{{% /details %}}


## Probleemoplossing

{{% details title="nvidia-smi command not found of faalt" closed="true" %}}

Check of NVIDIA modules geladen zijn:
```bash
lsmod | grep nvidia
```

Check system logs voor errors:
```bash
sudo journalctl -b | grep nvidia
```

Rebuild kernel modules:
```bash
sudo akmods --force --rebuild
sudo reboot
```

{{% /details %}}

{{% details title="MOK enrollment problemen of \"Key was rejected by service\" error" closed="true" %}}

Als je de error krijgt `modprobe: ERROR: could not insert 'nvidia': Key was rejected by service`, zijn de kernel modules gebouwd voordat MOK enrollment voltooid was.

Oplossing:
```bash
# Rebuild modules na MOK enrollment
sudo akmods --force --rebuild

# Reboot
sudo reboot
```

Om MOK te resetten indien nodig:
```bash
sudo mokutil --reset
```

Reboot en probeer enrollment opnieuw.

{{% /details %}}

{{% details title="Draait X11 in plaats van Wayland" closed="true" %}}

Check sessie type:
```bash
echo $XDG_SESSION_TYPE
```

Als output `x11` is, zorg dat Wayland ingeschakeld is in GDM:
```bash
sudo nano /etc/gdm/custom.conf
```

Verifieer dat deze regel aanwezig is en niet uitgecommentarieerd:
```
WaylandEnable=true
```

Reboot na wijzigingen.

{{% /details %}}

{{% details title="Kernel module build failures" closed="true" %}}

Zorg dat kernel headers overeenkomen met draaiende kernel:
```bash
sudo dnf install kernel-devel-$(uname -r)
```

Forceer rebuild:
```bash
sudo akmods --force
```

{{% /details %}}


## Technische weetjes

### Package Naming
De package `xorg-x11-drv-nvidia` is een legacy naam. De driver ondersteunt zowel X11 als Wayland. Fedora 43 gebruikt standaard Wayland met GNOME.

### Secure Boot
Akmod handelt Secure Boot module signing automatisch af. De akmods systemd service rebuildt kernel modules automatisch na kernel updates.

### GNOME Software
GNOME Software toont "NVIDIA Linux Graphics Driver" met "Pending" status na initiële installatie. Dit is normaal. Na MOK enrollment en module rebuild wordt de status "Installed".


## Aanvullende Bronnen

- [RPM Fusion NVIDIA Driver Guide](https://www.if-not-true-then-false.com/2015/fedora-nvidia-guide/)
- [Ryzen AI 9 HX 370 Linux Support](https://forums.linuxmint.com/viewtopic.php?t=429052)
- [NVIDIA vs Nouveau Performance](https://machaddr.substack.com/p/nouveau-vs-nvidia-the-battle-between)
- [Zephyrus G16 2024 Linux Guide](https://www.ehmiiz.se/blog/linux_asus_g16_2024/)
- [Fedora Discussion: Zephyrus External Monitor Issues](https://discussion.fedoraproject.org/t/asus-zephyrus-g16-with-nvidia-and-external-monitor-crashes-every-few-minutes/147175)
