# Any2PPT Workflow

## Image-First Flow

Any2PPT v0.3 has one active route: `image-first`.

The output sequence is:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` when actual image generation is performed
- optional `dist/<deck-name>.pptx` only as a non-editable container around generated PNGs

In this workflow, "image" means an actual image-generation step through the official `$imagegen` skill. A PowerPoint file with full-slide PNGs is only an optional delivery container after the PNGs are generated. Do not interpret image-first as "draw slides with PIL/canvas/HTML/SVG and insert them into PPTX."

Do not offer alternate native-PowerPoint or mixed production routes as active choices. If the user asks for editable PowerPoint, explain that this plugin currently produces generated slide images, optionally packaged into PPTX as non-editable full-slide images.

Do not delegate an Any2PPT run to installed presentation/PPTX skills or plugins, even if they are available locally. This includes Codex `Presentations` and Anthropic `pptx`. Those skills are native-PPTX assemblers and conflict with the active v0.3 route.

## Default Flow

1. `deck-producer` interprets the request, source, target output, and budget; it records `production_mode: image-first`.
2. If the source is a `.pdf` or an `http(s)` URL, `document-ingestor` converts it into `source/input.md`.
3. `story-architect` creates `work/deck-brief.md` when the source needs argument shaping.
4. `slide-storyboarder` creates `work/storyboard.md`.
5. `visual-director` creates model-ready image prompts in `prompts/*.md`.
6. If the user requested actual generated slides and `$imagegen` is available, invoke `$imagegen` once per slide prompt and save the resulting PNGs under `assets/generated-slides/`. If `$imagegen` is unavailable, stop at the prompt pack and report that generated images are pending.
7. `deck-producer` performs a final quality check (manual checklist or `any2ppt-dev review`) and summarizes deliverables.

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
uv run any2ppt-dev new-run --source <text-or-pdf-or-url> --name <run-name> --budget <budget>
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
- If another installed presentation/PPTX skill offers to help, do not route to it. Keep the run inside Any2PPT's own skill chain and `$imagegen`.

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
