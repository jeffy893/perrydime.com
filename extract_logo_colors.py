#!/usr/bin/env python3
"""
Logo Color Palette Extractor for Perry Dime Website
Analyzes the logo PNG file and extracts primary and secondary colors
to create CSS variables for the site's theme.
"""

import sys
from pathlib import Path
from PIL import Image
from collections import Counter
import colorsys

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
LOGO_PATH = SCRIPT_DIR / "source/branding/perrydime-logo.png"
OUTPUT_CSS = SCRIPT_DIR / "docs/assets/css/variables.css"

def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color code."""
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def rgb_to_hsl(rgb):
    """Convert RGB to HSL."""
    r, g, b = [x / 255.0 for x in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return (int(h * 360), int(s * 100), int(l * 100))

def color_distance(c1, c2):
    """Calculate Euclidean distance between two RGB colors."""
    return sum((a - b) ** 2 for a, b in zip(c1, c2)) ** 0.5

def is_grayscale(rgb, threshold=15):
    """Check if a color is grayscale (low saturation)."""
    r, g, b = rgb
    return max(r, g, b) - min(r, g, b) < threshold

def get_luminance(rgb):
    """Calculate perceived luminance of a color."""
    r, g, b = [x / 255.0 for x in rgb]
    # Apply gamma correction
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def cluster_colors(colors, min_distance=30):
    """Cluster similar colors together."""
    if not colors:
        return []
    
    clusters = []
    for color, count in colors:
        # Find if this color belongs to an existing cluster
        found_cluster = False
        for cluster in clusters:
            if color_distance(color, cluster['representative']) < min_distance:
                cluster['colors'].append((color, count))
                cluster['total_count'] += count
                found_cluster = True
                break
        
        if not found_cluster:
            clusters.append({
                'representative': color,
                'colors': [(color, count)],
                'total_count': count
            })
    
    # Sort clusters by total count
    clusters.sort(key=lambda x: x['total_count'], reverse=True)
    
    # Calculate average color for each cluster
    for cluster in clusters:
        total_r = sum(c[0][0] * c[1] for c in cluster['colors'])
        total_g = sum(c[0][1] * c[1] for c in cluster['colors'])
        total_b = sum(c[0][2] * c[1] for c in cluster['colors'])
        total_count = cluster['total_count']
        
        cluster['average'] = (
            int(total_r / total_count),
            int(total_g / total_count),
            int(total_b / total_count)
        )
    
    return clusters

def extract_palette(image_path, num_colors=10):
    """Extract color palette from image."""
    print(f"Analyzing logo: {image_path}")
    
    # Open image
    img = Image.open(image_path)
    
    # Convert to RGB if necessary
    if img.mode != 'RGB':
        # Handle transparency
        if img.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
            img = background
        else:
            img = img.convert('RGB')
    
    # Resize for faster processing
    img.thumbnail((400, 400))
    
    print(f"Image size: {img.size}")
    
    # Get all colors
    colors = img.getcolors(img.size[0] * img.size[1])
    
    if not colors:
        print("ERROR: Could not extract colors from image")
        return None
    
    print(f"Found {len(colors)} unique colors")
    
    # Filter out near-white and near-black colors (likely background)
    filtered_colors = []
    for count, color in colors:
        if isinstance(color, int):
            color = (color, color, color)
        
        # Skip very light colors (near white)
        if all(c > 240 for c in color):
            continue
        # Skip very dark colors (near black) unless they're significant
        if all(c < 15 for c in color) and count < 100:
            continue
        
        filtered_colors.append((color, count))
    
    print(f"After filtering: {len(filtered_colors)} colors")
    
    # Cluster similar colors
    clusters = cluster_colors(filtered_colors, min_distance=40)
    
    print(f"Found {len(clusters)} color clusters")
    
    # Separate chromatic and grayscale colors
    chromatic = []
    grayscale = []
    
    for cluster in clusters:
        color = cluster['average']
        if is_grayscale(color):
            grayscale.append((color, cluster['total_count']))
        else:
            chromatic.append((color, cluster['total_count']))
    
    print(f"Chromatic colors: {len(chromatic)}")
    print(f"Grayscale colors: {len(grayscale)}")
    
    return {
        'chromatic': chromatic[:num_colors],
        'grayscale': grayscale[:num_colors],
        'all_clusters': clusters[:num_colors * 2]
    }

def generate_css_variables(palette):
    """Generate CSS variables from color palette."""
    
    lines = []
    lines.append("/**")
    lines.append(" * Perry Dime Website - Color Variables")
    lines.append(" * Extracted from perrydime-logo.png")
    lines.append(" * ")
    lines.append(" * This file defines the foundational color palette for the entire site,")
    lines.append(" * derived directly from the Perry Dime logo.")
    lines.append(" */")
    lines.append("")
    lines.append(":root {")
    lines.append("  /* PRIMARY COLORS (from logo) */")
    lines.append("")
    
    # Primary colors (chromatic)
    if palette['chromatic']:
        for i, (color, count) in enumerate(palette['chromatic'][:5], 1):
            hex_color = rgb_to_hex(color)
            h, s, l = rgb_to_hsl(color)
            lines.append(f"  --color-primary-{i}: {hex_color};")
            lines.append(f"  --color-primary-{i}-rgb: {color[0]}, {color[1]}, {color[2]};")
            lines.append(f"  --color-primary-{i}-hsl: {h}, {s}%, {l}%;")
            lines.append("")
    
    lines.append("  /* SECONDARY COLORS (grayscale from logo) */")
    lines.append("")
    
    # Secondary colors (grayscale)
    if palette['grayscale']:
        for i, (color, count) in enumerate(palette['grayscale'][:5], 1):
            hex_color = rgb_to_hex(color)
            h, s, l = rgb_to_hsl(color)
            lines.append(f"  --color-secondary-{i}: {hex_color};")
            lines.append(f"  --color-secondary-{i}-rgb: {color[0]}, {color[1]}, {color[2]};")
            lines.append(f"  --color-secondary-{i}-hsl: {h}, {s}%, {l}%;")
            lines.append("")
    
    # Semantic color assignments
    lines.append("  /* SEMANTIC COLOR ASSIGNMENTS */")
    lines.append("")
    
    if palette['chromatic']:
        primary = palette['chromatic'][0][0]
        lines.append("  --color-brand: var(--color-primary-1);")
        lines.append("  --color-accent: var(--color-primary-2);")
        
        # Determine if primary is light or dark
        if get_luminance(primary) > 0.5:
            lines.append("  --color-text-on-brand: #000000;")
        else:
            lines.append("  --color-text-on-brand: #ffffff;")
        lines.append("")
    
    # Add standard variables
    lines.append("  /* NEUTRAL COLORS */")
    lines.append("  --color-white: #ffffff;")
    lines.append("  --color-black: #000000;")
    lines.append("  --color-gray-light: #f5f5f5;")
    lines.append("  --color-gray-medium: #999999;")
    lines.append("  --color-gray-dark: #333333;")
    lines.append("")
    lines.append("  /* TEXT COLORS */")
    lines.append("  --color-text-primary: var(--color-secondary-1, #333333);")
    lines.append("  --color-text-secondary: var(--color-secondary-2, #666666);")
    lines.append("  --color-text-muted: var(--color-gray-medium);")
    lines.append("")
    lines.append("  /* BACKGROUND COLORS */")
    lines.append("  --color-bg-primary: var(--color-white);")
    lines.append("  --color-bg-secondary: var(--color-gray-light);")
    lines.append("  --color-bg-accent: var(--color-primary-1);")
    lines.append("")
    lines.append("  /* SPACING */")
    lines.append("  --spacing-xs: 0.25rem;")
    lines.append("  --spacing-sm: 0.5rem;")
    lines.append("  --spacing-md: 1rem;")
    lines.append("  --spacing-lg: 1.5rem;")
    lines.append("  --spacing-xl: 2rem;")
    lines.append("  --spacing-2xl: 3rem;")
    lines.append("")
    lines.append("  /* TYPOGRAPHY */")
    lines.append("  --font-family-primary: 'Georgia', 'Times New Roman', serif;")
    lines.append("  --font-family-secondary: 'Helvetica Neue', Arial, sans-serif;")
    lines.append("  --font-size-base: 1rem;")
    lines.append("  --font-size-lg: 1.25rem;")
    lines.append("  --font-size-xl: 1.5rem;")
    lines.append("  --font-size-2xl: 2rem;")
    lines.append("  --line-height-normal: 1.5;")
    lines.append("}")
    lines.append("")
    
    # Add color reference comments
    lines.append("/* EXTRACTED COLOR PALETTE:")
    lines.append(" * ")
    
    if palette['chromatic']:
        lines.append(" * PRIMARY (Chromatic) Colors:")
        for i, (color, count) in enumerate(palette['chromatic'][:5], 1):
            hex_color = rgb_to_hex(color)
            lines.append(f" *   {i}. {hex_color} - RGB({color[0]}, {color[1]}, {color[2]}) - {count} pixels")
    
    lines.append(" * ")
    
    if palette['grayscale']:
        lines.append(" * SECONDARY (Grayscale) Colors:")
        for i, (color, count) in enumerate(palette['grayscale'][:5], 1):
            hex_color = rgb_to_hex(color)
            lines.append(f" *   {i}. {hex_color} - RGB({color[0]}, {color[1]}, {color[2]}) - {count} pixels")
    
    lines.append(" */")
    
    return '\n'.join(lines)

def main():
    """Main execution."""
    print("=" * 70)
    print("Perry Dime Logo Color Palette Extractor")
    print("=" * 70)
    print()
    
    # Check if logo exists
    if not LOGO_PATH.exists():
        print(f"ERROR: Logo file not found: {LOGO_PATH}")
        sys.exit(1)
    
    # Extract palette
    palette = extract_palette(LOGO_PATH)
    
    if not palette:
        print("ERROR: Failed to extract color palette")
        sys.exit(1)
    
    # Display results
    print("\n" + "=" * 70)
    print("EXTRACTED COLOR PALETTE")
    print("=" * 70)
    
    if palette['chromatic']:
        print("\nPRIMARY (Chromatic) Colors:")
        for i, (color, count) in enumerate(palette['chromatic'][:5], 1):
            hex_color = rgb_to_hex(color)
            print(f"  {i}. {hex_color} - RGB{color} - {count} pixels")
    
    if palette['grayscale']:
        print("\nSECONDARY (Grayscale) Colors:")
        for i, (color, count) in enumerate(palette['grayscale'][:5], 1):
            hex_color = rgb_to_hex(color)
            print(f"  {i}. {hex_color} - RGB{color} - {count} pixels")
    
    # Generate CSS
    print("\n" + "=" * 70)
    print("GENERATING CSS VARIABLES")
    print("=" * 70)
    
    css_content = generate_css_variables(palette)
    
    # Ensure output directory exists
    OUTPUT_CSS.parent.mkdir(parents=True, exist_ok=True)
    
    # Write CSS file
    with open(OUTPUT_CSS, 'w') as f:
        f.write(css_content)
    
    print(f"\nCSS variables saved to: {OUTPUT_CSS}")
    print(f"File size: {OUTPUT_CSS.stat().st_size} bytes")
    
    print("\n" + "=" * 70)
    print("SUCCESS!")
    print("=" * 70)
    print("\nThe color palette has been extracted and saved as CSS variables.")
    print("These variables form the foundation of the site's visual theme.")

if __name__ == "__main__":
    main()
