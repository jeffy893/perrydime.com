#!/usr/bin/env python3
"""
HEIC to PNG Converter for Perry Dime Art Gallery
Converts HEIC images to high-quality, web-optimized PNG format
while strictly preserving the subdirectory structure.
"""

import os
import sys
from pathlib import Path
from PIL import Image
import pillow_heif

# Register HEIF opener with Pillow
pillow_heif.register_heif_opener()

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
SOURCE_DIR = SCRIPT_DIR / "source/art"
OUTPUT_DIR = SCRIPT_DIR / "docs/assets/img/art"
PNG_QUALITY = 95  # High quality for web
MAX_DIMENSION = 2400  # Max width or height for web optimization

def ensure_directory(path):
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)

def get_relative_path(file_path, base_dir):
    """Get the relative path from base directory."""
    return file_path.relative_to(base_dir)

def optimize_image(image, max_dimension=MAX_DIMENSION):
    """
    Optimize image for web while maintaining quality.
    Resize if larger than max_dimension while preserving aspect ratio.
    """
    width, height = image.size
    
    if width > max_dimension or height > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int((max_dimension / width) * height)
        else:
            new_height = max_dimension
            new_width = int((max_dimension / height) * width)
        
        print(f"    Resizing from {width}x{height} to {new_width}x{new_height}")
        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return image

def convert_heic_to_png(heic_path, png_path):
    """Convert a single HEIC file to PNG format."""
    try:
        # Open HEIC file
        with Image.open(heic_path) as img:
            # Convert to RGB if necessary (HEIC can have different color modes)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Keep transparency if present
                pass
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Optimize for web
            img = optimize_image(img)
            
            # Save as PNG with optimization
            img.save(
                png_path,
                'PNG',
                optimize=True,
                compress_level=6  # Good balance between size and speed
            )
        
        return True
    except Exception as e:
        print(f"    ERROR: {e}")
        return False

def find_heic_files(directory):
    """Recursively find all HEIC files in directory."""
    heic_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.upper().endswith('.HEIC'):
                heic_files.append(Path(root) / file)
    return heic_files

def main():
    """Main conversion process."""
    print("=" * 70)
    print("HEIC to PNG Converter - Perry Dime Art Gallery")
    print("=" * 70)
    print()
    
    # Check if source directory exists
    if not SOURCE_DIR.exists():
        print(f"ERROR: Source directory '{SOURCE_DIR}' does not exist!")
        sys.exit(1)
    
    # Find all HEIC files
    print(f"Scanning '{SOURCE_DIR}' for HEIC files...")
    heic_files = find_heic_files(SOURCE_DIR)
    
    if not heic_files:
        print("No HEIC files found!")
        sys.exit(0)
    
    print(f"Found {len(heic_files)} HEIC file(s)")
    print()
    
    # Ensure output directory exists
    ensure_directory(OUTPUT_DIR)
    
    # Convert each file
    converted = 0
    failed = 0
    skipped = 0
    
    for heic_path in heic_files:
        # Get relative path from source directory
        rel_path = heic_path.relative_to(SOURCE_DIR)
        
        # Create corresponding PNG path in output directory
        png_rel_path = rel_path.with_suffix('.png')
        png_path = OUTPUT_DIR / png_rel_path
        
        # Ensure subdirectory exists
        ensure_directory(png_path.parent)
        
        # Display progress
        print(f"[{converted + failed + skipped + 1}/{len(heic_files)}] {rel_path}")
        
        # Check if PNG already exists
        if png_path.exists():
            print(f"    SKIPPED: {png_rel_path} already exists")
            skipped += 1
            continue
        
        # Convert
        print(f"    Converting to: {png_rel_path}")
        if convert_heic_to_png(heic_path, png_path):
            file_size = png_path.stat().st_size / 1024  # KB
            print(f"    SUCCESS: {file_size:.1f} KB")
            converted += 1
        else:
            failed += 1
        
        print()
    
    # Summary
    print("=" * 70)
    print("CONVERSION SUMMARY")
    print("=" * 70)
    print(f"Total files found:  {len(heic_files)}")
    print(f"Successfully converted: {converted}")
    print(f"Skipped (already exist): {skipped}")
    print(f"Failed: {failed}")
    print()
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 70)

if __name__ == "__main__":
    main()
