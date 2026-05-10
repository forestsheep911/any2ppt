---
name: deck-producer
description: Main Any2PPT coordinator for budget-aware presentation production. Use when Codex needs to turn source material, transcripts, notes, or outlines into a deck workflow; choose quick, balanced, or premium scope; coordinate story architecture, slide storyboarding, visual direction, and delivery artifacts.
---

# Deck Producer

Act as the production owner for Any2PPT deck work. Optimize for a usable presentation under real constraints: source quality, token budget, time, image generation cost, and requested output.

## Workflow

1. Identify the user's source material and desired output. If the source is a `.pdf` or an `http(s)` URL, route through `document-ingestor` first to produce `source/input.md`.
2. Choose a **production mode**: `image-first`, `pptx-native`, or `hybrid`. Mode is picked **before** budget.
3. Choose a **budget mode**: `quick`, `balanced`, or `premium`. The default when the user is silent is `balanced`.
4. Select the minimum specialist workflow needed.
5. Keep intermediate artifacts in predictable paths.
6. Apply quality gates before calling the work done.

Use `../../references/workflow.md` for the production flow and `../../references/budget-modes.md` for budget decisions.

## Production Mode

Mode decides what kind of artifact the deck eventually becomes; budget decides how thoroughly each step is executed. Skipping mode selection forces every run into image-first by default, because `visual-director` defaults to writing image prompts.

Three modes:

- **image-first** — `visual-director` writes complete per-slide image prompts; the final deck is a sequence of generated full-slide images. Use when visual polish matters more than downstream editing.
- **pptx-native** — `visual-director` writes layout, chart, table, and image needs (no full image prompts). The final deck is an editable PowerPoint file assembled by `pptx-assembler` (V2 work; the V1 `any2ppt-dev pptx draft` subcommand is an experimental two-archetype prototype, not a production assembler — see [docs/pptx-native-experiment.md](../../../../docs/pptx-native-experiment.md)). Use when the user wants to keep editing in PowerPoint.
- **hybrid** — combination. Each slide is explicitly tagged image-first or pptx-native in the storyboard. Use when some slides need visual polish and others need editability.

Mode selection rules:

- If the user states "I need a PowerPoint I can edit" or asks for `.pptx`, choose `pptx-native`.
- If the user states "I need slides as images" or asks for visual polish, choose `image-first`.
- If the user is silent, ask once. Do not silently default. If asking is impossible, default to `image-first` and record the default choice in `run.json` and the brief's "Skill Notes" section.

Mode affects specialist output:

- `image-first` → `visual-director` produces `prompts/README.md` + `prompts/<slide-id>.md`.
- `pptx-native` → `visual-director` produces `work/layouts.md` (per-slide layout, chart, table, image needs) instead of full image prompts.
- `hybrid` → `visual-director` produces both `prompts/<slide-id>.md` and `work/layouts.md`, with the storyboard tagging which slides go which way.

Record the chosen mode in:

- `run.json` (when the dev tool created the run folder).
- The deck brief's "Skill Notes" section.
- The first line of `prompts/README.md` or `work/layouts.md`.

## Source Inputs (V1)

V1 accepts three source kinds, all normalized into `source/input.md` inside the run folder:

- Text or Markdown files (`.md`, `.markdown`, `.txt`) — copied directly.
- `.pdf` files — routed through `document-ingestor` for text extraction.
- `http(s)` URLs — routed through `document-ingestor` for HTML-to-Markdown.

Standard local run shape:

- `source/input.md` (or `source/input.txt` for raw text)
- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md` and `prompts/<slide-id>.md` (image-first / hybrid)
- `work/layouts.md` (pptx-native / hybrid)
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

Image-first mode (default if mode cannot be confirmed):

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`

PPTX-native mode:

- `work/deck-brief.md`
- `work/storyboard.md`
- `work/layouts.md`
- `dist/<deck-name>.pptx` (when `pptx-assembler` is available)

Hybrid mode produces both `prompts/<slide-id>.md` and `work/layouts.md`.

For v1, prefer these text artifacts over heavy automation. Do not require PPTX assembly, YouTube ingestion, document parsing, or a local UI unless the user explicitly asks for that expansion.

## Quality Gates

Before delivery, verify that:

- The deck has one clear central thesis.
- Each slide has one primary job.
- Slide titles are specific and presentable.
- The sequence has a logical arc.
- Visual direction supports the argument.
- The chosen workflow fits the user's budget and timing.
- Production mode is recorded in `run.json` and the brief's "Skill Notes".

Run the gate by either reading every artifact and checking each item by hand, or (preferred when available) by running `any2ppt-dev review --run <name>` and archiving the output to `dist/review.md`. Do not declare delivery without one of the two.
