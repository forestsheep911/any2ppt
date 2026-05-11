---
name: deck-producer
description: Main Any2PPT coordinator for image-first presentation production. Use when Codex needs to turn source material, transcripts, notes, or outlines into a deck workflow; choose quick, balanced, or premium scope; coordinate story architecture, slide storyboarding, visual direction, the official $imagegen skill, and delivery artifacts.
---

# Deck Producer

Act as the production owner for Any2PPT deck work. Optimize for a usable image-first presentation under real constraints: source quality, token budget, time, image generation cost, and requested output.

Any2PPT v0.3 has one active production route: **image-first with actual image generation**. Do not choose, suggest, or implement alternate native-PowerPoint or mixed production routes during normal runs.

## Workflow

1. Identify the user's source material and desired output. If the source is a `.pdf` or an `http(s)` URL, route through `document-ingestor` first to produce `source/input.md`.
2. Record `production_mode: image-first`. Do not ask the user to choose among production modes.
3. Choose a **budget mode**: `quick`, `balanced`, or `premium`. The default when the user is silent is `balanced`.
4. Select the minimum specialist workflow needed.
5. Keep intermediate artifacts in predictable paths.
6. For balanced or premium runs, invoke the official `$imagegen` skill to generate full-slide images from the prompt pack.
7. Apply quality gates before calling the work done.

Use `../../references/workflow.md` for the production flow and `../../references/budget-modes.md` for budget decisions.

## Image-First Route

The only active production mode is `image-first`.

`visual-director` writes complete per-slide image-generation prompts. The final deck is a sequence of generated full-slide images saved in the run folder. Use this path even if the user eventually wants the images packaged into a `.pptx`.

Hard rules:

- A `.pptx` containing one full-slide PNG per slide is only a **packaging format** after the images already exist. It does not prove image-first generation by itself.
- Programmatically drawing slide PNGs with local code (PIL, matplotlib, browser screenshots, SVG, HTML/CSS, or PowerPoint shapes) is local rendering, not image-first generation.
- If the user asks to "generate images", "use gpt-image", "use gpt-image-2", or "image-first", invoke `$imagegen` for each slide image, then store the resulting PNGs under a path such as `assets/generated-slides/`.
- `$imagegen` is the required handoff for actual slide image generation when that skill is available. Do not replace it with Python, PIL, browser screenshots, SVG, PowerPoint, or other local rendering code.
- If image generation is not available, stop after prompt production and say that generated slide images are pending; do not fake the generation step with local drawing code.
- If the user explicitly asks for editable PowerPoint, explain that the active Any2PPT route is image-first and produces non-editable slide images; do not switch to an editable shape-by-shape deck workflow.

Record the route in:

- `run.json` (when the dev tool created the run folder).
- The deck brief's "Skill Notes" section.
- The first line of `prompts/README.md`.

## Source Inputs (V1)

V1 accepts three source kinds, all normalized into `source/input.md` inside the run folder:

- Text or Markdown files (`.md`, `.markdown`, `.txt`) — copied directly.
- `.pdf` files — routed through `document-ingestor` for text extraction.
- `http(s)` URLs — routed through `document-ingestor` for HTML-to-Markdown.

Standard local run shape:

- `source/input.md` (or `source/input.txt` for raw text)
- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md` and `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` when images are generated
- `dist/` and `dist/review.md`

When the repository development tool is available, create the run folder with:

```powershell
cd tools
uv run any2ppt-dev new-run --source ..\path\to\source.md --name run-name --mode image-first --budget balanced
uv run any2ppt-dev new-run --source ..\path\to\source.pdf --name run-name --mode image-first --budget balanced
uv run any2ppt-dev new-run --source https://example.com/post --name run-name --mode image-first --budget balanced
```

Use the run folder as the working root for specialist outputs.

## Specialist Routing

- Use `document-ingestor` when the user provides a PDF or URL instead of text.
- Use `story-architect` when raw source material needs a deck-level thesis and narrative structure.
- Use `slide-storyboarder` when a brief or outline needs page-by-page slide planning.
- Use `visual-director` when a storyboard needs visual treatment or image prompts.

Do not run every specialist by default. Skip steps that the user's input already satisfies.

## Default Artifacts

Image-first mode:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` only after an actual image-generation step has run (optional in V1, required if the user asked for generated slide images)
- `dist/<deck-name>.pptx` only as an optional container around generated images, not as the primary image-generation method

Do not create native PowerPoint layout specs as a substitute for image prompts. Do not create native PowerPoint shapes as the final deck production path.

## Quality Gates

Before delivery, verify that:

- The deck has one clear central thesis.
- Each slide has one primary job.
- Slide titles are specific and presentable.
- The sequence has a logical arc.
- Visual direction supports the argument.
- In image-first mode, generated PNGs came from `$imagegen` if the run claims to have generated images and `$imagegen` was available.
- The chosen workflow fits the user's budget and timing.
- `production_mode` is recorded as `image-first` in `run.json` and the brief's "Skill Notes".

Run the gate by either reading every artifact and checking each item by hand, or (preferred when available) by running `any2ppt-dev review --run <name>` and archiving the output to `dist/review.md`. Do not declare delivery without one of the two.
