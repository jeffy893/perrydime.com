---
inclusion: manual
---

# Image Conversion Process

## HEIC to PNG Conversion

### Overview
All HEIC images from `source/art/` have been converted to high-quality, web-optimized PNG format and stored in `docs/assets/img/art/` with the subdirectory structure strictly preserved.

### Conversion Script
**File**: `convert_heic_to_png.py`

### Configuration
- **Python Version**: 3.10
- **Max Dimension**: 2400px (width or height)
- **PNG Quality**: High (optimize=True, compress_level=6)
- **Resampling**: LANCZOS (highest quality)

### Dependencies
```bash
pip install -r requirements.txt
```

Required packages:
- Pillow >= 10.0.0
- pillow-heif >= 0.13.0

### Running the Conversion
```bash
python3.10 convert_heic_to_png.py
```

### Directory Structure Preservation
The script maintains exact subdirectory structure:
- `source/art/Female_Form/IMG_0272.HEIC` → `docs/assets/img/art/Female_Form/IMG_0272.png`
- `source/art/Home_Art/IMG_3451.HEIC` → `docs/assets/img/art/Home_Art/IMG_3451.png`

### Conversion Results (Initial Run)
- **Total files found**: 50
- **Successfully converted**: 50
- **Failed**: 0
- **Average file size**: ~4.5 MB per PNG

### Image Optimization
Images are automatically optimized for web:
1. Resized if larger than 2400px (maintaining aspect ratio)
2. PNG compression applied (level 6)
3. Optimization flag enabled
4. Original HEIC files preserved in source/

### Re-running the Script
The script is idempotent:
- Skips files that already exist in the output directory
- Safe to run multiple times
- Only converts new or missing files

### Future Additions
When adding new HEIC files to `source/art/`:
1. Place them in the appropriate subdirectory
2. Run `python3.10 convert_heic_to_png.py`
3. Only new files will be converted
4. Directory structure will be automatically preserved
