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
  Fedora 43 op de ASUS ROG Zephyrus G16 GA605WV &mdash; stap-voor-stap handleidingen voor NVIDIA drivers, VMs, YubiKey en meer.
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx-mb-6">
{{< hextra/hero-badge link="/nl/docs/" >}}
  <span>Bekijk de handleidingen</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}
</div>

> **Disclaimer:** Dit is een onafhankelijk persoonlijk project waarin ik mijn eigen onderzoek en bevindingen documenteer bij het opzetten van Fedora 43 op mijn ASUS ROG Zephyrus G16 GA605WV (2024). Ik ben niet gelieerd aan, goedgekeurd door, of handelend namens Microsoft, Windows, ASUS, ROG, G-Helper, of enig ander bedrijf of project dat hier wordt genoemd. Deze repository deelt mijn persoonlijke configuratie en troubleshooting-aantekeningen. Geen stabiliteitgarantie wordt gegeven. Jouw resultaten kunnen afwijken.

## tl;dr

In 2026 ben ik naar Fedora 43 gegaan op mijn Zephyrus G16. Het is niet perfect, maar de stabiliteit zit dicht bij Windows 11 Pro en ik heb weer controle over mijn systeem.

Deze site bevat de concrete stappen, tweaks en workarounds die ik gebruikt heb. Ik werk hem bij als Fedora en de drivers veranderen.

## Handleidingen

{{< cards >}}
  {{< card link="docs/nvidia-driver-installation" title="NVIDIA Driver Installatie" subtitle="Proprietary NVIDIA drivers met Secure Boot op Fedora 43" icon="chip" >}}
  {{< card link="docs/vm-setup" title="Windows 11 VM Setup" subtitle="KVM/QEMU VM met VirtIO, SPICE GL en Hyper-V enlightenments" icon="desktop-computer" >}}
  {{< card link="docs/autologin" title="GDM Autologin" subtitle="GDM inlogscherm overslaan na LUKS ontgrendeling" icon="lock-open" >}}
  {{< card link="docs/yubikey" title="YubiKey 5C NFC" subtitle="FIDO2 LUKS poging en wat vandaag werkt" icon="key" >}}
  {{< card link="docs/looking-glass-attempt" title="Looking Glass Poging" subtitle="GPU passthrough poging (niet werkend op deze hardware)" icon="eye" >}}
  {{< card link="docs/asusctl-rog-control" title="asusctl & ROG Control Center" subtitle="Fan curves, performance profielen, GPU switching, Slash LED" icon="adjustments" >}}
{{< /cards >}}
