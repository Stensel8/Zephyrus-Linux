---
title: "Looking Glass B7 — GPU Passthrough Poging"
weight: 21
---

> **Vereiste:** Deze handleiding gaat ervan uit dat je al een werkende Windows 11 VM hebt opgezet met virt-manager. Zo niet, volg dan eerst de [VM Setup Handleiding]({{< relref "/docs/vm-setup" >}}).

> **TL;DR:** Looking Glass werkt **niet** op de ASUS ROG Zephyrus G16 GA605WV. De fundamentele beperking is dat de RTX 4060 geen display-outputs heeft — alle fysieke poorten (HDMI, USB-C) lopen via de AMD iGPU. Windows kan daardoor geen "valid output device" vinden voor frame capture. Dit document beschrijft alle stappen die zijn uitgevoerd en waarom het mislukt, als referentie voor anderen.


## Wat is Looking Glass?

[Looking Glass](https://looking-glass.io) is een open-source project waarmee je een GPU-passthrough Windows VM kunt gebruiken **zonder fysiek scherm** aan de dGPU. De Windows VM krijgt de echte GPU toegewezen en het beeld wordt via gedeeld geheugen (IVSHMEM) naar de Linux host gestreamd. Het resultaat is near-native GPU performance in een VM, zichtbaar in een venster op je Linux desktop.

**Vereisten voor werking:**
- dGPU met directe display-output (DisplayPort, HDMI) — of een virtuele display dongle
- IOMMU-isolatie van de dGPU van de rest van het systeem
- KVMFR kernel module op de host
- Looking Glass host application in de Windows VM

---

**Systeemconfiguratie:**
- Model: ASUS ROG Zephyrus G16 GA605WV (2024)
- CPU: AMD Ryzen AI 9 HX 370
- iGPU: AMD Radeon 890M — card0, renderD128
- dGPU: NVIDIA GeForce RTX 4060 Mobile — card1, renderD129
- OS: Fedora 43, kernel 6.18.9
- Secure Boot: Ingeschakeld
- VM: Windows 11 (AtlasOS 0.5.0)


## Fase 1 — IOMMU en VFIO instellen

### IOMMU-groepen checken

```bash
for d in /sys/kernel/iommu_groups/*/devices/*; do
    n=${d#*/iommu_groups/*}; n=${n%%/*}
    printf 'IOMMU Group %s ' "$n"
    lspci -nns "${d##*/}"
done | grep -E "NVIDIA|AMD|10de|1002" | head -20
```

De RTX 4060 zat in een schone eigen groep:
```
IOMMU Group 20: 65:00.0 VGA [10de:28e0] NVIDIA GeForce RTX 4060 Max-Q
IOMMU Group 20: 65:00.1 Audio [10de:22be] NVIDIA HD Audio
IOMMU Group 21: 66:00.0 Display [1002:150e] AMD Radeon 890M
```

### VFIO kernel parameters instellen

```bash
sudo grubby --update-kernel=ALL \
  --args="vfio-pci.ids=10de:28e0,10de:22be \
          rd.driver.pre=vfio-pci \
          iommu=1 \
          rd.driver.blacklist=nouveau,nova_core \
          modprobe.blacklist=nouveau,nova_core \
          amdgpu.dcdebugmask=0x600"
```

### VFIO configuratiebestanden aanmaken

**`/etc/modprobe.d/vfio.conf`:**
```
options vfio-pci ids=10de:28e0,10de:22be
softdep nvidia pre: vfio-pci
softdep nvidia_drm pre: vfio-pci
softdep nvidia_modeset pre: vfio-pci
softdep nouveau pre: vfio-pci
```

**`/etc/dracut.conf.d/vfio.conf`:**
```
add_drivers+=" vfio vfio_iommu_type1 vfio_pci "
```

### nvidia-fallback.service uitschakelen

Bij VFIO claimt `vfio-pci` de GPU vóór de NVIDIA driver, waardoor `nvidia-fallback.service` foutmeldingen geeft:

```bash
sudo systemctl disable nvidia-fallback.service
sudo systemctl mask nvidia-fallback.service
```

### Initramfs rebuilden en rebooten

```bash
sudo dracut --force
sudo reboot
```

### Verificatie na reboot

```bash
lspci -nnk -d 10de:28e0
# Verwacht: Kernel driver in use: vfio-pci

lspci -nnk -d 1002:150e
# Verwacht: Kernel driver in use: amdgpu

nvidia-smi
# Verwacht: NVIDIA-SMI has failed because... (normaal bij VFIO)
```


## Fase 2 — KVMFR kernel module installeren

De KVMFR module levert de `/dev/kvmfr0` interface voor de IVSHMEM shared memory buffer.

### Module builden en installeren via DKMS

```bash
cd ~/source/looking-glass-B7/module
sudo dkms install .
```

### MOK enrollment voor Secure Boot

```bash
sudo mokutil --import /var/lib/dkms/mok.pub
# Stel een tijdelijk wachtwoord in
sudo reboot
# Bij reboot: Enroll MOK → Continue → Yes → wachtwoord → reboot
```

### Module automatisch laden en configureren

```bash
echo "kvmfr" | sudo tee /etc/modules-load.d/kvmfr.conf

echo "options kvmfr static_size_mb=128" | sudo tee /etc/modprobe.d/kvmfr.conf
```

### Udev permissions instellen

```bash
echo 'SUBSYSTEM=="kvmfr", OWNER="sten", GROUP="kvm", MODE="0660"' | \
  sudo tee /etc/udev/rules.d/99-kvmfr.rules

sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Module handmatig laden en testen

```bash
sudo modprobe -r kvmfr
sudo modprobe kvmfr

ls -la /dev/kvmfr0
# Verwacht: crw-rw---- 1 sten kvm 508, 0 ...

# Als permissions nog niet kloppen na udev:
sudo chown sten:kvm /dev/kvmfr0
sudo chmod 660 /dev/kvmfr0
```


## Fase 3 — Looking Glass client bouwen

### Source downloaden

```bash
mkdir -p ~/source
cd ~/source
git clone https://github.com/gnif/LookingGlass.git looking-glass-B7
cd looking-glass-B7
git submodule update --init --recursive
```

### Dependencies installeren

De dependencies moesten stuk voor stuk worden uitgezocht. De complete lijst voor Fedora 43:

```bash
sudo dnf install cmake gcc gcc-c++ libglvnd-devel fontconfig-devel \
  spice-protocol wayland-devel wayland-protocols-devel pipewire-devel \
  libxkbcommon-devel libsamplerate-devel libudev-devel nettle-devel \
  desktop-file-utils libXi-devel libXfixes-devel libXScrnSaver-devel \
  libXinerama-devel libXcursor-devel libXpresent-devel libXrandr-devel \
  libdecor-devel pulseaudio-libs-devel binutils-devel
```

Ontbrekende packages per build-fout:

| Fout | Ontbrekende package |
|------|---------------------|
| `wayland-client.h: No such file` | `wayland-devel` |
| `xkbcommon.h: No such file` | `libxkbcommon-devel` |
| `samplerate.h: No such file` | `libsamplerate-devel` |
| `Xi.h: No such file` | `libXi-devel` |
| `Xfixes.h: No such file` | `libXfixes-devel` |
| `bfd.h: No such file` | `binutils-devel` |
| `Xrandr.h: No such file` | `libXrandr-devel` |

### Bouwen en installeren

```bash
cd ~/source/looking-glass-B7/client
mkdir build && cd build
cmake ../
make -j$(nproc)
sudo make install
# Installeert naar /usr/local/bin/looking-glass-client
```

### Verificatie

```bash
which looking-glass-client
looking-glass-client --version
# Output: Looking Glass (B7), CPU: AMD Ryzen AI 9 HX 370 w/ Radeon 890M
```


## Fase 4 — VM XML aanpassen

Aanpassingen via `sudo virsh edit win11`:

**SPICE — GL uitschakelen (alleen input/clipboard):**
```xml
<graphics type="spice">
  <listen type="none"/>
  <image compression="off"/>
  <streaming mode="filter"/>
  <gl enable="no"/>
</graphics>
```

**Video — Looking Glass vervangt het display:**
```xml
<video>
  <model type="none"/>
</video>
```

> **Let op:** Met `type="none"` toont virt-manager een leeg scherm. Dat is verwacht. Tijdelijk terug naar `type="vga"` voor als je Windows-toegang nodig hebt tijdens setup.

**RTX 4060 PCI passthrough:**
```xml
<hostdev mode="subsystem" type="pci" managed="yes">
  <source>
    <address domain="0x0000" bus="0x65" slot="0x00" function="0x0"/>
  </source>
</hostdev>
<hostdev mode="subsystem" type="pci" managed="yes">
  <source>
    <address domain="0x0000" bus="0x65" slot="0x00" function="0x1"/>
  </source>
</hostdev>
```

**IVSHMEM buffer:**
```xml
<shmem name="looking-glass">
  <model type="ivshmem-plain"/>
  <size unit="M">128</size>
</shmem>
```


## Fase 5 — Looking Glass host in Windows installeren

### Tijdelijk VGA toegang herstellen

```bash
sudo virsh edit win11
# Verander: <model type="none"/> naar <model type="vga"/>
sudo virsh destroy win11
sudo virsh start win11
```

### Host installer in Windows

- Download `looking-glass-host-setup.exe` van **https://looking-glass.io/downloads** (B7)
- Rechtsklik → **Run as administrator**
- Next → Agree → Next → Install → Close

Dit installeert automatisch de IVSHMEM driver en de Looking Glass Host service.

### NVIDIA driver installeren in Windows

De RTX 4060 werd weergegeven als "Microsoft Basic Display Adapter". Download de driver via **https://www.nvidia.com/drivers** en installeer deze.

### VGA terug naar none

```bash
sudo virsh edit win11
# Verander: <model type="vga"/> terug naar <model type="none"/>
sudo virsh destroy win11
sudo virsh start win11
```


## Fase 6 — Client verbinden

### Shared memory permissions checken

```bash
ls -la /dev/kvmfr0

# QEMU fallback:
ls -la /dev/shm/looking-glass
sudo chown sten:kvm /dev/shm/looking-glass  # als permissions niet kloppen
```

### Client starten

```bash
looking-glass-client -s
```

Resultaat: **"Host Application Not Running"** — shared memory werkt, maar de host stuurt geen frames.


## Waarom het mislukt

### Host application log

`C:\ProgramData\Looking Glass (host)\looking-glass-host.txt`:

```
[I] d12.c | Not using unsupported adapter: Microsoft Basic Render Driver
[E] d12.c | Failed to locate a valid output device
[I] dxgi.c | Not using unsupported adapter: Microsoft Basic Render Driver
[E] dxgi.c | Failed to locate a valid output device
[E] app.c | Failed to find a supported capture interface
```

### Diagnose via PowerShell in Windows

```powershell
Get-PnpDevice | Where-Object {
    $_.FriendlyName -like "*NVIDIA*" -or $_.FriendlyName -like "*display*"
} | Format-Table FriendlyName, Status, Class

# Resultaat:
# NVIDIA GeForce RTX 4060 Laptop GPU  OK  Display
# Microsoft Basic Display Adapter     OK  Display
```

De RTX 4060 was herkend en de driver was geïnstalleerd — maar de host kon hem niet gebruiken omdat er geen display-output is.

### De fundamentele hardwarebeperking

Bevestigd via `ls /sys/class/drm/`:

```
card0-HDMI-A-1      ← HDMI zit op AMD iGPU (card0)
card0-eDP-2         ← intern scherm via AMD (Dynamic MUX mode)
card1-DP-1 t/m DP-8 ← NVIDIA virtuele outputs (geen fysieke connectors)
card1-eDP-1         ← intern scherm via NVIDIA (dGPU MUX mode)
```

**Alle fysieke poorten op deze laptop zitten op de AMD iGPU.** De RTX 4060 heeft geen enkele fysieke display-aansluiting. DirectX 12 en DXGI vereisen een actieve display-output voor frame capture — dit is hardwarematig onmogelijk op deze laptop.


## Bijkomende bevindingen

### nvidia-fallback.service

Geeft foutmeldingen wanneer VFIO actief is. Oplossing: maskeren (zie Fase 1). Bij terugdraaien herstellen:
```bash
sudo systemctl unmask nvidia-fallback.service
sudo systemctl enable nvidia-fallback.service
```

### Samsung S24U monitor USB hub errors

Herhaalde dmesg errors bij gebruik van de Samsung S24U via USB-C:
```
usb 5-1: device not accepting address, error -71
```
Niet gerelateerd aan VM of GPU passthrough — ingebouwde USB hub van de monitor.

### QEMU shared memory fallback

Als `/dev/kvmfr0` niet beschikbaar is, gebruikt QEMU `/dev/shm/looking-glass` (128MB, owned by `qemu:qemu`). De client valt hier automatisch op terug.


## Alles terugdraaien

```bash
# Kernel parameters herstellen
sudo grubby --update-kernel=ALL \
  --remove-args="vfio-pci.ids=10de:28e0,10de:22be rd.driver.pre=vfio-pci \
                 rd.driver.blacklist=nouveau,nova_core modprobe.blacklist=nouveau,nova_core" \
  --args="nvidia-drm.modeset=1 nvidia-drm.fbdev=1 \
          nvidia.NVreg_PreserveVideoMemoryAllocations=1 iommu=pt"

# VFIO config verwijderen
sudo rm /etc/modprobe.d/vfio.conf
sudo rm /etc/dracut.conf.d/vfio.conf
sudo rm /etc/modules-load.d/kvmfr.conf
sudo rm /etc/udev/rules.d/99-kvmfr.rules
sudo rm /etc/modprobe.d/kvmfr.conf

# nvidia-fallback herstellen
sudo systemctl unmask nvidia-fallback.service
sudo systemctl enable nvidia-fallback.service

# KVMFR DKMS module verwijderen
sudo dkms remove kvmfr/0.0.12 --all

# DKMS MOK key verwijderen (optioneel)
sudo mokutil --delete /var/lib/dkms/mok.pub
# Stel wachtwoord in voor de MOK prompt bij reboot

# Initramfs rebuilden
sudo akmods --force
sudo dracut --force

sudo reboot
# Bij reboot: blauw MOK scherm → Delete MOK → wachtwoord → reboot
```

VM XML herstellen via `sudo virsh edit win11`: verwijder de twee `<hostdev>` blokken en het `<shmem>` blok, zet video terug naar `type="virtio"` met `accel3d="yes"`, en zet SPICE terug naar `gl enable="yes" rendernode="/dev/dri/by-path/pci-0000:66:00.0-render"`.


## Conclusie

Looking Glass is een indrukwekkend project maar vereist hardware die op de Zephyrus G16 simpelweg niet aanwezig is. Voor Windows applicaties op deze laptop zijn de beste opties:

- **[virt-manager met VirtIO + SPICE GL]({{< relref "/docs/vm-setup" >}})** — goede performance voor office/productiviteit (zie de [VM Setup Handleiding]({{< relref "/docs/vm-setup" >}}) voor configuratiedetails)
- **Bottles/Wine** — voor compatibele Windows applicaties
- **Native Linux alternatieven** — wanneer beschikbaar


## Referenties

- [Looking Glass officiële documentatie B7](https://looking-glass.io/docs/B7/)
- [Looking Glass GitHub](https://github.com/gnif/LookingGlass)
- [VFIO GPU Passthrough Guide — Arch Wiki](https://wiki.archlinux.org/title/PCI_passthrough_via_OVMF)
- [GA605WV display routing — Arch Linux Forums](https://bbs.archlinux.org/viewtopic.php?id=299932)


