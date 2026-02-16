---
title: "Zephyrus Linux"
toc: false
---

<div class="hx-mt-6 hx-mb-6">
{{< hextra/hero-headline >}}
  Zephyrus Linux
{{< /hextra/hero-headline >}}
</div>

<div class="hx-mb-12">
{{< hextra/hero-subtitle >}}
  Fedora 43 on the ASUS ROG Zephyrus G16 GA605WV &mdash; step-by-step guides for NVIDIA drivers, VMs, YubiKey, and more.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx-mb-6">
{{< hextra/hero-badge link="/docs/" >}}
  <span>Browse the Guides</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}
</div>

<div class="hx-mt-6"></div>

{{< callout type="warning" >}}
**Experimental — use at your own risk.** This is an independent personal project documenting my testing with Fedora on the Zephyrus G16. Not official instructions. Requires **kernel 6.18+** — all versions below are problematic (display issues, GPU crashes, suspend failures). No stability guarantees. Your mileage may vary.
{{< /callout >}}

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="NVIDIA Driver Installation"
    subtitle="Proprietary NVIDIA drivers with Secure Boot on Fedora 43"
    icon="chip"
    link="docs/nvidia-driver-installation"
  >}}
  {{< hextra/feature-card
    title="Windows 11 VM Setup"
    subtitle="KVM/QEMU VM with VirtIO, SPICE GL, and Hyper-V enlightenments"
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
    subtitle="FIDO2 LUKS attempt and what works today"
    icon="key"
    link="docs/yubikey"
  >}}
  {{< hextra/feature-card
    title="Looking Glass Attempt"
    subtitle="GPU passthrough attempt (not working on this hardware)"
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
