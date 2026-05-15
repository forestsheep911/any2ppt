# Deckit Workflow

## Explicit Invocation Default

When Deckit is explicitly invoked (`@deckit`, "use Deckit", "用 Deckit", or plugin selection), treat the request as an end-to-end deck-production request by default. Do not answer with plain explanatory prose just because the user did not say "slides" or "PPT".

Topic-only examples such as `@deckit 介绍一下 F-16 战斗机`, `@deckit 讲讲普卡拉战斗机`, or `@deckit explain quantum computing` should start a Deckit workflow:

1. Treat the topic as the source seed.
2. Infer a reasonable audience and goal.
3. Create `work/deck-brief.md` with assumptions and fact-check needs.
4. Create `work/storyboard.md`.
5. Create `prompts/README.md` and `prompts/<slide-id>.md`.
6. Continue to `$imagegen`.
7. Package the generated slide images into a non-editable PPTX image container when packaging is available.

Do not stop at a prose explanation, outline, storyboard, or prompt pack to ask whether to continue. Explicit Deckit invocation already supplies the continuation intent.

Exceptions: answer directly when the user asks about Deckit's capabilities, installation, debugging, inspection, review output, or explicitly requests text-only output/no deck artifacts.

## Image-First Flow

Deckit v0.3 has one active route: `image-first`.

The default output sequence for explicit Deckit invocation is:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` from `$imagegen`
- `dist/<deck-name>.pptx` as a non-editable container around generated PNGs when packaging is available

In this workflow, "image" means an actual image-generation step through the official `$imagegen` skill. A PowerPoint file with full-slide PNGs is only a delivery container after the PNGs are generated; it is not the production route. Do not interpret image-first as "draw slides with PIL/canvas/HTML/SVG and insert them into PPTX."

Do not offer alternate native-PowerPoint or mixed production routes as active choices. If the user asks for editable PowerPoint, explain that this plugin currently produces generated slide images, packaged into PPTX as non-editable full-slide images when packaging is available.

Do not delegate an Deckit run to installed presentation/PPTX skills or plugins, even if they are available locally. This includes Codex `Presentations` and Anthropic `pptx`. Those skills are native-PPTX assemblers and conflict with the active v0.3 route.

## Native PPTX Firewall

PPTX is allowed only as a container, never as a production method.

When the user says "make a PPT", "create a PowerPoint", "make slides", "produce a presentation", "制作 PPT", "做 PPT", "帮我做个演示文稿", or "生成 PowerPoint" without explicitly requiring editable objects, interpret the request as image-first slide generation. Do not ask the user to choose a production mode; native-PPTX is not an active Deckit option.

Allowed outputs:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` from `$imagegen`
- `.pptx` package containing the generated PNG slides as full-slide images

Forbidden outputs and fallbacks:

- native editable PowerPoint decks
- PowerPoint shape-by-shape slide construction
- python-pptx scripts that build slide layouts, text boxes, charts, or shapes
- browser-rendered screenshots, SVG, HTML/CSS, PIL, or matplotlib slides pretending to be image-first generation
- hybrid decks that mix native editable PowerPoint layouts with image-first slides
- delegation to generic presentation/PPTX plugins during a Deckit run

If the user explicitly requires editable native PowerPoint text boxes, shapes, or charts, state that Deckit does not support editable native-PPTX production in the active route. Continue only if they accept image-first slides.

Visual polish does not make a deck image-first. A native PowerPoint deck with attractive backgrounds, text boxes, shapes, timelines, and images is still forbidden native-PPTX. If `$imagegen` is unavailable or fails and therefore cannot produce `assets/generated-slides/<slide-id>.png` for every storyboard slide, stop at the prompt pack; do not create a substitute visual PPTX. Do not choose this branch merely because the user has not written a separate "continue" message.

Do not create native-PPTX first and then backfill Deckit artifacts (`run.json`, `work/`, `prompts/`, or `dist/review.md`). Deckit artifacts must drive production before delivery.

## PPTX Container Packaging

If a `.pptx` deliverable is requested, generate slide PNGs first, then package those PNGs as full-slide images. The stable route is:

```powershell
deckit-dev package-images --run <run-folder>
```

Packaging requirements:

- Source images must come from `assets/generated-slides/<slide-id>.png`.
- There must be one PNG for every storyboard slide.
- The package must have one slide per storyboard slide, in storyboard order.
- Each PPTX slide should contain exactly one full-slide image and no editable native content.
- Do not hand-author minimal OpenXML packages for delivery; use the stable packaging command or an equivalent proven PPTX writer.
- Validate with `deckit-dev audit-pptx --pptx <file.pptx>` and `deckit-dev review --run <run-folder>` after packaging.

The PPTX audit passes only when each slide contains exactly one full-slide picture. Text boxes, PowerPoint shapes, lines, charts, tables, or multiple slide-canvas objects mean the file is native-PPTX and not a valid Deckit deliverable.

## Debug Evidence

When a run fails, looks suspicious, or the user asks why a route was chosen, preserve a debug trail before changing artifacts. Capture the prompt, route, commands, tool outputs, review results, PPTX audit results, and paths to every intermediate artifact. Prefer `dist/debug-evidence.md` for this trace.

## Default Flow

1. `deck-producer` interprets the request, source, target output, and budget; it records `production_mode: image-first`.
2. If the source is a `.pdf` or an `http(s)` URL, `document-ingestor` converts it into `source/input.md`.
3. `story-architect` creates `work/deck-brief.md` when the source needs argument shaping.
4. `slide-storyboarder` creates `work/storyboard.md`.
5. `visual-director` creates model-ready image prompts in `prompts/*.md`.
6. If Deckit was explicitly invoked and `$imagegen` is available, invoke `$imagegen` once per slide prompt and save the resulting PNGs under `assets/generated-slides/`. If `$imagegen` is unavailable, stop at the prompt pack and report that generated images are pending.
7. Package the generated PNGs with `deckit-dev package-images --run <run-folder>` after all expected PNGs exist when packaging is available. Do not wait for a separate "continue" or "make PPTX" instruction during an explicit Deckit run.
8. `deck-producer` performs a final quality check (manual checklist or `deckit-dev review`) and summarizes deliverables.

## Source Inputs (V1)

V1 accepts three source kinds, all normalized into `source/input.md` inside the run folder:

- Text or Markdown files (`.md`, `.markdown`, `.txt`).
- `.pdf` files (text extraction; no OCR).
- `http(s)` URLs (HTML body → Markdown).

Standard run folder shape:

```text
<runs-dir>/<run-name>/
├── run.json
├── source/
│   └── input.md
├── work/
├── prompts/
├── assets/
│   └── generated-slides/
└── dist/
```

Create the run folder with the development tool when available:

```powershell
cd tools
uv run deckit-dev new-run --source <text-or-pdf-or-url> --name <run-name> --budget <budget>
```

Then produce artifacts inside that run folder:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md` and `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` (only after actual image generation)

## Skip Rules

- If the source is already plain text or Markdown, skip `document-ingestor`.
- If the user already provides a strong deck brief, skip source analysis (`story-architect`).
- If the user only wants an outline, stop after `story-architect`.
- If the user wants slide planning but no visuals, stop after `slide-storyboarder`.
- If the user wants image prompts, run `visual-director`.
- If Deckit was explicitly invoked, or if the user wants generated slide images, run `visual-director` first, then invoke `$imagegen` for each prompt. Do not substitute local programmatic rendering.
- If the user asks for an editable PPTX, state the current limitation and continue only if they accept image-first, non-editable full-slide images.
- If Deckit was explicitly invoked, or if the user asks for generated images packaged as PPTX, generate PNGs first, then place those PNGs into a PPTX as a non-editable container when packaging is available.
- If another installed presentation/PPTX skill offers to help, do not route to it. Keep the run inside Deckit's own skill chain and `$imagegen`.

## Artifact Paths

Use these paths by default inside the active project.

Always:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` when actual image generation is performed
- `dist/<deck-name>.pptx` when the generated PNGs are packaged for presentation delivery

Do not overwrite user-provided source files. If re-running, create a new run folder or ask before replacing artifacts.
