# Perry Dime Website - Kiro Context

This `.kiro` folder contains project context and steering files for the Perry Dime website project.

## Purpose
These files guide AI assistants (like Kiro) in understanding the project structure, goals, and workflows when making changes to the website.

## Contents

### steering/project-context.md
Core project information including:
- Project overview and goals
- Technical specifications
- Primary change management directive (upsert pattern)

### steering/upsert-workflow.md
Detailed workflow for making targeted updates to the website without full regeneration:
- Step-by-step upsert process
- When to regenerate vs. update
- Best practices and examples

### steering/site-structure.md
Website structure documentation:
- Directory layout
- Content categories
- HTML structure guidelines
- Asset management

## Key Principle
**Always prefer targeted upserts over full site regeneration** unless explicitly requested or structurally necessary.

## Usage
These steering files are automatically included in Kiro's context when working on this project, ensuring consistent and intelligent updates to the website.
