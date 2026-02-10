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
sudo dnf install @virtualization swtpm swtpm-tools edk2-ovmf
```

**Note:** The `virtio-win` package is not available in Fedora's default repositories. We'll download the ISO directly in the next step.

**2. Add user to libvirt group:**
```bash
sudo usermod --append --groups libvirt $(whoami)
```

> **⚠️ IMPORTANT:** You MUST log out and log back in (or reboot) for the group membership to take effect. Virt-manager will not work until you do this!

**3. Start and enable libvirtd:**
```bash
# Start the libvirt daemon
sudo systemctl enable --now libvirtd
sudo systemctl start libvirtd

# Verify it's running
sudo systemctl status libvirtd
```

**4. Configure default network:**
```bash
sudo virsh net-start default
sudo virsh net-autostart default
```

**Note:** If you see "network is already active", that's fine - it means the network is already running.

**5. Download VirtIO drivers ISO:**
```bash
# Download the official stable VirtIO drivers ISO (~753 MB)
sudo curl -L -o /var/lib/libvirt/images/virtio-win.iso \
  https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso

# Verify the download (should be ~753 MB)
ls -lh /var/lib/libvirt/images/virtio-win.iso
```

> **⚠️ IMPORTANT:** The download is large (~753 MB). Do not cancel it (Ctrl+C) - let it complete fully!
>
> **💡 TIP:** `/var/lib/libvirt/images/` is the default location for ISOs and VM disk images. Virt-manager shows this directory automatically.

**6. Verify your setup:**
```bash
# Check if you're in the libvirt group (after logging back in)
groups

# You should see "libvirt" in the output
# If not, log out and back in again

# Test if libvirt works
sudo virsh list --all
```

**7. Log out and log back in**

After completing all steps above, **log out and log back in** (or reboot) before opening virt-manager.

**8. Prepare Windows ISO:**

Download or copy your Windows 11 IoT LTSC ISO to `/var/lib/libvirt/images/`:
```bash
# If you already downloaded the ISO:
sudo cp ~/Downloads/win11-iot-ltsc-eval.iso /var/lib/libvirt/images/

# Or download directly to the correct location:
sudo curl -L -o /var/lib/libvirt/images/win11-iot-ltsc-eval.iso [ISO_URL]
```

Virt-manager can now directly select both ISOs from this directory.

**9. Create VM in virt-manager:**
- File → New Virtual Machine → Local install media
- Select Windows 11 IoT LTSC ISO
- Memory: **8192 MB** (8 GB), CPUs: **6**, Storage: 100 GB (qcow2)
- **Check "Customize configuration before install"**

**10. Configure hardware:**

| Setting | Value |
|---------|-------|
| Chipset | Q35 |
| Firmware | UEFI x86_64: `/usr/share/edk2/ovmf/OVMF_CODE.secboot.fd` |
| TPM | Add Hardware → TPM: Type Emulated, Model CRB, Version 2.0 |
| Disk bus | VirtIO |
| Network | Device model: virtio |
| Display | SPICE |
| Video | QXL |

**11. Add VirtIO ISO:**
- Add Hardware → Storage → CDROM
- Select `/var/lib/libvirt/images/virtio-win.iso`
- Bus: SATA

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

**"Could not detect a default hypervisor" error in virt-manager:**

```bash
# 1. Start libvirtd
sudo systemctl start libvirtd

# 2. Check group membership
groups  # Must contain "libvirt"

# If "libvirt" is missing:
sudo usermod --append --groups libvirt $(whoami)
# Then log out and log back in
```

**Manually add connection in virt-manager:**
1. Open virt-manager
2. File → Add Connection
3. Hypervisor: **QEMU/KVM**
4. ✓ Connect to local hypervisor
5. Leave all other fields empty
6. Click **Connect**

**VirtIO ISO download is incomplete:**

The ISO must be exactly ~753 MB. If smaller:
```bash
# Remove incomplete download
sudo rm /var/lib/libvirt/images/virtio-win.iso

# Download again (don't cancel with Ctrl+C!)
sudo curl -L -o /var/lib/libvirt/images/virtio-win.iso \
  https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso

# Verify size
ls -lh /var/lib/libvirt/images/virtio-win.iso
```

**Permission denied when starting VM:**
```bash
sudo restorecon -Rv /var/lib/libvirt/images/
```

**Black screen:**
- Install QXL drivers from VirtIO ISO
- Install SPICE Guest Tools

**Clipboard doesn't work:**
- SPICE Guest Tools installed?
