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

> **Disclaimer:** This is an independent personal project documenting my own research and findings while setting up Fedora 43 on the ASUS ROG Zephyrus G16 GA605WV (2024). I am not affiliated with, endorsed by, or acting on behalf of Microsoft, Windows, ASUS, ROG, G-Helper, or any other company or project mentioned herein. This repository shares my personal configuration and troubleshooting notes. No stability guarantees are provided. Your mileage may vary.

## tl;dr

In 2026 I moved this Zephyrus G16 to Fedora 43. It is not perfect, but stability is close to Windows 11 Pro and I prefer the control.

This site documents the steps, tweaks, and workarounds I use and I keep it updated as Fedora and drivers change.

## Guides

{{< cards >}}
  {{< card link="docs/nvidia-driver-installation" title="NVIDIA Driver Installation" subtitle="Proprietary NVIDIA drivers with Secure Boot on Fedora 43" icon="chip" >}}
  {{< card link="docs/vm-setup" title="Windows 11 VM Setup" subtitle="KVM/QEMU VM with VirtIO, SPICE GL, and Hyper-V enlightenments" icon="desktop-computer" >}}
  {{< card link="docs/autologin" title="GDM Autologin" subtitle="Skip GDM login after LUKS unlock" icon="lock-open" >}}
  {{< card link="docs/yubikey" title="YubiKey 5C NFC" subtitle="FIDO2 LUKS attempt and what works today" icon="key" >}}
  {{< card link="docs/looking-glass-attempt" title="Looking Glass Attempt" subtitle="GPU passthrough attempt (not working on this hardware)" icon="eye" >}}
  {{< card link="docs/asusctl-rog-control" title="asusctl & ROG Control Center" subtitle="Fan curves, performance profiles, GPU switching, Slash LED" icon="adjustments" >}}
{{< /cards >}}
