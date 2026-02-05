---
inclusion: manual
---

# Footer Configuration

## Contact Information

### Email
**Jefferson@richards.plus**
- Primary contact email
- Used in "Connect" section of footer
- Mailto link for direct email

## Social Media Links

### Instagram
- **URL**: https://instagram.com/jefferson.cloud
- **Icon**: White Instagram icon from simpleicons.org
- **Location**: Footer "About" section (icon) and "Connect" section (text link)

### LinkedIn
- **URL**: https://www.linkedin.com/in/jefferson-richards/
- **Icon**: White LinkedIn icon from simpleicons.org
- **Location**: Footer "About" section (icon) and "Connect" section (text link)

### GitHub
- **URL**: https://github.com/jeffy893
- **Icon**: White GitHub icon from simpleicons.org
- **Location**: Footer "About" section (icon) and "Connect" section (text link)

## Footer Structure

### Three Columns

1. **About Perry Dime** (Left)
   - Description text
   - Social media icons (circular buttons)
   - Hover effects with lift animation

2. **Explore** (Center)
   - Navigation links to all main pages
   - Home, Publications, Art, Dreams, Music

3. **Connect** (Right)
   - Email address (mailto link)
   - Social media text links
   - All open in new tabs

### Footer Bottom
- Copyright notice: © 2026 Perry Dime. All rights reserved.
- Centered text
- Subtle opacity

## Social Icons Styling

### Design
- Circular buttons (40px × 40px)
- White icons (20px × 20px)
- Semi-transparent background: rgba(255, 255, 255, 0.1)
- Hover: Increased opacity + lift effect

### CSS Classes
- `.social-links` - Container (flexbox)
- `.social-links a` - Individual icon buttons
- `.social-links img` - Icon images

### Icon Source
Using Simple Icons CDN for consistent, high-quality icons:
- `https://cdn.simpleicons.org/instagram/white`
- `https://cdn.simpleicons.org/linkedin/white`
- `https://cdn.simpleicons.org/github/white`

## Responsive Behavior

### Desktop (> 768px)
- Three-column layout
- Icons and text links both visible

### Mobile (≤ 768px)
- Single column stack
- Icons remain visible
- Text links stack vertically
- Full-width touch targets

## Consistency Note

Footer structure and styling match the reference implementation from captive.integralmass.com, adapted for Perry Dime branding and contact information.
