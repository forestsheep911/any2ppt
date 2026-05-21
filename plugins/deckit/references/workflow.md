# Deckit Workflow

## Explicit Invocation Default

When Deckit is explicitly invoked (`@deckit`, "use Deckit", "用 Deckit", or plugin selection), treat the request as an end-to-end deck-production request by default. Do not answer with plain explanatory prose just because the user did not say "slides" or "PPT".

## Recommendation Gate

Before starting an expensive image-first run, Deckit normally pauses once with a recommended production plan. This protects users from hidden defaults while avoiding an up-front questionnaire.

Run this recommendation gate for explicit Deckit production requests unless the user already gave a complete production specification or explicitly said to use defaults / no questions / just proceed. The gate happens before run artifacts, file writes, `$imagegen`, or packaging.

The first response should recommend a single plan and stop. Include quality, slide count, final delivery target, and a coarse 3-6 section outline. Include aspect ratio only when it is likely to matter. Then ask the user to choose exactly one path:

- `A` = accept the recommendation and start production.
- `B` = show more options across the key dimensions.
- `C` = let the user add custom requirements.

Use this style:

```text
我建议这样做：
- 质量：balanced
- 页数：8 页
- 输出：PPTX（图片式非编辑容器），并自动生成 preview
- 粗大纲：时代背景 → 生平节点 → 代表实验 → 科学影响 → 后世纪念

请选择：
A 接受推荐方案，直接制作
B 展开更多选项让我挑
C 我补充自定义需求
```

If the user replies `A`, `默认`, `default`, or an equivalent acceptance, proceed using the recommended plan and record it in `work/deck-brief.md` "Skill Notes". If the user replies `B`, show the expanded preflight options below. If the user replies `C`, ask for or accept the user's custom requirements, then proceed after the custom constraints are clear enough. If the custom input is still ambiguous, ask only for the missing fields.

If the user prompt already includes useful constraints, map them into the recommendation instead of asking the user to restate them. For example: "高质量" maps to `premium`, "6 页" maps to 6 slides, "按背景/挑战/方案/案例/结论" maps to the rough outline, and "输出 PDF" maps to `pdf`.

## Expanded Preflight Options

Use expanded preflight only when the user chooses `B`, or when a `C` custom response asks to pick from options. Ask at most four items in one response:

1. Quality/budget: `quick`, `balanced` (default), or `premium`.
2. Approximate page/slide count, offered as concrete choices rather than a yes/no acceptance question.
3. A coarse 3-6 section outline and whether the user accepts it.
4. Final delivery target: `pptx` (default) or `pdf`.

If the user says to use defaults, proceed without more questions. If they answer partially, infer the rest from defaults and record the assumptions. Recommendation/preflight is allowed only before artifact production. It must not become a continuation gate between brief, storyboard, prompts, image generation, and packaging.

Aspect ratio is optional but should be included in the same compact preflight block when it is likely to matter. Default to landscape `169` for ordinary computer/projector decks. Offer common alternatives plus a custom-ratio code, but keep custom ratios within `$imagegen` / `gpt-image-2` constraints: the long-to-short ratio must be `<= 3:1`, and the eventual pixel size must use edges that are multiples of `16px`, max edge `<= 3840px`, with total pixels between `655,360` and `8,294,400`. If the user requests a custom ratio outside `1:3` through `3:1`, ask for another ratio before image generation.

Prefer a default-plus-override short-code interaction over a numbered questionnaire. Start with the default plan, then let the user reply with `默认` / `default` or only the codes they want to change. The user should not need to type item numbers such as `1 quick 2 8页`.

Short-code conventions:

- Codes must be unique within the preflight block, without relying on question numbers.
- Prefer letters and digits only; avoid punctuation and symbols in codes the user is expected to type.
- Codes are case-insensitive. Display them in uppercase, but parse by trimming whitespace and uppercasing first.
- Never use case to distinguish meanings. For example, `p` and `P` must not mean different options.
- Use semantic codes where possible: `Q` = quick, `B` = balanced, `P` = premium, `PPTX` = pptx, `PDF` = pdf, `O` = revise outline.
- Use plain numbers for page counts: `5`, `8`, `12`.
- Use plain digits for aspect ratios when offered: `169` = 16:9, `916` = 9:16, `43` = 4:3, `11` = 1:1.
- For a free custom ratio, use `R<width>BY<height>` with letters and digits only, such as `R21BY9` or `R4BY5`. Parse it case-insensitively and validate that the ratio is within `1:3` through `3:1` before proceeding.
- If a short code would conflict, lengthen it instead of adding punctuation or depending on case. For example, reserve `P` for premium and use `PPTX` for PowerPoint.
- If many options are needed, extend with Excel-style alphanumeric codes such as `A`...`Z`, `AA`, `AB`, while keeping each code unique in the displayed block.

Skip the recommendation/preflight entirely only when the user explicitly says to use defaults / no questions / just proceed, or when the user has already supplied a complete production specification and asks you to execute it. Do not ask users to restate or "confirm" information that is already present in their request. Treat custom follow-up questions as a missing-field check:

- if all key fields are present, proceed directly and record them as constraints;
- if only a few fields are missing, ask only those fields or safely fill defaults;
- only use the full options template when the user chose `B` or explicitly asked for choices.

Key fields include quality/budget, approximate page count, audience or goal, rough structure, and final delivery target. Map explicit user wording into settings instead of asking again: "高质量" → `premium`, "6 页" → `target_slide_count: 6`, "按背景/挑战/方案/案例/结论" → accepted rough outline, and "输出 PDF" → `pdf`.

Generated slide PNGs are always retained under `assets/generated-slides/`, and Deckit produces standard automatic preview artifact(s): `dist/preview.png` up to 32 slides, or numbered `dist/preview-XX.png` files above 32 slides. Do not present raw PNGs, a single PNG, or a stitched long image as final delivery choices in preflight. If the user asks for a PNG/preview/long image, keep the generated slide PNGs and the standard vertical preview artifact, but still ask for or infer only `pptx` or `pdf` as the final packaged deliverable unless the user explicitly requests a partial image-only run.

For the page-count preflight item, provide 3-4 choices with the recommended option first, plus a custom option. Examples:

- balanced/default: `标准 8 页（推荐） / 精简 5 页 / 完整 12 页 / 自定义`
- quick: `快速 5 页（推荐） / 稍完整 6 页 / 上限 7 页 / 自定义`
- premium: `完整 12 页（推荐） / 紧凑 8 页 / 深入 14 页 / 自定义`

Do not phrase the page-count item as only "建议 7-10 页，是否接受？"; that forces a yes/no answer and gives the user too little control.

Use this style for expanded options:

```text
为了避免跑偏，我先确认几个默认值。
默认：B / 8页 / PPTX / 接受粗大纲
粗大纲：时代背景 → 生平节点 → 代表实验 → 科学影响 → 后世纪念

回复“默认”直接开始；或只回复要改的短码，可多个组合：
Q = quick
P = premium
5 = 5页
12 = 12页
PDF = 输出 PDF
O = 修改粗大纲

例：q 12 pdf
=> quick，12页，输出 PDF，其余默认
```

If aspect ratio is part of the decision, keep the same punctuation-free code style:

```text
默认：B / 8页 / 169 / PPTX / 接受粗大纲
916 = 竖屏 9:16
43 = 4:3
11 = 1:1
R21BY9 = 自定义 21:9；可改成 R宽BY高，比例必须在 1:3 到 3:1 内
```

Topic-only examples such as `@deckit 介绍一下 F-16 战斗机`, `@deckit 讲讲普卡拉战斗机`, or `@deckit explain quantum computing` should start a Deckit workflow:

1. Treat the topic as the source seed.
2. Run the recommendation gate unless the user explicitly skipped questions or already gave a complete production specification; otherwise infer a reasonable audience and goal inside the recommended plan.
3. Create `work/deck-brief.md` with assumptions and fact-check needs.
4. Create `work/storyboard.md`.
5. Create `prompts/README.md` and `prompts/<slide-id>.md`.
6. Continue to `$imagegen`.
7. Package the generated slide images into the requested final delivery target and produce the standard preview image.

Do not stop at a prose explanation, outline, storyboard, or prompt pack to ask whether to continue. Explicit Deckit invocation plus the preflight answer/defaults already supplies the continuation intent.

Exceptions: answer directly when the user asks about Deckit's capabilities, installation, debugging, inspection, review output, or explicitly requests text-only output/no deck artifacts.

## Image-First Flow

Deckit v0.4 has one active route: `image-first`.

The default output sequence for explicit Deckit invocation is:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` from `$imagegen`
- the requested final delivery target; default is `dist/<deck-name>.pptx` as a non-editable container around generated PNGs
- `dist/preview.png` for decks up to 32 slides, or numbered `dist/preview-XX.png` files for longer decks, as the standard medium-size vertical preview artifact(s)

In this workflow, "image" means an actual image-generation step through the official `$imagegen` skill. A PowerPoint file with full-slide PNGs is only a delivery container after the PNGs are generated; it is not the production route. Do not interpret image-first as "draw slides with PIL/canvas/HTML/SVG and insert them into PPTX."

Do not offer alternate native-PowerPoint or mixed production routes as active choices. If the user asks for editable PowerPoint, explain that this plugin currently produces generated slide images, packaged into PPTX as non-editable full-slide images.

Do not delegate an Deckit run to installed presentation/PPTX skills or plugins, even if they are available locally. This includes Codex `Presentations` and Anthropic `pptx`. Those skills are native-PPTX assemblers and conflict with the active v0.4 route.

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

Visual polish does not make a deck image-first. A native PowerPoint deck with attractive backgrounds, text boxes, shapes, timelines, and images is still forbidden native-PPTX. If `$imagegen` is truly unavailable or fails and therefore cannot produce `assets/generated-slides/<slide-id>.png` for every storyboard slide, stop at the prompt pack; do not create a substitute visual PPTX. Do not choose this branch merely because the user has not written a separate "continue" message.

Do not treat the built-in `$imagegen` tool's lack of a destination-path argument as unavailability. In normal built-in mode, `$imagegen` saves generated images under `$CODEX_HOME/generated_images/...`; for Deckit runs, generate first, then copy or move the selected output PNGs into `<run-folder>/assets/generated-slides/<slide-id>.png`.

Do not treat a missing `deckit-dev` command as an image-generation or packaging blocker. `deckit-dev` is a source-repository development and verification helper, not a required capability of the installed Deckit plugin. Do not mention `deckit-dev` to normal users during production runs unless they are debugging Deckit itself or working from the source repository.

Do not create native-PPTX first and then backfill Deckit artifacts (`run.json`, `work/`, `prompts/`, or `dist/review.md`). Deckit artifacts must drive production before delivery.

## PPTX Container Packaging

If a `.pptx` deliverable is requested, generate slide PNGs first, then package those PNGs as full-slide images. Prefer the repository development packaging helper when it is available; otherwise use a proven local image-container packaging path such as `python-pptx`, provided it inserts exactly one full-slide PNG per slide and no editable slide content.

Packaging requirements:

- Source images must come from `assets/generated-slides/<slide-id>.png`.
- There must be one PNG for every storyboard slide.
- The package must have one slide per storyboard slide, in storyboard order.
- Each PPTX slide should contain exactly one full-slide image and no editable native content.
- Do not hand-author minimal OpenXML packages for delivery; use a proven PPTX writer.
- Validate after packaging with an automated or manual audit and keep the result in `dist/review.md` or `dist/debug-evidence.md`.

The PPTX audit passes only when each slide contains exactly one full-slide picture. Text boxes, PowerPoint shapes, lines, charts, tables, or multiple slide-canvas objects mean the file is native-PPTX and not a valid Deckit deliverable.

## PDF Delivery and Standard Preview

PDF delivery also packages generated PNGs and remains image-first:

- `pdf`: create an image-only PDF, one generated slide image per page. PDF packaging should preserve slide-image fidelity and should not JPEG-recompress or downsample generated PNGs unless the user explicitly asks for compression.

Deckit should also produce a standard preview image after generated slide PNGs exist.

Preview requirements:

- Output path: `dist/preview.png` for decks up to 32 slides; for 33+ slides, generate numbered files only, `dist/preview-01.png`, `dist/preview-02.png`, etc.
- Use generated slide PNGs in storyboard order.
- Each preview file contains at most 32 slides.
- Determine columns per preview chunk: 1-3 slides => 1 column; 4-8 slides => 2 columns; 9-15 slides => 3 columns; 16-32 slides => 4 columns.
- Fill slides left-to-right, top-to-bottom. If the final row is incomplete, leave the missing cells empty; do not center, rebalance, or add placeholders.
- Keep a fixed medium preview width and let height grow by row count; the preview is not a full-resolution long-image deliverable and only needs to show the overall deck flow clearly.

Do not use PDF or preview packaging to bypass `$imagegen`. The required source remains `assets/generated-slides/<slide-id>.png`.

## Debug Evidence

When a run fails, looks suspicious, or the user asks why a route was chosen, preserve a debug trail before changing artifacts. Capture the prompt, route, commands or local scripts, tool outputs, review results, PPTX audit results, and paths to every intermediate artifact. Prefer `dist/debug-evidence.md` for this trace.

## Default Flow

1. `deck-producer` interprets the request, source, target output, and budget; if needed, it runs the preflight gate before artifact production. It records `production_mode: image-first`.
2. If the source is a `.pdf` or an `http(s)` URL, `document-ingestor` converts it into `source/input.md`.
3. `story-architect` creates `work/deck-brief.md` when the source needs argument shaping.
4. `slide-storyboarder` creates `work/storyboard.md`.
5. `visual-director` creates model-ready image prompts in `prompts/*.md`.
6. If Deckit was explicitly invoked and `$imagegen` is available, invoke `$imagegen` once per slide prompt. In built-in mode, copy or move the generated images from `$CODEX_HOME/generated_images/...` into `assets/generated-slides/`. If `$imagegen` is truly unavailable, stop at the prompt pack and report that generated images are pending.
7. Package the generated PNGs according to `requested_output.delivery_target` after all expected PNGs exist. Use the repository packaging helper only when it is available; otherwise use a local image-container packaging path that keeps the same one-image-per-page invariant. Ensure the standard preview artifact(s) are produced: `dist/preview.png` up to 32 slides, or numbered `dist/preview-XX.png` files above 32 slides. Do not wait for a separate "continue" instruction during an explicit Deckit run.
8. `deck-producer` performs a final quality check (manual checklist or available development review helper) and summarizes deliverables.

## Source Inputs (V1)

V1 accepts three source kinds, all normalized into `source/input.md` inside the run folder:

- Text or Markdown files (`.md`, `.markdown`, `.txt`).
- `.pdf` files (text extraction; no OCR).
- `http(s)` URLs (HTML body → Markdown).

Standard run folder shape:

```text
<workdir>/outputs/<run-name>/
├── run.json
├── source/
│   └── input.md
├── work/
├── prompts/
├── assets/
│   └── generated-slides/
└── dist/
```

Output-root policy:

- Normal user runs must write artifacts under the user's active working directory, preferably `<workdir>/outputs/<run-name>/`.
- Do not write production outputs into the plugin installation directory, plugin cache, or Deckit development repository.
- Do not keep a second mirror copy of the same run under `local-runs/` when the requested deliverable already exists in the user's workspace.
- `local-runs/` is development-only scratch space for Deckit repo smoke tests.

Create the run folder under the user's workspace. In normal installed-plugin runs, it is fine to create the directory structure directly. When a source-repository development helper is available, it may scaffold the same structure, but its absence must not block production.

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
- If Deckit was explicitly invoked, or if the user asks for generated images packaged as PPTX, generate PNGs first, then place those PNGs into a PPTX as a non-editable container.
- If the user asks for PDF output, still generate PNGs first, then package the PNGs into an image-only PDF.
- If the user asks for a PNG preview or long-image style overview, do not treat it as the final delivery target; produce the standard preview artifact(s) from the generated slide PNGs (`dist/preview.png` up to 32 slides; numbered `dist/preview-XX.png` files above 32 slides) and choose/ask for PPTX or PDF as the final package.
- If another installed presentation/PPTX skill offers to help, do not route to it. Keep the run inside Deckit's own skill chain and `$imagegen`.

## Artifact Paths

Use these paths by default inside the active project.

Always:

- `work/deck-brief.md`
- `work/storyboard.md`
- `prompts/README.md`
- `prompts/<slide-id>.md`
- `assets/generated-slides/<slide-id>.png` when actual image generation is performed
- `dist/<deck-name>.pptx` or `.pdf` when the generated PNGs are packaged for the requested final delivery target
- `dist/preview.png` for decks up to 32 slides, or numbered `dist/preview-XX.png` files for longer decks, as the standard medium-size vertical preview artifact(s)

Do not overwrite user-provided source files. If re-running, create a new run folder or ask before replacing artifacts.
