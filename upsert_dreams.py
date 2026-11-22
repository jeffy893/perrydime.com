#!/usr/bin/env python3.10
"""
Dreams Page Generator for Perry Dime Website
Scans source/dreams/ for PDF files and generates dreams.html
"""

import shutil
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

# Paths
BASE_DIR = Path(__file__).parent
DREAMS_DIR = BASE_DIR / "source/dreams"
OUTPUT_FILE = BASE_DIR / "docs/dreams.html"
TEMPLATE_FILE = BASE_DIR / "docs/music.html"
PDF_DEST_DIR = BASE_DIR / "docs/assets/pdfs/dreams"


# Dream art: compressed JPGs (full + thumbnail) are generated from source/dreams/dream-art
ART_SRC_DIR = BASE_DIR / "source/dreams/dream-art"
ART_DEST_DIR = BASE_DIR / "docs/assets/img/dreams"

ALLEGORIES_TABS_HTML = """
<div class="art-tabs">
  <a class="art-tab allegories-tab" href="https://wiki.richards.systems/pages/Allegories_17760257.html" target="_blank" rel="noopener">
    <span class="tab-icon">📜</span>
    <span class="tab-label">Allegories</span>
    <span class="tab-count">↗</span>
  </a>
</div>
"""

DREAM_STORY_HTML = """
<article class="dream-story-panel">
  <h3 class="dream-story-title">2014 Cosmos Introduction</h3>
  <p class="dream-story-meta">Yuma, AZ · 2014</p>
  <figure class="dream-story-figure">
    <img src="assets/img/dreams/alien-librarian.jpg" alt="The alien librarian" loading="lazy"/>
  </figure>
  <p>I spent a week in the summer sun bathing with no clothes, fasting from food, but staying hydrated.</p>
  <p>On the seventh day, I drove out to the remote parts of the Colorado River, and hiked through a wash till finding a suitable hill.</p>
  <p>My cousin had told me to not stay in one place too long, or the scorpions would be attracted to my heat.</p>
  <p>I meditated, cross-legged, looking straight up into the cosmos, until the cosmos recognized me.</p>
  <p>A giant white moth flew up to me. A burro whinnied in the distance.</p>
  <p>Amongst the most fear and awe I had ever felt, I fell asleep:</p>
  <blockquote>In my dream, I sat as a tiny man, swinging my feet on a tiny ledge in a giant library with a giant and long-bodied alien librarian. The librarian brought a book down to my face - from which I could only make out one line. This one line that I read from the alien language, I was told, would take books and books of english mathematics and artificial computer languages to spell out.</blockquote>
  <p>I woke abruptly, and knew my introduction was complete…</p>
  <p>When back down in the wash, headed towards my car, I turned around, and my headlamp lit up ~20 eyes of coyotes… I quickened my pace, while rotating, to validate I was staying ahead of the approaching eyes.</p>
  <p>I made it to the car, drove home, had a sandwich,…, and went to bed.</p>
</article>
"""


def append_html(parent, html):
    """Parse an HTML fragment and append its nodes to parent"""
    for el in list(BeautifulSoup(html, 'html.parser').contents):
        parent.append(el)


def scan_dream_art():
    """Compress dream art PNGs to JPG (full + thumb) and return entries"""
    from PIL import Image
    items = []
    if not ART_SRC_DIR.exists():
        return items
    ART_DEST_DIR.mkdir(parents=True, exist_ok=True)
    for src in sorted(ART_SRC_DIR.glob("*.png")):
        full = ART_DEST_DIR / f"{src.stem}.jpg"
        thumb = ART_DEST_DIR / f"{src.stem}-thumb.jpg"
        if not full.exists() or full.stat().st_mtime < src.stat().st_mtime:
            im = Image.open(src).convert("RGB")
            for dest, size, quality in ((full, 1800, 82), (thumb, 800, 80)):
                c = im.copy()
                c.thumbnail((size, size), Image.LANCZOS)
                c.save(dest, "JPEG", quality=quality, optimize=True, progressive=True)
        items.append({'title': src.stem.replace('-', ' ').title(), 'stem': src.stem})
        print(f"  ✓ Dream art: {src.name}")
    return items


def dream_art_item_html(art):
    return (
        f'<figure class="dream-art-item">'
        f'<a class="art-link" data-title="{art["title"]}" href="assets/img/dreams/{art["stem"]}.jpg">'
        f'<img alt="{art["title"]}" loading="lazy" src="assets/img/dreams/{art["stem"]}-thumb.jpg"/>'
        f'</a><figcaption>{art["title"]}</figcaption></figure>'
    )


def parse_dream_filename(filename):
    """Parse dream PDF filename to extract date and title"""
    # Expected format: YYYY-MM-DD_Title_With_Underscores.pdf
    stem = filename.stem
    
    # Try to extract date (YYYY-MM-DD)
    parts = stem.split('_', 3)
    if len(parts) >= 2:
        date_str = parts[0]
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            date_display = date_obj.strftime('%B %d, %Y')
        except:
            date_display = date_str
        
        # Extract title (remaining parts after date)
        if len(parts) >= 2:
            title_parts = parts[1:]
            title = ' '.join(title_parts).replace('_', ' ')
        else:
            title = stem.replace('_', ' ')
    else:
        date_display = ''
        title = stem.replace('_', ' ')
    
    return {
        'title': title,
        'date': date_display,
        'filename': filename.name
    }

def scan_dreams():
    """Scan dreams directory for PDF files"""
    dreams = []
    
    if not DREAMS_DIR.exists():
        print(f"Warning: {DREAMS_DIR} not found")
        return dreams
    
    # Find all PDF files
    pdf_files = sorted(DREAMS_DIR.glob("*.pdf"), reverse=True)  # Most recent first
    
    for pdf_file in pdf_files:
        dream_info = parse_dream_filename(pdf_file)
        
        # Copy PDF to destination
        PDF_DEST_DIR.mkdir(parents=True, exist_ok=True)
        dest_file = PDF_DEST_DIR / pdf_file.name
        shutil.copy(pdf_file, dest_file)
        
        dream_info['pdf_path'] = f"assets/pdfs/dreams/{pdf_file.name}"
        dreams.append(dream_info)
        
        print(f"  ✓ Copied: {pdf_file.name}")
    
    return dreams

def generate_dreams_html(dreams):
    """Generate dreams.html with dream entries"""
    
    # Read template
    if not TEMPLATE_FILE.exists():
        print(f"Error: Template file {TEMPLATE_FILE} not found")
        return
    
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Update page title
    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = "Dreams | Perry Dime"
    
    # Update hero section
    hero = soup.find('section', class_='hero')
    if hero:
        hero_h2 = hero.find('h2')
        if hero_h2:
            hero_h2.string = "Dreams"
        hero_p = hero.find('p', class_='lead')
        if hero_p:
            hero_p.string = "Handwritten dream journals and reflections."
    
    # Update navigation active state
    nav_links = soup.find_all('a', href='music.html')
    for link in nav_links:
        if 'active' in link.get('class', []):
            link['class'].remove('active')
    
    dreams_links = soup.find_all('a', href='dreams.html')
    for link in dreams_links:
        classes = link.get('class', [])
        if 'active' not in classes:
            classes.append('active')
        link['class'] = classes
    
    # Find the music section to replace
    music_section = soup.find('section', class_='music-section')
    if not music_section:
        print("Error: Could not find music-section to replace")
        return
    
    # Clear and update section
    music_section['class'] = ['dreams-section']
    container = music_section.find('div', class_='container')
    if container:
        container.clear()
    else:
        container = soup.new_tag('div', **{'class': 'container'})
        music_section.append(container)
    
    # Intro
    intro_h2 = soup.new_tag('h2')
    intro_h2.string = "Dreams"
    container.append(intro_h2)

    intro_p = soup.new_tag('p', **{'class': 'section-intro'})
    intro_p.string = "Dream stories, dream art, and handwritten dream journals documenting the subconscious narrative."
    container.append(intro_p)

    # Allegories link, styled like the tabs on other pages
    append_html(container, ALLEGORIES_TABS_HTML)

    # Dream story panel
    append_html(container, DREAM_STORY_HTML)

    # Dream art gallery
    art_h2 = soup.new_tag('h2', **{'class': 'dream-subhead'})
    art_h2.string = "Dream Art"
    container.append(art_h2)
    art_gallery = soup.new_tag('div', **{'class': 'dream-art-gallery'})
    for art in scan_dream_art():
        append_html(art_gallery, dream_art_item_html(art))
    container.append(art_gallery)

    # Dream journals go last
    journals_h2 = soup.new_tag('h2', **{'class': 'dream-subhead'})
    journals_h2.string = "Dream Journals"
    container.append(journals_h2)

    journals_p = soup.new_tag('p', **{'class': 'section-intro'})
    journals_p.string = "A collection of handwritten dream descriptions and reflections."
    container.append(journals_p)

    dreams_grid = soup.new_tag('div', **{'class': 'dreams-grid'})
    for dream in dreams:
        dreams_grid.append(create_dream_card(soup, dream))
    container.append(dreams_grid)

    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    
    print(f"✓ Generated {OUTPUT_FILE}")
    print(f"  - Dreams: {len(dreams)} entries")

def create_dream_card(soup, dream):
    """Create a dream card element"""
    card = soup.new_tag('div', **{'class': 'dream-card'})
    
    # Icon/Visual element
    icon_div = soup.new_tag('div', **{'class': 'dream-icon'})
    icon_svg = soup.new_tag('svg', xmlns='http://www.w3.org/2000/svg', 
                            width='48', height='48', viewBox='0 0 24 24', 
                            fill='none', stroke='currentColor', 
                            **{'stroke-width': '2', 'stroke-linecap': 'round', 
                               'stroke-linejoin': 'round'})
    # Moon icon
    path1 = soup.new_tag('path', d='M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z')
    icon_svg.append(path1)
    icon_div.append(icon_svg)
    card.append(icon_div)
    
    # Content
    content_div = soup.new_tag('div', **{'class': 'dream-content'})
    
    # Title
    title_h3 = soup.new_tag('h3')
    title_h3.string = dream['title']
    content_div.append(title_h3)
    
    # Date
    if dream['date']:
        date_p = soup.new_tag('p', **{'class': 'dream-date'})
        date_p.string = dream['date']
        content_div.append(date_p)
    
    # View button
    link_div = soup.new_tag('div', **{'class': 'dream-link'})
    pdf_link = soup.new_tag('a', href=dream['pdf_path'], target='_blank', 
                            **{'class': 'dream-button'})
    pdf_link.string = "View Dream Journal"
    link_div.append(pdf_link)
    content_div.append(link_div)
    
    card.append(content_div)
    
    return card

def main():
    print("=" * 70)
    print("Perry Dime Dreams Generator")
    print("=" * 70)
    
    # Scan dreams directory
    print("\n1. Scanning dreams directory...")
    dreams = scan_dreams()
    
    if not dreams:
        print("No dreams found!")
        return
    
    # Generate HTML
    print("\n2. Generating dreams.html...")
    generate_dreams_html(dreams)
    
    print("\n" + "=" * 70)
    print("Dreams generation complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
