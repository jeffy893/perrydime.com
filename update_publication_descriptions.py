#!/usr/bin/env python3.10
"""
Update publication descriptions to be more concise for card display.
Ensures Survitality of the Synapse mentions AI.
"""

import json
from pathlib import Path

# New concise descriptions (max ~150 characters for card display)
NEW_DESCRIPTIONS = {
    "Survitality of the Synapse": "Exploring the intersection of neurobiology, AI, and data architecture. Bridges organic neural networks with artificial intelligence and machine learning systems through systems thinking.",
    
    "Stockholm Forgiveness of Responsibility: A Futures Market": "A philosophical exploration of responsibility, insurance, and governance. Introduces 'Responsibility Futures' and the formula R = I/N (Intention/Negligence) through actuarial science and systems theory.",
    
    "Critique of Judgment": "Kant's masterwork on aesthetics, beauty, and the sublime. The third critique bridges theoretical and practical reason, examining how we judge art, nature, and purposiveness in the world.",
    
    "Relativity: The Special and General Theory": "Einstein's groundbreaking theories explained for general readers. Transforms our understanding of space, time, and gravity through clear, accessible prose by the master himself.",
    
    "Flatland: A Romance of Many Dimensions": "Abbott's satirical novella exploring dimensions, social hierarchy, and perception. A square's journey from 2D Flatland to 3D Spaceland challenges our understanding of reality.",
    
    "Letters on Natural Philosophy": "Euler's accessible introduction to physics through letters to a German princess. Covers mechanics, optics, astronomy, and sound with clarity and charm from one of history's greatest mathematicians.",
    
    "The Second Treatise of Government": "Locke's foundational work on natural rights, property, and the social contract. Essential reading for understanding liberal democracy, individual liberty, and the limits of government power.",
    
    "Meditations": "Marcus Aurelius's personal reflections on Stoic philosophy and leadership. Written as private notes by a Roman Emperor, these timeless meditations on virtue, duty, and resilience remain profoundly relevant.",
    
    "The Gallic Wars": "Caesar's firsthand account of his military campaigns in Gaul (58-50 BC). A masterclass in military strategy, political maneuvering, and classical Latin prose from one of history's greatest generals.",
    
    "The Parables of Jesus": "A collection of Jesus's teaching stories from the Gospels. These timeless parables use everyday situations to convey profound spiritual and moral truths about the Kingdom of God.",
    
    "The Prophet": "Gibran's poetic masterpiece on life, love, and the human condition. Twenty-six prose poems offering wisdom on marriage, children, work, freedom, and death with lyrical beauty."
}

def update_metadata_file(metadata_path, new_description):
    """Update a metadata JSON file with new description."""
    print(f"  Updating: {metadata_path.parent.name}")
    
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    old_desc = metadata.get('description', '')
    metadata['description'] = new_description
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"    Old length: {len(old_desc)} chars")
    print(f"    New length: {len(new_description)} chars")
    print(f"    ✓ Updated")

def main():
    """Update all publication descriptions."""
    prose_dir = Path(__file__).parent / "source" / "publications-prose"
    
    print(f"\n{'='*70}")
    print("UPDATING PUBLICATION DESCRIPTIONS")
    print(f"{'='*70}\n")
    
    # Map folder names to titles
    folder_to_title = {
        "Survitality": "Survitality of the Synapse",
        "Responsibility-futures": "Stockholm Forgiveness of Responsibility: A Futures Market",
        "Critique-of-judgment": "Critique of Judgment",
        "Einsteins-relativity": "Relativity: The Special and General Theory",
        "Flatland": "Flatland: A Romance of Many Dimensions",
        "Letters-of-euler": "Letters on Natural Philosophy",
        "second-treatise": "The Second Treatise of Government",
        "Meditations": "Meditations",
        "Gallic-wars": "The Gallic Wars",
        "Jesus-parables": "The Parables of Jesus",
        "the-prophet": "The Prophet"
    }
    
    updated_count = 0
    
    for folder_name, title in folder_to_title.items():
        folder_path = prose_dir / folder_name
        
        if not folder_path.exists():
            print(f"  ⚠️  Folder not found: {folder_name}")
            continue
        
        # Find metadata file
        metadata_files = list(folder_path.glob("*metadata.json"))
        
        if not metadata_files:
            print(f"  ⚠️  No metadata file in: {folder_name}")
            continue
        
        metadata_path = metadata_files[0]
        
        if title in NEW_DESCRIPTIONS:
            update_metadata_file(metadata_path, NEW_DESCRIPTIONS[title])
            updated_count += 1
        else:
            print(f"  ⚠️  No new description for: {title}")
    
    print(f"\n{'='*70}")
    print(f"✓ UPDATED {updated_count} DESCRIPTIONS")
    print(f"{'='*70}\n")
    print("Next step: Run upsert_publications.py to regenerate publications.html")
    print()

if __name__ == "__main__":
    main()
