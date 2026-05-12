---
name: slide-storyboarder
description: Convert an Deckit deck brief, outline, or narrative plan into a slide-by-slide storyboard. Use when Codex needs page titles, slide purposes, core claims, support points, slide archetypes, and presenter intent before visual design.
---

# Slide Storyboarder

Convert the deck argument into page-by-page slide plans.

## Output

Write a storyboard, usually at `work/storyboard.md`, where each slide includes:

- Slide ID (see "Slide ID Format" below).
- Title.
- Primary job.
- Core claim.
- 2-4 support points.
- Recommended slide archetype.
- Presenter intent or notes when useful.

Use `../../references/slide-archetypes.md` when choosing slide types.

## Slide ID Format

Use `NN_slug`:

- `NN`: two-digit zero-padded index, starting at `00` for the cover.
- `slug`: lowercase, words joined by underscores, no spaces or hyphens.

Examples: `00_cover`, `03_production_team`, `07_closing`.

`visual-director` and any later assembler reuse this ID directly as the prompt or layout filename, so any drift breaks the prompts → storyboard mapping.

## Guidance

- Give each slide one job.
- Write titles that can be spoken aloud by a presenter, and keep titles under 80 characters (the `deckit-dev review` tool warns above this).
- Avoid repetitive slide structures unless the repetition has a purpose.
- Keep support points short enough to become slide text.
- Include transitions when the deck's logic could feel abrupt.
- Do not write visual descriptions, palette choices, or image prompts; that is the job of `visual-director`.

## Slide Count Bands

Default: one slide per section in the deck brief; merge or split only when an explicit reason is recorded in the storyboard.

Target slide counts per budget mode:

- `quick`: 5-7 slides
- `balanced`: 7-10 slides
- `premium`: 8-14 slides

The `deckit-dev review` tool warns when the storyboard's slide count is outside the band for the chosen budget. A documented exception is allowed (record the reason in the storyboard's Deck Meta or in the brief's Skill Notes).

## Support Point Counts by Archetype

The default rule is 2-4 support points per slide. Some archetypes break this rule on purpose:

- `cover` and `closing`: not constrained — these slides carry composition elements (subtitle, source line, takeaways) that are not arguments.
- `process`: 2-7 (steps may legitimately exceed 4).
- `evidence cards`: 2-10 (a card grid may carry many small items).
- `timeline`: 2-10 (dated entries).
- `thesis`: 2-6 (multiple pillars allowed).
- All other archetypes: 2-4.

The `deckit-dev review` tool enforces these per-archetype bands; treat its warnings as evidence to either reshape the slide or document the exception.
