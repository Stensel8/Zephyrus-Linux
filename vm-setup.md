# Windows 11 VM Setup - KVM/QEMU on Fedora 43

English | [Nederlands](vm-setup.nl.md)

Windows 11 VM for apps that do not run under Wine.

**System Configuration:**
- Model: ASUS ROG Zephyrus G16 GA605WV (2024)
- CPU: AMD Ryzen AI 9 HX 370
- OS: Fedora 43
- Kernel: 6.18.9-200.fc43.x86_64
- Virtualization: virt-manager (KVM/QEMU)
- Guest: Windows 11 Enterprise 25H2


## Windows 11 Enterprise ISO

Download evaluation ISO (~6.6 GB):
```
microsoft.com/en-us/evalcenter/download-windows-11-enterprise
```

90 days free, no bloatware, no mandatory Microsoft account.


## Installation

**1. Install packages:**
```bash
sudo dnf install @virtualization swtpm swtpm-tools edk2-ovmf
```

**Note:** The `virtio-win` package is not available in Fedora's default repositories. We'll download the ISO directly in a later step.

**2. Add user to libvirt group:**
```bash
sudo usermod --append --groups libvirt $(whoami)
```
Log out and log back in (or reboot) before opening virt-manager.

**3. Start and enable libvirtd:**
```bash
sudo systemctl enable --now libvirtd
```

**4. Configure default network:**
```bash
sudo virsh net-start default
sudo virsh net-autostart default
```

Note: If you see "network is already active", it is already running.

**5. Download VirtIO drivers ISO:**
```bash
# Download the official stable VirtIO drivers ISO (~753 MB)
sudo curl -L -o /var/lib/libvirt/images/virtio-win.iso \
  https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso

# Verify the download (should be ~753 MB)
ls -lh /var/lib/libvirt/images/virtio-win.iso
```
Let the download finish; it is large.

**6. Verify your setup:**
```bash
# Check if you're in the libvirt group (after logging back in)
groups

# You should see "libvirt" in the output
# If not, log out and back in again

# Test if libvirt works
sudo virsh list --all
```

**7. Prepare Windows ISO:**

Download or copy your Windows 11 Enterprise ISO to `/var/lib/libvirt/images/`:
```bash
# If you already downloaded the ISO:
sudo cp ~/Downloads/Enterprise-25H2.iso /var/lib/libvirt/images/

# Or download directly to the correct location:
sudo curl -L -o /var/lib/libvirt/images/Enterprise-25H2.iso [ISO_URL]
```

Virt-manager can now directly select both ISOs from this directory.

**8. (Optional) Create a separate storage pool for VM disks:**

By default, virt-manager stores everything in `/var/lib/libvirt/images/`. If you want VM disks on a separate drive or partition:

1. Create the mount point and mount your drive (e.g. `/mnt/vmstore`)
2. In virt-manager: Edit → Connection Details → Storage
3. Click **+** to add a new pool
4. Name: `vmstore`, Type: dir, Target Path: `/mnt/vmstore`

This keeps large VM disk images off your root filesystem.

**9. Create VM in virt-manager:**
- File → New Virtual Machine → Local install media
- Select Windows 11 Enterprise ISO
- Memory: **8192 MB** (8 GB), CPUs: **8**, Storage: 200 GB (qcow2)
- **Check "Customize configuration before install"**

**10. Configure hardware:**

| Setting | Value |
|---------|-------|
| Chipset | Q35 |
| Firmware | UEFI x86_64: `/usr/share/edk2/ovmf/OVMF_CODE_4M.secboot.qcow2` |
| CPU | Copy host CPU configuration (host-passthrough) |
| TPM | Add Hardware → TPM: Type Emulated, Model CRB, Version 2.0 |
| Disk bus | VirtIO |
| Network | Device model: virtio |
| Display | SPICE |
| Video | Virtio (3D acceleration enabled) |

<details>
<summary>Full VM XML reference (click to expand)</summary>

```xml
<domain type="kvm">
  <name>win11</name>
  <uuid>2a2aa4b0-5f6e-4d0e-a422-de3d63b8966f</uuid>
  <title>win11</title>
  <metadata>
    <libosinfo:libosinfo xmlns:libosinfo="http://libosinfo.org/xmlns/libvirt/domain/1.0">
      <libosinfo:os id="http://microsoft.com/win/11"/>
    </libosinfo:libosinfo>
  </metadata>
  <memory unit="KiB">8388608</memory>
  <currentMemory unit="KiB">8388608</currentMemory>
  <vcpu placement="static">8</vcpu>
  <os firmware="efi">
    <type arch="x86_64" machine="pc-q35-10.1">hvm</type>
    <firmware>
      <feature enabled="yes" name="enrolled-keys"/>
      <feature enabled="yes" name="secure-boot"/>
    </firmware>
    <loader readonly="yes" secure="yes" type="pflash" format="qcow2">/usr/share/edk2/ovmf/OVMF_CODE_4M.secboot.qcow2</loader>
    <nvram template="/usr/share/edk2/ovmf/OVMF_VARS_4M.secboot.qcow2" templateFormat="qcow2" format="qcow2">/var/lib/libvirt/qemu/nvram/win11_VARS.qcow2</nvram>
  </os>
  <features>
    <acpi/>
    <apic/>
    <hyperv mode="custom">
      <relaxed state="on"/>
      <vapic state="on"/>
      <spinlocks state="on" retries="8191"/>
      <vpindex state="on"/>
      <runtime state="on"/>
      <synic state="on"/>
      <stimer state="on"/>
      <frequencies state="on"/>
      <tlbflush state="on"/>
      <ipi state="on"/>
      <avic state="on"/>
    </hyperv>
    <vmport state="off"/>
    <smm state="on"/>
  </features>
  <cpu mode="host-passthrough" check="none" migratable="on">
    <topology sockets="1" dies="1" clusters="1" cores="8" threads="1"/>
  </cpu>
  <clock offset="localtime">
    <timer name="rtc" tickpolicy="catchup"/>
    <timer name="pit" tickpolicy="delay"/>
    <timer name="hpet" present="no"/>
    <timer name="hypervclock" present="yes"/>
  </clock>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>destroy</on_crash>
  <pm>
    <suspend-to-mem enabled="no"/>
    <suspend-to-disk enabled="no"/>
  </pm>
  <devices>
    <emulator>/usr/bin/qemu-system-x86_64</emulator>
    <disk type="file" device="disk">
      <driver name="qemu" type="qcow2"/>
      <source file="/mnt/vmstore/win11.qcow2"/>
      <target dev="vda" bus="virtio"/>
    </disk>
    <disk type="file" device="cdrom">
      <driver name="qemu" type="raw"/>
      <source file="/var/lib/libvirt/images/Enterprise-25H2.iso"/>
      <target dev="sdc" bus="sata"/>
      <readonly/>
    </disk>
    <disk type="file" device="cdrom">
      <driver name="qemu" type="raw"/>
      <source file="/var/lib/libvirt/images/virtio-win.iso"/>
      <target dev="sdd" bus="sata"/>
      <readonly/>
    </disk>
    <interface type="network">
      <source network="default"/>
      <model type="virtio"/>
    </interface>
    <channel type="spicevmc">
      <target type="virtio" name="com.redhat.spice.0"/>
    </channel>
    <input type="tablet" bus="usb"/>
    <tpm model="tpm-crb">
      <backend type="emulator" version="2.0"/>
    </tpm>
    <graphics type="spice" autoport="yes">
      <listen type="address"/>
      <image compression="off"/>
    </graphics>
    <sound model="ich9"/>
    <audio id="1" type="spice"/>
    <video>
      <model type="virtio" heads="1" primary="yes">
        <acceleration accel3d="yes"/>
      </model>
    </video>
    <memballoon model="virtio"/>
  </devices>
</domain>
```

> This is a simplified version. Auto-generated PCI addresses and controller definitions are omitted — libvirt adds those automatically. You can export your own XML with `virsh dumpxml win11`.

</details>

**11. Add VirtIO ISO:**
- Add Hardware → Storage → CDROM
- Select `/var/lib/libvirt/images/virtio-win.iso`
- Bus: SATA

Click **Begin Installation**.


## Windows Installation

**1. Load VirtIO storage driver:**

At "Where do you want to install Windows?":
- Load driver → Browse → `viostor\w11\amd64\` → Next

**2. Complete installation**

**3. Local account:**

If "I don't have internet" is not available:
- Shift+F10 → `start ms-cxh:localonly` → Enter

**4. Install VirtIO guest tools (during OOBE):**

Before finishing the OOBE setup, install the VirtIO guest drivers for better performance:
- Press **Shift+F10** to open a command prompt
- The VirtIO ISO is mounted as a CD-ROM drive (e.g. D: or E:)
- Run the installer: `D:\virtio-win-guest-tools.exe`
- After installation finishes, close the command prompt and continue the OOBE

This installs all VirtIO drivers (network, display, balloon, etc.) so Windows runs with optimal performance from the start.

**5. SPICE Guest Tools:**

Download and install for clipboard/file sharing:
```
spice-guest-tools-latest.exe (from spice-space.org)
```

Windows should now run with good performance.


## Snapshots

```bash
# Create snapshot (VM must be off)
virsh shutdown win11
qemu-img snapshot -c snapshot-name /mnt/vmstore/win11.qcow2

# List
qemu-img snapshot -l /mnt/vmstore/win11.qcow2

# Revert
qemu-img snapshot -a snapshot-name /mnt/vmstore/win11.qcow2
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
4. Connect to local hypervisor
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
sudo restorecon -Rv /mnt/vmstore/
```

**Black screen:**
- Check that Video model is set to Virtio (not QXL)
- Install VirtIO guest tools from the VirtIO ISO
- Install SPICE Guest Tools

**Clipboard doesn't work:**
- SPICE Guest Tools installed?
