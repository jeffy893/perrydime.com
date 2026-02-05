# Perry Dime Website Project Context

## Project Overview
- **Repository**: perrydime.com
- **Domain**: perrydime.com
- **Full Title**: Perry Dime: Publications, Art, Dreams, and Music
- **Output Directory**: `docs/` (in repository root)
- **Site Type**: Static website

## Project Goals
Generate and maintain a static website that showcases Perry Dime's creative works including publications, art, dreams, and music.

## Technical Specifications
- All website output must be contained within the `docs/` folder
- Static HTML/CSS/JS structure
- Hosted at perrydime.com

## Change Management Directive
**PRIMARY DIRECTIVE**: Future modifications should follow an "upsert" pattern:
1. Read content from "source" folders in the repository root
2. Perform targeted updates (upsert operations) to the HTML structure in `docs/`
3. **DO NOT** regenerate the entire site from scratch unless explicitly requested
4. Preserve existing structure and only modify/add content as needed

## Workflow Pattern
1. Identify source content in root-level folders
2. Parse and process source content
3. Update corresponding sections in `docs/` HTML files
4. Maintain consistency across the site structure
5. Preserve custom styling and navigation elements

## Content Sources
Source content will be provided from folders in the repository root. These should be monitored for:
- New content additions
- Content updates
- Content removals

The upsert operation should intelligently merge changes without destroying the existing site architecture.
