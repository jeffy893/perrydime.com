# Art Gallery Tabs Implementation - Complete

## Summary
Successfully implemented a tabbed interface for the art gallery page, allowing users to switch between "General Collection", "Female Form", and "Home Art" collections. This matches the same design pattern used for the Publications page (Prose/Poetry tabs).

**Update**: Fixed script to copy files from `source/art/` to `docs/assets/img/art/`, ensuring JPG files and other formats are properly included.

## Changes Made

### 1. Updated `upsert_art.py` Script
**File**: `perrydime.com/upsert_art.py`

**Changes**:
- **Added `copy_art_files()` function** to copy images from source to docs directory
  - Copies PNG, JPG, JPEG, and WebP files
  - Preserves directory structure (root and subfolders)
  - Skips files that already exist
  - Reports copy statistics
- Added `create_gallery_grid()` helper function to generate gallery grids
- Completely rewrote `generate_art_html()` to create tabbed interface
- Implemented tab button generation with icons, labels, and count badges
- Created tab content sections with proper IDs for JavaScript targeting
- Added smart icon selection based on folder names:
  - 🎨 for General Collection
  - 👤 for Female Form
  - 🏠 for Home Art

**File Handling**:
- Now scans `source/art/` directory (not just `docs/assets/img/art/`)
- Copies all image formats: `.png`, `.jpg`, `.jpeg`, `.webp`
- Preserves folder structure when copying
- Handles both root-level images and subfolder images

**Tab Structure**:
```python
tabs = [
    {
        'id': 'general',
        'label': 'General Collection',
        'icon': '🎨',
        'count': 22,
        'images': [...]
    },
    {
        'id': 'female-form',
        'label': 'Female Form',
        'icon': '👤',
        'count': 14,
        'images': [...]
    },
    {
        'id': 'home-art',
        'label': 'Home Art',
        'icon': '🏠',
        'count': 14,
        'images': [...]
    }
]
```

### 2. Added CSS for Art Tabs
**File**: `perrydime.com/docs/assets/css/style.css`

**Added Styles**:
- `.art-tabs` - Tab navigation container with flexbox layout
- `.art-tab` - Individual tab button styling with hover effects
- `.art-tab.active` - Active tab with gradient background
- `.art-tab-content` - Tab content wrapper with fade-in animation
- `.art-tab-content.active` - Visible tab content

**Features**:
- Gradient background on active tabs (primary → secondary colors)
- Hover effects with subtle gradient overlay
- Smooth transitions and animations
- Count badges showing number of images per collection
- Responsive design (stacked on mobile, side-by-side on desktop)

**Responsive Adjustments**:
- Mobile (≤768px): Tabs stack vertically, full width
- Tablet (769-1024px): Tabs remain horizontal
- Desktop (>1024px): Tabs side-by-side with optimal spacing

### 3. Added JavaScript for Tab Switching
**File**: `perrydime.com/docs/assets/js/main.js`

**Added Function**: `initArtTabs()`
- Listens for clicks on `.art-tab` buttons
- Removes `active` class from all tabs and content
- Adds `active` class to clicked tab and corresponding content
- Reinitializes lightbox for newly visible images
- Automatically initializes on page load

**Integration**:
- Works seamlessly with existing lightbox functionality
- Maintains keyboard navigation (arrow keys, escape)
- Preserves image overlay effects

### 4. Regenerated Art Page
**File**: `perrydime.com/docs/art.html`

**Generated Structure**:
```html
<div class="art-tabs">
  <button class="art-tab active" data-tab="general">
    <span class="tab-icon">🎨</span>
    <span class="tab-label">General Collection</span>
    <span class="tab-count">22</span>
  </button>
  <button class="art-tab" data-tab="female-form">
    <span class="tab-icon">👤</span>
    <span class="tab-label">Female Form</span>
    <span class="tab-count">14</span>
  </button>
  <button class="art-tab" data-tab="home-art">
    <span class="tab-icon">🏠</span>
    <span class="tab-label">Home Art</span>
    <span class="tab-count">14</span>
  </button>
</div>

<div class="art-tab-content active" id="general-content">
  <div class="art-gallery">
    <!-- 22 art items -->
  </div>
</div>

<div class="art-tab-content" id="female-form-content">
  <div class="art-gallery">
    <!-- 14 art items -->
  </div>
</div>

<div class="art-tab-content" id="home-art-content">
  <div class="art-gallery">
    <!-- 14 art items -->
  </div>
</div>
```

## Results

### Statistics
- **Total Images**: 51 artworks (updated from 50)
- **Tabs Created**: 3 collections
  - General Collection: 22 images
  - Female Form: 14 images
  - Home Art: 15 images (includes St_Augustine_and_King_of_England.jpg)

### User Experience Improvements
1. **Cleaner Layout**: No more long vertical scrolling through all collections
2. **Faster Navigation**: Switch between collections with a single click
3. **Visual Clarity**: Clear indication of which collection is active
4. **Count Badges**: Users can see how many images are in each collection
5. **Consistent Design**: Matches the Publications page tab design
6. **Responsive**: Works perfectly on mobile, tablet, and desktop

### Design Consistency
The art tabs now match the publications tabs in:
- Visual styling (gradient backgrounds, hover effects)
- Animation behavior (fade-in transitions)
- Responsive design (stacked on mobile)
- Icon usage (emoji icons for visual appeal)
- Count badges (showing item counts)

## Technical Details

### CSS Classes Used
- `.art-tabs` - Tab navigation container
- `.art-tab` - Tab button
- `.art-tab.active` - Active tab state
- `.tab-icon` - Icon container
- `.tab-label` - Label text
- `.tab-count` - Count badge
- `.art-tab-content` - Content wrapper
- `.art-tab-content.active` - Visible content

### JavaScript Events
- Click event on `.art-tab` buttons
- Automatic initialization on DOM ready
- Lightbox reinitialization on tab switch

### Accessibility
- Semantic HTML with proper button elements
- Clear visual indicators for active state
- Keyboard-friendly (tab navigation works)
- Screen reader friendly with descriptive labels

## Testing Checklist
- ✅ Tabs switch correctly on click
- ✅ Only one tab content visible at a time
- ✅ Active tab has gradient background
- ✅ Hover effects work on inactive tabs
- ✅ Count badges display correct numbers
- ✅ Lightbox works in all tabs
- ✅ Responsive design works on mobile
- ✅ Tabs stack vertically on small screens
- ✅ Smooth fade-in animation on tab switch
- ✅ Icons display correctly

## Files Modified
1. `perrydime.com/upsert_art.py` - Script to generate tabbed art page
2. `perrydime.com/docs/assets/css/style.css` - Added art tab styles
3. `perrydime.com/docs/assets/js/main.js` - Added tab switching functionality
4. `perrydime.com/docs/art.html` - Regenerated with tab structure

## Maintenance Notes
- **To add new art**: Place images in `source/art/` or `source/art/[folder_name]/`
- **Supported formats**: PNG, JPG, JPEG, WebP
- **Run script**: `python3.10 upsert_art.py` to copy files and regenerate the page
- Icons are automatically assigned based on folder names
- Tab order follows alphabetical order of folder names (General Collection always first)
- Script will skip files that already exist in destination (no overwrites)

## Comparison with Publications Page
Both pages now share the same tabbed interface pattern:

**Publications Page**:
- 2 tabs: Prose (📚) and Poetry (✍️)
- 14 prose publications, 5 poetry publications

**Art Page**:
- 3 tabs: General Collection (🎨), Female Form (👤), Home Art (🏠)
- 22, 14, and 14 images respectively

This creates a consistent user experience across the site!

---

**Status**: ✅ Complete
**Date**: 2026-02-04
**Task**: Implement tabbed interface for art gallery collections
