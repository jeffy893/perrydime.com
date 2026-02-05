#!/usr/bin/env python3.10
"""
Publications Page Generator for Perry Dime Website
Reads CSV summary files from publications-prose and publications-poetry
Generates publications.html with Prose and Poetry subsections
"""

import csv
import shutil
import json
from pathlib import Path
from bs4 import BeautifulSoup

# Paths
BASE_DIR = Path(__file__).parent
PROSE_DIR = BASE_DIR / "source/publications-prose"
POETRY_DIR = BASE_DIR / "source/publications-poetry"
PROSE_CSV = PROSE_DIR / "Prose-Summary.csv"
POETRY_CSV = POETRY_DIR / "Poetry-Summary.csv"
OUTPUT_FILE = BASE_DIR / "docs/publications.html"
TEMPLATE_FILE = BASE_DIR / "docs/music.html"
LOGO_SOURCE = BASE_DIR / "source/publications-prose/perrydime-publications-logo.png"
LOGO_DEST = BASE_DIR / "docs/assets/img/perrydime-publications-logo.png"

def read_csv_summary(csv_path):
    """Read CSV summary file and return list of publications"""
    publications = []
    
    if not csv_path.exists():
        print(f"Warning: {csv_path} not found")
        return publications
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            publications.append(row)
    
    return publications

def read_metadata_json(json_path):
    """Read metadata.json file"""
    if not json_path.exists():
        return None
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return None

def parse_inline_metadata(metadata_str):
    """Parse inline metadata from CSV (format: Title: X Author: Y Description: Z Written: W)"""
    metadata = {
        'title': '',
        'author': '',
        'description': '',
        'year': ''
    }
    
    if not metadata_str or metadata_str.strip() == '':
        return metadata
    
    # Parse inline format
    parts = metadata_str.split('Author:')
    if len(parts) >= 2:
        # Extract title
        title_part = parts[0].replace('Title:', '').strip()
        metadata['title'] = title_part
        
        # Extract author and remaining
        remaining = parts[1]
        desc_parts = remaining.split('Description:')
        if len(desc_parts) >= 2:
            metadata['author'] = desc_parts[0].strip()
            
            # Extract description and year
            written_parts = desc_parts[1].split('Written:')
            if len(written_parts) >= 2:
                metadata['description'] = written_parts[0].strip()
                metadata['year'] = written_parts[1].strip()
            else:
                metadata['description'] = desc_parts[1].strip()
    
    return metadata

def process_publication(row, base_dir):
    """Process a single publication entry from CSV"""
    folder = row.get('Folder', '').strip()
    if not folder:
        return None
    
    # Get the base directory for the script
    script_dir = Path(__file__).parent
    
    # Normalize folder name (handle case variations)
    pub_dir = base_dir / folder
    if not pub_dir.exists():
        # Try lowercase
        pub_dir = base_dir / folder.lower()
        if not pub_dir.exists():
            print(f"Warning: Folder not found: {folder}")
            return None
    
    # Get metadata - either from JSON file or inline in CSV
    metadata_field = row.get('Metadata', '').strip()
    
    if metadata_field.endswith('.json'):
        # Read from JSON file
        json_path = pub_dir / metadata_field
        json_data = read_metadata_json(json_path)
        if json_data:
            title = json_data.get('title', folder.replace('-', ' ').title())
            author = json_data.get('author', 'Jefferson Richards')
            description = json_data.get('description', '')
            year = json_data.get('publication_year', json_data.get('original_publication_year', ''))
        else:
            # Fallback
            title = folder.replace('-', ' ').title()
            author = 'Jefferson Richards'
            description = ''
            year = ''
    else:
        # Parse inline metadata
        inline_meta = parse_inline_metadata(metadata_field)
        title = inline_meta['title'] or folder.replace('-', ' ').title()
        author = inline_meta['author'] or 'Jefferson Richards'
        description = inline_meta['description']
        year = inline_meta['year']
    
    # Process cover art
    cover_art_file = row.get('Cover Art', '').strip()
    cover_path = None
    
    if cover_art_file:
        cover_source = pub_dir / cover_art_file
        if cover_source.exists():
            # Copy to docs/assets/img/
            dest_dir = script_dir / "docs/assets/img"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / f"pub-{folder}-{cover_art_file}"
            
            shutil.copy(cover_source, dest_file)
            cover_path = f"assets/img/pub-{folder}-{cover_art_file}"
            print(f"  ✓ Copied cover: {cover_art_file}")
        else:
            print(f"  Warning: Cover not found: {cover_art_file}")
    
    # Get Amazon links
    amazon_ebook = row.get('Amazon eBook Link', '').strip()
    amazon_print = row.get('Amazon Print link', '').strip()
    
    # Get backup PDF
    pdf_file = row.get('If No Amazon Link - then PDF Slip in Folder', '').strip()
    pdf_path = None
    
    # Only process PDF if no Amazon links exist
    if pdf_file and not amazon_ebook and not amazon_print:
        pdf_source = pub_dir / pdf_file
        if pdf_source.exists():
            # Copy to docs/assets/pdfs/
            dest_dir = script_dir / "docs/assets/pdfs"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_file = dest_dir / f"{folder}.pdf"
            
            shutil.copy(pdf_source, dest_file)
            pdf_path = f"assets/pdfs/{folder}.pdf"
            print(f"  ✓ Copied PDF: {pdf_file}")
        else:
            print(f"  Warning: PDF not found: {pdf_file}")
    
    return {
        'folder': folder,
        'title': title,
        'author': author,
        'description': description,
        'year': year,
        'cover': cover_path,
        'amazon_ebook': amazon_ebook,
        'amazon_print': amazon_print,
        'pdf': pdf_path
    }

def scan_publications():
    """Scan both prose and poetry directories"""
    publications = {
        'prose': [],
        'poetry': []
    }
    
    # Process Prose
    prose_csv = PROSE_DIR / "Prose-Summary.csv"
    if prose_csv.exists():
        prose_rows = read_csv_summary(prose_csv)
        for row in prose_rows:
            pub = process_publication(row, PROSE_DIR)
            if pub:
                publications['prose'].append(pub)
    
    # Process Poetry
    poetry_csv = POETRY_DIR / "Poetry-Summary.csv"
    if poetry_csv.exists():
        poetry_rows = read_csv_summary(poetry_csv)
        for row in poetry_rows:
            pub = process_publication(row, POETRY_DIR)
            if pub:
                publications['poetry'].append(pub)
    
    return publications

def generate_publications_html(publications):
    """Generate publications.html with Prose and Poetry sections"""
    
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
        title_tag.string = "Publications | Perry Dime"
    
    # Update hero section
    hero = soup.find('section', class_='hero')
    if hero:
        hero_h2 = hero.find('h2')
        if hero_h2:
            hero_h2.string = "Publications"
        hero_p = hero.find('p', class_='lead')
        if hero_p:
            hero_p.string = "Literary works, essays, and poetry by Perry Dime Publications."
    
    # Update navigation active state
    nav_links = soup.find_all('a', href='music.html')
    for link in nav_links:
        if 'active' in link.get('class', []):
            link['class'].remove('active')
    
    pub_links = soup.find_all('a', href='publications.html')
    for link in pub_links:
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
    music_section['class'] = ['publications-section']
    container = music_section.find('div', class_='container')
    if container:
        container.clear()
    else:
        container = soup.new_tag('div', **{'class': 'container'})
        music_section.append(container)
    
    # Add Perry Dime Publications logo
    logo_div = soup.new_tag('div', **{'class': 'publications-logo'})
    logo_img = soup.new_tag('img', src='assets/img/perrydime-publications-logo.png', 
                            alt='Perry Dime Publications', **{'class': 'pub-logo'})
    logo_div.append(logo_img)
    container.append(logo_div)
    
    # Add intro
    intro_h2 = soup.new_tag('h2')
    intro_h2.string = "Literary Works"
    container.append(intro_h2)
    
    intro_p = soup.new_tag('p', **{'class': 'section-intro'})
    intro_p.string = "A collection of prose, poetry, and philosophical writings."
    container.append(intro_p)
    
    # Create tab navigation
    tab_nav = soup.new_tag('div', **{'class': 'pub-tabs'})
    
    # Prose tab button
    prose_tab = soup.new_tag('button', **{'class': 'pub-tab active', 'data-tab': 'prose'})
    prose_icon = soup.new_tag('span', **{'class': 'tab-icon'})
    prose_icon.string = "📚"
    prose_label = soup.new_tag('span', **{'class': 'tab-label'})
    prose_label.string = "Prose"
    prose_count = soup.new_tag('span', **{'class': 'tab-count'})
    prose_count.string = str(len(publications['prose']))
    prose_tab.append(prose_icon)
    prose_tab.append(prose_label)
    prose_tab.append(prose_count)
    tab_nav.append(prose_tab)
    
    # Poetry tab button
    poetry_tab = soup.new_tag('button', **{'class': 'pub-tab', 'data-tab': 'poetry'})
    poetry_icon = soup.new_tag('span', **{'class': 'tab-icon'})
    poetry_icon.string = "✍️"
    poetry_label = soup.new_tag('span', **{'class': 'tab-label'})
    poetry_label.string = "Poetry"
    poetry_count = soup.new_tag('span', **{'class': 'tab-count'})
    poetry_count.string = str(len(publications['poetry']))
    poetry_tab.append(poetry_icon)
    poetry_tab.append(poetry_label)
    poetry_tab.append(poetry_count)
    tab_nav.append(poetry_tab)
    
    container.append(tab_nav)
    
    # Generate Prose content
    if publications['prose']:
        prose_content = soup.new_tag('div', **{'class': 'pub-tab-content active', 'id': 'prose-content'})
        prose_grid = soup.new_tag('div', **{'class': 'publications-grid'})
        
        for pub in publications['prose']:
            pub_card = create_publication_card(soup, pub)
            prose_grid.append(pub_card)
        
        prose_content.append(prose_grid)
        container.append(prose_content)
    
    # Generate Poetry content
    if publications['poetry']:
        poetry_content = soup.new_tag('div', **{'class': 'pub-tab-content', 'id': 'poetry-content'})
        poetry_grid = soup.new_tag('div', **{'class': 'publications-grid'})
        
        for pub in publications['poetry']:
            pub_card = create_publication_card(soup, pub)
            poetry_grid.append(pub_card)
        
        poetry_content.append(poetry_grid)
        container.append(poetry_content)
    
    # Write output
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    
    print(f"✓ Generated {OUTPUT_FILE}")
    print(f"  - Prose: {len(publications['prose'])} publications")
    print(f"  - Poetry: {len(publications['poetry'])} publications")

def create_publication_card(soup, pub):
    """Create a publication card element"""
    card = soup.new_tag('div', **{'class': 'pub-card'})
    
    # Cover image
    if pub['cover']:
        cover_div = soup.new_tag('div', **{'class': 'pub-cover'})
        cover_img = soup.new_tag('img', src=pub['cover'], alt=pub['title'], loading='lazy')
        cover_div.append(cover_img)
        card.append(cover_div)
    
    # Content
    content_div = soup.new_tag('div', **{'class': 'pub-content'})
    
    # Title
    title_h4 = soup.new_tag('h4')
    title_h4.string = pub['title']
    content_div.append(title_h4)
    
    # Author
    author_p = soup.new_tag('p', **{'class': 'pub-author'})
    author_p.string = f"by {pub['author']}"
    content_div.append(author_p)
    
    # Year
    if pub['year']:
        year_p = soup.new_tag('p', **{'class': 'pub-year'})
        year_p.string = pub['year']
        content_div.append(year_p)
    
    # Description
    if pub['description']:
        desc_p = soup.new_tag('p', **{'class': 'pub-description'})
        desc_p.string = pub['description'][:200] + ('...' if len(pub['description']) > 200 else '')
        content_div.append(desc_p)
    
    # Links
    links_div = soup.new_tag('div', **{'class': 'pub-links'})
    
    if pub['amazon_ebook']:
        ebook_link = soup.new_tag('a', href=pub['amazon_ebook'], target='_blank', **{'class': 'pub-link'})
        ebook_link.string = "Kindle eBook"
        links_div.append(ebook_link)
    
    if pub['amazon_print']:
        print_link = soup.new_tag('a', href=pub['amazon_print'], target='_blank', **{'class': 'pub-link'})
        print_link.string = "Print Edition"
        links_div.append(print_link)
    
    if pub['pdf']:
        pdf_link = soup.new_tag('a', href=pub['pdf'], target='_blank', **{'class': 'pub-link pdf-link'})
        pdf_link.string = "Read PDF"
        links_div.append(pdf_link)
    
    content_div.append(links_div)
    card.append(content_div)
    
    return card

def main():
    print("=" * 70)
    print("Perry Dime Publications Generator")
    print("=" * 70)
    
    # Scan publications
    print("\n1. Scanning publications directories...")
    publications = scan_publications()
    
    # Generate HTML
    print("\n2. Generating publications.html...")
    generate_publications_html(publications)
    
    print("\n" + "=" * 70)
    print("Publications generation complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
