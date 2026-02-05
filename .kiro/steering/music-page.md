---
inclusion: always
---

# Music Page Implementation

## Overview
The Music page displays SoundCloud embeds in a responsive grid layout, showcasing Perry Dime's musical compositions and sonic explorations.

## Source Data
- **Source File**: `source/productions/List-of-SoundCloud-Embed.html`
- **Track Count**: 13 tracks
- **Format**: SoundCloud iframe embeds

## Implementation Details

### Python Script: `upsert_music.py`
- **Purpose**: Extract SoundCloud embeds and generate/update music.html
- **Upsert Logic**: 
  - Reads existing music.html if present
  - Extracts track IDs from source file
  - Only adds new tracks (prevents duplicates)
  - Preserves existing HTML structure
- **Track Extraction**: Uses BeautifulSoup to parse iframe src attributes
- **Title Extraction**: Parses track titles from SoundCloud URLs

### HTML Structure: `docs/music.html`
- **Layout**: Full page with header, hero, music grid, footer
- **Grid Container**: `.music-grid` with responsive columns
- **Track Items**: `.music-item` containing iframe and `.music-info`
- **Data Attributes**: Each item has `data-track-id` for future updates

### CSS Styling: `docs/assets/css/style.css`
- **Grid Layout**: 
  - Desktop: auto-fit columns (min 350px)
  - Tablet: 2 columns
  - Mobile: 1 column
- **Card Design**: White background, rounded corners, shadow effects
- **Hover Effects**: Lift animation (translateY -3px) with enhanced shadow
- **Responsive**: Breakpoints at 768px and 1024px

## Track List
1. Dont Let Go (1472220244)
2. Fight The Day (1473702832)
3. What Do You Got To Say (1472747476)
4. Intro - Testing the Water (1428883423)
5. Devestate Economies - Smith (1428883402)
6. SteppePirates - Buff (1428883381)
7. Homage And Delight (1428883255)
8. Wade in the Shore (1428883372)
9. BillionAirbitrate (1428883363)
10. Sing with Apollo (1428883387)
11. GameOfGo - Buff (1428883393)
12. Mortal Layman - Mauze (1428883345)
13. Bad Hand / Burn the Day Down - Mauze (1428883357)

## Future Updates
To add new tracks:
1. Add new SoundCloud embed to `source/productions/List-of-SoundCloud-Embed.html`
2. Run `python upsert_music.py`
3. Script will automatically detect and add only new tracks

## Design Consistency
- Uses color palette from `docs/assets/css/variables.css`
- Matches card styling from homepage
- Consistent header/footer across all pages
- Mobile-responsive with hamburger menu

## Testing Checklist
- [x] All 13 tracks display correctly
- [x] SoundCloud embeds are functional
- [x] Grid layout responsive on mobile/tablet/desktop
- [x] Hover effects work smoothly
- [x] Navigation link from homepage works
- [x] Footer links are correct
- [x] Page loads without errors

## Notes
- SoundCloud embeds require internet connection to display
- Track IDs are preserved in data attributes for future reference
- Iframe height set to 300px for consistent appearance
- Visual mode enabled in SoundCloud player for artwork display
