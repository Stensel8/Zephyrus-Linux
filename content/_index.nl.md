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
  Fedora 43 op de ASUS ROG Zephyrus G16 GA605WV &mdash; stap-voor-stap handleidingen voor NVIDIA drivers, VMs, YubiKey en meer.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx-mb-6">
{{< hextra/hero-badge link="/nl/docs/" >}}
  <span>Bekijk de handleidingen</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}
</div>

<div class="hx-mt-6"></div>

{{< callout type="warning" >}}
**Experimenteel — gebruik op eigen risico.** Dit is een onafhankelijk persoonlijk project waarin ik mijn tests met Fedora op de Zephyrus G16 documenteer. Geen officiële instructies. Vereist **kernel 6.18+** — alle versies daaronder zijn problematisch (display-problemen, GPU crashes, suspend failures). Geen stabiliteitgarantie. Jouw resultaten kunnen afwijken.
{{< /callout >}}

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="NVIDIA Driver Installatie"
    subtitle="Proprietary NVIDIA drivers met Secure Boot op Fedora 43"
    icon="chip"
    link="docs/nvidia-driver-installation"
  >}}
  {{< hextra/feature-card
    title="Windows 11 VM Setup"
    subtitle="KVM/QEMU VM met VirtIO, SPICE GL en Hyper-V enlightenments"
    icon="desktop-computer"
    link="docs/vm-setup"
  >}}
  {{< hextra/feature-card
    title="GDM Autologin"
    subtitle="GDM inlogscherm overslaan na LUKS ontgrendeling"
    icon="lock-open"
    link="docs/autologin"
  >}}
  {{< hextra/feature-card
    title="YubiKey 5C NFC"
    subtitle="FIDO2 LUKS poging en wat vandaag werkt"
    icon="key"
    link="docs/yubikey"
  >}}
  {{< hextra/feature-card
    title="Looking Glass Poging"
    subtitle="GPU passthrough poging (niet werkend op deze hardware)"
    icon="eye"
    link="docs/looking-glass-attempt"
  >}}
  {{< hextra/feature-card
    title="asusctl & ROG Control Center"
    subtitle="Fan curves, performance profielen, GPU switching, Slash LED"
    icon="adjustments"
    link="docs/asusctl-rog-control"
  >}}
{{< /hextra/feature-grid >}}
