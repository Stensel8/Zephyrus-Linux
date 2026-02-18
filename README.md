# Zephyrus-Linux

English | [Nederlands](README.nl.md)

Fedora 43 on the ASUS ROG Zephyrus G16 GA605WV (2024). My personal setup log — documenting what worked, what didn't, and how I fixed it.

**Browse the full documentation site: [zephyrus-linux.stentijhuis.nl](https://zephyrus-linux.stentijhuis.nl/)**


## About this project

This is my personal setup log for running Fedora Linux on this laptop. I'm not a software engineer or developer — just someone who switched to Linux and ran into a lot of things that didn't work out of the box. I figured I'd write it all down so others don't have to go through the same trial and error I did.

I'm still actively testing and experimenting — things may change, break, or turn out to be wrong. Everything here is based on my own experience and should be taken as-is, at your own risk.

I am not affiliated with, endorsed by, or acting on behalf of ASUS, NVIDIA, Microsoft, Fedora, or any other company or project mentioned here.


## System specs

| Component | Specification |
|-----------|---------------|
| **Model** | ASUS ROG Zephyrus G16 GA605WV (2024) |
| **CPU** | AMD Ryzen AI 9 HX 370 |
| **iGPU** | AMD Radeon 890M |
| **dGPU** | NVIDIA GeForce RTX 4060 Laptop (Max-Q) |
| **OS** | Fedora 43 |
| **Kernel** | 6.18+ |
| **Desktop** | GNOME 49 / Wayland |
| **Secure Boot** | Enabled |


## Building the site locally

This documentation site is built with [Hugo](https://gohugo.io/) using the [Hextra](https://imfing.github.io/hextra/) theme. The theme is included as a git submodule.

**Prerequisites:**
- [Hugo extended](https://gohugo.io/installation/) (v0.152.2 or later)
- Git

**Clone with submodules:**
```bash
git clone --recurse-submodules https://github.com/Stensel8/Zephyrus-Linux.git
cd Zephyrus-Linux
```

If you already cloned without `--recurse-submodules`:
```bash
git submodule update --init --recursive
```

**Run the development server:**
```bash
hugo server
```

The site is available at `http://localhost:1313/`. Hugo watches for file changes and reloads automatically.

**Build for production:**
```bash
hugo --gc --minify
```

The output is written to `./public/`. On push to `main`, GitHub Actions builds and deploys to GitHub Pages automatically.


## Credits & resources

This project wouldn't exist without the work of these people and communities:

- **[Luke Jones](https://asus-linux.org/)** — Creator of `asusctl`, `rog-control-center`, and the `asus-armoury` kernel driver. The ASUS Linux project is the reason modern ASUS laptops work well on Linux at all.
- **[RPM Fusion](https://rpmfusion.org/)** — Provides the packaged NVIDIA proprietary drivers for Fedora, making installation and Secure Boot enrollment straightforward.
- **[Fedora Project](https://fedoraproject.org/)** — The distribution itself, with excellent hardware support and a fast release cycle.
- **[lz42/libinput-config](https://github.com/lz42/libinput-config)** — Third-party workaround for GNOME/Wayland's missing scroll speed setting.
- **[Looking Glass](https://looking-glass.io/)** — Low-latency VM display project. Didn't work on this hardware, but the project and documentation are excellent.
- **[Mastermindzh/tidal-hifi](https://github.com/Mastermindzh/tidal-hifi)** — Community Electron client for Tidal on Linux.
- **[Hextra](https://imfing.github.io/hextra/)** — The Hugo theme powering the documentation site.


## License

This project is licensed under the [MIT License](LICENSE).
