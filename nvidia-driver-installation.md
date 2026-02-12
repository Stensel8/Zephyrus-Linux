# NVIDIA Driver Installation - ROG Zephyrus G16 GA605WV (2024)

English | [Nederlands](nvidia-driver-installation.nl.md)

Guide for installing NVIDIA proprietary drivers on Fedora 43 with Secure Boot enabled.

**System Configuration:**
- Model: ASUS ROG Zephyrus G16 GA605WV (2024)
- CPU: AMD Ryzen AI 9 HX 370
- GPU: NVIDIA GeForce RTX 4060 Laptop (Max-Q)
- OS: Fedora 43
- Kernel: 6.18.8-200.fc43.x86_64
- Display Server: Wayland (GNOME)
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
- `nvidia-settings` - NVIDIA control panel
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
sudo systemctl enable nvidia-hibernate.service nvidia-suspend.service nvidia-resume.service nvidia-powerd.service
```

**What these services do:**
- `nvidia-hibernate.service` - Properly saves GPU state before hibernation
- `nvidia-suspend.service` - Manages GPU state during system suspend
- `nvidia-resume.service` - Restores GPU state after resume
- `nvidia-powerd.service` - NVIDIA dynamic power management daemon

These services prevent GPU state issues after suspend/resume cycles.

**Reference:**
- [NVIDIA Power Management Documentation](https://download.nvidia.com/XFree86/Linux-x86_64/470.74/README/powermanagement.html)
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
sudo grubby --update-kernel=ALL --args="rd.driver.blacklist=nouveau modprobe.blacklist=nouveau nvidia-drm.modeset=1"
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

**Why blacklist Nouveau:**
- The proprietary NVIDIA driver and Nouveau cannot coexist
- Blacklisting prevents conflicts and ensures the proprietary driver is always used
- If the NVIDIA driver fails, you can remove these parameters from GRUB to fall back to Nouveau

**Benefits:**
- Better Wayland performance and stability
- Prevents driver conflicts during boot
- Improved external monitor support
- Smoother graphics performance in general

**Note:** These parameters are optional but recommended for optimal performance.

**References:**
- [NVIDIA Driver Modesetting - Arch Wiki](https://wiki.archlinux.org/title/NVIDIA)
- [Understanding nvidia-drm.modeset=1 - NVIDIA Developer Forums](https://forums.developer.nvidia.com/t/understanding-nvidia-drm-modeset-1-nvidia-linux-driver-modesetting/204068)
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


echo $XDG_SESSION_TYPE
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


