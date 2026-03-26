#!/usr/bin/env python3.10
"""
Music Page Upsert Script for Perry Dime Website
Reads SoundCloud embeds from source/productions subfolders and melotations PDFs
Generates music.html with Optionality Album, Proofs of Concept, and Melotations tabs
"""

import re
import shutil
from pathlib import Path
from bs4 import BeautifulSoup

# Configuration
SCRIPT_DIR = Path(__file__).parent.resolve()
PRODUCTIONS_DIR = SCRIPT_DIR / "source/productions"
MELOTATIONS_SOURCE = SCRIPT_DIR / "source/productions-melotations"
MELOTATIONS_DEST = SCRIPT_DIR / "docs/assets/pdfs/melotations"
OUTPUT_FILE = SCRIPT_DIR / "docs/music.html"
TEMPLATE_FILE = SCRIPT_DIR / "docs/index.html"

# Tab configuration: (subfolder_name, tab_id, tab_label, tab_icon, html_filename_pattern)
TRACK_TABS = [
    ("Optionality Album", "optionality-album", "Optionality Album", "💿", "List-of-SoundCloud-Embed_Optionality.html"),
    ("Proofs of Concept", "proofs-of-concept", "Proofs of Concept", "🎵", "List-of-SoundCloud-Embed_Proofs.html"),
]

def copy_melotations():
    """Copy melotation PDFs from source to docs"""
    if not MELOTATIONS_SOURCE.exists():
        print(f"Warning: {MELOTATIONS_SOURCE} does not exist")
        return []

    MELOTATIONS_DEST.mkdir(parents=True, exist_ok=True)

    copied_count = 0
    skipped_count = 0
    melotations = []

    for pdf_file in sorted(MELOTATIONS_SOURCE.glob("*.pdf")):
        dest_file = MELOTATIONS_DEST / pdf_file.name
        title = pdf_file.stem
        title = re.sub(r'^\d{4}-\d{2}-\d{2}_', '', title)
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
    iframes = re.findall(r'<iframe[^>]*src="([^"]*)"[^>]*></iframe>', embed_html)
    titles = re.findall(r'title="([^"]*)"[^>]*style="color: #cccccc; text-decoration: none;">([^<]*)</a></div>', embed_html)

    for i, iframe_src in enumerate(iframes):
        track_id_match = re.search(r'tracks%253A(\d+)', iframe_src)
        if track_id_match:
            track_id = track_id_match.group(1)
            title = "Unknown Track"
            if i < len(titles):
                title = titles[i][1] if len(titles[i]) > 1 else titles[i][0]
            tracks.append({
                'id': track_id,
                'title': title,
                'embed_src': iframe_src,
                'full_embed': f'<iframe width="100%" height="300" scrolling="no" frameborder="no" allow="autoplay" src="{iframe_src}"></iframe>'
            })
    return tracks


def load_tracks_from_subfolders():
    """Load tracks from each subfolder in source/productions."""
    all_tabs = []
    for subfolder_name, tab_id, tab_label, tab_icon, html_filename in TRACK_TABS:
        source_file = PRODUCTIONS_DIR / subfolder_name / html_filename
        if not source_file.exists():
            print(f"  Warning: {source_file} not found, skipping")
            continue
        with open(source_file, 'r', encoding='utf-8') as f:
            source_html = f.read()
        tracks = extract_track_info(source_html)
        print(f"  Found {len(tracks)} tracks in {subfolder_name}")
        all_tabs.append({
            'tab_id': tab_id,
            'tab_label': tab_label,
            'tab_icon': tab_icon,
            'tracks': tracks,
        })
    return all_tabs


def create_music_page(track_tabs, melotations, template_file, output_file):
    """Create or update the music.html page with tabs."""
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()

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

    main_tag = soup.find('main')
    if main_tag:
        # Build tab buttons HTML
        tab_buttons = []
        tab_contents = []
        first = True
        for tab in track_tabs:
            active_class = ' active' if first else ''
            tab_buttons.append(
                f'''                    <button class="music-tab{active_class}" data-tab="{tab['tab_id']}">
                        <span class="tab-icon">{tab['tab_icon']}</span>
                        <span class="tab-label">{tab['tab_label']}</span>
                        <span class="tab-count">{len(tab['tracks'])}</span>
                    </button>'''
            )
            tracks_embeds = '\n'.join([
                f'''                <div class="music-item" data-track-id="{track['id']}">
                    {track['full_embed']}
                    <div class="music-info">
                        <h3>{track['title']}</h3>
                    </div>
                </div>''' for track in tab['tracks']
            ])
            tab_contents.append(
                f'''                <div class="music-tab-content{active_class}" id="{tab['tab_id']}-content">
                    <div class="music-grid">
{tracks_embeds}
                    </div><!-- end music-grid -->
                </div>'''
            )
            first = False

        # Melotations tab button
        tab_buttons.append(
            f'''                    <button class="music-tab" data-tab="melotations">
                        <span class="tab-icon">🎼</span>
                        <span class="tab-label">Melotations</span>
                        <span class="tab-count">{len(melotations)}</span>
                    </button>'''
        )

        # Melotations tab content
        melotations_cards = '\n'.join([
            f'''                <div class="melotation-card">
                    <div class="melotation-icon">🎼</div>
                    <div class="melotation-content">
                        <h4>{melotation['title']}</h4>
                        <a href="{melotation['path']}" target="_blank" class="melotation-link">View Sheet Music (PDF)</a>
                    </div>
                </div>''' for melotation in melotations
        ])
        tab_contents.append(
            f'''                <div class="music-tab-content" id="melotations-content">
                    <div class="melotations-grid">
{melotations_cards}
                    </div><!-- end melotations-grid -->
                </div>'''
        )

        tab_buttons_html = '\n'.join(tab_buttons)
        tab_contents_html = '\n'.join(tab_contents)

        total_tracks = sum(len(t['tracks']) for t in track_tabs)

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
{tab_buttons_html}
                </div>
                
                <!-- Tab Contents -->
{tab_contents_html}
            </div>
        </section>
'''
        main_tag.clear()
        main_tag.append(BeautifulSoup(new_main, 'html.parser'))

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))

    total_tracks = sum(len(t['tracks']) for t in track_tabs)
    return total_tracks, len(melotations)


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

    # Load tracks from subfolders
    print(f"\n2. Reading SoundCloud embeds from subfolders in: {PRODUCTIONS_DIR}")
    track_tabs = load_tracks_from_subfolders()

    if not track_tabs:
        print("No track tabs found!")
        return

    # Display tracks per tab
    for tab in track_tabs:
        print(f"\n  {tab['tab_label']}:")
        for i, track in enumerate(tab['tracks'], 1):
            print(f"    {i}. {track['title']} (ID: {track['id']})")

    if melotations:
        print("\n  Melotations:")
        for i, m in enumerate(melotations, 1):
            print(f"    {i}. {m['title']}")

    # Create music page
    print(f"\n3. Generating music page: {OUTPUT_FILE}")
    tracks_count, melotations_count = create_music_page(track_tabs, melotations, TEMPLATE_FILE, OUTPUT_FILE)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total tracks: {tracks_count}")
    print(f"Total melotations: {melotations_count}")
    print(f"Tabs: {', '.join(t['tab_label'] for t in track_tabs)} + Melotations")
    print(f"Output file: {OUTPUT_FILE}")
    print("=" * 70)


if __name__ == "__main__":
    main()
