# Perry Dime CSS Assets

## variables.css
Foundation stylesheet containing all CSS custom properties (variables) for the site.

### Color Palette
Extracted directly from `perrydime-logo.png`:
- **Primary Colors**: Warm beige (#c8af99), dark brown (#603e29), dusty rose (#c07b7e), soft blue-gray (#a4babe)
- **Secondary Colors**: Light grays and neutrals for backgrounds and text

### Usage
Import this file first in all HTML pages:
```html
<link rel="stylesheet" href="/assets/css/variables.css">
```

Then reference variables in your CSS:
```css
.header {
  background-color: var(--color-brand);
  color: var(--color-text-on-brand);
}
```

### Available Variable Categories
- Colors (primary, secondary, semantic)
- Spacing (xs through 3xl)
- Typography (font families, sizes, weights, line heights)
- Borders & radius
- Shadows
- Transitions
- Breakpoints

### Regenerating
If the logo changes, run:
```bash
python3.10 extract_logo_colors.py
```

This will automatically update `variables.css` with the new color palette.
