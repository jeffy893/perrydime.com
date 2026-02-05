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
    
    # Add intro
    intro_h2 = soup.new_tag('h2')
    intro_h2.string = "Dream Journals"
    container.append(intro_h2)
    
    intro_p = soup.new_tag('p', **{'class': 'section-intro'})
    intro_p.string = "A collection of handwritten dream descriptions and reflections, documenting the subconscious narrative."
    container.append(intro_p)
    
    # Generate dreams grid
    dreams_grid = soup.new_tag('div', **{'class': 'dreams-grid'})
    
    for dream in dreams:
        dream_card = create_dream_card(soup, dream)
        dreams_grid.append(dream_card)
    
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
