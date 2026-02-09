# NVIDIA Driver Installatie - ROG Zephyrus G16 GA605WV (2024)

[English](NVIDIA_DRIVER_INSTALLATION.md) | Nederlands

Volledige handleiding voor het installeren van NVIDIA proprietary drivers op Fedora 43 met Secure Boot ingeschakeld.

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

Vereist: Kernel 6.10+ voor Ryzen AI 9 HX 370 ondersteuning

```bash
uname -r
```

Verwachte output:
```
6.18.8-200.fc43.x86_64
```
</details>

<details>
<summary>Check Secure Boot status</summary>

```bash
mokutil --sb-state
```

Verwachte output:
```
SecureBoot enabled
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

Verwachte output:
```
Removed X files, Y directories (total of Z MiB)
Updating and loading repositories:
[...]
Metadata cache created.
```
</details>

<details>
<summary><strong>Stap 2:</strong> RPM Fusion repositories toevoegen</summary>

RPM Fusion biedt NVIDIA drivers voor Fedora. NVIDIA's officiële CUDA repository ondersteunt Fedora 43 nog niet.

```bash
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y
```

Verwachte output:
```
[...]
Installing:
 rpmfusion-free-release          noarch    43-1
 rpmfusion-nonfree-release       noarch    43-1
[...]
Complete!
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

Verwachte output:
```
Name           : akmod-nvidia
Version        : 580.119.02
Release        : 1.fc43
Repository     : rpmfusion-nonfree-nvidia-driver
```
</details>

<details>
<summary><strong>Stap 5:</strong> NVIDIA driver installeren</summary>

Installeer driver met CUDA ondersteuning:

```bash
sudo dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda -y
```

Dit installeert ongeveer 74 packages (~1 GB download):
- `akmod-nvidia` - Automatische kernel module builder
- `xorg-x11-drv-nvidia` - NVIDIA driver (ondersteunt X11 en Wayland)
- `xorg-x11-drv-nvidia-cuda` - CUDA libraries
- `nvidia-settings` - NVIDIA configuratiepaneel
- Build dependencies (gcc, kernel-devel, etc.)

Verwachte output:
```
[...]
Transaction Summary:
 Installing:        74 packages
[...]
Complete!
```
</details>

<details>
<summary><strong>Stap 6:</strong> Kernel modules bouwen</summary>

Forceer akmod om NVIDIA kernel modules te bouwen:

```bash
sudo akmods --force
```

Verwachte output:
```
Checking kmods exist for 6.18.8-200.fc43.x86_64 [  OK  ]
```

Dit proces kan 5-10 minuten duren.
</details>

<details>
<summary><strong>Stap 7:</strong> Kernel modules verifiëren</summary>

Check dat kernel modules gebouwd zijn:

```bash
ls /lib/modules/$(uname -r)/extra/nvidia/
```

Verwachte output:
```
nvidia-drm.ko  nvidia.ko  nvidia-modeset.ko  nvidia-peermem.ko  nvidia-uvm.ko
```

Alle vijf kernel modules moeten aanwezig zijn.
</details>

<details>
<summary><strong>Stap 8:</strong> Eerste reboot en GNOME Software checken</summary>

```bash
sudo reboot
```

Na reboot, open GNOME Software (Software Center - witte tas icoon):
- De NVIDIA driver toont als "Pending"
- Een MOK enrollment notificatie verschijnt met een enrollment code
- Schrijf deze enrollment code op

De driver is op dit punt nog niet functioneel.
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

Verwachte output:
```
Checking kmods exist for 6.18.8-200.fc43.x86_64 [  OK  ]
Building and installing nvidia-kmod [  OK  ]
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

Activeer NVIDIA power services voor beter suspend/resume gedrag en energiebeheer:

```bash
sudo systemctl enable nvidia-hibernate.service nvidia-suspend.service nvidia-resume.service nvidia-powerd.service
```

Verwachte output:
```
Created symlink /etc/systemd/system/systemd-hibernate.service.requires/nvidia-hibernate.service → /usr/lib/systemd/system/nvidia-hibernate.service.
Created symlink /etc/systemd/system/systemd-suspend.service.requires/nvidia-suspend.service → /usr/lib/systemd/system/nvidia-suspend.service.
Created symlink /etc/systemd/system/systemd-resume.service.requires/nvidia-resume.service → /usr/lib/systemd/system/nvidia-resume.service.
Created symlink /etc/systemd/system/multi-user.target.wants/nvidia-powerd.service → /usr/lib/systemd/system/nvidia-powerd.service.
```

**Wat deze services doen:**
- `nvidia-hibernate.service` - Slaat GPU state correct op voor hibernation
- `nvidia-suspend.service` - Beheert GPU state tijdens system suspend
- `nvidia-resume.service` - Herstelt GPU state na resume
- `nvidia-powerd.service` - NVIDIA dynamisch energiebeheer daemon

Deze services voorkomen GPU state problemen na suspend/resume cycli.

**Referentie:**
- [NVIDIA Power Management Documentatie](https://download.nvidia.com/XFree86/Linux-x86_64/470.74/README/powermanagement.html)
</details>

## Verificatie Na Installatie

<details>
<summary><strong>Test 1:</strong> Verifieer NVIDIA driver</summary>

Na reboot, check driver status:

```bash
nvidia-smi
```

Verwachte output:
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 580.119.02             Driver Version: 580.119.02     CUDA Version: 13.0     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4060 ...    Off |   00000000:65:00.0 Off |                  N/A |
| N/A   44C    P8              2W /   65W |      12MiB /   8188MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
```
</details>

<details>
<summary><strong>Test 2:</strong> Verifieer Wayland sessie</summary>

Bevestig dat Wayland draait (niet X11):

```bash
echo $XDG_SESSION_TYPE
```

Verwachte output:
```
wayland
```
</details>

<details>
<summary><strong>Test 3:</strong> Check geladen kernel modules</summary>

```bash
lsmod | grep nvidia
```

Verwachte output (meerdere nvidia modules moeten vermeld staan):
```
nvidia_uvm           4206592  0
nvidia_drm            159744  6
nvidia_modeset       2265088  4 nvidia_drm
nvidia_wmi_ec_backlight    12288  0
nvidia              15896576  62 nvidia_uvm,nvidia_modeset
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
sudo grubby --update-kernel=ALL --args="rd.driver.blacklist=nouveau modprobe.blacklist=nouveau nvidia-drm.modeset=1"
```

**Stap 2: Verifieer dat parameters toegevoegd zijn**

```bash
sudo grubby --info=ALL | grep args
```

Verwachte output moet bevatten:
```
args="... rd.driver.blacklist=nouveau modprobe.blacklist=nouveau nvidia-drm.modeset=1 ..."
```

**Stap 3: Reboot om wijzigingen toe te passen**

```bash
sudo reboot
```

**Wat deze parameters doen:**

- `rd.driver.blacklist=nouveau` - Voorkomt dat de open-source Nouveau driver laadt tijdens early boot (initramfs)
- `modprobe.blacklist=nouveau` - Voorkomt dat Nouveau laadt na boot
- `nvidia-drm.modeset=1` - Schakelt NVIDIA kernel mode setting in voor betere Wayland ondersteuning en performance

**Waarom Nouveau blacklisten:**
- De proprietary NVIDIA driver en Nouveau kunnen niet samen bestaan
- Blacklisting voorkomt conflicten en zorgt ervoor dat de proprietary driver altijd gebruikt wordt
- Als de NVIDIA driver faalt, kun je deze parameters verwijderen uit GRUB om terug te vallen op Nouveau

**Voordelen:**
- Betere Wayland performance en stabiliteit
- Voorkomt driver conflicten tijdens boot
- Verbeterde externe monitor ondersteuning
- Soepelere graphics performance in het algemeen

**Opmerking:** Deze parameters zijn optioneel maar aanbevolen voor optimale performance.

**Referenties:**
- [NVIDIA Driver Modesetting - Arch Wiki](https://wiki.archlinux.org/title/NVIDIA)
- [Understanding nvidia-drm.modeset=1 - NVIDIA Developer Forums](https://forums.developer.nvidia.com/t/understanding-nvidia-drm-modeset-1-nvidia-linux-driver-modesetting/204068)
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


## Command Referentie

Volledige command sequence voor installatie:

```bash
# Systeem verificatie
uname -r
mokutil --sb-state

# Fix repository problemen (indien nodig)
sudo dnf clean all
sudo dnf makecache

# Voeg RPM Fusion repositories toe
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y

# Update systeem
sudo dnf update -y

# Verifieer driver versie
dnf info akmod-nvidia

# Installeer NVIDIA driver
sudo dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda -y

# Bouw kernel modules
sudo akmods --force

# Verifieer modules gebouwd
ls /lib/modules/$(uname -r)/extra/nvidia/

# Eerste reboot (check GNOME Software voor MOK code)
sudo reboot

# Tweede reboot (MOK enrollment blue screen)
sudo reboot

# Na MOK enrollment: rebuild modules met enrolled key
sudo akmods --force --rebuild

# Definitieve reboot
sudo reboot

# Activeer NVIDIA power management services
sudo systemctl enable nvidia-hibernate.service nvidia-suspend.service nvidia-resume.service nvidia-powerd.service

# Optioneel: Voeg performance optimalisatie kernel parameters toe
sudo grubby --update-kernel=ALL --args="rd.driver.blacklist=nouveau modprobe.blacklist=nouveau nvidia-drm.modeset=1"
sudo grubby --info=ALL | grep args
sudo reboot

# Verificatie na installatie
nvidia-smi
echo $XDG_SESSION_TYPE
lsmod | grep nvidia
```


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


