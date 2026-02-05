---
inclusion: always
---

# Perry Dime Website Structure

## Site Title
**Perry Dime: Publications, Art, Dreams, and Music**

## Directory Structure
```
perrydime.com/
├── docs/                    # Website output (served at perrydime.com)
│   ├── index.html          # Homepage
│   ├── publications/       # Publications section
│   ├── art/                # Art gallery section
│   ├── dreams/             # Dreams section
│   ├── music/              # Music section
│   ├── assets/             # CSS, JS, images
│   └── ...
├── source/                 # Source content folders (to be created/used)
│   ├── publications/
│   ├── art/
│   ├── dreams/
│   └── music/
└── .kiro/                  # Project context (this folder)
```

## Content Categories

### Publications
Written works, essays, articles, books, and other textual content.

### Art
Visual artwork, illustrations, designs, and creative visual projects.

### Dreams
Dream journals, interpretations, and dream-related content.

### Music
Musical compositions, recordings, lyrics, and music-related projects.

## HTML Structure Guidelines

### Consistent Elements
All pages should include:
- Header with site title and navigation
- Main content area
- Footer with copyright/contact info
- Responsive design elements
- Consistent styling via shared CSS

### Navigation
- Clear links to all main sections
- Breadcrumb navigation where appropriate
- Back to home link on all pages

### Content Organization
- Chronological or alphabetical ordering
- Clear titles and dates
- Metadata (author, date, category)
- Tags or categories where relevant

## Asset Management
- CSS files in `docs/assets/css/`
- JavaScript in `docs/assets/js/`
- Images in `docs/assets/images/`
- Fonts in `docs/assets/fonts/`

## Responsive Design
- Mobile-first approach
- Breakpoints for tablet and desktop
- Accessible navigation on all devices
