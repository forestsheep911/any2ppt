---
name: story-architect
description: Build the narrative foundation for Any2PPT decks. Use when source material, transcripts, notes, or articles need to become a presentation thesis, audience framing, narrative arc, and section-level deck brief before slide planning.
---

# Story Architect

Turn source material into a deck-level argument. Preserve the user's intent, but remove tangents that do not serve the presentation.

## Output

Write a deck brief, usually at `work/deck-brief.md`, with:

- Source summary.
- Intended audience.
- Presentation goal.
- Central thesis.
- Narrative arc.
- Section outline.
- Material to exclude or compress.
- Risks, assumptions, or fact-check needs.
- Skill Notes (optional last section): record decisions that affect downstream specialists, including the chosen production mode and budget mode, deviations from defaults, and any limitations of the source.

Do not write slide titles or visual descriptions in the brief; those are the jobs of `slide-storyboarder` and `visual-director`.

## Guidance

- Prefer a clear argument over exhaustive coverage.
- Keep the thesis specific enough that slide titles can derive from it. A working test: the thesis should survive the deck being shortened to a single slide.
- Preserve important nuance, but convert long discussion into presentable claims.
- Flag source gaps instead of inventing support.
- When the source is long, summarize by argument relevance, not by chronology alone.
- If the source is dominated by negation ("what not to do"), propose at least one positive framing in the brief so the storyboard does not inherit a negative tone by default.
- If the source is too thin to support a deck (single paragraph, placeholder content, etc.), say so in the brief and recommend either aborting the run or finding a richer source. Do not invent a deck around an empty source.

## Reference Sample

See `../../assets/sample-decks/sanmiao-victory-day/brief.md` for a brief whose central thesis was deliberately compressible into one slide (`01_core_thesis.md` of the same sample). The brief demonstrates how to declare audience, presentation goal, narrative arc, and material-to-exclude in a way that downstream specialists can act on without re-reading the source.
