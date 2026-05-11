---
name: visual-director
description: Direct the visual treatment for Any2PPT slide storyboards. Use when Codex needs per-slide visual strategy, layout guidance, or image-generation prompts for presentation slides with readable text and argument-supporting visuals.
---

# Visual Director

Turn a slide storyboard into visual treatments and model-ready image-generation prompts.

## Output

Any2PPT v0.3 has one active production route: image-first with actual image generation. Create:

- `prompts/README.md` with global style direction and source references. Its first line should record the production mode.
- `prompts/<slide-id>.md` with one complete prompt per slide.

These prompts are meant for `$imagegen`. If the run proceeds beyond prompt writing, the expected downstream artifact is `assets/generated-slides/<slide-id>.png` (or equivalent) produced by the official `$imagegen` skill. Do not replace that step with locally drawn slide images from PIL, canvas, HTML screenshots, SVG, matplotlib, or PowerPoint shapes.

Reuse the slide IDs from `work/storyboard.md` verbatim as filenames (`prompts/<slide-id>.md`). Do not rename, abbreviate, or reformat slide IDs — see the "Slide ID Format" section in `../slide-storyboarder/SKILL.md`.

## Guidance

- Make visuals serve the slide's argument.
- Avoid decorative-only cinematic backgrounds.
- Prefer presentation-native forms: timelines, comparison tables, process diagrams, evidence cards, maps, charts, and structured callouts.
- Keep generated text short, large, high-contrast, and readable.
- Maintain consistent language, tone, palette, and information density across slides.
- Treat full-slide images as slide screenshots, not background art, unless the user explicitly asks otherwise.
- Keep image-first prompts model-ready: include the intended use, visual subject, composition, exact text to render, style constraints, and negative constraints. Avoid instructions that imply the assistant should implement the slide by writing rendering code.
- If the user asks for a `.pptx` after image generation, treat it as a packaging step around already generated images; do not write native PowerPoint layout specs or local rendering code.
- Prefer prompts that explicitly say "Use case: productivity-visual" and "Asset type: 16:9 presentation slide image" so `$imagegen` receives an image task, not a PowerPoint assembly task.

## Reference Sample

See `../../assets/sample-decks/sanmiao-victory-day/` for an image-first sample that fixes palette and typography globally and bans common generator failures explicitly. Reuse the per-slide structure (Meta / Visual Concept / Composition / Text to Render / Style / Negative) and the practice of repeating the exact characters to render in a "Text to Render" block.
