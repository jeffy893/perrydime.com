---
inclusion: always
---

# Perry Dime Color Palette

## Source
All colors extracted from `source/branding/perrydime-logo.png`

## Primary Colors (Chromatic)
These are the main brand colors derived from the logo:

1. **#c8af99** - Warm Beige (primary brand color)
   - RGB: 200, 175, 153
   - HSL: 28°, 29%, 69%
   - Most prominent color (6,367 pixels)
   - Warm, earthy, sophisticated

2. **#603e29** - Dark Brown (accent)
   - RGB: 96, 62, 41
   - HSL: 22°, 40%, 26%
   - Rich, grounding color (5,140 pixels)

3. **#c07b7e** - Dusty Rose
   - RGB: 192, 123, 126
   - HSL: 357°, 35%, 61%
   - Soft, artistic accent (5,080 pixels)

4. **#a4babe** - Soft Blue-Gray
   - RGB: 164, 186, 190
   - HSL: 189°, 16%, 69%
   - Cool, calming accent (3,086 pixels)

5. **#91765f** - Medium Brown
   - RGB: 145, 118, 95
   - HSL: 27°, 20%, 47%
   - Earthy mid-tone (1,869 pixels)

## Secondary Colors (Grayscale)
Neutral colors for backgrounds and text:

1. **#eeeeee** - Light Gray (primary background)
   - RGB: 238, 238, 238
   - Most common background color (84,453 pixels)

2. **#e7e6e1** - Warm Off-White
   - RGB: 231, 230, 225
   - Subtle warm background (25,031 pixels)

3. **#494a4a** - Dark Gray (text)
   - RGB: 73, 74, 74
   - For body text

4. **#636464** - Medium Gray
   - RGB: 99, 100, 100
   - For secondary text

## CSS Variables Location
`docs/assets/css/variables.css`

## Usage Guidelines

### Brand Identity
- Primary brand color: `var(--color-brand)` → #c8af99
- Accent color: `var(--color-accent)` → #603e29

### Text
- Primary text: `var(--color-text-primary)` → #eeeeee
- Secondary text: `var(--color-text-secondary)` → #e7e6e1
- Muted text: `var(--color-text-muted)` → #999999

### Backgrounds
- Primary background: `var(--color-bg-primary)` → #ffffff
- Secondary background: `var(--color-bg-secondary)` → #f5f5f5
- Accent background: `var(--color-bg-accent)` → #c8af99

### Color Harmony
The palette creates a warm, earthy, artistic aesthetic:
- Warm beiges and browns evoke natural, organic feel
- Dusty rose adds artistic, creative touch
- Soft blue-gray provides cool balance
- Grayscale neutrals ensure readability

## Design Philosophy
The color scheme reflects Perry Dime's artistic and literary nature:
- **Warm & Inviting**: Beige and brown tones create welcoming atmosphere
- **Sophisticated**: Muted, refined colors avoid harsh contrasts
- **Artistic**: Dusty rose and blue-gray add creative flair
- **Readable**: High-contrast grayscale ensures text legibility

## Regenerating Colors
If the logo changes, run:
```bash
python3.10 extract_logo_colors.py
```

This will re-analyze the logo and update `variables.css` automatically.
