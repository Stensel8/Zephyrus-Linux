---
title: ""
toc: false
---

<div class="hx-mt-6 hx-mb-6">
{{< hextra/hero-headline >}}
  Zephyrus Linux
{{< /hextra/hero-headline >}}
</div>

<div class="hx-mb-12">
{{< hextra/hero-subtitle >}}
  Fedora 43 on the ASUS ROG Zephyrus G16 GA605WV. Step-by-step guides for NVIDIA drivers, VMs, YubiKey, and more.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx-mb-6">
{{< hextra/hero-badge link="/docs/" >}}
  <span>Browse the Guides</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}
</div>

<div class="hx-mt-6"></div>

{{< callout type="info" >}}
**Personal Documentation.** This is an independent project where I'm progressively figuring out how to get the most out of Linux on this laptop. Everything here is at your own risk. I'm not responsible for any changes you make to your system. Requires kernel 6.18+.
{{< /callout >}}

## News

### Kernel 7.0: ASUS laptop quirks + newer AMDGPU enablement

Linus confirmed the next kernel will be 7.0, with the merge window now open and a stable release expected mid-April 2026. For this ASUS ROG G16, the headline is better graphics driver coverage: the DRM updates bring AMDGPU enablement for newer RDNA 3.5-class IP blocks (GFX11.5.4) plus ongoing NVIDIA Nova/Nouveau work, which should translate into better handling of both the iGPU and dGPU. Early expectations are that the Radeon 890M could see around a 20% uplift moving from kernel 6.18 to 7.0. Not a drop-in upgrade for Fedora 43 yet, but a good sign for upcoming releases.

**Sources:** [Linus confirms Linux 7.0](https://www.phoronix.com/news/Linux-7.0-Is-Next) · [HID laptop quirks for ASUS ROG models](https://www.phoronix.com/news/Linux-7.0-HID) · [Linux 7.0 DRM/AMDGPU updates](https://www.phoronix.com/news/Linux-7.0-Graphics-Drivers)

### Kernel 6.19: asus-armoury driver lands in mainline

The `asus-armoury` driver has been [merged into Linux 6.19](https://www.phoronix.com/news/ASUS-Armoury-Driver-Linux-6.19). This new `platform/x86` driver replaces parts of the older `asus-wmi` with a cleaner sysfs-based API, enabling panel mode switching, APU memory allocation, PPT tuning, and more directly from the kernel. The driver is entirely community-developed by [Luke Jones](https://asus-linux.org/) (ASUS Linux project), with no involvement from ASUS themselves. It's not just for handhelds like the ROG Ally; any recent ASUS gaming laptop benefits, including features in ROG Control Center like power limit adjustments.

Currently on kernel 6.18, the driver is not yet available:

![ROG Control showing asus-armoury driver not loaded](/images/rog-control-armoury.png)

Fedora 44 is expected to ship with kernel 6.19, bringing native asus-armoury support.

**Sources:** [Phoronix article](https://www.phoronix.com/news/ASUS-Armoury-Driver-Linux-6.19) · [Community discussion](https://www.phoronix.com/forums/forum/software/linux-gaming/1593500-asus-armoury-driver-set-to-be-introduced-in-linux-6-19) · [Patch series (lore.kernel.org)](https://lore.kernel.org/all/20251102215319.3126879-1-denis.benato@linux.dev/)

## Current System Configuration

| Component | Specification |
|-----------|---------------|
| **Model** | ASUS ROG Zephyrus G16 GA605WV (2024) |
| **CPU** | AMD Ryzen AI 9 HX 370 |
| **iGPU** | AMD Radeon 890M |
| **dGPU** | NVIDIA GeForce RTX 4060 Laptop (Max-Q) |
| **OS** | Fedora 43 |
| **Kernel** | 6.18.9-200.fc43.x86_64 |
| **Display Server** | Wayland (GNOME 49) |
| **Secure Boot** | Enabled |

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="NVIDIA Driver Installation"
    subtitle="Proprietary NVIDIA drivers with Secure Boot on Fedora 43"
    icon="chip"
    link="docs/nvidia-driver-installation"
  >}}
  {{< hextra/feature-card
    title="Windows 11 VM Setup"
    subtitle="KVM/QEMU VM with VirtIO and SPICE GL"
    icon="desktop-computer"
    link="docs/vm-setup"
  >}}
  {{< hextra/feature-card
    title="GDM Autologin"
    subtitle="Skip GDM login after LUKS unlock"
    icon="lock-open"
    link="docs/autologin"
  >}}
  {{< hextra/feature-card
    title="YubiKey 5C NFC"
    subtitle="FIDO2 LUKS unlock and what currently works"
    icon="key"
    link="docs/yubikey"
  >}}
  {{< hextra/feature-card
    title="Looking Glass Attempt"
    subtitle="GPU passthrough attempt, not working on this hardware"
    icon="eye"
    link="docs/looking-glass-attempt"
  >}}
  {{< hextra/feature-card
    title="asusctl & ROG Control Center"
    subtitle="Fan curves, performance profiles, GPU switching, Slash LED"
    icon="adjustments"
    link="docs/asusctl-rog-control"
  >}}
{{< /hextra/feature-grid >}}

---
