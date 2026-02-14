# asusctl & ROG Control Center - ROG Zephyrus G16 GA605WV (2024)

English | [Nederlands](asusctl-rog-control.nl.md)

Guide for setting up ASUS ROG hardware controls on Fedora 43: fan curves, performance profiles, GPU switching, Slash LED, and battery management.

**System Configuration:**
- Model: ASUS ROG Zephyrus G16 GA605WV (2024)
- CPU: AMD Ryzen AI 9 HX 370
- GPU: NVIDIA GeForce RTX 4060 Laptop (Max-Q) + AMD Radeon 890M (iGPU)
- OS: Fedora 43
- Kernel: 6.18.9-200.fc43.x86_64
- Display Server: Wayland (GNOME 49)
- Secure Boot: Enabled

**Package Information:**
- `asusctl` 6.3.2-1 — CLI for fan curves, profiles, battery limit, RGB, Slash LED
- `asusctl-rog-gui` 6.3.2 — ROG Control Center GUI
- `supergfxctl` 5.2.7-8 — GPU mode switching
- Source: [lukenukem COPR](https://copr.fedorainfracloud.org/coprs/lukenukem/asus-linux/) (maintained by Luke Jones, primary asusctl developer)


## Prerequisites

<details>
<summary>Why lukenukem COPR and not a regular repo</summary>

COPR is Fedora's official community package hosting platform (similar to AUR for Arch). The `lukenukem` COPR is maintained by Luke Jones (flukejones), the primary developer of asusctl itself — not a random third party.

The packages are GPG-signed (`gpgcheck=1`) and this is the officially recommended installation method by the asus-linux project.

**Note:** If you search for "lukenukem COPR" on Reddit, you may find threads raising concerns. These are typically about the openSUSE repository going temporarily offline — not a security issue with the COPR itself.

</details>

<details>
<summary>Compatibility with tuned (power-profiles-daemon conflict) — Fedora-specific</summary>

`asusctl` requires the `power-profiles-daemon` D-Bus API to manage performance profiles (Silent/Balanced/Performance). On Arch Linux, you simply install `power-profiles-daemon` and it works. On Fedora however, this conflicts with `tuned`, which [replaced `power-profiles-daemon` as the default power management daemon since Fedora 41](https://fedoraproject.org/wiki/Changes/TunedAsTheDefaultPowerProfileManagementDaemon).

The solution is `tuned-ppd`, a Fedora-provided compatibility layer that exposes the `power-profiles-daemon` D-Bus interface while using `tuned` internally. This allows `asusctl` to manage profiles without removing `tuned`.

**Note:** The asus-linux project does not document this because it is a Fedora-specific issue. Their [FAQ](https://asus-linux.org/faq/) and [ArchWiki page](https://wiki.archlinux.org/title/Asusctl) only state that `power-profiles-daemon` must be running.

If you have `tuned` installed (Fedora default), you must switch to `tuned-ppd` before installing asusctl, otherwise profile switching will not work.

**References:**
- [Fedora Wiki: Tuned as Default Power Profile Daemon (F41)](https://fedoraproject.org/wiki/Changes/TunedAsTheDefaultPowerProfileManagementDaemon)
- [Phoronix: Fedora 41 Goes Tuned PPD](https://www.phoronix.com/news/Fedora-41-Goes-Tuned-PPD)
- [asus-linux FAQ](https://asus-linux.org/faq/)
- [asusctl ArchWiki](https://wiki.archlinux.org/title/Asusctl)

</details>


## Installation

<details>
<summary><strong>Step 1:</strong> Add lukenukem COPR repository</summary>

```bash
sudo dnf copr enable lukenukem/asus-linux
```

</details>

<details>
<summary><strong>Step 2:</strong> Switch from tuned to tuned-ppd (Fedora-specific)</summary>

`asusctl` needs the `power-profiles-daemon` D-Bus API. On Fedora 41+, `tuned` is the default and conflicts with `power-profiles-daemon`. Install `tuned-ppd` as the compatibility layer:

```bash
sudo dnf install tuned-ppd
sudo systemctl disable tuned.service
sudo systemctl enable --now tuned-ppd.service
```

`tuned-ppd` exposes the `power-profiles-daemon` D-Bus interface while using `tuned` profiles internally. `asusctl` talks to `tuned-ppd` as if it were `power-profiles-daemon` — no modifications needed.

**Verify:**
```bash
systemctl status tuned-ppd
```

**Note:** On Arch Linux, install `power-profiles-daemon` directly instead. This step is only needed on Fedora.

</details>

<details>
<summary><strong>Step 3:</strong> Install asusctl, ROG Control Center, and supergfxctl</summary>

```bash
sudo dnf install asusctl asusctl-rog-gui supergfxctl
```

This installs:
- `asusctl` — main CLI daemon and client
- `asusctl-rog-gui` — ROG Control Center GUI
- `supergfxctl` — GPU mode switching daemon

</details>

<details>
<summary><strong>Step 4:</strong> Enable services</summary>

```bash
sudo systemctl enable --now asusd.service
sudo systemctl enable supergfxd.service
```

Reboot to ensure all services start correctly:
```bash
sudo reboot
```

</details>

<details>
<summary><strong>Step 5:</strong> Verify hardware detection</summary>

After reboot, verify asusctl detected your hardware correctly:

```bash
asusctl info
```

Expected output should include:
```
Product family: ROG Zephyrus G16
Board name: GA605WV
```

</details>

<details>
<summary><strong>Step 6 (optional):</strong> Install monitoring tools</summary>

Useful utilities for monitoring hardware alongside asusctl:

```bash
sudo dnf install nvtop powertop s-tui lm_sensors i2c-tools
```

| Package | Description |
|---------|-------------|
| `nvtop` | GPU process monitor (AMD + NVIDIA simultaneously) |
| `powertop` | Power consumption analysis per process/device |
| `s-tui` | TUI dashboard: CPU frequency, temperature, load, stress test |
| `lm_sensors` | Hardware temperature sensor readout |
| `i2c-tools` | Low-level hardware bus diagnostics |

</details>


## Configuration

<details>
<summary>Set battery charge limit (recommended: 80%)</summary>

Limiting the charge to 80% significantly extends battery lifespan. The laptop runs normally on AC power regardless of this setting.

**Set via CLI:**
```bash
asusctl battery --charge-limit 80
```

**Set via GUI:**
Open ROG Control Center (`rog-control-center`) → System Control → Battery Charge Limit.

**Verify:**
```bash
asusctl battery
```

This setting persists across reboots and is managed by `asusd`.

</details>

<details>
<summary>Configure Slash LED (the light bar on the lid)</summary>

The Slash LED is the diagonal light bar on the lid of the G16. It supports multiple animations and can be configured to turn off on battery.

**Show available animations:**
```bash
asusctl slash --list
```

Available animations: `Static`, `Bounce`, `Slash`, `Loading`, `BitStream`, `Transmission`, `Flow`, `Flux`, `Phantom`, `Spectrum`, `Hazard`, `Interfacing`, `Ramp`, `GameOver`, `Start`, `Buzzer`

**Recommended setup (AC only, off on battery and during sleep):**
```bash
asusctl slash --enable -b false -s false
```

**What these flags do:**
- `--enable` — turn on the Slash LED
- `-b false` — disable on battery power
- `-s false` — disable during sleep

**Set animation:**
```bash
asusctl slash --mode Spectrum
```

**Set brightness (0–255):**
```bash
asusctl slash -l 128
```

</details>

<details>
<summary>Performance profiles</summary>

asusctl provides three performance profiles that control CPU/GPU power limits and fan behavior:

| Profile | Description |
|---------|-------------|
| `Silent` | Low power, quiet fans, throttled performance |
| `Balanced` | Default. Moderate power and noise |
| `Performance` | Maximum CPU/GPU power, aggressive fans |

**Set a profile:**
```bash
asusctl profile -P Balanced
asusctl profile -P Silent
asusctl profile -P Performance
```

**Cycle through profiles:**
```bash
asusctl profile --next
```

**Check current profile:**
```bash
asusctl profile
```

> **Note:** Profile switching requires `tuned-ppd` to be running. See the installation steps above.

</details>

<details>
<summary>GPU mode switching (supergfxctl)</summary>

The GA605WV has a hybrid GPU setup: the AMD Radeon 890M (iGPU) drives the internal display, and the NVIDIA RTX 4060 (dGPU) handles GPU workloads.

`supergfxctl` manages which GPU mode is active:

| Mode | Description |
|------|-------------|
| `Hybrid` | Both GPUs active. NVIDIA handles GPU workloads, AMD drives the display. Best for gaming. |
| `Integrated` | Only AMD iGPU. Lower power consumption, no NVIDIA. Good for battery. |
| `AsusMuxDgpu` | NVIDIA directly drives the display via hardware MUX switch. Lowest latency for gaming. Requires reboot. |

**Check current mode:**
```bash
supergfxctl --mode
```

**Switch mode:**
```bash
supergfxctl --mode Hybrid
supergfxctl --mode Integrated
```

> **Note:** Switching between Hybrid and Integrated requires a logout/login. Switching to AsusMuxDgpu requires a reboot.

> **Important:** `nvidia-powerd.service` must remain disabled and **masked** on this laptop. It conflicts with AMD ATPX power management and causes soft lockups and reboot hangs (black screen, backlights stay on). Masking is essential because `supergfxd` directly calls `systemctl start nvidia-powerd.service` during GPU mode switches — `disable` alone does not prevent this. The mask (symlink to `/dev/null`) blocks both `supergfxd` and NVIDIA driver updates from re-enabling it. GPU power is managed via ATPX (via ACPI). See [NVIDIA Driver Installation Guide](nvidia-driver-installation.md) for diagnosis details and commands.

</details>

<details>
<summary>Keyboard RGB (Aura)</summary>

**Set keyboard backlight brightness (0–100):**
```bash
asusctl led-brighter
asusctl led-dimmer
```

**Open Aura configuration in ROG Control Center:**
```bash
rog-control-center
```

Navigate to the "Keyboard Aura" section for animation, color, and per-key configuration.

</details>

<details>
<summary>Custom fan curves</summary>

Fan curves can be configured per performance profile in ROG Control Center or via CLI.

**Open ROG Control Center:**
```bash
rog-control-center
```

Navigate to "Fan Curves" to set temperature/speed curves per profile (Silent, Balanced, Performance).

**CLI fan curve format:**
```bash
# Show current fan curve data for a profile
asusctl fan-curve -m Balanced

# Set a custom curve (8 temperature/speed pairs: temp:speed,temp:speed,...)
asusctl fan-curve -m Balanced -D 30:0,40:10,50:30,60:50,70:70,80:85,90:100,100:100
```

> **Note:** Fan curve customization requires the `asus-armoury` kernel driver. On kernel < 6.19, the driver is not available and curves set in the GUI may not persist as expected. See the Known Issues section below.

</details>


## Monitoring

<details>
<summary>Hardware monitoring commands</summary>

**GPU monitor (AMD + NVIDIA):**
```bash
nvtop
```

**CPU frequency, temperature, load dashboard:**
```bash
s-tui
```

**Power consumption per process/device:**
```bash
sudo powertop
```

**Hardware temperatures:**
```bash
sensors
```

**Check asusd service logs:**
```bash
sudo journalctl -b -u asusd
```

**Check supergfxd service logs:**
```bash
sudo journalctl -b -u supergfxd
```

</details>


## Known Issues

<details>
<summary>ROG Control Center warning: "The asus-armoury driver is not loaded"</summary>

**Problem:**
ROG Control Center shows a warning that the `asus-armoury` kernel driver is not loaded. Some advanced features (PPT power limits, APU memory allocation, MUX switch control) are unavailable.

**Cause:**
The `asus-armoury` driver was merged into the Linux mainline kernel in version 6.19. On kernel 6.18.x (current Fedora 43 default), the driver does not exist.

**What still works without the driver:**
- Fan curves (basic)
- Performance profiles (Silent / Balanced / Performance)
- Battery charge limit
- Slash LED
- Keyboard Aura / RGB
- GPU switching via supergfxctl

**Solution:**
Wait for Fedora 43 to ship kernel 6.19 via `dnf update`. No manual action required.

After the kernel update, verify the driver loaded:
```bash
lsmod | grep asus_armoury
```

If it loads, reopen ROG Control Center — the warning should be gone and advanced features will be available.

> **Note on GA605WV support:** The initial 6.19 release lists GA403-series models explicitly. If the GA605WV is not yet in the DMI table, some model-specific features (PPT tuning, APU memory) may still not appear even on 6.19. This is expected to be resolved via follow-up kernel patches.

</details>


## CLI Quick Reference

| Command | Description |
|---------|-------------|
| `asusctl info` | Show detected hardware |
| `asusctl battery --charge-limit 80` | Set battery charge limit to 80% |
| `asusctl battery` | Show current charge limit |
| `asusctl profile` | Show current performance profile |
| `asusctl profile -P Balanced` | Set performance profile |
| `asusctl profile --next` | Cycle to next profile |
| `asusctl slash --list` | List available Slash LED animations |
| `asusctl slash --enable -b false -s false` | Enable Slash LED, off on battery and sleep |
| `asusctl slash --mode Spectrum` | Set Slash LED animation |
| `asusctl slash -l 128` | Set Slash LED brightness (0–255) |
| `supergfxctl --mode` | Show current GPU mode |
| `supergfxctl --mode Hybrid` | Switch to Hybrid GPU mode |
| `supergfxctl --mode Integrated` | Switch to integrated GPU only |
| `rog-control-center` | Open ROG Control Center GUI |


## Additional Resources

- [asus-linux.org](https://asus-linux.org/) — Official project site
- [asusctl GitLab](https://gitlab.com/asus-linux/asusctl) — Source code and issue tracker
- [lukenukem COPR](https://copr.fedorainfracloud.org/coprs/lukenukem/asus-linux/) — Fedora package repository
- [NVIDIA Driver Installation Guide](nvidia-driver-installation.md) — NVIDIA driver setup and known issues
