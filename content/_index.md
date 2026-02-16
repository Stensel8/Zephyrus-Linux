---
title: "Zephyrus Linux"
layout: hextra-home
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

{{< callout type="warning" >}}
**Experimental — use at your own risk.** This site documents personal testing and experimentation with Fedora Linux on the Zephyrus G16. These are my findings, not official instructions. No stability guarantees are provided. Your mileage may vary.
{{< /callout >}}

{{< callout type="info" >}}
**Kernel requirement:** The ASUS ROG Zephyrus G16 GA605WV requires **kernel 6.18 or higher** for proper hardware support. All kernel versions below 6.18 are problematic on this laptop (display issues, GPU crashes, suspend/resume failures).
{{< /callout >}}

> **Disclaimer:** This is an independent personal project documenting my own research and findings while setting up Fedora 43 on the ASUS ROG Zephyrus G16 GA605WV (2024). I am not affiliated with, endorsed by, or acting on behalf of Microsoft, Windows, ASUS, ROG, G-Helper, or any other company or project mentioned herein. This repository shares my personal configuration and troubleshooting notes.

{{< callout type="info" >}}
**Personal Documentation.** This is an independent project where I'm progressively figuring out how to get the most out of Linux on this laptop. Everything here is at your own risk. I'm not responsible for any changes you make to your system. Requires kernel 6.18+.
{{< /callout >}}

## News

### Kernel 7.0: ASUS laptop quirks + newer AMDGPU enablement

Linus confirmed the next kernel will be 7.0, with the merge window now open and a stable release expected mid-April 2026. For this ASUS ROG G16, the headline is better graphics driver coverage: the DRM updates bring AMDGPU enablement for newer RDNA 3.5-class IP blocks (GFX11.5.4) plus ongoing NVIDIA Nova/Nouveau work, which should translate into better handling of both the iGPU and dGPU. Early expectations are that the Radeon 890M could see around a 20% uplift moving from kernel 6.18 to 7.0. Not a drop-in upgrade for Fedora 43 yet, but a good sign for upcoming releases.

{{< cards >}}
  {{< card link="docs/nvidia-driver-installation" title="NVIDIA Driver Installation" subtitle="Proprietary NVIDIA drivers with Secure Boot on Fedora 43" icon="chip" >}}
  {{< card link="docs/vm-setup" title="Windows 11 VM Setup" subtitle="KVM/QEMU VM with VirtIO, SPICE GL, and Hyper-V enlightenments" icon="desktop-computer" >}}
  {{< card link="docs/autologin" title="GDM Autologin" subtitle="Skip GDM login after LUKS unlock" icon="lock-open" >}}
  {{< card link="docs/yubikey" title="YubiKey 5C NFC" subtitle="FIDO2 LUKS attempt and what works today" icon="key" >}}
  {{< card link="docs/looking-glass-attempt" title="Looking Glass Attempt" subtitle="GPU passthrough attempt (not working on this hardware)" icon="eye" >}}
  {{< card link="docs/asusctl-rog-control" title="asusctl & ROG Control Center" subtitle="Fan curves, performance profiles, GPU switching, Slash LED" icon="adjustments" >}}
{{< /cards >}}

---

This project is licensed under the [MIT License](https://github.com/Stensel8/Zephyrus-Linux/blob/main/LICENSE).
