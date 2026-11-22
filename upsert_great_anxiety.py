#!/usr/bin/env python3
"""
Inserts the "The Great Anxiety" feature (read or listen to the audiobook) into the
home page and the publications page.

The section sits right after each page's hero and is wrapped in marker comments, so running
this again replaces it instead of adding a second copy. upsert_publications.py calls it after
regenerating publications.html.

Content mirrors story.jefferson.cloud (source:
02_jefferson.cloud/0000_TheGreatAnxiety/story-jefferson-cloud.html) and the KDP listing
(pub.perrydime.com/the-great-anxiety/KDP_LISTING.md).
"""
import re
from pathlib import Path

DOCS = Path(__file__).parent.resolve() / "docs"
PAGES = [DOCS / "index.html", DOCS / "publications.html"]

START = "<!-- great-anxiety:start -->"
END = "<!-- great-anxiety:end -->"

AMAZON = "https://www.amazon.com/gp/product/B0HRT8MGP9?ref_=dbs_m_mng_rwt_calw_tpbk_0&amp;th=1"
SPOTIFY = "https://open.spotify.com/episode/4LSzgZHxJTYgPK3bWJYWcw?si=FtKHFbmOTHW8z6cisaOI6g"
SPOTIFY_EMBED = "https://open.spotify.com/embed/episode/4LSzgZHxJTYgPK3bWJYWcw?utm_source=generator"
YOUTUBE = "https://youtu.be/ESqpSzsi2BM"
STORY = "https://story.jefferson.cloud"

SPOTIFY_LOGO = (
    '<svg viewBox="0 0 50 50" aria-hidden="true"><circle cx="25" cy="25" r="22" fill="#1ed760"/>'
    '<path d="M11 18 C 21 14.5, 32 15.5, 40 20" fill="none" stroke="#121212" stroke-width="3.6" stroke-linecap="round"/>'
    '<path d="M12.5 26 C 21 23, 30 23.8, 37 28" fill="none" stroke="#121212" stroke-width="3" stroke-linecap="round"/>'
    '<path d="M14 33 C 21 31, 28 31.6, 34 35" fill="none" stroke="#121212" stroke-width="2.5" stroke-linecap="round"/></svg>'
)
YOUTUBE_LOGO = (
    '<svg viewBox="0 0 56 40" aria-hidden="true"><rect x="2" y="2" width="52" height="36" rx="11" fill="#ff0000"/>'
    '<path d="M22 11 L38 20 L22 29 Z" fill="#ffffff"/></svg>'
)

SECTION = f"""{START}
   <section class="great-anxiety" aria-labelledby="great-anxiety-title">
    <div class="container ga-inner">
     <div class="ga-cover">
      <a href="{AMAZON}" target="_blank" rel="noopener">
       <img src="assets/img/great-anxiety-cover.jpg" alt="The Great Anxiety by Jefferson Richards, book cover" loading="lazy"/>
      </a>
     </div>
     <div class="ga-body">
      <p class="ga-kicker">Now an audiobook &middot; Book 1 of the Survitality Series</p>
      <h2 id="great-anxiety-title">The Great Anxiety</h2>
      <p class="ga-subtitle">A Decade of Thought Fat, 2016 to 2026 &middot; by Jefferson Richards</p>
      <p class="ga-hook">What do you do with ten years of thought fat?</p>
      <p class="ga-description">A memoir and an argument. From a Detroit suburb to San Diego Bay, a Boston neurosurgery ward, a Kentucky tobacco farm and a Tucson bar, it follows ten years of building language software and writing three books on language, insurance, loyalty and risk, and what it took to stay steady through a loud decade.</p>
      <div class="ga-listen">
       <p class="ga-listen-label">Listen free to the full audiobook</p>
       <iframe class="ga-spotify" title="The Great Anxiety audiobook on Spotify" src="{SPOTIFY_EMBED}" height="152" frameborder="0" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>
       <div class="ga-buttons">
        <a class="ga-btn ga-btn-spotify" href="{SPOTIFY}" target="_blank" rel="noopener">{SPOTIFY_LOGO}<span>Listen on Spotify</span></a>
        <a class="ga-btn ga-btn-youtube" href="{YOUTUBE}" target="_blank" rel="noopener">{YOUTUBE_LOGO}<span>Listen on YouTube</span></a>
       </div>
      </div>
      <p class="ga-read">Prefer to read? <a href="{AMAZON}" target="_blank" rel="noopener">Get the book on Amazon</a> &middot; <a href="{STORY}" target="_blank" rel="noopener">story.jefferson.cloud</a></p>
     </div>
    </div>
   </section>
   {END}"""

BLOCK_RE = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
HERO_END_RE = re.compile(r'(<section class="hero">.*?</section>)', re.S)


def upsert(page):
    html = page.read_text(encoding="utf-8")
    if START in html:
        html = BLOCK_RE.sub(lambda m: SECTION, html, count=1)
    else:
        m = HERO_END_RE.search(html)
        if not m:
            raise RuntimeError(f"no hero section found in {page}")
        html = html[:m.end()] + "\n   " + SECTION + html[m.end():]
    page.write_text(html, encoding="utf-8")
    print(f"  The Great Anxiety feature written to {page.name}")


def main():
    for page in PAGES:
        upsert(page)


if __name__ == "__main__":
    main()
