# Zephyrus-Linux

English | [Nederlands](README.nl.md)

Fedora 43 on the ASUS ROG Zephyrus G16 GA605WV (2024). Step-by-step guides for NVIDIA drivers, VMs, YubiKey, and more.

**Browse the full documentation site: [zephyrus-linux.stentijhuis.nl](https://zephyrus-linux.stentijhuis.nl/)**


## About this project

This is an independent personal project where I document my own findings while setting up and daily-driving Fedora Linux on this laptop. I'm still actively testing and experimenting — things may change, break, or turn out to be wrong. Everything here is based on my own experience and should be taken as-is, at your own risk.

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
