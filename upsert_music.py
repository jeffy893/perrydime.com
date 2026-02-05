#!/usr/bin/env python3.10
"""
Music Page Upsert Script for Perry Dime Website
Reads SoundCloud embeds from source and melotations PDFs
Generates music.html with Tracks and Melotations tabs
"""

import re
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
SOURCE_FILE = SCRIPT_DIR / "source/productions/List-of-SoundCloud-Embed.html"
MELOTATIONS_SOURCE = SCRIPT_DIR / "source/productions-melotations"
MELOTATIONS_DEST = SCRIPT_DIR / "docs/assets/pdfs/melotations"
OUTPUT_FILE = SCRIPT_DIR / "docs/music.html"
TEMPLATE_FILE = SCRIPT_DIR / "docs/index.html"

def copy_melotations():
    """Copy melotation PDFs from source to docs"""
    if not MELOTATIONS_SOURCE.exists():
        print(f"Warning: {MELOTATIONS_SOURCE} does not exist")
        return []
    
    # Create destination directory if it doesn't exist
    MELOTATIONS_DEST.mkdir(parents=True, exist_ok=True)
    
    copied_count = 0
    skipped_count = 0
    melotations = []
    
    # Copy PDF files
    for pdf_file in sorted(MELOTATIONS_SOURCE.glob("*.pdf")):
        dest_file = MELOTATIONS_DEST / pdf_file.name
        
        # Extract title from filename (remove date prefix if present)
        title = pdf_file.stem
        # Remove date prefix pattern like "2024-05-11_"
        title = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', title)
        # Replace underscores and hyphens with spaces
        title = title.replace('_', ' ').replace('-', ' ')
        
        if not dest_file.exists():
            shutil.copy2(pdf_file, dest_file)
            print(f"  ✓ Copied: {pdf_file.name}")
            copied_count += 1
        else:
            skipped_count += 1
        
        melotations.append({
            'filename': pdf_file.name,
            'title': title,
            'path': f"assets/pdfs/melotations/{pdf_file.name}"
        })
    
    print(f"\n  Melotations copied: {copied_count}")
    print(f"  Melotations skipped (already exist): {skipped_count}")
    
    return melotations

def extract_track_info(embed_html):
    """Extract track information from SoundCloud embed HTML."""
    tracks = []
    
    # Split by iframe tags
    iframes = re.findall(r'<iframe[^>]*src="([^"]*)"[^>]*></iframe>', embed_html)
    titles = re.findall(r'title="([^"]*)"[^>]*style="color: #cccccc; text-decoration: none;">([^<]*)</a></div>', embed_html)
    
    # Extract track IDs and titles
    for i, iframe_src in enumerate(iframes):
        # Extract track ID from URL
        track_id_match = re.search(r'tracks%253A(\d+)', iframe_src)
        if track_id_match:
            track_id = track_id_match.group(1)
            
            # Find corresponding title
            title = "Unknown Track"
            if i < len(titles):
                # titles[i] is a tuple: (artist_title, track_title)
                title = titles[i][1] if len(titles[i]) > 1 else titles[i][0]
            
            tracks.append({
                'id': track_id,
                'title': title,
                'embed_src': iframe_src,
                'full_embed': f'<iframe width="100%" height="300" scrolling="no" frameborder="no" allow="autoplay" src="{iframe_src}"></iframe>'
            })
    
    return tracks

def create_music_page(tracks, melotations, template_file, output_file):
    """Create or update the music.html page with tabs."""
    
    # Always regenerate from template for tab structure
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Replace title and content
    soup = BeautifulSoup(template, 'html.parser')
    
    # Update title
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = "Music | Perry Dime"
    
    # Update active nav link
    nav_links = soup.find_all('a', href=True)
    for link in nav_links:
        if 'index.html' in link.get('href', ''):
            classes = link.get('class', [])
            if 'active' in classes:
                classes.remove('active')
            link['class'] = classes
        if 'music.html' in link.get('href', ''):
            classes = link.get('class', [])
            if 'active' not in classes:
                classes.append('active')
            link['class'] = classes
    
    # Replace main content
    main_tag = soup.find('main')
    if main_tag:
        # Create tracks embeds HTML
        tracks_embeds = '\n'.join([
            f'''                <div class="music-item" data-track-id="{track['id']}">
                    {track['full_embed']}
                    <div class="music-info">
                        <h3>{track['title']}</h3>
                    </div>
                </div>''' for track in tracks
        ])
        
        # Create melotations cards HTML
        melotations_cards = '\n'.join([
            f'''                <div class="melotation-card">
                    <div class="melotation-icon">🎼</div>
                    <div class="melotation-content">
                        <h4>{melotation['title']}</h4>
                        <a href="{melotation['path']}" target="_blank" class="melotation-link">View Sheet Music (PDF)</a>
                    </div>
                </div>''' for melotation in melotations
        ])
        
        new_main = f'''
        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-content">
                <h2>Music</h2>
                <p class="lead">Musical compositions and sonic explorations by Perry Dime.</p>
            </div>
        </section>

        <!-- Music Section with Tabs -->
        <section class="music-section">
            <div class="container">
                <h2>Musical Works</h2>
                <p class="section-intro">Listen to original tracks and explore musical notation.</p>
                
                <!-- Tab Navigation -->
                <div class="music-tabs">
                    <button class="music-tab active" data-tab="tracks">
                        <span class="tab-icon">🎵</span>
                        <span class="tab-label">Tracks</span>
                        <span class="tab-count">{len(tracks)}</span>
                    </button>
                    <button class="music-tab" data-tab="melotations">
                        <span class="tab-icon">🎼</span>
                        <span class="tab-label">Melotations</span>
                        <span class="tab-count">{len(melotations)}</span>
                    </button>
                </div>
                
                <!-- Tracks Tab Content -->
                <div class="music-tab-content active" id="tracks-content">
                    <div class="music-grid">
{tracks_embeds}
                    </div><!-- end music-grid -->
                </div>
                
                <!-- Melotations Tab Content -->
                <div class="music-tab-content" id="melotations-content">
                    <div class="melotations-grid">
{melotations_cards}
                    </div><!-- end melotations-grid -->
                </div>
            </div>
        </section>
'''
        main_tag.clear()
        main_tag.append(BeautifulSoup(new_main, 'html.parser'))
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    return len(tracks), len(melotations)

def main():
    """Main execution."""
    print("=" * 70)
    print("Perry Dime Music Page Upsert")
    print("=" * 70)
    print()
    
    # Copy melotations PDFs
    print("1. Copying melotations PDFs from source...")
    melotations = copy_melotations()
    print(f"Found {len(melotations)} melotations")
    
    # Check if source file exists
    if not SOURCE_FILE.exists():
        print(f"ERROR: Source file not found: {SOURCE_FILE}")
        return
    
    # Read source file
    print(f"\n2. Reading SoundCloud embeds from: {SOURCE_FILE}")
    with open(SOURCE_FILE, 'r', encoding='utf-8') as f:
        source_html = f.read()
    
    # Extract track information
    tracks = extract_track_info(source_html)
    print(f"Found {len(tracks)} tracks in source file")
    
    if not tracks:
        print("No tracks found!")
        return
    
    # Display tracks
    print("\nTracks found:")
    for i, track in enumerate(tracks, 1):
        print(f"  {i}. {track['title']} (ID: {track['id']})")
    
    # Display melotations
    if melotations:
        print("\nMelotations found:")
        for i, melotation in enumerate(melotations, 1):
            print(f"  {i}. {melotation['title']}")
    
    # Create or update music page
    print(f"\n3. Generating music page: {OUTPUT_FILE}")
    tracks_count, melotations_count = create_music_page(tracks, melotations, TEMPLATE_FILE, OUTPUT_FILE)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total tracks: {tracks_count}")
    print(f"Total melotations: {melotations_count}")
    print(f"Output file: {OUTPUT_FILE}")
    print("=" * 70)

if __name__ == "__main__":
    main()
