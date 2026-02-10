# Windows 11 VM Setup - KVM/QEMU on Fedora 43

English | [Nederlands](VM_SETUP.nl.md)

Windows 11 VM for apps that don't run under Wine.

**Setup:**
- Host: Fedora 43 Workstation
- Guest: Windows 11 IoT Enterprise LTSC 2024
- Virtualization: virt-manager (KVM/QEMU)


## Windows 11 IoT LTSC ISO

Download evaluation ISO (~5 GB):
```
microsoft.com/en-us/evalcenter/download-windows-11-iot-enterprise-ltsc-eval
```

90 days free, no bloatware, no mandatory Microsoft account.


## Installation

**1. Install packages:**
```bash
sudo dnf install @virtualization swtpm swtpm-tools edk2-ovmf virtio-win
sudo usermod --append --groups libvirt $(whoami)
# Log out and back in
sudo virsh net-start default
sudo virsh net-autostart default
```

**2. Prepare ISO:**
```bash
sudo cp /path/to/win11-iot-ltsc-eval.iso /var/lib/libvirt/images/
```

**3. Create VM in virt-manager:**
- File → New Virtual Machine → Local install media
- Select Windows 11 IoT LTSC ISO
- Memory: 6144 MB, CPUs: 4-6, Storage: 100 GB (qcow2)
- **Check "Customize configuration before install"**

**4. Configure hardware:**

| Setting | Value |
|---------|-------|
| Chipset | Q35 |
| Firmware | UEFI x86_64: `/usr/share/edk2/ovmf/OVMF_CODE.secboot.fd` |
| TPM | Add Hardware → TPM: Type Emulated, Model CRB, Version 2.0 |
| Disk bus | VirtIO |
| Network | Device model: virtio |
| Display | SPICE |
| Video | QXL |

**5. Add VirtIO ISO:**
- Add Hardware → Storage → CDROM
- `/usr/share/virtio-win/virtio-win.iso`, Bus: SATA

Click **Begin Installation**.


## Windows Installation

**1. Load VirtIO driver:**

At "Where do you want to install Windows?":
- Load driver → Browse → `viostor\w11\amd64\` → Next

**2. Complete installation**

**3. Local account:**

If "I don't have internet" not available:
- Shift+F10 → `start ms-cxh localonly` → Enter

**4. Install VirtIO guest tools:**

After installation in Windows:
- Open VirtIO CD-ROM (D:)
- Run `virtio-win-guest-tools.exe`
- Reboot

**5. SPICE Guest Tools:**

Download and install for clipboard/file sharing:
```
spice-guest-tools-latest.exe (from spice-space.org)
```

Done - Windows now runs with good performance.


## Snapshots

```bash
# Create snapshot (VM must be off)
virsh shutdown win11
qemu-img snapshot -c snapshot-name /var/lib/libvirt/images/win11.qcow2

# List
qemu-img snapshot -l /var/lib/libvirt/images/win11.qcow2

# Revert
qemu-img snapshot -a snapshot-name /var/lib/libvirt/images/win11.qcow2
```


## Troubleshooting

**Permission denied when starting VM:**
```bash
sudo restorecon -Rv /var/lib/libvirt/images/
```

**Black screen:**
- Install QXL drivers from VirtIO ISO
- Install SPICE Guest Tools

**Clipboard doesn't work:**
- SPICE Guest Tools installed?
