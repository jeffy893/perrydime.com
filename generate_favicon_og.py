#!/usr/bin/env python3
"""
Generate Favicon Package and Open Graph Images
Reads the logo from source/branding/ and creates:
- favicon.ico (16x16, 32x32, 48x48)
- favicon.png (32x32)
- apple-touch-icon.png (180x180)
- og-image.png (1200x630 for social media)
"""

from PIL import Image
import os

# Paths
SOURCE_LOGO = "source/branding/perrydime-logo.png"
OUTPUT_DIR = "docs"
ASSETS_DIR = os.path.join(OUTPUT_DIR, "assets", "img")

# Ensure output directories exist
os.makedirs(ASSETS_DIR, exist_ok=True)

def create_favicon_package():
    """Generate all favicon sizes and formats"""
    print("=" * 70)
    print("Perry Dime - Favicon & Open Graph Image Generator")
    print("=" * 70)
    
    # Load the source logo
    print(f"\n📂 Loading logo from: {SOURCE_LOGO}")
    logo = Image.open(SOURCE_LOGO)
    print(f"   Original size: {logo.size}")
    
    # 1. Generate favicon.png (32x32)
    print("\n🎨 Generating favicon.png (32x32)...")
    favicon_32 = logo.copy()
    favicon_32.thumbnail((32, 32), Image.Resampling.LANCZOS)
    favicon_path = os.path.join(OUTPUT_DIR, "favicon.png")
    favicon_32.save(favicon_path, "PNG")
    print(f"   ✅ Saved: {favicon_path}")
    
    # 2. Generate favicon.ico (multi-size)
    print("\n🎨 Generating favicon.ico (16x16, 32x32, 48x48)...")
    favicon_16 = logo.copy()
    favicon_16.thumbnail((16, 16), Image.Resampling.LANCZOS)
    
    favicon_32_ico = logo.copy()
    favicon_32_ico.thumbnail((32, 32), Image.Resampling.LANCZOS)
    
    favicon_48 = logo.copy()
    favicon_48.thumbnail((48, 48), Image.Resampling.LANCZOS)
    
    favicon_ico_path = os.path.join(OUTPUT_DIR, "favicon.ico")
    favicon_16.save(
        favicon_ico_path,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48)]
    )
    print(f"   ✅ Saved: {favicon_ico_path}")
    
    # 3. Generate apple-touch-icon.png (180x180)
    print("\n🍎 Generating apple-touch-icon.png (180x180)...")
    apple_icon = logo.copy()
    apple_icon.thumbnail((180, 180), Image.Resampling.LANCZOS)
    apple_icon_path = os.path.join(OUTPUT_DIR, "apple-touch-icon.png")
    apple_icon.save(apple_icon_path, "PNG")
    print(f"   ✅ Saved: {apple_icon_path}")
    
    # 4. Generate Open Graph image (1200x630)
    print("\n📱 Generating og-image.png (1200x630 for social media)...")
    
    # Create a canvas with the brand color background
    og_width, og_height = 1200, 630
    og_image = Image.new("RGB", (og_width, og_height), color="#c8af99")
    
    # Calculate logo size (maintain aspect ratio, max 85% of canvas height for better visibility)
    logo_max_height = int(og_height * 0.85)
    logo_aspect = logo.width / logo.height
    logo_height = logo_max_height
    logo_width = int(logo_height * logo_aspect)
    
    # If logo is too wide, scale by width instead (allow up to 90% of width)
    if logo_width > og_width * 0.9:
        logo_width = int(og_width * 0.9)
        logo_height = int(logo_width / logo_aspect)
    
    # Resize logo
    logo_resized = logo.copy()
    logo_resized.thumbnail((logo_width, logo_height), Image.Resampling.LANCZOS)
    
    # Center the logo on the canvas
    x_offset = (og_width - logo_resized.width) // 2
    y_offset = (og_height - logo_resized.height) // 2
    
    # Paste logo (handle transparency)
    if logo_resized.mode == 'RGBA':
        og_image.paste(logo_resized, (x_offset, y_offset), logo_resized)
    else:
        og_image.paste(logo_resized, (x_offset, y_offset))
    
    og_image_path = os.path.join(ASSETS_DIR, "og-image.png")
    og_image.save(og_image_path, "PNG", optimize=True)
    print(f"   ✅ Saved: {og_image_path}")
    print(f"   📐 Dimensions: {og_width}x{og_height}")
    
    # 5. Copy logo to assets for easy access
    print("\n📋 Copying logo to assets...")
    logo_copy_path = os.path.join(ASSETS_DIR, "perrydime-logo.png")
    logo.save(logo_copy_path, "PNG")
    print(f"   ✅ Saved: {logo_copy_path}")
    
    print("\n" + "=" * 70)
    print("✅ Favicon package and Open Graph image generated successfully!")
    print("=" * 70)
    print("\nGenerated files:")
    print(f"  • {favicon_path}")
    print(f"  • {favicon_ico_path}")
    print(f"  • {apple_icon_path}")
    print(f"  • {og_image_path}")
    print(f"  • {logo_copy_path}")
    print("\n📝 Next: Update HTML files with proper meta tags")
    print("=" * 70)

if __name__ == "__main__":
    create_favicon_package()
