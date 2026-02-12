# ICC Color Profiles - GA605WV (2024)

Factory-calibrated ICC profiles for the Zephyrus G16 GA605WV display.

## Source

These profiles were extracted from the ASUS Windows driver package:

```
https://dlcdn-rogboxbu1.asus.com/pub/ASUS/APService/Gaming/SYS/ROGS/20016-BWVQPK-01624c1cdd5a3c05252bad472fab1240.zip
```

## Files

| Filename | Description | For GNOME |
|---|---|---|
| `GA605WV_1002_104D158E_CMDEF.icm` | **Recommended** - Factory-calibrated native profile for Sharp LQ160R1JW02 + AMD 890M | Import this |
| `ASUS_sRGB.icm` | sRGB colorspace (web, photo) | Optional |
| `ASUS_DisplayP3.icm` | Display P3 colorspace (Apple) | Optional |
| `ASUS_DCIP3.icm` | DCI-P3 colorspace (cinema) | Optional |

### Filename Reference

`GA605WV_1002_104D158E_CMDEF`:
- `GA605WV` = ASUS ROG Zephyrus G16 model
- `1002` = AMD GPU ID (Radeon 890M iGPU)
- `104D158E` = Sharp LQ160R1JW02 panel ID
- `CMDEF` = Factory-calibrated profile

## Install

Copy your GPU/panel profile and optional color spaces to GNOME:

```bash
mkdir -p ~/.local/share/icc

# Your GPU/panel combination
cp GA605WV_1002_104D158E_CMDEF.icm ~/.local/share/icc/

# Optional: Universal color spaces
cp ASUS_sRGB.icm ~/.local/share/icc/
cp ASUS_DisplayP3.icm ~/.local/share/icc/
cp ASUS_DCIP3.icm ~/.local/share/icc/
```

Then activate in **GNOME Settings** → **Color Management** → **Add Profile** → Select `GA605WV_1002_104D158E_CMDEF`.
