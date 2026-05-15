# Deckit Workflow

## Image-First Flow

Deckit v0.3 has one active route: `image-first`.

The output sequence is:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` when actual image generation is performed
- optional `dist/<deck-name>.pptx` only as a non-editable container around generated PNGs

In this workflow, "image" means an actual image-generation step through the official `$imagegen` skill. A PowerPoint file with full-slide PNGs is only an optional delivery container after the PNGs are generated. Do not interpret image-first as "draw slides with PIL/canvas/HTML/SVG and insert them into PPTX."

Do not offer alternate native-PowerPoint or mixed production routes as active choices. If the user asks for editable PowerPoint, explain that this plugin currently produces generated slide images, optionally packaged into PPTX as non-editable full-slide images.

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
- optional `.pptx` package containing the generated PNG slides as full-slide images

Forbidden outputs and fallbacks:

- native editable PowerPoint decks
- PowerPoint shape-by-shape slide construction
- python-pptx scripts that build slide layouts, text boxes, charts, or shapes
- browser-rendered screenshots, SVG, HTML/CSS, PIL, or matplotlib slides pretending to be image-first generation
- hybrid decks that mix native editable PowerPoint layouts with image-first slides
- delegation to generic presentation/PPTX plugins during a Deckit run

If the user explicitly requires editable native PowerPoint text boxes, shapes, or charts, state that Deckit does not support editable native-PPTX production in the active route. Continue only if they accept image-first slides.

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
- Validate with `deckit-dev review --run <run-folder>` after packaging.

## Default Flow

1. `deck-producer` interprets the request, source, target output, and budget; it records `production_mode: image-first`.
2. If the source is a `.pdf` or an `http(s)` URL, `document-ingestor` converts it into `source/input.md`.
3. `story-architect` creates `work/deck-brief.md` when the source needs argument shaping.
4. `slide-storyboarder` creates `work/storyboard.md`.
5. `visual-director` creates model-ready image prompts in `prompts/*.md`.
6. If the user requested actual generated slides and `$imagegen` is available, invoke `$imagegen` once per slide prompt and save the resulting PNGs under `assets/generated-slides/`. If `$imagegen` is unavailable, stop at the prompt pack and report that generated images are pending.
7. If the user requested a `.pptx`, package the generated PNGs with `deckit-dev package-images --run <run-folder>` after all expected PNGs exist.
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
- If the user wants generated slide images, run `visual-director` first, then invoke `$imagegen` for each prompt. Do not substitute local programmatic rendering.
- If the user asks for an editable PPTX, state the current limitation and continue only if they accept image-first, non-editable full-slide images.
- If the user asks for generated images packaged as PPTX, generate PNGs first, then optionally place those PNGs into a PPTX as a non-editable container.
- If another installed presentation/PPTX skill offers to help, do not route to it. Keep the run inside Deckit's own skill chain and `$imagegen`.

## Artifact Paths

Use these paths by default inside the active project.

Always:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` when actual image generation is performed
- `dist/<deck-name>.pptx` only when the generated PNGs are optionally packaged for presentation delivery

Do not overwrite user-provided source files. If re-running, create a new run folder or ask before replacing artifacts.
