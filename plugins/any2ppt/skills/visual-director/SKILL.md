---
name: visual-director
description: Direct the visual treatment for Any2PPT slide storyboards. Use when Codex needs per-slide visual strategy, layout guidance, or image-generation prompts for presentation slides with readable text and argument-supporting visuals.
---

# Visual Director

Turn a slide storyboard into visual treatments and image prompts.

## Output

The output depends on the production mode chosen by `deck-producer` (see `../deck-producer/SKILL.md`, "Production Mode").

For `image-first` decks, create:

- `prompts/README.md` with global style direction and source references. Its first line should record the production mode.
- `prompts/<slide-id>.md` with one complete prompt per slide.

For `pptx-native` decks, create `work/layouts.md` describing per-slide layout, visual hierarchy, chart and table needs, and image requirements. Do not write full image prompts in this mode.

For `hybrid` decks, create both, and let the storyboard tag which slide goes which way.

Reuse the slide IDs from `work/storyboard.md` verbatim as filenames (`prompts/<slide-id>.md`). Do not rename, abbreviate, or reformat slide IDs — see the "Slide ID Format" section in `../slide-storyboarder/SKILL.md`.

## Guidance

- Make visuals serve the slide's argument.
- Avoid decorative-only cinematic backgrounds.
- Prefer presentation-native forms: timelines, comparison tables, process diagrams, evidence cards, maps, charts, and structured callouts.
- Keep generated text short, large, high-contrast, and readable.
- Maintain consistent language, tone, palette, and information density across slides.
- Treat full-slide images as slide screenshots, not background art, unless the user explicitly asks otherwise.

## Reference Sample

See `../../assets/sample-decks/sanmiao-victory-day/` for an image-first sample that fixes palette and typography globally and bans common generator failures explicitly. Reuse the per-slide structure (Meta / Visual Concept / Composition / Text to Render / Style / Negative) and the practice of repeating the exact characters to render in a "Text to Render" block.
