---
inclusion: always
---

# Publications Page - Implementation Complete

## Overview
The Publications page has been successfully created with Prose and Poetry subsections, following the CSV master index pattern and implementing the exact link logic specified by the user.

## Implementation Details

### Script: `upsert_publications.py`
- Reads CSV master index files from `source/publications-prose/` and `source/publications-poetry/`
- Parses both JSON metadata files and inline CSV metadata
- Copies cover art to `docs/assets/img/` with `pub-{folder}-` prefix
- Copies PDFs to `docs/assets/pdfs/` only when no Amazon links exist
- Generates `docs/publications.html` with proper structure

### CSV Processing
The script correctly handles the CSV structure:
- **Folder**: Subfolder name containing assets
- **Metadata**: Either JSON filename or inline metadata string
- **Cover Art**: Image filename to copy
- **Amazon eBook Link**: Primary link option
- **Amazon Print link**: Secondary link option
- **If No Amazon Link - then PDF Slip in Folder**: Fallback PDF filename

### Link Priority Logic
```
1. Check Amazon eBook Link → Create "Kindle eBook" button
2. Check Amazon Print Link → Create "Print Edition" button
3. If both Amazon columns empty → Use PDF column → Create "Read PDF" button
```

## Files Generated

### HTML
- `docs/publications.html` (24 KB)
  - Perry Dime Publications logo at top
  - Prose section with 14 publications
  - Poetry section with 5 publications
  - Responsive card layout

### Assets Copied
- `docs/assets/img/perrydime-publications-logo.png` (2.1 MB)
- `docs/assets/img/pub-*.png|jpg` (19 cover images)
- `docs/assets/pdfs/*.pdf` (11 PDF files)

### CSS Styles Added
Added ~200 lines to `docs/assets/css/style.css`:
- `.publications-section` - Main section
- `.publications-logo` - Logo display (only on this page)
- `.pub-section-header` - Prose/Poetry headers
- `.publications-grid` - Responsive grid
- `.pub-card` - Card styling with hover effects
- `.pub-cover` - Cover image container
- `.pub-content` - Card content area
- `.pub-links` - Button container
- `.pub-link` - Button styling
- `.pub-link.pdf-link` - PDF button accent color
- Mobile responsive styles

## Publications Breakdown

### Prose (14)
1. Survitality of the Synapse (Amazon eBook + Print)
2. Stockholm Forgiveness of Responsibility (Amazon eBook + Print)
3. 2010 Neurosurgery Journal (PDF)
4. 2013 / Freedom to Model (PDF)
5. Letters from America (PDF)
6. Critique of Judgment (Amazon eBook + Print)
7. Einstein's Relativity (Amazon eBook)
8. Flatland (Amazon Print)
9. Gallic Wars (PDF)
10. Jesus Parables (PDF)
11. Letters of Euler (Amazon eBook + Print)
12. Meditations (PDF)
13. Second Treatise (Amazon eBook + Print)
14. The Prophet (PDF)

### Poetry (5)
1. Thought Fat: Selected Poems (Amazon eBook)
2. La Primavera Primera (PDF)
3. Thought Fat (PDF)
4. The Grapes of Sag (PDF)
5. Don't Care What You Call Me... (PDF)

## Design Features

### Visual Hierarchy
- Perry Dime Publications logo prominently displayed at top
- Clear section headers for Prose and Poetry
- Consistent card layout with cover images
- Title, Author, Year, Description on each card

### Interactive Elements
- Card hover effects (lift + shadow)
- Cover image zoom on hover
- Button hover effects (lift + shadow)
- Smooth transitions throughout

### Responsive Design
- Mobile (<768px): Single column, smaller logo
- Tablet (769-1024px): 2-3 columns
- Desktop (>1024px): 3-4 columns
- Flexible button layout

## Testing

### To Test Locally
```bash
cd perrydime.com
python3.10 serve_local.py
```
Visit: `http://localhost:8000/publications.html`

### Verification Checklist
- ✅ Logo displays prominently
- ✅ Prose section shows 14 publications
- ✅ Poetry section shows 5 publications
- ✅ All cover images load
- ✅ Amazon links work (open in new tab)
- ✅ PDF links work (open in new tab)
- ✅ Hover effects work
- ✅ Responsive layout works
- ✅ Navigation active state correct

## Maintenance

### To Add New Publications
1. Add entry to appropriate CSV file (`Prose-Summary.csv` or `Poetry-Summary.csv`)
2. Ensure subfolder exists with cover art and PDF (if needed)
3. Run: `python3.10 upsert_publications.py`
4. The script will update `docs/publications.html` automatically

### To Update Existing Publications
1. Update CSV entry or metadata JSON file
2. Run: `python3.10 upsert_publications.py`
3. The script will regenerate the page with updated information

## Notes
- The Perry Dime Publications logo is ONLY displayed on the Publications page
- The script follows the upsert pattern and can be re-run safely
- Cover images are prefixed with `pub-{folder}-` to avoid conflicts
- PDFs are named `{folder}.pdf` for consistency
- The script handles both JSON metadata files and inline CSV metadata
- Link priority: Amazon first, PDF as fallback
