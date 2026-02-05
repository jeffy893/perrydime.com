#!/usr/bin/env python3.10
"""
Art Gallery Page Generator for Perry Dime Website
Scans source/art/ directory, copies images to docs/assets/img/art/, and generates art.html with tabs
"""

import os
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

# Paths
SOURCE_ART_DIR = Path("source/art")
DEST_ART_DIR = Path("docs/assets/img/art")
OUTPUT_FILE = Path("docs/art.html")
TEMPLATE_FILE = Path("docs/music.html")  # Use music.html as template

def copy_art_files():
    """Copy art files from source to docs, preserving directory structure"""
    if not SOURCE_ART_DIR.exists():
        print(f"Warning: {SOURCE_ART_DIR} does not exist")
        return
    
    # Create destination directory if it doesn't exist
    DEST_ART_DIR.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    skipped_count = 0
    
    # Copy root level images
    for item in SOURCE_ART_DIR.iterdir():
        if item.is_file() and item.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
            dest_file = DEST_ART_DIR / item.name
            if not dest_file.exists():
                shutil.copy2(item, dest_file)
                print(f"  ✓ Copied: {item.name}")
                copied_count += 1
            else:
                skipped_count += 1
    
    # Copy subfolder images
    for subfolder in SOURCE_ART_DIR.iterdir():
        if subfolder.is_dir():
            dest_subfolder = DEST_ART_DIR / subfolder.name
            dest_subfolder.mkdir(parents=True, exist_ok=True)
            
            for img in subfolder.iterdir():
                if img.is_file() and img.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                    dest_file = dest_subfolder / img.name
                    if not dest_file.exists():
                        shutil.copy2(img, dest_file)
                        print(f"  ✓ Copied: {subfolder.name}/{img.name}")
                        copied_count += 1
                    else:
                        skipped_count += 1
    
    print(f"\n  Files copied: {copied_count}")
    print(f"  Files skipped (already exist): {skipped_count}")

def scan_art_directory():
    """Scan art directory and organize images by folder"""
    art_structure = {
        'root': [],
        'subfolders': {}
    }
    
    if not DEST_ART_DIR.exists():
        print(f"Error: {DEST_ART_DIR} does not exist")
        return art_structure
    
    # Get all items in art directory
    for item in sorted(DEST_ART_DIR.iterdir()):
        if item.is_file() and item.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
            # Root level image
            art_structure['root'].append({
                'filename': item.name,
                'path': f"assets/img/art/{item.name}",
                'title': item.stem.replace('_', ' ').replace('-', ' ')
            })
        elif item.is_dir():
            # Subfolder
            folder_name = item.name
            art_structure['subfolders'][folder_name] = []
            
            # Get images in subfolder
            for img in sorted(item.iterdir()):
                if img.is_file() and img.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']:
                    art_structure['subfolders'][folder_name].append({
                        'filename': img.name,
                        'path': f"assets/img/art/{folder_name}/{img.name}",
                        'title': img.stem.replace('_', ' ').replace('-', ' ')
                    })
    
    return art_structure

def format_folder_name(folder_name):
    """Convert folder name to display title"""
    # Replace underscores with spaces
    title = folder_name.replace('_', ' ')
    # Capitalize each word
    return title.title()

def create_gallery_grid(soup, images):
    """Create a gallery grid with art items"""
    gallery_grid = soup.new_tag('div', **{'class': 'art-gallery'})
    
    for img_data in images:
        # Gallery item
        item = soup.new_tag('div', **{'class': 'art-item'})
        
        # Image link (for lightbox)
        link = soup.new_tag('a', href=img_data['path'], **{
            'class': 'art-link',
            'data-title': img_data['title']
        })
        
        # Image
        img = soup.new_tag('img', src=img_data['path'], alt=img_data['title'], loading='lazy')
        link.append(img)
        
        # Overlay
        overlay = soup.new_tag('div', **{'class': 'art-overlay'})
        overlay_title = soup.new_tag('span', **{'class': 'art-title'})
        overlay_title.string = img_data['title']
        overlay.append(overlay_title)
        link.append(overlay)
        
        item.append(link)
        gallery_grid.append(item)
    
    return gallery_grid

def generate_art_html(art_structure):
    """Generate art.html with tabbed gallery sections"""
    
    # Read template
    if TEMPLATE_FILE.exists():
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
    else:
        print(f"Error: Template file {TEMPLATE_FILE} not found")
        return
    
    # Update page title
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = "Art | Perry Dime"
    
    # Update hero section
    hero = soup.find('section', class_='hero')
    if hero:
        hero_h2 = hero.find('h2')
        if hero_h2:
            hero_h2.string = "Art"
        hero_p = hero.find('p', class_='lead')
        if hero_p:
            hero_p.string = "Visual artwork, paintings, and creative explorations by Perry Dime."
    
    # Update navigation active state
    nav_links = soup.find_all('a', href='music.html')
    for link in nav_links:
        if 'active' in link.get('class', []):
            link['class'].remove('active')
    
    art_links = soup.find_all('a', href='art.html')
    for link in art_links:
        classes = link.get('class', [])
        if 'active' not in classes:
            classes.append('active')
        link['class'] = classes
    
    # Find the music section to replace with art galleries
    music_section = soup.find('section', class_='music-section')
    if not music_section:
        print("Error: Could not find music-section to replace")
        return
    
    # Clear the music section content
    music_section['class'] = ['art-section']
    container = music_section.find('div', class_='container')
    if container:
        container.clear()
    else:
        container = soup.new_tag('div', **{'class': 'container'})
        music_section.append(container)
    
    # Add intro
    intro_h2 = soup.new_tag('h2')
    intro_h2.string = "Gallery"
    container.append(intro_h2)
    
    intro_p = soup.new_tag('p', **{'class': 'section-intro'})
    intro_p.string = "A collection of visual artwork, paintings, and creative explorations."
    container.append(intro_p)
    
    # Create tab navigation
    tab_nav = soup.new_tag('div', **{'class': 'art-tabs'})
    
    # Prepare tab data
    tabs = []
    
    # General Collection tab (root images)
    if art_structure['root']:
        tabs.append({
            'id': 'general',
            'label': 'General Collection',
            'icon': '🎨',
            'count': len(art_structure['root']),
            'images': art_structure['root']
        })
    
    # Subfolder tabs
    for folder_name, images in sorted(art_structure['subfolders'].items()):
        if images:
            # Determine icon based on folder name
            icon = '🖼️'
            if 'female' in folder_name.lower():
                icon = '👤'
            elif 'home' in folder_name.lower():
                icon = '🏠'
            
            tabs.append({
                'id': folder_name.lower().replace('_', '-').replace(' ', '-'),
                'label': format_folder_name(folder_name),
                'icon': icon,
                'count': len(images),
                'images': images
            })
    
    # Create tab buttons
    for i, tab in enumerate(tabs):
        tab_button = soup.new_tag('button', **{
            'class': 'art-tab' + (' active' if i == 0 else ''),
            'data-tab': tab['id']
        })
        
        # Icon
        tab_icon = soup.new_tag('span', **{'class': 'tab-icon'})
        tab_icon.string = tab['icon']
        tab_button.append(tab_icon)
        
        # Label
        tab_label = soup.new_tag('span', **{'class': 'tab-label'})
        tab_label.string = tab['label']
        tab_button.append(tab_label)
        
        # Count
        tab_count = soup.new_tag('span', **{'class': 'tab-count'})
        tab_count.string = str(tab['count'])
        tab_button.append(tab_count)
        
        tab_nav.append(tab_button)
    
    container.append(tab_nav)
    
    # Create tab content sections
    total_images = 0
    for i, tab in enumerate(tabs):
        total_images += tab['count']
        
        # Tab content wrapper
        tab_content = soup.new_tag('div', **{
            'class': 'art-tab-content' + (' active' if i == 0 else ''),
            'id': f"{tab['id']}-content"
        })
        
        # Gallery grid
        gallery_grid = create_gallery_grid(soup, tab['images'])
        tab_content.append(gallery_grid)
        
        container.append(tab_content)
    
    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    
    print(f"✓ Generated {OUTPUT_FILE}")
    print(f"  - Total images: {total_images}")
    print(f"  - Tabs created: {len(tabs)}")
    for tab in tabs:
        print(f"    • {tab['label']}: {tab['count']} images")

def main():
    print("=" * 70)
    print("Perry Dime Art Gallery Generator")
    print("=" * 70)
    
    # Copy art files from source to docs
    print("\n1. Copying art files from source to docs...")
    copy_art_files()
    
    # Scan art directory
    print("\n2. Scanning art directory...")
    art_structure = scan_art_directory()
    
    # Generate HTML
    print("\n3. Generating art.html...")
    generate_art_html(art_structure)
    
    print("\n" + "=" * 70)
    print("Art gallery generation complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
