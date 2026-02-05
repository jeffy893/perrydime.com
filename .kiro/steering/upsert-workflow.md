---
inclusion: always
---

# Upsert Workflow for Perry Dime Website

## Core Principle
When making changes to the perrydime.com website, always prefer **targeted updates** over full regeneration.

## Upsert Process

### Step 1: Analyze Source Content
- Identify which source folder(s) contain new or updated content
- Determine the content type (publications, art, dreams, music)
- Parse the content structure and metadata

### Step 2: Locate Target in docs/
- Find the corresponding HTML file(s) in `docs/`
- Identify the specific section(s) that need updating
- Preserve surrounding content and structure

### Step 3: Perform Upsert
- **Insert**: Add new content if it doesn't exist
- **Update**: Modify existing content if it has changed
- **Preserve**: Keep unchanged content intact
- Maintain consistent formatting and styling

### Step 4: Update Navigation/Index
- Update any index pages or navigation menus
- Ensure links are correct and functional
- Maintain alphabetical or chronological ordering as appropriate

### Step 5: Verify Integrity
- Check that all links work
- Ensure styling is consistent
- Verify no content was accidentally removed

## When to Regenerate
Only regenerate the entire site when:
- Explicitly requested by the user
- Major structural changes are needed
- The existing structure is fundamentally incompatible with new requirements

## Best Practices
1. Always read the existing `docs/` content before making changes
2. Use precise string replacement or DOM-like operations
3. Maintain existing CSS classes and IDs
4. Preserve meta tags and SEO elements
5. Keep backup comments in HTML for reference points
6. Document significant structural changes

## Example Upsert Scenarios

### Adding a New Publication
1. Read source file from publications folder
2. Parse title, date, content
3. Find insertion point in `docs/publications.html`
4. Insert new entry maintaining sort order
5. Update index/navigation if needed

### Updating Existing Content
1. Identify changed source file
2. Locate corresponding section in `docs/`
3. Replace only the changed content
4. Preserve surrounding HTML structure

### Removing Content
1. Identify removed source file
2. Find and remove corresponding section in `docs/`
3. Update navigation/index
4. Ensure no broken links remain
