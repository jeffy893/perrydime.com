---
inclusion: always
---

# Art Gallery Implementation

## Overview
The Art Gallery page displays 50 converted PNG images organized into three sections: General Collection (root), Female Form, and Home Art. Features responsive grid layout and interactive lightbox for full-size viewing.

## Source Data
- **Source Directory**: `docs/assets/img/art/`
- **Total Images**: 50 PNG files
- **Organization**:
  - Root: 22 images (General Collection)
  - Female_Form/: 14 images
  - Home_Art/: 14 images

## Implementation Details

### Python Script: `upsert_art.py`
- **Purpose**: Scan art directory and generate/update art.html
- **Logic**:
  - Scans `docs/assets/img/art/` recursively
  - Identifies root images and subfolders
  - Generates gallery sections for each folder
  - Creates responsive grid layout
  - Adds lightbox data attributes
- **Folder Name Formatting**: Converts `Female_Form` → "Female Form"
- **Image Titles**: Extracts from filename (removes extension, replaces underscores)

### HTML Structure: `docs/art.html`
- **Layout**: Full page with header, hero, gallery sections, footer
- **Sections**:
  1. General Collection (22 images)
  2. Female Form (14 images)
  3. Home Art (14 images)
- **Gallery Items**: `.art-item` containing:
  - `.art-link` with href and data-title
  - `<img>` with lazy loading
  - `.art-overlay` with title (appears on hover)

### CSS Styling: `docs/assets/css/style.css`
Added art gallery styles:

#### Gallery Grid
- **Desktop**: auto-fill columns (min 280px)
- **Tablet**: auto-fill columns (min 220px)
- **Mobile**: auto-fill columns (min 150px)
- **Aspect Ratio**: 1:1 (square cards)
- **Gap**: Responsive spacing

#### Gallery Items
- White background with shadow
- Rounded corners
- Hover effects:
  - Lift animation (translateY -5px)
  - Enhanced shadow
  - Image zoom (scale 1.1)
  - Overlay slides up from bottom

#### Gallery Headers
- Centered section titles
- Decorative underline (gradient)
- Consistent spacing between sections

#### Lightbox Modal
- Full-screen overlay (95% opacity black)
- Centered image display
- Navigation buttons (prev/next)
- Close button (top-right)
- Keyboard support (arrows, escape)
- Click outside to close
- Image title display

### JavaScript: `docs/assets/js/main.js`
Added lightbox functionality:

#### Features
- Click any image to open lightbox
- Navigate with arrow buttons or keyboard
- Close with X button, Escape key, or background click
- Smooth transitions
- Prevents body scroll when open
- Displays image title

#### Keyboard Controls
- **Left Arrow**: Previous image
- **Right Arrow**: Next image
- **Escape**: Close lightbox

#### Navigation
- Circular navigation (wraps around)
- Maintains image order from gallery
- Works across all gallery sections

## Gallery Sections

### 1. General Collection (22 images)
Root-level images including:
- 000_Fishbowl.png
- 00_IMG_0964.png
- IMG_0943.png through IMG_0969.png

### 2. Female Form (14 images)
Subfolder: `Female_Form/`
- IMG_0272.png through IMG_0289.png
- Artistic figure studies

### 3. Home Art (14 images)
Subfolder: `Home_Art/`
- IMG_3451.png through IMG_3466.png
- Domestic and interior artwork

## Design Features

### Responsive Grid
- **Desktop (>1024px)**: 4-5 columns
- **Tablet (769-1024px)**: 3-4 columns
- **Mobile (≤768px)**: 2 columns

### Image Optimization
- Lazy loading enabled
- PNG format (converted from HEIC)
- Max dimension: 2400px
- High quality compression

### Hover Effects
- Image zoom on hover
- Overlay slides up with title
- Smooth transitions (0.3s)
- Enhanced shadow

### Accessibility
- Alt text on all images
- ARIA labels on buttons
- Keyboard navigation
- Focus indicators
- Semantic HTML structure

## Color Palette
Uses variables from `docs/assets/css/variables.css`:
- Primary: #c8af99 (warm beige)
- Secondary: #603e29 (dark brown)
- Accent: #c07b7e (dusty rose)
- Background: #eeeeee (light gray)
- White: #ffffff

## File Structure
```
perrydime.com/
├── docs/
│   ├── art.html (generated page)
│   └── assets/
│       ├── img/
│       │   └── art/
│       │       ├── *.png (22 root images)
│       │       ├── Female_Form/ (14 images)
│       │       └── Home_Art/ (14 images)
│       ├── css/
│       │   └── style.css (gallery styles)
│       └── js/
│           └── main.js (lightbox functionality)
└── upsert_art.py (generation script)
```

## Future Updates

### Adding New Images
1. Add images to `docs/assets/img/art/` (root or subfolder)
2. Run: `python3.10 upsert_art.py`
3. Script automatically detects and adds new images

### Creating New Sections
1. Create new subfolder in `docs/assets/img/art/`
2. Add images to subfolder
3. Run: `python3.10 upsert_art.py`
4. New section automatically generated

### Updating Existing Images
1. Replace image file in `docs/assets/img/art/`
2. Clear browser cache
3. No script run needed (same filename)

## Performance Considerations

### Lazy Loading
- Images load as they enter viewport
- Reduces initial page load time
- Improves performance on mobile

### Image Format
- PNG format for quality
- Already optimized during conversion
- Consider WebP for future optimization

### Grid Layout
- CSS Grid for efficient rendering
- Hardware-accelerated transforms
- Minimal repaints on hover

## Browser Compatibility
- Chrome/Edge: Full support
- Firefox: Full support
- Safari: Full support
- Mobile browsers: Full support
- IE11: Partial support (no CSS Grid)

## Testing Checklist
- [x] All 50 images display correctly
- [x] Three sections render properly
- [x] Grid layout responsive on all screen sizes
- [x] Hover effects work smoothly
- [x] Lightbox opens on click
- [x] Lightbox navigation works (prev/next)
- [x] Keyboard controls functional
- [x] Close button works
- [x] Click outside closes lightbox
- [x] Image titles display correctly
- [x] Lazy loading functional
- [x] Navigation links work
- [x] Footer links correct

## Known Issues
None currently.

## Notes
- Images maintain aspect ratio in lightbox
- Overlay text may be hard to read on light images
- Consider adding image metadata/descriptions in future
- Could add filtering/sorting functionality
- Could add download button in lightbox
- Could add social sharing in lightbox

---

**Status**: COMPLETE ✓  
**Date**: 2026-02-04  
**Task**: Art Gallery Page (Task 7)
