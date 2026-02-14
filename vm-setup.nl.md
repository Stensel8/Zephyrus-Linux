# Windows 11 VM Setup - KVM/QEMU op Fedora 43

[English](vm-setup.md) | Nederlands

Windows 11 VM voor apps die niet draaien onder Wine.

**Systeemconfiguratie:**
- Model: ASUS ROG Zephyrus G16 GA605WV (2024)
- CPU: AMD Ryzen AI 9 HX 370
- OS: Fedora 43
- Kernel: 6.18.9-200.fc43.x86_64
- Virtualisatie: virt-manager (KVM/QEMU)
- Guest: Windows 11 Enterprise 25H2


## Windows 11 Enterprise ISO

Download evaluatie ISO (~6,6 GB):
```
microsoft.com/en-us/evalcenter/download-windows-11-enterprise
```

90 dagen gratis, geen bloatware, geen verplichte Microsoft-account.


## Installatie

**1. Packages installeren:**
```bash
sudo dnf install @virtualization swtpm swtpm-tools edk2-ovmf
```

**Let op:** Het `virtio-win` pakket is niet beschikbaar in de standaard Fedora repositories. We downloaden de ISO direct in een latere stap.

**2. Gebruiker toevoegen aan libvirt groep:**
```bash
sudo usermod --append --groups libvirt $(whoami)
```
Log uit en weer in (of herstart) voordat je virt-manager opent.

**3. Libvirtd starten en enablen:**
```bash
sudo systemctl enable --now libvirtd
```

**4. Standaard netwerk configureren:**
```bash
sudo virsh net-start default
sudo virsh net-autostart default
```

Let op: Als je "network is already active" ziet, draait het netwerk al.

**5. VirtIO drivers ISO downloaden:**
```bash
# Download de officiële stable VirtIO drivers ISO (~753 MB)
sudo curl -L -o /var/lib/libvirt/images/virtio-win.iso \
  https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso

# Controleer de download (moet ~753 MB zijn)
ls -lh /var/lib/libvirt/images/virtio-win.iso
```
Laat de download volledig afronden; het is een groot bestand.

**6. Controleer je setup:**
```bash
# Check of je in de libvirt groep zit (na opnieuw inloggen)
groups

# Je zou "libvirt" in de output moeten zien
# Zo niet, log dan uit en weer in

# Test of libvirt werkt
sudo virsh list --all
```

**7. Windows ISO klaarzetten:**

Download of kopieer je Windows 11 Enterprise ISO naar `/var/lib/libvirt/images/`:
```bash
# Als je de ISO al hebt gedownload:
sudo cp ~/Downloads/Enterprise-25H2.iso /var/lib/libvirt/images/

# Of download direct naar de juiste locatie:
sudo curl -L -o /var/lib/libvirt/images/Enterprise-25H2.iso [ISO_URL]
```

Virt-manager kan nu beide ISO's direct selecteren uit deze directory.

**8. (Optioneel) Apart storage pool aanmaken voor VM disks:**

Standaard slaat virt-manager alles op in `/var/lib/libvirt/images/`. Als je VM disks op een aparte schijf of partitie wilt:

1. Maak het mountpoint aan en mount je schijf (bijv. `/mnt/vmstore`)
2. In virt-manager: Edit → Connection Details → Storage
3. Klik op **+** om een nieuw pool toe te voegen
4. Naam: `vmstore`, Type: dir, Target Path: `/mnt/vmstore`

Zo houd je grote VM disk images van je root-bestandssysteem af.

**9. VM aanmaken in virt-manager:**
- File → New Virtual Machine → Local install media
- Selecteer Windows 11 Enterprise ISO
- Memory: **8192 MB** (8 GB), CPUs: **8**, Storage: 200 GB (qcow2)
- **Vink "Customize configuration before install" aan**

**10. Hardware configureren:**

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
<summary>Volledige VM XML referentie (klik om uit te vouwen)</summary>

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

> Dit is een vereenvoudigde versie. Automatisch gegenereerde PCI-adressen en controller-definities zijn weggelaten — libvirt voegt die zelf toe. Je kunt je eigen XML exporteren met `virsh dumpxml win11`.

</details>

**11. VirtIO ISO toevoegen:**
- Add Hardware → Storage → CDROM
- Selecteer `/var/lib/libvirt/images/virtio-win.iso`
- Bus: SATA

Klik **Begin Installation**.


## Windows Installatie

**1. VirtIO storage driver laden:**

Op "Where do you want to install Windows?":
- Load driver → Browse → `viostor\w11\amd64\` → Next

**2. Installatie voltooien**

**3. Lokaal account:**

Als "I don't have internet" niet beschikbaar is:
- Shift+F10 → `start ms-cxh:localonly` → Enter

**4. VirtIO guest tools installeren (tijdens OOBE):**

Installeer de VirtIO guest drivers voor betere prestaties voordat je de OOBE afrondt:
- Druk op **Shift+F10** om een opdrachtprompt te openen
- De VirtIO ISO is gemount als CD-ROM station (bijv. D: of E:)
- Voer de installer uit: `D:\virtio-win-guest-tools.exe`
- Sluit na installatie de opdrachtprompt en ga verder met de OOBE

Dit installeert alle VirtIO drivers (netwerk, display, balloon, etc.) zodat Windows vanaf het begin met optimale prestaties draait.

**5. SPICE Guest Tools:**

Download en installeer voor klembord/bestandsdeling:
```
spice-guest-tools-latest.exe (van spice-space.org)
```

Windows draait nu met goede performance.


## Snapshots

```bash
# Snapshot maken (VM moet uit)
virsh shutdown win11
qemu-img snapshot -c snapshot-naam /mnt/vmstore/win11.qcow2

# Lijst
qemu-img snapshot -l /mnt/vmstore/win11.qcow2

# Terugdraaien
qemu-img snapshot -a snapshot-naam /mnt/vmstore/win11.qcow2
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
4. Connect to local hypervisor
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
sudo restorecon -Rv /mnt/vmstore/
```

**Zwart scherm:**
- Controleer dat Video model op Virtio staat (niet QXL)
- Installeer VirtIO guest tools van de VirtIO ISO
- Installeer SPICE Guest Tools

**Klembord werkt niet:**
- SPICE Guest Tools geïnstalleerd?
