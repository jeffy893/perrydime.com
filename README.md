# perrydime.com

A creative portfolio website for Perry Dime (Jefferson Richards), showcasing publications, art, dreams, and music.

## Live Site

**URL:** [perrydime.com](https://perrydime.com)

## Overview

This is a static website built with HTML, CSS, and JavaScript, designed to be hosted on GitHub Pages. The site features a mobile-first responsive design with a cohesive color palette derived from the Perry Dime logo.

## Site Structure

```
docs/                    # Production files (GitHub Pages root)
├── index.html           # Home page
├── publications.html    # Publications (Prose/Poetry tabs)
├── art.html             # Art gallery (General/Female Form/Home Art tabs)
├── dreams.html          # Dream journals
├── music.html           # Music (Tracks/Melotations tabs)
└── assets/
    ├── css/
    │   ├── variables.css    # CSS custom properties
    │   └── style.css        # Main stylesheet
    ├── js/
    │   └── main.js          # JavaScript (lightbox, tabs, mobile menu)
    ├── img/                 # Images (art, covers, branding)
    └── pdfs/                # PDF files (publications, dreams, melotations)

source/                  # Source content (processed by upsert scripts)
├── branding/            # Logo and brand assets
├── art/                 # Original art images
├── dreams/              # Dream journal PDFs
├── productions/         # SoundCloud embed list
├── productions-melotations/  # Sheet music PDFs
├── publications-prose/  # Prose publications with CSV index
└── publications-poetry/ # Poetry publications with CSV index
```

## Color Palette

All colors are derived from `source/branding/perrydime-logo.png`:

| Name | Hex | Usage |
|------|-----|-------|
| Warm Beige | `#c8af99` | Primary background, accents |
| Deep Brown | `#603e29` | Headers, footer, text |
| Dusty Rose | `#c07b7e` | Accent color, highlights |
| Soft Blue-Gray | `#a4babe` | Secondary accents |
| Medium Brown | `#91765f` | Gradients, borders |

## Sections

### Publications
- **Prose Tab (14 items):** Books, essays, and academic works
- **Poetry Tab (5 items):** Poetry collections
- Features Perry Dime Publications logo
- Links to Amazon (Kindle/Print) or PDF downloads

### Art Gallery
- **General Collection (22 images):** Root-level artwork
- **Female Form (14 images):** Figure studies
- **Home Art (14 images):** Domestic and interior artwork
- Interactive lightbox with keyboard navigation (arrows, escape)
- Lazy loading for performance

### Dreams
- 9 dream journal PDFs
- Sorted by date (most recent first)
- Moon icon theme with card layout

### Music
- **Tracks Tab (13 items):** SoundCloud embeds
- **Melotations Tab:** Sheet music PDFs

## Upsert Scripts

The site uses Python scripts to update content without regenerating the entire site:

```bash
# Update publications from CSV indexes
python3.10 upsert_publications.py

# Update art gallery from source images
python3.10 upsert_art.py

# Update dreams from PDF files
python3.10 upsert_dreams.py

# Update music from SoundCloud list and melotations
python3.10 upsert_music.py
```

### Requirements
- Python 3.10
- BeautifulSoup4 (`pip install beautifulsoup4`)
- lxml (`pip install lxml`)

## Local Development

### Start Local Server
```bash
cd perrydime.com
python3.10 serve_local.py
```
Visit: http://localhost:8000

### Adding New Content

**Publications:**
1. Add folder to `source/publications-prose/` or `source/publications-poetry/`
2. Include cover image and optional PDF
3. Update the corresponding CSV index file
4. Run: `python3.10 upsert_publications.py`

**Art:**
1. Add PNG images to `docs/assets/img/art/` (or create subfolder for new section)
2. Run: `python3.10 upsert_art.py`

**Dreams:**
1. Add PDF to `source/dreams/` with format: `YYYY-MM-DD_Title_With_Underscores.pdf`
2. Run: `python3.10 upsert_dreams.py`

**Music:**
1. Update `source/productions/List-of-SoundCloud-Embed.html` for tracks
2. Add PDFs to `source/productions-melotations/` for sheet music
3. Run: `python3.10 upsert_music.py`

## Design Features

- **Mobile-first responsive design** with breakpoint at 768px
- **Tabbed interfaces** for Publications, Art, and Music sections
- **Interactive lightbox** for art gallery with keyboard navigation
- **Gradient backgrounds** and hover effects throughout
- **WCAG AA compliant** text contrast (4.5:1 minimum)
- **Lazy loading** for images
- **Inline SVG icons** (no external CDN dependencies)

## Contact

- **Email:** Jefferson@richards.plus
- **Instagram:** [@jefferson.cloud](https://instagram.com/jefferson.cloud)
- **Socialize:** [jefferson.cloud](https://jefferson.cloud)
- **Decode:** [richards.systems](https://richards.systems)
- **Consult:** [richards.plus](https://richards.plus)

## Deployment

The site is deployed via GitHub Pages from the `docs/` folder. Any push to the main branch automatically updates the live site.

## License

© Perry Dime. All rights reserved.
