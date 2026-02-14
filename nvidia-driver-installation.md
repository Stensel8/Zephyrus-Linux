# NVIDIA Driver Installation - ROG Zephyrus G16 GA605WV (2024)

English | [Nederlands](nvidia-driver-installation.nl.md)

Guide for installing NVIDIA proprietary drivers on Fedora 43 with Secure Boot enabled.

**System Configuration:**
- Model: ASUS ROG Zephyrus G16 GA605WV (2024)
- CPU: AMD Ryzen AI 9 HX 370
- GPU: NVIDIA GeForce RTX 4060 Laptop (Max-Q) + AMD Radeon 890M (iGPU)
- OS: Fedora 43
- Kernel: 6.18.9-200.fc43.x86_64
- Display Server: Wayland (GNOME 49)
- Secure Boot: Enabled

**Driver Information:**
- Version: 580.119.02
- Source: RPM Fusion
- Installation Method: akmod (automatic kernel module rebuilding)


## Prerequisites

### System Verification

<details>
<summary>Check kernel version</summary>

Required: Kernel 6.10+ for Ryzen AI 9 HX 370 support.

```bash
uname -r
```

</details>

<details>
<summary>Check Secure Boot status</summary>

```bash
mokutil --sb-state
```

</details>

### Why Proprietary Driver

The open-source Nouveau driver has poor performance on modern NVIDIA GPUs. The proprietary driver is required for:
- Gaming and graphics-intensive applications
- CUDA workloads
- Proper Wayland support (available since driver 555+)


## Installation Steps

<details>
<summary><strong>Step 1:</strong> Resolve repository issues</summary>

If encountering checksum errors during `dnf update`, clean the cache:

```bash
sudo dnf clean all
sudo dnf makecache
```

</details>

<details>
<summary><strong>Step 2:</strong> Add RPM Fusion repositories</summary>

RPM Fusion provides NVIDIA drivers for Fedora. NVIDIA's official CUDA repository does not yet support Fedora 43.

```bash
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm -y
```

</details>

<details>
<summary><strong>Step 3:</strong> Update system</summary>

```bash
sudo dnf update -y
```

Wait for update completion.
</details>

<details>
<summary><strong>Step 4:</strong> Verify driver version</summary>

Check available NVIDIA driver version:

```bash
dnf info akmod-nvidia
```

Confirm the version matches the current release for Fedora 43.
</details>

<details>
<summary><strong>Step 5:</strong> Install NVIDIA driver</summary>

Install driver with CUDA support:

```bash
sudo dnf install akmod-nvidia xorg-x11-drv-nvidia-cuda -y
```

This installs the driver, CUDA libraries, and build dependencies (about 1 GB).
- `akmod-nvidia` - Automatic kernel module builder
- `xorg-x11-drv-nvidia` - NVIDIA driver (supports both X11 and Wayland)
- `xorg-x11-drv-nvidia-cuda` - CUDA libraries
- Build dependencies (gcc, kernel-devel, etc.)

Note: A MOK password prompt may not appear during installation. This is normal.
</details>

<details>
<summary><strong>Step 6:</strong> Build kernel modules</summary>

Force akmod to build NVIDIA kernel modules:

```bash
sudo akmods --force
```

This process may take 5-10 minutes.
</details>

<details>
<summary><strong>Step 7:</strong> Verify kernel modules</summary>

Check that kernel modules were built:

```bash
ls /lib/modules/$(uname -r)/extra/nvidia/
```

All five kernel modules should be present.
</details>

<details>
<summary><strong>Step 8:</strong> First reboot and check GNOME Software</summary>

```bash
sudo reboot
```

After reboot, open GNOME Software and note the MOK enrollment code. The driver is not yet active.
</details>

<details>
<summary><strong>Step 9:</strong> MOK enrollment on next boot</summary>

Reboot again:

```bash
sudo reboot
```

During boot, the MOK Management screen (blue screen) will appear:
1. Select "Enroll MOK"
2. Select "Continue"
3. Select "Yes"
4. Enter the MOK enrollment code from GNOME Software
5. Reboot

The system will boot normally after MOK enrollment.
</details>

<details>
<summary><strong>Step 10:</strong> Rebuild modules after MOK enrollment</summary>

After MOK enrollment, rebuild the kernel modules. They will now be signed with the enrolled key.

```bash
sudo akmods --force --rebuild
```

</details>

<details>
<summary><strong>Step 11:</strong> Final reboot</summary>

```bash
sudo reboot
```

The NVIDIA driver will now load correctly. GNOME Software should show the driver as installed (not pending).
</details>

<details>
<summary><strong>Step 12:</strong> Enable NVIDIA power management services</summary>

Enable NVIDIA power services for better suspend/resume behavior and power management:

```bash
sudo systemctl enable nvidia-hibernate.service nvidia-suspend.service nvidia-resume.service
```

**What these services do:**
- `nvidia-hibernate.service` - Properly saves GPU state before hibernation
- `nvidia-suspend.service` - Manages GPU state during system suspend
- `nvidia-resume.service` - Restores GPU state after resume

These services prevent GPU state issues after suspend/resume cycles.

**Important: Do NOT enable `nvidia-powerd` — mask it permanently**

The `nvidia-powerd.service` manages NVIDIA Dynamic Boost, which shifts extra wattage (~5-15W) from the CPU to the GPU during heavy GPU loads. While useful on Intel-based laptops, it conflicts with AMD ATPX power management on the Zephyrus G16 and causes soft lockups and "GPU has fallen off the bus" errors.

On this laptop, GPU power is managed via ATPX (AMD-driven via ACPI). The NVIDIA suspend/hibernate/resume services and `supergfxctl` handle power states correctly without `nvidia-powerd`.

**What you lose by disabling it:** Minimal — a few FPS less during heavy GPU workloads. The ~5-15W Dynamic Boost is not worth the instability on AMD ATPX hardware.

**Disable and mask permanently:**
```bash
sudo systemctl disable nvidia-powerd.service
sudo systemctl stop nvidia-powerd.service
sudo systemctl mask nvidia-powerd.service
```

Masking creates a symlink to `/dev/null`, preventing any process — including NVIDIA driver updates via `dnf` — from re-enabling the service.

**If you want to try re-enabling it later** (e.g., after a kernel or driver update that may fix the ATPX conflict):
```bash
sudo systemctl unmask nvidia-powerd.service
sudo systemctl enable --now nvidia-powerd.service
```

**Reference:**
- [NVIDIA Power Management Documentation](https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/powermanagement.html)
</details>


## Post-Installation Verification

<details>
<summary><strong>Test 1:</strong> Verify NVIDIA driver</summary>

After reboot, check driver status:

```bash
nvidia-smi
```

You should see the NVIDIA driver and CUDA versions listed.
</details>

<details>
<summary><strong>Test 2:</strong> Verify Wayland session</summary>

Confirm running Wayland (not X11):

```bash
echo $XDG_SESSION_TYPE
```

</details>

<details>
<summary><strong>Test 3:</strong> Check loaded kernel modules</summary>

```bash
lsmod | grep nvidia
```

The NVIDIA modules are loaded and the driver is functional.
</details>

<details>
<summary><strong>Test 4:</strong> Verify in GNOME Software</summary>

Open GNOME Software (white bag icon):
- Navigate to "Installed"
- Search for "NVIDIA Linux Graphics Driver"
- Status should show "Installed" (not "Pending")
- "Uninstall" button is visible

This confirms the system recognizes the driver as properly installed.
</details>


## Performance Optimizations

<details>
<summary>Kernel parameters for improved performance and stability</summary>

Adding certain kernel parameters can improve NVIDIA driver performance, especially for Wayland sessions and dual-GPU setups.

**Step 1: Add recommended kernel parameters**

```bash
sudo grubby --update-kernel=ALL --args="rd.driver.blacklist=nouveau modprobe.blacklist=nouveau nvidia-drm.modeset=1 nvidia-drm.fbdev=1 nvidia.NVreg_PreserveVideoMemoryAllocations=1"
```

**Step 2: Verify parameters were added**

```bash
sudo grubby --info=ALL | grep args
```

Expected output should include the added kernel parameters.

**Step 3: Reboot to apply changes**

```bash
sudo reboot
```

**What these parameters do:**

- `rd.driver.blacklist=nouveau` - Prevents the open-source Nouveau driver from loading during early boot (initramfs)
- `modprobe.blacklist=nouveau` - Prevents Nouveau from loading after boot
- `nvidia-drm.modeset=1` - Enables NVIDIA kernel mode setting for better Wayland support and performance
- `nvidia-drm.fbdev=1` - Makes NVIDIA use its framebuffer via the kernel DRM framework instead of a generic framebuffer. Improves handoff between console and Wayland/GNOME and prevents race conditions during suspend/resume on hybrid GPU laptops
- `nvidia.NVreg_PreserveVideoMemoryAllocations=1` - Preserves VRAM allocations during suspend/resume instead of releasing and rebuilding them. Prevents corrupted VRAM after resume, which can cause soft lockups

**Why blacklist Nouveau:**
- The proprietary NVIDIA driver and Nouveau cannot coexist
- Blacklisting prevents conflicts and ensures the proprietary driver is always used
- If the NVIDIA driver fails, you can remove these parameters from GRUB to fall back to Nouveau

**Benefits:**
- Better Wayland performance and stability
- Prevents driver conflicts during boot
- Improved external monitor support
- More stable suspend/resume cycles on hybrid GPU setups
- Smoother graphics performance in general

**Note:** These parameters are optional but recommended for optimal performance.

**Re-enable graphical boot splash:**

Fedora uses `rhgb` (Red Hat Graphical Boot) and `quiet` to show a Plymouth splash screen during boot instead of scrolling kernel text. If you removed these while debugging NVIDIA or boot issues, re-add them:

```bash
sudo grubby --update-kernel=ALL --args="rhgb quiet"
```

The default Plymouth theme (`bgrt`) shows the ASUS/BIOS manufacturer logo. To debug boot issues in the future, you can temporarily remove them:

```bash
sudo grubby --update-kernel=ALL --remove-args="rhgb quiet"
```

**References:**
- [NVIDIA Driver Modesetting - Arch Wiki](https://wiki.archlinux.org/title/NVIDIA)
- [Understanding nvidia-drm.modeset=1 - NVIDIA Developer Forums](https://forums.developer.nvidia.com/t/understanding-nvidia-drm-modeset-1-nvidia-linux-driver-modesetting/204068)
- [NVIDIA Power Management Documentation](https://download.nvidia.com/XFree86/Linux-x86_64/580.119.02/README/powermanagement.html)
</details>


## ICC Color Profiles

<details>
<summary>Install ASUS GameVisual color profiles for Sharp LQ160R1JW02 panel</summary>

The GA605WV ships with a Sharp LQ160R1JW02 16" 2560x1600 240Hz display. ASUS factory-calibrates each panel and provides color profiles via their ASUS System Control Interface. On Windows, these are automatically applied by Armoury Crate/GameVisual. On Linux, we must install them manually.

These color profiles were extracted from ASUS Windows driver packages and optimized for GNOME Color Management.

**Install the color profiles:**

The ICC color profiles are located in the `assets/icc-profiles/` directory of this repository. Clone the repository or manually download the profiles and copy them to `~/.local/share/icc`:

```bash
mkdir -p ~/.local/share/icc

# If you've already cloned the repository:
cp assets/icc-profiles/*.icm ~/.local/share/icc/

# Or download the specific profiles you need from the repository
```

**Activate Native profile in GNOME:**

1. Open **Settings** → **Color Management**
2. Select **Built-In Screen**
3. Click **Add Profile**
4. Select **Native**
5. Click **Add**

**Note:** If GNOME Settings shows old technical names (e.g., "ASUS GA605WV 1002 104D158E CMDEF" instead of "Native"), close Settings and reopen, or log out/in to refresh the color cache.

**Available color profiles:**

| GNOME Name | File | Description |
|---|---|---|
| **Native** | `GA605WV_1002_104D158E_CMDEF.icm` | **Recommended** - Factory-calibrated for Sharp LQ160R1JW02 panel, best color accuracy |
| DCI-P3 | `ASUS_DCIP3.icm` | Saturated DCI-P3 colors for gaming/media (Vivid mode) |
| Display P3 | `ASUS_DisplayP3.icm` | Display P3 colorspace for Apple-compatible workflows |
| sRGB | `ASUS_sRGB.icm` | sRGB standard for web/photo work |

**Recommendation:**

Use **Native** for best color accuracy. This profile contains factory calibration specific to the Sharp LQ160R1JW02 panel in this laptop. The other profiles (DCI-P3, Display P3, sRGB) are generic colorspaces without panel-specific corrections.

**Note:** The `_1002_` in the filename refers to the AMD iGPU (Vendor ID 0x1002), which drives the internal eDP display on this hybrid GPU laptop.

**Background:**

The profiles were found through analysis of ASUS Windows driver packages. The ASUS CDN URL structure:
```
https://dlcdn-rogboxbu1.asus.com/pub/ASUS/APService/Gaming/SYS/ROGS/{id}-{code}-{hash}.zip
```

For the GA605WV, this is: `20016-BWVQPK-01624c1cdd5a3c05252bad472fab1240.zip`

The profiles contain factory color corrections specific to the Sharp LQ160R1JW02 panel (Panel ID: 104D158E) used in this laptop model.

**Technical Details:**

The profiles in this repository are pre-processed with custom ICC metadata 'desc' tags so they appear with readable names directly in GNOME Color Management. For users interested in how such modifications work, you can implement similar ICC 'desc' tag manipulation yourself using Python's PIL/ImageCms.
</details>


## Known Issues

<details>
<summary>System crashes with external monitors (AMD GPU PSR bug)</summary>

**Problem:**
System freezes or crashes when using external monitors via Thunderbolt/USB-C, especially when connecting/disconnecting displays. Logs show AMD GPU errors:
```
amdgpu 0000:66:00.0: amdgpu: MES failed to respond to msg=RESET
amdgpu 0000:66:00.0: amdgpu: Ring gfx_0.0.0 reset failed
amdgpu 0000:66:00.0: amdgpu: GPU reset begin!
```

**Cause:**
This laptop has dual GPUs (AMD Radeon 890M integrated + NVIDIA RTX 4060 discrete). The AMD GPU's PSR (Panel Self Refresh) feature has a bug causing crashes with external Thunderbolt monitors.

**Solution:**
Disable AMD PSR by adding a kernel parameter:

```bash
sudo grubby --update-kernel=ALL --args="amdgpu.dcdebugmask=0x600"
```

Verify it was added:
```bash
sudo grubby --info=ALL | grep args
```

Reboot:
```bash
sudo reboot
```

**What this does:**
- `amdgpu.dcdebugmask=0x600` disables PSR (Panel Self Refresh) on the AMD GPU
- PSR is a power-saving feature where the display refreshes itself without GPU involvement
- The PSR implementation has bugs with Thunderbolt/USB-C external monitors

**Trade-offs:**
- Pro: Stable system with external monitors
- Con: Slightly higher power consumption (PSR disabled)

**Verification:**
Monitor for AMD GPU errors while using external displays:
```bash
sudo journalctl -f -k | grep -i amdgpu
```

If no `amdgpu: [drm] *ERROR*` messages appear, the fix is working.

**Reference:**
- [Fedora Discussion: Zephyrus G16 External Monitor Crashes](https://discussion.fedoraproject.org/t/asus-zephyrus-g16-with-nvidia-and-external-monitor-crashes-every-few-minutes/147175)
</details>

<details>
<summary>VS Code crashes system (AMD GPU page fault - Kernel 6.18.x bug)</summary>

**What's happening:**
System freezes completely during VS Code use. Kernel 6.18.x/6.19.x have critical amdgpu driver bugs. VS Code hardware acceleration triggers AMD Radeon 890M page fault → complete freeze.

**Fix:**
Add to `~/.config/Code/User/settings.json`:
```json
{
    "disable-hardware-acceleration": true
}
```

**Next steps:**
Restart VS Code. System stays stable, VS Code slightly slower but perfectly usable.

**Sources:**
- [VS Code Issue #238088](https://github.com/microsoft/vscode/issues/238088)
- [Framework: Critical amdgpu bugs kernel 6.18.x](https://community.frame.work/t/attn-critical-bugs-in-amdgpu-driver-included-with-kernel-6-18-x-6-19-x/79221)
</details>

<details>
<summary>Brave Browser crashes system (AMD GPU page fault - Kernel 6.18.x bug)</summary>

**What's happening:**
System freezes or crashes during Brave Browser use, even with minimal workload (a few tabs). This is the same underlying issue as the VS Code crash: Chromium-based applications with hardware acceleration trigger AMD Radeon 890M page faults on kernel 6.18.x/6.19.x.

Typical crash sequence in logs:
```
amdgpu: [gfxhub] page fault (src_id:0 ring:24 vmid:2)
amdgpu: Faulty UTCL2 client ID: SQC (data)
amdgpu: ring gfx_0.0.0 timeout, signaled seq=302899, emitted seq=302901
amdgpu: GPU reset begin!
```

After GPU reset, gnome-shell crashes (Signal 6 ABRT) because it detects a context reset.

**Fix:**
Open Brave Browser and go to `brave://settings/system`. Turn off **"Use hardware acceleration when available"**.

Alternatively via terminal:
```bash
sed -i 's/"hardware_acceleration_mode_previous":true/"hardware_acceleration_mode_previous":false/' ~/.config/BraveSoftware/Brave-Browser/Local\ State
```

Or start Brave with the `--disable-gpu` flag:
```bash
brave-browser-stable --disable-gpu
```

**Next steps:**
Restart Brave. Verify via `brave://gpu` that GPU acceleration is disabled. System stays stable, Brave is slightly slower on heavy pages but perfectly usable.

**Background:**
Brave, VS Code, and other Chromium-based applications (Chrome, Edge, Electron apps) use GPU shader compilation via Mesa. On kernel 6.18.x, the amdgpu driver has a bug in the Shader Queue Controller (SQC) memory access, causing page faults that trigger a full GPU reset. The fix is to disable hardware acceleration per application until a kernel/Mesa update resolves the issue.

**Sources:**
- [Framework: Critical amdgpu bugs kernel 6.18.x](https://community.frame.work/t/attn-critical-bugs-in-amdgpu-driver-included-with-kernel-6-18-x-6-19-x/79221)
</details>

<details>
<summary>NVIDIA soft lockup with minimal GPU load (hybrid GPU power management)</summary>

**What's happening:**
System freezes with an NVIDIA soft lockup, even without active GPU use. Kernel logs show:
```
watchdog: BUG: soft lockup - CPU#23 stuck for 62s!
NVRM: Xid (PCI:0000:65:00): 79, pid=<...>, GPU has fallen off the bus
```

This can occur due to a combination of factors on hybrid GPU laptops:
- `nvidia-powerd` conflicts with AMD ATPX power management
- NVIDIA dGPU power state transitions fail
- Corrupted VRAM after suspend/resume cycles

**Additional symptom: Reboot hang (black screen, backlights stay on)**

The system appears to shut down but never completes the hardware reset — the screen goes black but keyboard and screen backlights remain on. This occurs when `nvidia-powerd` interferes with ACPI power state transitions during shutdown/reboot.

**Root cause: `supergfxd` starts `nvidia-powerd` behind your back**

Even when `nvidia-powerd` is disabled via `systemctl disable`, `supergfxd` (the GPU switching daemon from asusctl) directly calls `systemctl start nvidia-powerd.service` during GPU mode switches. This bypasses the disabled state and re-activates the conflict with ATPX.

**How this was diagnosed:**

Checking the logs of the hung boot reveals `supergfxd` starting `nvidia-powerd`:
```bash
journalctl -b -1 --no-pager | grep -iE "nvidia.*powerd|supergfxd"
```

Key evidence:
```
supergfxd: [DEBUG supergfxctl] Did CommandArgs { inner: ["start", "nvidia-powerd.service"] }
nvidia-powerd: ERROR! Client (presumably SBIOS) has requested to disable Dynamic Boost DC controller
```

The SBIOS error confirms the firmware rejected Dynamic Boost, but `nvidia-powerd` was already running and interfering with power state management. Checking the shutdown sequence:

```bash
journalctl -b -1 --reverse | head -20
```

Shows the hardware watchdog failed to stop, confirming the ACPI reboot never completed:
```
watchdog: watchdog0: watchdog did not stop!
```

**Fix:**

1. Disable and **mask** `nvidia-powerd` (masking is essential — `disable` alone is not enough because `supergfxd` bypasses it):
```bash
sudo systemctl disable nvidia-powerd.service
sudo systemctl stop nvidia-powerd.service
sudo systemctl mask nvidia-powerd.service
```

2. Add kernel parameters for more stable NVIDIA power management:
```bash
sudo grubby --update-kernel=ALL --args="nvidia-drm.fbdev=1 nvidia.NVreg_PreserveVideoMemoryAllocations=1"
```

3. Reboot:
```bash
sudo reboot
```

**Next steps:**
System is more stable after these changes. The NVIDIA dGPU is still properly managed via ATPX (AMD-driven power switching) without `nvidia-powerd` interfering. The mask creates a symlink to `/dev/null`, ensuring no process — including `supergfxd` and NVIDIA driver updates — can re-enable the service.

**Background:**
On laptops with AMD iGPU + NVIDIA dGPU, the ATPX framework (via ACPI) controls which GPU is active. `nvidia-powerd` tries to make power decisions independently, which conflicts with ATPX. The `NVreg_PreserveVideoMemoryAllocations=1` parameter prevents VRAM from being lost during power transitions, and `nvidia-drm.fbdev=1` provides cleaner framebuffer handoff.
</details>


## Troubleshooting

<details>
<summary>nvidia-smi command not found or fails</summary>

Check if NVIDIA modules are loaded:
```bash
lsmod | grep nvidia
```

Check system logs for errors:
```bash
sudo journalctl -b | grep nvidia
```

Rebuild kernel modules:
```bash
sudo akmods --force --rebuild
sudo reboot
```
</details>

<details>
<summary>MOK enrollment issues or "Key was rejected by service" error</summary>

If you receive the error `modprobe: ERROR: could not insert 'nvidia': Key was rejected by service`, the kernel modules were built before MOK enrollment completed.

Solution:
```bash
# Rebuild modules after MOK enrollment
sudo akmods --force --rebuild

# Reboot
sudo reboot
```

To reset MOK if needed:
```bash
sudo mokutil --reset
```

Reboot and attempt enrollment again.
</details>

<details>
<summary>Running X11 instead of Wayland</summary>

Check session type:
```bash
echo $XDG_SESSION_TYPE
```

If output is `x11`, ensure Wayland is enabled in GDM:
```bash
sudo nano /etc/gdm/custom.conf
```

Verify this line is present and not commented:
```
WaylandEnable=true
```

Reboot after changes.
</details>

<details>
<summary>Kernel module build failures</summary>

Ensure kernel headers match running kernel:
```bash
sudo dnf install kernel-devel-$(uname -r)
```

Force rebuild:
```bash
sudo akmods --force
```
</details>


## Technical Notes

### Package Naming
The package `xorg-x11-drv-nvidia` is a legacy name. The driver supports both X11 and Wayland. Fedora 43 defaults to Wayland with GNOME.

### Secure Boot
Akmod handles Secure Boot module signing automatically. The akmods systemd service rebuilds kernel modules automatically after kernel updates.

### GNOME Software
GNOME Software may show "NVIDIA Linux Graphics Driver" with "Pending install" status. This is a GUI synchronization issue and can be ignored. The driver is properly installed via DNF.


## Additional Resources

- [RPM Fusion NVIDIA Driver Guide](https://www.if-not-true-then-false.com/2015/fedora-nvidia-guide/)
- [Ryzen AI 9 HX 370 Linux Support](https://forums.linuxmint.com/viewtopic.php?t=429052)
- [NVIDIA vs Nouveau Performance](https://machaddr.substack.com/p/nouveau-vs-nvidia-the-battle-between)
- [Zephyrus G16 2024 Linux Guide](https://www.ehmiiz.se/blog/linux_asus_g16_2024/)
- [Fedora Discussion: Zephyrus External Monitor Issues](https://discussion.fedoraproject.org/t/asus-zephyrus-g16-with-nvidia-and-external-monitor-crashes-every-few-minutes/147175)


