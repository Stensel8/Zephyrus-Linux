# Zephyrus-Linux

Nederlands | [English](README.md)

Fedora 43 op de ASUS ROG Zephyrus G16 GA605WV (2024). Mijn persoonlijke setup-log — wat werkte, wat niet, en hoe ik het heb opgelost.

**Bekijk de volledige documentatiesite: [zephyrus-linux.stentijhuis.nl](https://zephyrus-linux.stentijhuis.nl/nl/)**


## Over dit project

Dit is mijn persoonlijke setup-log voor Fedora Linux op deze laptop. Ik ben geen software-engineer of developer — gewoon iemand die naar Linux is overgestapt en daarna tegen van alles aanliep wat niet meteen werkte. Ik heb alles opgeschreven zodat anderen niet hetzelfde hoeven uitzoeken als ik.

Ik ben nog actief aan het testen en experimenteren — dingen kunnen veranderen, kapot gaan of achteraf onjuist blijken. Alles wat hier staat is gebaseerd op mijn eigen ervaring en is op eigen risico.

Ik ben niet gelieerd aan, goedgekeurd door, of handelend namens ASUS, NVIDIA, Microsoft, Fedora, of enig ander bedrijf of project dat hier wordt genoemd.


## Systeemspecificaties

| Onderdeel | Specificatie |
|-----------|--------------|
| **Model** | ASUS ROG Zephyrus G16 GA605WV (2024) |
| **CPU** | AMD Ryzen AI 9 HX 370 |
| **iGPU** | AMD Radeon 890M |
| **dGPU** | NVIDIA GeForce RTX 4060 Laptop (Max-Q) |
| **OS** | Fedora 43 |
| **Kernel** | 6.18+ |
| **Desktop** | GNOME 49 / Wayland |
| **Secure Boot** | Ingeschakeld |


## De site lokaal bouwen

Deze documentatiesite is gebouwd met [Hugo](https://gohugo.io/) en het [Hextra](https://imfing.github.io/hextra/)-thema. Het thema is opgenomen als git submodule.

**Vereisten:**
- [Hugo extended](https://gohugo.io/installation/) (v0.152.2 of later)
- Git

**Clone met submodules:**
```bash
git clone --recurse-submodules https://github.com/Stensel8/Zephyrus-Linux.git
cd Zephyrus-Linux
```

Als je al gekloond hebt zonder `--recurse-submodules`:
```bash
git submodule update --init --recursive
```

**Ontwikkelserver starten:**
```bash
hugo server
```

De site is beschikbaar op `http://localhost:1313/`. Hugo detecteert wijzigingen en herlaadt automatisch.

**Bouwen voor productie:**
```bash
hugo --gc --minify
```

De output wordt geschreven naar `./public/`. Bij een push naar `main` bouwt GitHub Actions de site automatisch en deployt naar GitHub Pages.


## Credits & bronnen

Dit project zou niet bestaan zonder het werk van deze mensen en communities:

- **[Luke Jones](https://asus-linux.org/)** — Maker van `asusctl`, `rog-control-center` en de `asus-armoury` kernel driver. Het ASUS Linux project is de reden dat moderne ASUS laptops goed werken op Linux.
- **[RPM Fusion](https://rpmfusion.org/)** — Levert de verpakte NVIDIA proprietary drivers voor Fedora, waardoor installatie en Secure Boot enrollment eenvoudig zijn.
- **[Fedora Project](https://fedoraproject.org/)** — De distributie zelf, met uitstekende hardware-ondersteuning en een snelle release-cyclus.
- **[lz42/libinput-config](https://github.com/lz42/libinput-config)** — Third-party workaround voor de ontbrekende scroll speed-instelling in GNOME/Wayland.
- **[Looking Glass](https://looking-glass.io/)** — Low-latency VM display project. Werkt niet op deze hardware, maar het project en de documentatie zijn uitstekend.
- **[Mastermindzh/tidal-hifi](https://github.com/Mastermindzh/tidal-hifi)** — Community Electron-client voor Tidal op Linux.
- **[Hextra](https://imfing.github.io/hextra/)** — Het Hugo-thema waarop de documentatiesite is gebouwd.


## Licentie

Dit project valt onder de [MIT-licentie](LICENSE).
