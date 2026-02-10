# Windows 11 VM Setup - KVM/QEMU op Fedora 43

[English](VM_SETUP.md) | Nederlands

Windows 11 VM voor apps die niet draaien onder Wine.

**Setup:**
- Host: Fedora 43 Workstation
- Guest: Windows 11 IoT Enterprise LTSC 2024
- Virtualisatie: virt-manager (KVM/QEMU)


## Windows 11 IoT LTSC ISO

Download evaluatie ISO (~5 GB):
```
microsoft.com/en-us/evalcenter/download-windows-11-iot-enterprise-ltsc-eval
```

90 dagen gratis, geen bloatware, geen verplichte Microsoft-account.


## Installatie

**1. Packages installeren:**
```bash
sudo dnf install @virtualization swtpm swtpm-tools edk2-ovmf
```

**Let op:** Het `virtio-win` pakket is niet beschikbaar in de standaard Fedora repositories. We downloaden de ISO direct in de volgende stap.

**2. Gebruiker toevoegen aan libvirt groep:**
```bash
sudo usermod --append --groups libvirt $(whoami)
```

> **⚠️ BELANGRIJK:** Je MOET uitloggen en opnieuw inloggen (of herstarten) voordat de groepslidmaatschap actief wordt. Virt-manager werkt niet totdat je dit doet!

**3. Libvirtd starten en enablen:**
```bash
# Start de libvirt daemon
sudo systemctl enable --now libvirtd
sudo systemctl start libvirtd

# Controleer of het draait
sudo systemctl status libvirtd
```

**4. Standaard netwerk configureren:**
```bash
sudo virsh net-start default
sudo virsh net-autostart default
```

**Let op:** Als je "network is already active" ziet, is dat prima - het betekent dat het netwerk al draait.

**5. VirtIO drivers ISO downloaden:**
```bash
# Download de officiële stable VirtIO drivers ISO (~753 MB)
sudo curl -L -o /var/lib/libvirt/images/virtio-win.iso \
  https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso

# Controleer de download (moet ~753 MB zijn)
ls -lh /var/lib/libvirt/images/virtio-win.iso
```

> **⚠️ BELANGRIJK:** De download is groot (~753 MB). Annuleer deze niet (Ctrl+C) - laat hem volledig downloaden!
>
> **💡 TIP:** `/var/lib/libvirt/images/` is de standaard locatie voor ISO's en VM disk images. Virt-manager toont deze directory automatisch.

**6. Controleer je setup:**
```bash
# Check of je in de libvirt groep zit (na opnieuw inloggen)
groups

# Je zou "libvirt" in de output moeten zien
# Zo niet, log dan uit en weer in

# Test of libvirt werkt
sudo virsh list --all
```

**7. Log uit en weer in**

Na het voltooien van alle bovenstaande stappen, **log uit en weer in** (of herstart) voordat je virt-manager opent.

**8. Windows ISO klaarzetten:**

Download of kopieer je Windows 11 IoT LTSC ISO naar `/var/lib/libvirt/images/`:
```bash
# Als je de ISO al hebt gedownload:
sudo cp ~/Downloads/win11-iot-ltsc-eval.iso /var/lib/libvirt/images/

# Of download direct naar de juiste locatie:
sudo curl -L -o /var/lib/libvirt/images/win11-iot-ltsc-eval.iso [ISO_URL]
```

Virt-manager kan nu beide ISO's direct selecteren uit deze directory.

**9. VM aanmaken in virt-manager:**
- File → New Virtual Machine → Local install media
- Selecteer Windows 11 IoT LTSC ISO
- Memory: **8192 MB** (8 GB), CPUs: **6**, Storage: 100 GB (qcow2)
- **Vink "Customize configuration before install" aan**

**10. Hardware configureren:**

| Setting | Value |
|---------|-------|
| Chipset | Q35 |
| Firmware | UEFI x86_64: `/usr/share/edk2/ovmf/OVMF_CODE.secboot.fd` |
| TPM | Add Hardware → TPM: Type Emulated, Model CRB, Version 2.0 |
| Disk bus | VirtIO |
| Network | Device model: virtio |
| Display | SPICE |
| Video | QXL |

**11. VirtIO ISO toevoegen:**
- Add Hardware → Storage → CDROM
- Selecteer `/var/lib/libvirt/images/virtio-win.iso`
- Bus: SATA

Klik **Begin Installation**.


## Windows Installatie

**1. VirtIO driver laden:**

Op "Where do you want to install Windows?":
- Load driver → Browse → `viostor\w11\amd64\` → Next

**2. Installatie voltooien**

**3. Lokaal account:**

Als "I don't have internet" niet beschikbaar:
- Shift+F10 → `start ms-cxh localonly` → Enter

**4. VirtIO guest tools installeren:**

Na installatie in Windows:
- Open VirtIO CD-ROM (D:)
- Run `virtio-win-guest-tools.exe`
- Herstart

**5. SPICE Guest Tools:**

Download en installeer voor klembord/bestandsdeling:
```
spice-guest-tools-latest.exe (van spice-space.org)
```

Klaar - Windows draait nu met goede performance.


## Snapshots

```bash
# Snapshot maken (VM moet uit)
virsh shutdown win11
qemu-img snapshot -c snapshot-naam /var/lib/libvirt/images/win11.qcow2

# Lijst
qemu-img snapshot -l /var/lib/libvirt/images/win11.qcow2

# Terugdraaien
qemu-img snapshot -a snapshot-naam /var/lib/libvirt/images/win11.qcow2
```


## Troubleshooting

**"Could not detect a default hypervisor" error in virt-manager:**

```bash
# 1. Start libvirtd
sudo systemctl start libvirtd

# 2. Controleer groepslidmaatschap
groups  # Moet "libvirt" bevatten

# Als "libvirt" ontbreekt:
sudo usermod --append --groups libvirt $(whoami)
# Dan uitloggen en opnieuw inloggen
```

**Handmatig connectie toevoegen in virt-manager:**
1. Open virt-manager
2. File → Add Connection
3. Hypervisor: **QEMU/KVM**
4. ✓ Connect to local hypervisor
5. Laat alle andere velden leeg
6. Klik **Connect**

**VirtIO ISO download is incompleet:**

De ISO moet exact ~753 MB zijn. Als deze kleiner is:
```bash
# Verwijder incomplete download
sudo rm /var/lib/libvirt/images/virtio-win.iso

# Download opnieuw (annuleer niet met Ctrl+C!)
sudo curl -L -o /var/lib/libvirt/images/virtio-win.iso \
  https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso

# Controleer grootte
ls -lh /var/lib/libvirt/images/virtio-win.iso
```

**Permission denied bij VM start:**
```bash
sudo restorecon -Rv /var/lib/libvirt/images/
```

**Zwart scherm:**
- Installeer QXL drivers van VirtIO ISO
- Installeer SPICE Guest Tools

**Klembord werkt niet:**
- SPICE Guest Tools geïnstalleerd?
