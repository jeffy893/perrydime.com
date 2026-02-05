---
inclusion: always
---

# Dreams Page - Implementation Complete

## Overview
The Dreams page has been successfully created by scanning `source/dreams/` for PDF files and generating a clean card layout with moon icons and formatted dates.

## Implementation Details

### Script: `upsert_dreams.py`
- Scans `source/dreams/` directory for PDF files
- Parses filenames to extract date (YYYY-MM-DD) and title
- Copies PDFs to `docs/assets/pdfs/dreams/`
- Generates `docs/dreams.html` with responsive card layout
- Sorts dreams by date (most recent first)

### Filename Parsing
Expected format: `YYYY-MM-DD_Title_With_Underscores.pdf`
- Extracts date and formats as "Month DD, YYYY"
- Converts underscores to spaces for readable titles
- Handles edge cases gracefully

## Files Generated

### HTML
- `docs/dreams.html` - Main dreams page with 9 dream journal cards

### Assets Copied
- `docs/assets/pdfs/dreams/*.pdf` - 9 dream journal PDFs (~23.4 MB total)

### CSS Styles Added
Added ~120 lines to `docs/assets/css/style.css`:
- `.dreams-section` - Main section
- `.dreams-grid` - Responsive grid layout
- `.dream-card` - Card with left border accent and hover effects
- `.dream-icon` - Circular gradient background with moon SVG
- `.dream-content` - Content area
- `.dream-date` - Date styling
- `.dream-button` - Button with slide-right hover effect
- Mobile responsive styles

## Dream Journals (9 total)

Sorted by date (newest first):

1. **A Hardened Heart Consolidates** (August 12, 2024) - 819 KB
2. **The Great Polished Catamaran** (July 05, 2024) - 2.4 MB
3. **Social Econ** (June 16, 2024) - 4.2 MB
4. **Ravings Econ Dreams** (June 09, 2024) - 1.8 MB
5. **Post SCJ Dream Analysis** (May 26, 2024) - 676 KB
6. **Posterity Series** (May 13, 2024) - 4.1 MB
7. **System2** (May 09, 2024) - 432 KB
8. **May2024 Sleeper Cell Journal** (May 03, 2024) - 7.3 MB
9. **Pre SCJ Dream Analysis** (May 01, 2024) - 1.8 MB

## Design Features

### Card Structure
Each dream card includes:
- **Moon Icon**: Crescent moon SVG with gradient background
- **Title**: Parsed from filename, underscores converted to spaces
- **Date**: Formatted as "Month DD, YYYY"
- **Button**: "View Dream Journal" link to PDF

### Visual Effects
- **Card Hover**: Lift up 5px, shadow increases, border color changes
- **Button Hover**: Slide right 5px, background color changes
- **Icon**: Gradient from primary to secondary color
- **Border**: 4px left accent border

### Responsive Layout
- **Desktop (>1024px)**: 3 columns, 320px min width
- **Tablet (769-1024px)**: 2 columns, 280px min width
- **Mobile (<768px)**: 1 column, centered layout, stacked icon

## Testing

### To Test Locally
```bash
cd perrydime.com
python3.10 serve_local.py
```
Visit: `http://localhost:8000/dreams.html`

### Verification Checklist
- ✅ All 9 dreams display correctly
- ✅ Dates are properly formatted
- ✅ Titles are readable
- ✅ Moon icons display with gradient
- ✅ PDF links work (open in new tab)
- ✅ Hover effects work
- ✅ Responsive layout works
- ✅ Navigation active state correct

## Maintenance

### To Add New Dreams
1. Add PDF to `source/dreams/` with format: `YYYY-MM-DD_Title.pdf`
2. Run: `python3.10 upsert_dreams.py`
3. Page automatically updates with new dream

### To Update Existing Dreams
1. Replace PDF in `source/dreams/`
2. Run: `python3.10 upsert_dreams.py`
3. Page regenerates with updated content

## Technical Notes
- Dreams sorted by date (most recent first)
- Original PDF filenames preserved
- Moon icon is inline SVG (no external dependencies)
- Script follows upsert pattern (can be re-run safely)
- Handles filename parsing edge cases
- Responsive grid uses CSS Grid with auto-fill
