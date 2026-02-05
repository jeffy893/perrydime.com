#!/usr/bin/env python3.10
"""
Fix navigation bar across all HTML pages.
Improves UX with cleaner design and better mobile experience.
"""

from pathlib import Path
from bs4 import BeautifulSoup

def update_navigation(html_file):
    """Update navigation in a single HTML file."""
    print(f"Processing: {html_file.name}")
    
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Find the navigation container
    nav_container = soup.find('div', class_='nav-container')
    if not nav_container:
        print(f"  ⚠️  No nav-container found in {html_file.name}")
        return
    
    # Determine current page
    current_page = html_file.name
    
    # Create new navigation structure
    new_nav_html = f'''
    <div class="nav-container">
        <div class="logo">
            <h1><a href="index.html">Perry Dime</a></h1>
            <p class="tagline">Publications, Art, Dreams, and Music</p>
        </div>
        
        <!-- Mobile Menu Toggle -->
        <button class="mobile-menu-toggle" aria-label="Toggle navigation menu">
            <span></span>
            <span></span>
            <span></span>
        </button>
        
        <!-- Navigation Links -->
        <ul class="nav-links">
            <li><a href="index.html" class="{'active' if current_page == 'index.html' else ''}">Home</a></li>
            <li><a href="publications.html" class="{'active' if current_page == 'publications.html' else ''}">Publications</a></li>
            <li><a href="art.html" class="{'active' if current_page == 'art.html' else ''}">Art</a></li>
            <li><a href="dreams.html" class="{'active' if current_page == 'dreams.html' else ''}">Dreams</a></li>
            <li><a href="music.html" class="{'active' if current_page == 'music.html' else ''}">Music</a></li>
        </ul>
    </div>
    '''
    
    # Parse new navigation
    new_nav = BeautifulSoup(new_nav_html, 'html.parser')
    
    # Replace old navigation
    nav_container.replace_with(new_nav.find('div', class_='nav-container'))
    
    # Write back to file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup.prettify()))
    
    print(f"  ✓ Updated {html_file.name}")

def main():
    """Update navigation in all HTML files."""
    docs_dir = Path(__file__).parent / "docs"
    
    # Find all HTML files
    html_files = list(docs_dir.glob("*.html"))
    
    print(f"\n{'='*70}")
    print("FIXING NAVIGATION BAR")
    print(f"{'='*70}\n")
    print(f"Found {len(html_files)} HTML files to process\n")
    
    for html_file in sorted(html_files):
        update_navigation(html_file)
    
    print(f"\n{'='*70}")
    print("✓ NAVIGATION FIX COMPLETE")
    print(f"{'='*70}\n")
    print("All navigation bars have been updated with:")
    print("  • Cleaner structure")
    print("  • Proper active state highlighting")
    print("  • Better mobile UX")
    print("  • Consistent styling across all pages")
    print()

if __name__ == "__main__":
    main()
