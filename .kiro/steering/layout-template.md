---
inclusion: always
---

# Perry Dime Layout Template

## Main Template Structure

### File: `docs/index.html`
The main layout template for the Perry Dime website, based on the structure from captive.integralmass.com.

## Header Structure

### Sticky Navigation
The header uses `position: sticky` to remain visible while scrolling:
- **Background**: Primary brand color (#c8af99)
- **Z-index**: 1000 (stays above content)
- **Shadow**: Increases on scroll for depth
- **Responsive**: Collapses to hamburger menu on mobile

### Header Components
1. **Logo Section**
   - Site title: "Perry Dime"
   - Tagline: "Publications, Art, Dreams, and Music"
   - Links to homepage

2. **Navigation Links**
   - Home
   - Publications
   - Art
   - Dreams
   - Music

3. **Mobile Menu Toggle**
   - Hamburger icon (3 horizontal lines)
   - Animates to X when open
   - JavaScript-controlled

## Navigation Behavior

### Desktop (> 768px)
- Horizontal navigation bar
- Links displayed inline
- Hover effects with background highlight
- Active page indicator

### Mobile (≤ 768px)
- Hamburger menu button
- Vertical dropdown menu
- Full-width links
- Closes after link click

## Footer Structure

### Three-Column Layout
1. **About Section**
   - Description of Perry Dime
   - Mission/purpose statement

2. **Explore Section**
   - Quick links to all main pages
   - Same as navigation

3. **Connect Section**
   - Contact information
   - Social media links (future)

### Footer Bottom
- Copyright notice
- Additional disclaimers if needed

## CSS Architecture

### File Structure
```
docs/assets/css/
├── variables.css    # Color palette & design tokens
└── style.css        # Main stylesheet
```

### Import Order
1. `variables.css` - Must be loaded first
2. `style.css` - Uses variables from first file

### Key CSS Features
- CSS Custom Properties (variables)
- Flexbox for navigation
- Grid for content layouts
- Mobile-first responsive design
- Smooth transitions and animations

## JavaScript Functionality

### File: `docs/assets/js/main.js`

#### Features
1. **Mobile Menu Toggle**
   - Opens/closes navigation
   - Animates hamburger icon
   - Closes on link click

2. **Smooth Scrolling**
   - For anchor links
   - Smooth scroll behavior

3. **Header Scroll Effect**
   - Increases shadow on scroll
   - Enhances depth perception

4. **Active Link Highlighting**
   - Automatically sets active class
   - Based on current page

5. **Lazy Loading**
   - Intersection Observer API
   - For future image optimization

## Responsive Breakpoints

### Mobile: ≤ 768px
- Single column layouts
- Hamburger menu
- Stacked buttons
- Reduced padding/margins

### Tablet: 769px - 1024px
- Two-column grids
- Horizontal navigation
- Adjusted spacing

### Desktop: > 1024px
- Full multi-column layouts
- Maximum content width: 1200px
- Optimal spacing and typography

## Design Principles

### Color Usage
- **Primary brand color**: Headers, navigation
- **Accent colors**: Buttons, highlights
- **Neutral colors**: Text, backgrounds
- **Gradients**: Hero sections, CTAs

### Typography
- **Primary font**: Georgia (serif) - body text
- **Secondary font**: Helvetica Neue (sans-serif) - UI elements
- **Hierarchy**: Clear size differentiation

### Spacing
- Consistent use of CSS variables
- Multiples of base spacing unit
- Responsive adjustments

### Shadows
- Subtle elevation for cards
- Increased on hover
- Enhanced on scroll (header)

## Template Replication

### Creating New Pages
1. Copy `index.html` structure
2. Update `<title>` tag
3. Update active navigation link
4. Replace main content section
5. Keep header and footer identical

### Maintaining Consistency
- Always use CSS variables
- Follow established spacing patterns
- Maintain navigation structure
- Keep footer content synchronized

## Future Enhancements

### Planned Features
- Search functionality
- Category filtering
- Dark mode toggle
- Print stylesheets
- Accessibility improvements (ARIA labels)

### Performance Optimizations
- Image lazy loading (implemented)
- CSS/JS minification
- Asset caching headers
- Service worker (PWA)
