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
  Fedora 43 op de ASUS ROG Zephyrus G16 GA605WV. Handleidingen voor NVIDIA drivers, VMs, YubiKey en meer.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx-mb-6">
{{< hextra/hero-badge link="/nl/docs/" >}}
  <span>Bekijk de handleidingen</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}
</div>

{{< callout type="warning" >}}
**Experimenteel — gebruik op eigen risico.** Deze site documenteert persoonlijke tests en experimenten met Fedora Linux op de Zephyrus G16. Dit zijn mijn bevindingen, geen officiële instructies. Geen stabiliteitgarantie wordt gegeven. Jouw resultaten kunnen afwijken.
{{< /callout >}}

{{< callout type="info" >}}
**Kernel vereiste:** De ASUS ROG Zephyrus G16 GA605WV vereist **kernel 6.18 of hoger** voor goede hardware-ondersteuning. Alle kernelversies onder 6.18 zijn problematisch op deze laptop (display-problemen, GPU crashes, suspend/resume failures).
{{< /callout >}}

> **Disclaimer:** Dit is een onafhankelijk persoonlijk project waarin ik mijn eigen onderzoek en bevindingen documenteer bij het opzetten van Fedora 43 op mijn ASUS ROG Zephyrus G16 GA605WV (2024). Ik ben niet gelieerd aan, goedgekeurd door, of handelend namens Microsoft, Windows, ASUS, ROG, G-Helper, of enig ander bedrijf of project dat hier wordt genoemd. Deze repository deelt mijn persoonlijke configuratie en troubleshooting-aantekeningen.

{{< callout type="info" >}}
**Persoonlijke Documentatie.** Dit is een onafhankelijk project waarin ik stap voor stap probeer om steeds meer voor elkaar te krijgen met Linux op deze laptop. Alles wat hier staat is op eigen risico. Ik ben niet verantwoordelijk voor wat je met je systeem doet. Vereist kernel 6.18+.
{{< /callout >}}

## Nieuws

### Kernel 7.0: ASUS laptop quirks + nieuw AMDGPU-werk

Linus heeft bevestigd dat de volgende kernel 7.0 is, met de merge window nu open en een stabiele release verwacht rond midden april 2026. Voor deze ASUS ROG G16 is het belangrijkste nieuws betere grafische driver-ondersteuning: de DRM-updates brengen AMDGPU-enablement voor nieuwere RDNA 3.5-klasse IP blocks (GFX11.5.4) plus verder werk aan NVIDIA Nova/Nouveau, wat moet zorgen voor betere afhandeling van zowel de iGPU als dGPU. Verwachting is dat de Radeon 890M ongeveer 20% sneller kan worden bij de stap van kernel 6.18 naar 7.0. Nog geen directe upgrade voor Fedora 43, maar wel een goed teken voor komende releases.

{{< cards >}}
  {{< card link="docs/nvidia-driver-installation" title="NVIDIA Driver Installatie" subtitle="Proprietary NVIDIA drivers met Secure Boot op Fedora 43" icon="chip" >}}
  {{< card link="docs/vm-setup" title="Windows 11 VM Setup" subtitle="KVM/QEMU VM met VirtIO, SPICE GL en Hyper-V enlightenments" icon="desktop-computer" >}}
  {{< card link="docs/autologin" title="GDM Autologin" subtitle="GDM inlogscherm overslaan na LUKS ontgrendeling" icon="lock-open" >}}
  {{< card link="docs/yubikey" title="YubiKey 5C NFC" subtitle="FIDO2 LUKS poging en wat vandaag werkt" icon="key" >}}
  {{< card link="docs/looking-glass-attempt" title="Looking Glass Poging" subtitle="GPU passthrough poging (niet werkend op deze hardware)" icon="eye" >}}
  {{< card link="docs/asusctl-rog-control" title="asusctl & ROG Control Center" subtitle="Fan curves, performance profielen, GPU switching, Slash LED" icon="adjustments" >}}
{{< /cards >}}

---

Dit project valt onder de [MIT Licentie](https://github.com/Stensel8/Zephyrus-Linux/blob/main/LICENSE).
