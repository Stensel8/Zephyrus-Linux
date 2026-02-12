# ICC Color Profiles - Sharp LQ160R1JW02 Panel

Factory-calibrated ICC color profiles for the Sharp LQ160R1JW02 16" 2560x1600 240Hz display used in the ASUS ROG Zephyrus G16 GA605WV (2024).

## Profiles Included

| Profile Name (in GNOME) | Filename | Description |
|---|---|---|
| **Native** | `GA605WV_1002_104D158E_CMDEF.icm` | **Recommended** - Factory-calibrated for Sharp LQ160R1JW02 panel |
| DCI-P3 | `GA605WV_DCIP3.icm` | Vivid mode - Saturated DCI-P3 colors for gaming/media |
| Display P3 | `GA605WV_DisplayP3.icm` | Apple Display P3 colorspace |
| sRGB | `GA605WV_sRGB.icm` | Standard sRGB for web/photo work |

## Installation

```bash
mkdir -p ~/.local/share/icc
curl -L https://raw.githubusercontent.com/Stensel8/Zephyrus-Linux/development/assets/icc-profiles/GA605WV_1002_104D158E_CMDEF.icm -o ~/.local/share/icc/GA605WV_1002_104D158E_CMDEF.icm
curl -L https://raw.githubusercontent.com/Stensel8/Zephyrus-Linux/development/assets/icc-profiles/GA605WV_DCIP3.icm -o ~/.local/share/icc/GA605WV_DCIP3.icm
curl -L https://raw.githubusercontent.com/Stensel8/Zephyrus-Linux/development/assets/icc-profiles/GA605WV_DisplayP3.icm -o ~/.local/share/icc/GA605WV_DisplayP3.icm
curl -L https://raw.githubusercontent.com/Stensel8/Zephyrus-Linux/development/assets/icc-profiles/GA605WV_sRGB.icm -o ~/.local/share/icc/GA605WV_sRGB.icm
```

Then activate in **GNOME Settings** → **Color Management** → **Add Profile** → Select **Native**.

## Profile Source & Technical Details

These profiles originate from ASUS Windows driver packages, distributed via ASUS CDN for GameVisual/Armoury Crate software:

**Original ASUS CDN URL:**
```
https://dlcdn-rogboxbu1.asus.com/pub/ASUS/APService/Gaming/SYS/ROGS/20016-BWVQPK-01624c1cdd5a3c05252bad472fab1240.zip
```

URL structure: `https://dlcdn-rogboxbu1.asus.com/pub/ASUS/APService/Gaming/SYS/ROGS/{id}-{code}-{hash}.zip`  
For GA605WV: ID=`20016`, Code=`BWVQPK`, Hash=`01624c1cdd5a3c05252bad472fab1240`

**Modifications made:**
- ICC profile 'desc' tag metadata modified from technical identifiers (e.g., `ASUS_GA605WV_1002_104D158E_CMDEF`) to user-friendly names (e.g., `Native`)
- Filenames standardized with `GA605WV_` prefix for clear model identification
- Compatible with GNOME Color Management (colord) and other Linux color management systems

For technical implementation details of ICC metadata modification, see [`rename-icc-profiles.py`](../../rename-icc-profiles.py) in the repository root.

Panel ID: `104D158E` (Sharp LQ160R1JW02)  
GPU ID: `1002` (AMD Radeon 890M iGPU - drives internal eDP display)

## Compatibility

**Compatible with:**
- ASUS ROG Zephyrus G16 GA605WV (2024) with Sharp LQ160R1JW02 panel
- Any system using the same Sharp LQ160R1JW02 16" 2560x1600 240Hz panel

**Not compatible with:**
- GA605WV units with BOE panel (Panel ID: E5090C19)
- GA605WV units with Samsung panel (Panel ID: 834C41AE)

To check your panel:
```bash
sudo dnf install v4l-utils -y
edid-decode /sys/class/drm/card*-eDP-*/edid 2>/dev/null | grep "Manufacturer\|Product"
```

If you see "LQ160R1JW02" or Sharp manufacturer, these profiles are correct for your system.
