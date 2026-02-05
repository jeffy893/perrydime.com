# Music Page Testing Guide

## Quick Start

### 1. Start Local Server
```bash
cd perrydime.com
python3.10 serve_local.py
```

Server will run at: **http://localhost:8000**

### 2. Navigate to Music Page
Open in browser: **http://localhost:8000/music.html**

---

## Testing Checklist

### ✅ Visual Layout
- [ ] Header displays "Perry Dime" with tagline
- [ ] Navigation shows: Home, Publications, Art, Dreams, Music
- [ ] "Music" link is highlighted/active
- [ ] Hero section displays "Music" title
- [ ] Music grid displays 13 track cards
- [ ] Footer shows contact info and social links

### ✅ SoundCloud Embeds
- [ ] All 13 tracks display SoundCloud player
- [ ] Track titles appear below each embed
- [ ] Players show album artwork
- [ ] Play buttons are functional
- [ ] Volume controls work
- [ ] Share buttons visible

### ✅ Responsive Design

#### Desktop (>1024px)
- [ ] Grid shows 3 columns
- [ ] Cards have consistent spacing
- [ ] Hover effects work (lift + shadow)
- [ ] Navigation is horizontal

#### Tablet (769-1024px)
- [ ] Grid shows 2 columns
- [ ] Cards resize appropriately
- [ ] Navigation remains horizontal

#### Mobile (≤768px)
- [ ] Grid shows 1 column
- [ ] Hamburger menu appears
- [ ] Menu toggles on click
- [ ] Cards stack vertically
- [ ] Embeds resize to fit screen

### ✅ Navigation
- [ ] Clicking "Home" goes to index.html
- [ ] Clicking "Music" stays on music.html
- [ ] Footer links work correctly
- [ ] Social icons link to correct profiles

### ✅ Styling
- [ ] Colors match logo palette
- [ ] Fonts are consistent
- [ ] Spacing is uniform
- [ ] Shadows appear on hover
- [ ] Transitions are smooth (0.3s)

### ✅ Performance
- [ ] Page loads quickly
- [ ] No console errors
- [ ] Images load properly
- [ ] SoundCloud embeds load
- [ ] Smooth scrolling works

---

## Track List Verification

Verify all 13 tracks are present:

1. ✅ Dont Let Go (1472220244)
2. ✅ Fight The Day (1473702832)
3. ✅ What Do You Got To Say (1472747476)
4. ✅ Intro - Testing the Water (1428883423)
5. ✅ Devestate Economies - Smith (1428883402)
6. ✅ SteppePirates - Buff (1428883381)
7. ✅ Homage And Delight (1428883255)
8. ✅ Wade in the Shore (1428883372)
9. ✅ BillionAirbitrate (1428883363)
10. ✅ Sing with Apollo (1428883387)
11. ✅ GameOfGo - Buff (1428883393)
12. ✅ Mortal Layman - Mauze (1428883345)
13. ✅ Bad Hand / Burn the Day Down - Mauze (1428883357)

---

## Browser Testing

Test in multiple browsers:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

---

## Common Issues & Solutions

### Issue: SoundCloud embeds not loading
**Solution**: Check internet connection. Embeds require external API access.

### Issue: Hamburger menu not working
**Solution**: Verify `main.js` is loaded. Check browser console for errors.

### Issue: Hover effects not working
**Solution**: Clear browser cache. Verify CSS is loaded.

### Issue: Grid layout broken
**Solution**: Check browser supports CSS Grid. Update browser if needed.

### Issue: Images not loading
**Solution**: Verify paths are correct. Check `docs/assets/` folder exists.

---

## Developer Tools Testing

### Chrome DevTools
1. Open DevTools (F12)
2. Check Console for errors
3. Use Device Toolbar for responsive testing
4. Network tab to verify all resources load
5. Lighthouse audit for performance

### Responsive Testing Sizes
- Mobile: 375px × 667px (iPhone SE)
- Tablet: 768px × 1024px (iPad)
- Desktop: 1920px × 1080px (Full HD)

---

## Accessibility Testing

### Keyboard Navigation
- [ ] Tab through all links
- [ ] Enter activates links
- [ ] Focus indicators visible
- [ ] Skip to content link works

### Screen Reader
- [ ] Header structure logical
- [ ] Alt text on images
- [ ] ARIA labels present
- [ ] Link text descriptive

### Color Contrast
- [ ] Text readable on backgrounds
- [ ] Links distinguishable
- [ ] Focus indicators visible
- [ ] Meets WCAG AA standards

---

## Performance Metrics

Target metrics:
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1

---

## Update Testing

### Adding New Track
1. Add embed to `source/productions/List-of-SoundCloud-Embed.html`
2. Run: `python3.10 upsert_music.py`
3. Verify new track appears in music.html
4. Check no duplicates created
5. Verify grid layout adjusts

---

## Sign-Off

**Tested By**: _______________  
**Date**: _______________  
**Browser**: _______________  
**Device**: _______________  
**Result**: ☐ Pass  ☐ Fail  

**Notes**:
_______________________________________
_______________________________________
_______________________________________

---

## Quick Commands

```bash
# Start server
python3.10 serve_local.py

# Update music page
python3.10 upsert_music.py

# Convert images
python3.10 convert_heic_to_png.py

# Extract colors
python3.10 extract_logo_colors.py
```

---

**Last Updated**: 2026-02-04  
**Version**: 1.0
