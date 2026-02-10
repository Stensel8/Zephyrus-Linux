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
sudo dnf install @virtualization swtpm swtpm-tools edk2-ovmf virtio-win
sudo usermod --append --groups libvirt $(whoami)
# Log uit en weer in
sudo virsh net-start default
sudo virsh net-autostart default
```

**2. ISO voorbereiden:**
```bash
sudo cp /pad/naar/win11-iot-ltsc-eval.iso /var/lib/libvirt/images/
```

**3. VM aanmaken in virt-manager:**
- File → New Virtual Machine → Local install media
- Selecteer Windows 11 IoT LTSC ISO
- Memory: 6144 MB, CPUs: 4-6, Storage: 100 GB (qcow2)
- **Vink "Customize configuration before install" aan**

**4. Hardware configureren:**

| Setting | Value |
|---------|-------|
| Chipset | Q35 |
| Firmware | UEFI x86_64: `/usr/share/edk2/ovmf/OVMF_CODE.secboot.fd` |
| TPM | Add Hardware → TPM: Type Emulated, Model CRB, Version 2.0 |
| Disk bus | VirtIO |
| Network | Device model: virtio |
| Display | SPICE |
| Video | QXL |

**5. VirtIO ISO toevoegen:**
- Add Hardware → Storage → CDROM
- `/usr/share/virtio-win/virtio-win.iso`, Bus: SATA

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

**Permission denied bij VM start:**
```bash
sudo restorecon -Rv /var/lib/libvirt/images/
```

**Zwart scherm:**
- Installeer QXL drivers van VirtIO ISO
- Installeer SPICE Guest Tools

**Klembord werkt niet:**
- SPICE Guest Tools geïnstalleerd?
