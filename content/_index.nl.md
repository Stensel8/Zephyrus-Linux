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
  Alles wat je moet weten over het draaien van Fedora 43 op je Zephyrus
{{< /hextra/hero-subtitle >}}
</div>

<div class="hx-mb-6">
{{< hextra/hero-badge link="/nl/docs/" >}}
  <span>Bekijk de handleidingen</span>
  {{< icon name="arrow-circle-right" attributes="height=14" >}}
{{< /hextra/hero-badge >}}
</div>

<div class="hx-mt-6"></div>

{{< callout type="info" >}}
**Persoonlijke Documentatie.** Dit is een onafhankelijk project waarin ik stap voor stap probeer om steeds meer voor elkaar te krijgen met Linux op deze laptop. Alles wat hier staat is op eigen risico. Ik ben niet verantwoordelijk voor wat je met je systeem doet. Vereist kernel 6.18+.
{{< /callout >}}

## Nieuws

### Kernel 7.0: ASUS laptop quirks + nieuw AMDGPU-werk

Linus heeft bevestigd dat de volgende kernel 7.0 is, met de merge window nu open en een stabiele release verwacht rond midden april 2026. Voor deze ASUS ROG G16 is het belangrijkste nieuws betere grafische driver-ondersteuning: de DRM-updates brengen AMDGPU-ondersteuning voor nieuwere RDNA 3.5-klasse IP blocks (GFX11.5.4) plus verder werk aan NVIDIA Nova/Nouveau, wat moet zorgen voor betere afhandeling van zowel de iGPU als dGPU. Verwachting is dat de Radeon 890M ongeveer 20% sneller kan worden bij de stap van kernel 6.18 naar 7.0. Nog geen directe upgrade voor Fedora 43, maar wel een goed teken voor komende releases.

**Bronnen:** [Linus bevestigt Linux 7.0](https://www.phoronix.com/news/Linux-7.0-Is-Next) · [HID laptop quirks voor ASUS ROG modellen](https://www.phoronix.com/news/Linux-7.0-HID) · [Linux 7.0 DRM/AMDGPU updates](https://www.phoronix.com/news/Linux-7.0-Graphics-Drivers)

### Kernel 6.19: asus-armoury driver in mainline Linux

De `asus-armoury` driver is [gemerged in Linux 6.19](https://www.phoronix.com/news/ASUS-Armoury-Driver-Linux-6.19). Deze nieuwe `platform/x86` driver vervangt delen van de oudere `asus-wmi` met een schonere sysfs-gebaseerde API, waarmee o.a. paneel modus wisselen, APU geheugentoewijzing, PPT tuning en meer mogelijk wordt direct vanuit de kernel. De driver is volledig ontwikkeld door de community, door [Luke Jones](https://asus-linux.org/) (ASUS Linux project), zonder enige betrokkenheid van ASUS zelf. Het is niet alleen voor handhelds zoals de ROG Ally; elke recente ASUS gaming laptop profiteert ervan, inclusief functies in ROG Control Center zoals power limit aanpassingen.

Op kernel 6.18 is de driver nog niet beschikbaar:

![ROG Control toont dat de asus-armoury driver niet geladen is](/images/rog-control-armoury.avif)

Fedora 44 zal naar verwachting met kernel 6.19 worden geleverd, met native asus-armoury ondersteuning.

**Bronnen:** [Phoronix artikel](https://www.phoronix.com/news/ASUS-Armoury-Driver-Linux-6.19) · [Community discussie](https://www.phoronix.com/forums/forum/software/linux-gaming/1593500-asus-armoury-driver-set-to-be-introduced-in-linux-6-19) · [Patch series (lore.kernel.org)](https://lore.kernel.org/all/20251102215319.3126879-1-denis.benato@linux.dev/)

## Huidige Systeemconfiguratie

| Onderdeel | Specificatie |
|-----------|--------------|
| **Model** | ASUS ROG Zephyrus G16 GA605WV (2024) |
| **CPU** | AMD Ryzen AI 9 HX 370 |
| **iGPU** | AMD Radeon 890M |
| **dGPU** | NVIDIA GeForce RTX 4060 Laptop (Max-Q) |
| **OS** | Fedora 43 |
| **Kernel** | 6.18.9-200.fc43.x86_64 |
| **Display Server** | Wayland (GNOME 49) |
| **Secure Boot** | Ingeschakeld |

## Aan de slag

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="Aan de slag"
    subtitle="Van schone Fedora-installatie tot volledig geconfigureerd systeem"
    icon="play"
    link="docs/getting-started"
  >}}
{{< /hextra/feature-grid >}}

## Referentie Handleidingen

{{< hextra/feature-grid >}}
  {{< hextra/feature-card
    title="NVIDIA Driver Installatie"
    subtitle="Proprietary NVIDIA drivers met Secure Boot op Fedora 43"
    icon="chip"
    link="docs/nvidia-driver-installation"
  >}}
  {{< hextra/feature-card
    title="Windows 11 VM Setup"
    subtitle="KVM/QEMU VM met VirtIO en SPICE GL"
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
    subtitle="GPU passthrough poging (werkt niet op deze hardware)"
    icon="eye"
    link="docs/looking-glass-attempt"
  >}}
  {{< hextra/feature-card
    title="asusctl & ROG Control Center"
    subtitle="Fan curves, performance profielen, GPU switching, Slash LED"
    icon="adjustments"
    link="docs/asusctl-rog-control"
  >}}
  {{< hextra/feature-card
    title="eduroam Setup"
    subtitle="PEAP/MSCHAPv2 configuratie die daadwerkelijk werkt op Linux"
    icon="wifi"
    link="docs/eduroam-network-installation"
  >}}
{{< /hextra/feature-grid >}}

---
