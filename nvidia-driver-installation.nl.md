# NVIDIA Driver Installatie - ROG Zephyrus G16 GA605WV (2024)

[English](nvidia-driver-installation.md) | Nederlands

Handleiding voor het installeren van NVIDIA proprietary drivers op Fedora 43 met Secure Boot ingeschakeld.

**Systeemconfiguratie:**
- Model: ASUS ROG Zephyrus G16 GA605WV (2024)
- CPU: AMD Ryzen AI 9 HX 370
- GPU: NVIDIA GeForce RTX 4060 Laptop (Max-Q)
- OS: Fedora 43
- Kernel: 6.18.8-200.fc43.x86_64
- Display Server: Wayland (GNOME)
- Secure Boot: Ingeschakeld

**Driver Informatie:**
- Versie: 580.119.02
- Bron: RPM Fusion
- Installatiemethode: akmod (automatisch kernel module rebuilding)


## Vereisten

### Systeem Verificatie

<details>
<summary>Check kernel versie</summary>

Vereist: Kernel 6.10+ voor Ryzen AI 9 HX 370 ondersteuning.

```bash
uname -r
```

</details>

<details>
<summary>Check Secure Boot status</summary>

```bash
mokutil --sb-state
```

</details>

### Waarom Proprietary Driver

De open-source Nouveau driver heeft slechte prestaties op moderne NVIDIA GPU's. De proprietary driver is vereist voor:
- Gaming en graphics-intensieve applicaties
- CUDA workloads
- Goede Wayland ondersteuning (beschikbaar sinds driver 555+)


## Installatiestappen

<details>
<summary><strong>Stap 1:</strong> Repository problemen oplossen</summary>

Bij checksum errors tijdens `dnf update`, clean de cache:

```bash
sudo dnf clean all
sudo dnf makecache
```

</details>

<details>
<summary><strong>Stap 2:</strong> RPM Fusion repositories toevoegen</summary>

RPM Fusion biedt NVIDIA drivers voor Fedora. NVIDIA's officiële CUDA repository ondersteunt Fedora 43 nog niet.

```bash
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y
```

</details>

<details>
<summary><strong>Stap 3:</strong> Systeem updaten</summary>

```bash
sudo dnf update -y
```

Wacht tot update voltooid is.
</details>

<details>
<summary><strong>Stap 4:</strong> Driver versie verifiëren</summary>

Check beschikbare NVIDIA driver versie:

```bash
dnf info akmod-nvidia
```

Controleer dat de versie overeenkomt met de huidige release voor Fedora 43.
</details>

<details>
<summary><strong>Stap 5:</strong> NVIDIA driver installeren</summary>

Installeer driver met CUDA ondersteuning:

```bash
sudo dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda -y
```

Dit installeert de driver, CUDA libraries en build dependencies (ongeveer 1 GB).
- `akmod-nvidia` - Automatische kernel module builder
- `xorg-x11-drv-nvidia` - NVIDIA driver (ondersteunt X11 en Wayland)
- `xorg-x11-drv-nvidia-cuda` - CUDA libraries
- Build dependencies (gcc, kernel-devel, etc.)

</details>

<details>
<summary><strong>Stap 6:</strong> Kernel modules bouwen</summary>

Forceer akmod om NVIDIA kernel modules te bouwen:

```bash
sudo akmods --force
```

Dit proces kan 5-10 minuten duren.
</details>

<details>
<summary><strong>Stap 7:</strong> Kernel modules verifiëren</summary>

Check dat kernel modules gebouwd zijn:

```bash
ls /lib/modules/$(uname -r)/extra/nvidia/
```

Alle vijf kernel modules moeten aanwezig zijn.
</details>

<details>
<summary><strong>Stap 8:</strong> Eerste reboot en GNOME Software checken</summary>

```bash
sudo reboot
```

Na reboot, open GNOME Software en noteer de MOK enrollment code. De driver is nog niet actief.
</details>

<details>
<summary><strong>Stap 9:</strong> MOK enrollment bij volgende boot</summary>

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
</details>

<details>
<summary><strong>Stap 10:</strong> Modules rebuilden na MOK enrollment</summary>

Na MOK enrollment, rebuild de kernel modules. Ze worden nu gesigneerd met de enrolled key.

```bash
sudo akmods --force --rebuild
```

</details>

<details>
<summary><strong>Stap 11:</strong> Definitieve reboot</summary>

```bash
sudo reboot
```

De NVIDIA driver laadt nu correct. GNOME Software toont de driver als geïnstalleerd (niet pending).
</details>

<details>
<summary><strong>Stap 12:</strong> NVIDIA power management services activeren</summary>

Activeer NVIDIA power services voor beter suspend/resume gedrag:

```bash
sudo systemctl enable nvidia-hibernate.service nvidia-suspend.service nvidia-resume.service
```

**Wat deze services doen:**
- `nvidia-hibernate.service` - Slaat GPU state correct op voor hibernation
- `nvidia-suspend.service` - Beheert GPU state tijdens system suspend
- `nvidia-resume.service` - Herstelt GPU state na resume

Deze services voorkomen GPU state problemen na suspend/resume cycli.

**Belangrijk: `nvidia-powerd` niet activeren**

De `nvidia-powerd.service` (NVIDIA dynamisch energiebeheer daemon) kan conflicteren met AMD ATPX power management op de Zephyrus G16 en soft lockups veroorzaken.

Als je `nvidia-powerd` per ongeluk hebt ingeschakeld:
```bash
sudo systemctl disable nvidia-powerd.service
sudo systemctl stop nvidia-powerd.service
```

**Referentie:**
- [NVIDIA Power Management Documentatie](https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/powermanagement.html)
</details>

## Verificatie Na Installatie

<details>
<summary><strong>Test 1:</strong> Verifieer NVIDIA driver</summary>

Na reboot, check driver status:

```bash
nvidia-smi
```

Je ziet de NVIDIA driver- en CUDA-versies in de output.
</details>

<details>
<summary><strong>Test 2:</strong> Verifieer Wayland sessie</summary>

Bevestig dat Wayland draait (niet X11):

```bash
echo $XDG_SESSION_TYPE
```

</details>

<details>
<summary><strong>Test 3:</strong> Check geladen kernel modules</summary>

```bash
lsmod | grep nvidia
```

De NVIDIA modules zijn geladen en de driver is functioneel.
</details>

<details>
<summary><strong>Test 4:</strong> Verifieer in GNOME Software</summary>

Open GNOME Software (witte tas icoon):
- Ga naar "Installed"
- Zoek "NVIDIA Linux Graphics Driver"
- Status moet "Installed" zijn (niet "Pending")
- "Uninstall" knop is zichtbaar

Dit bevestigt dat het systeem de driver erkent als correct geïnstalleerd.
</details>


## Performance Optimalisaties

<details>
<summary>Kernel parameters voor verbeterde performance en stabiliteit</summary>

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

**Referenties:**
- [NVIDIA Driver Modesetting - Arch Wiki](https://wiki.archlinux.org/title/NVIDIA)
- [Understanding nvidia-drm.modeset=1 - NVIDIA Developer Forums](https://forums.developer.nvidia.com/t/understanding-nvidia-drm-modeset-1-nvidia-linux-driver-modesetting/204068)
- [NVIDIA Power Management Documentatie](https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/powermanagement.html)
</details>


## ICC Kleurprofielen

<details>
<summary>ASUS GameVisual kleurprofielen installeren voor Sharp LQ160R1JW02 panel</summary>

De GA605WV wordt geleverd met een Sharp LQ160R1JW02 16" 2560x1600 240Hz display. ASUS kalibreert elk paneel in de fabriek en levert kleurprofielen via hun ASUS System Control Interface. Op Windows worden deze automatisch toegepast door Armoury Crate/GameVisual. Op Linux moeten we deze handmatig installeren.

Deze kleurprofielen zijn geëxtraheerd uit ASUS Windows driver packages en aangepast voor optimale weergave in GNOME Color Management.

**Installeer de kleurprofielen:**

De ICC kleurprofielen staan in de `assets/icc-profiles/` map van deze repository. Clone de repository of download de profielen handmatig en kopieer ze naar `~/.local/share/icc`:

```bash
mkdir -p ~/.local/share/icc

# Als je de repository al hebt gecloned:
cp assets/icc-profiles/*.icm ~/.local/share/icc/

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
</details>


## Bekende Problemen

<details>
<summary>Systeem crasht met externe monitoren (AMD GPU PSR bug)</summary>

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
</details>

<details>
<summary>VS Code crasht systeem (AMD GPU page fault - Kernel 6.18.x bug)</summary>

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
</details>

<details>
<summary>Brave Browser crasht systeem (AMD GPU page fault - Kernel 6.18.x bug)</summary>

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
</details>

<details>
<summary>NVIDIA soft lockup bij minimale GPU load (hybrid GPU power management)</summary>

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

**Fix:**

1. Disable `nvidia-powerd`:
```bash
sudo systemctl disable nvidia-powerd.service
sudo systemctl stop nvidia-powerd.service
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
Systeem is stabieler na deze wijzigingen. De NVIDIA dGPU wordt nog steeds correct beheerd via ATPX (AMD-gestuurde power switching) zonder dat `nvidia-powerd` interfereert.

**Achtergrond:**
Op laptops met AMD iGPU + NVIDIA dGPU regelt het ATPX framework (via ACPI) welke GPU actief is. `nvidia-powerd` probeert zelfstandig power decisions te maken, wat conflicteert met ATPX. De `NVreg_PreserveVideoMemoryAllocations=1` parameter voorkomt dat VRAM verloren gaat tijdens power transitions, en `nvidia-drm.fbdev=1` zorgt voor een schonere framebuffer handoff.
</details>


## Probleemoplossing

<details>
<summary>nvidia-smi command not found of faalt</summary>

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
</details>

<details>
<summary>MOK enrollment problemen of "Key was rejected by service" error</summary>

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
</details>

<details>
<summary>Draait X11 in plaats van Wayland</summary>

Check sessie type:
```bash
echo $XDG_SESSION_TYPE
```

Als output `x11` is, zorg dat Wayland ingeschakeld is in GDM:
```bash
sudo nano /etc/gdm/custom.conf
```

Verifieer dat deze regel aanwezig is en niet gecommentarieerd:
```
WaylandEnable=true
```

Reboot na wijzigingen.
</details>

<details>
<summary>Kernel module build failures</summary>

Zorg dat kernel headers overeenkomen met draaiende kernel:
```bash
sudo dnf install kernel-devel-$(uname -r)
```

Forceer rebuild:
```bash
sudo akmods --force
```
</details>


## Technische goed om te weten

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
