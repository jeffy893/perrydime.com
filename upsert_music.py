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
AUDIO_DEST_ROOT = SCRIPT_DIR / "docs/assets/audio"
OUTPUT_FILE = SCRIPT_DIR / "docs/music.html"
TEMPLATE_FILE = SCRIPT_DIR / "docs/index.html"

# Tab configuration: (subfolder_name, tab_id, tab_label, tab_icon, html_filename_pattern)
TRACK_TABS = [
    ("Optionality Album", "optionality-album", "Optionality Album", "💿", "List-of-SoundCloud-Embed_Optionality.html"),
    ("Proofs of Concept", "proofs-of-concept", "Proofs of Concept", "🎵", "List-of-SoundCloud-Embed_Proofs.html"),
]

# Tabs built from local MP3 files: (subfolder_name, tab_id, tab_label, tab_icon)
# Files are named "NN_Artist_Track-Name.mp3": NN sets the order, and the text after
# "Artist_" (dashes replaced with spaces) is the displayed title.
AUDIO_TABS = [
    ("Christmas", "christmas", "Christmas", "🎄"),
]

# Optional intro block shown above a tab's grid (kept here so regeneration preserves it)
ALBUM_DESCRIPTIONS = {
    "optionality-album": """                    <div class="album-description" style="max-width: 760px; margin: 0 auto 2.5rem; padding: 1.75rem 2rem; border-left: 4px solid var(--accent-color, #ff5500); background: rgba(255, 85, 0, 0.04); border-radius: 0 8px 8px 0;">
                        <p style="margin: 0 0 0.35rem; font-size: 0.85rem; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.7;">Jan 2021 – Mar 2026</p>
                        <h3 style="margin: 0 0 0.75rem; font-size: 1.4rem;">Optionality: An Experimental Album</h3>
                        <p style="margin: 0 0 1rem; font-style: italic; opacity: 0.85;">An honest depiction of the Optionality differential and resultant adaptation with Usury.</p>
                        <p style="margin: 0; line-height: 1.7;">A four-year journey bridging written poetry and musical composition. Prototyped tracks with MIDI, Ableton, and vocal arrangements, then validated via SoundCloud engagement data. Used Zipf's Law distribution in listener behavior to select the top 11 tracks. Nested the lead track in raw form at the axis point while leveraging Suno AI for production—exploring human intent meets generative technology. With a kicker leaning into Uncle YahYoKah's grace.</p>
                    </div>""",
}


def load_audio_tabs():
    """Copy local MP3s to docs/assets/audio/<tab_id>/ and build tab data."""
    tabs = []
    for subfolder_name, tab_id, tab_label, tab_icon in AUDIO_TABS:
        src_dir = PRODUCTIONS_DIR / subfolder_name
        if not src_dir.exists():
            print(f"  Warning: {src_dir} not found, skipping")
            continue
        dest_dir = AUDIO_DEST_ROOT / tab_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        tracks = []
        for mp3 in sorted(src_dir.glob("[0-9][0-9]_*.mp3")):
            dest = dest_dir / mp3.name
            if not dest.exists() or dest.stat().st_size != mp3.stat().st_size:
                shutil.copy2(mp3, dest)
                print(f"  ✓ Copied: {mp3.name}")
            parts = mp3.stem.split('_', 2)
            number = parts[0]
            title = (parts[2] if len(parts) == 3 else parts[-1]).replace('-', ' ')
            tracks.append({
                'id': f"{tab_id}-{number}",
                'title': title,
                'full_embed': (
                    f'<audio controls preload="none">'
                    f'<source src="assets/audio/{tab_id}/{mp3.name}" type="audio/mpeg"/>'
                    f'Your browser does not support audio playback.</audio>'
                ),
            })
        print(f"  Found {len(tracks)} tracks in {subfolder_name}")
        tabs.append({'tab_id': tab_id, 'tab_label': tab_label, 'tab_icon': tab_icon, 'tracks': tracks})
    return tabs


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


# Melotations shown as on-page sheet music (SVG) with a playable MP3, generated
# by build_soul_beat.py: (folder name, title, description)
SCORE_MELOTATIONS = [
    ("artificial-intercourse", "Artificial_Intercourse", "Guitar music from the Survitality book."),
    ("natural-intercourse", "Natural_Intercourse", "Guitar music from the Survitality book."),
    ("shareholder-son", "Shareholder Son", "In a dream, I flew a spaceship past the lesser gods to Doc Zeus at the port of a goddess. While he courted, he asked me to take the helm. The chant: \"My shareholder son, I give my chair to you.\""),
    ("soul-beat", "Soul Beat", "The beat that has rested in my soul throughout my life. It comes out when I drum my hands on my chest, in bed or at my desk, while being skooled."),
]
SCORE_ASSET_DIR = "assets/melotations"


def build_score_cards():
    """Cards that display sheet music inline with an audio player."""
    cards = []
    for folder, title, description in SCORE_MELOTATIONS:
        base = SCRIPT_DIR / "docs" / SCORE_ASSET_DIR / folder
        svg, mp3 = base / f"{folder}.svg", base / f"{folder}.mp3"
        if not (svg.exists() and mp3.exists()):
            print(f"  Warning: score assets missing for {folder}, run build_soul_beat.py")
            continue
        cards.append(
            f'''                <div class="melotation-score">
                    <h4>{title}</h4>
                    <p>{description}</p>
                    <img src="{SCORE_ASSET_DIR}/{folder}/{folder}.svg" alt="Sheet music for {title}" loading="lazy"/>
                    <p class="melotation-score-hint">Press play to hear it rendered from the notation.</p>
                    <audio controls="" preload="none">
                        <source src="{SCORE_ASSET_DIR}/{folder}/{folder}.mp3" type="audio/mpeg"/>
                        Your browser does not support audio playback.
                    </audio>
                </div>''')
    return '\n'.join(cards)


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
{ALBUM_DESCRIPTIONS.get(tab['tab_id'], '')}
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
                        <span class="tab-count">{len(melotations) + len(SCORE_MELOTATIONS)}</span>
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
        score_cards = build_score_cards()
        tab_contents.append(
            f'''                <div class="music-tab-content" id="melotations-content">
                    <div class="melotations-grid">
{melotations_cards}
                    </div><!-- end melotations-grid -->
{score_cards}
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
    print("\n   Reading local MP3 albums...")
    track_tabs += load_audio_tabs()

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
