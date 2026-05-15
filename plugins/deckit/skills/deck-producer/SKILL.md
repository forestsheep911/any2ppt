---
name: deck-producer
description: Main Deckit coordinator for end-to-end image-first deck production. Use whenever Deckit is explicitly invoked, including topic-only prompts like "@deckit 介绍一下 F-16", even if the user did not say slides/PPT. Runs brief, storyboard, visual prompts, official $imagegen slide generation, review, and PPTX image-container packaging unless the user explicitly asks for text-only/no deck artifacts or a required tool is unavailable.
---

# Deck Producer

Act as the production owner for Deckit deck work. Optimize for a usable image-first presentation under real constraints: source quality, token budget, time, image generation cost, and requested output.

Deckit v0.3 has one active production route: **image-first with actual image generation, followed by review and PPTX image-container packaging**. Do not choose, suggest, or implement alternate native-PowerPoint or mixed production routes during normal runs.

## Invocation Default

When the user explicitly invokes Deckit (`@deckit`, "use Deckit", "用 Deckit", or selecting the Deckit plugin), assume they want Deckit to produce a complete presentation deliverable, not a plain prose answer.

Do not respond with "you have not asked for slides yet" when Deckit was explicitly invoked. If the user gives only a topic, turn that topic into a deck seed and start the image-first workflow.

Treat these as deck-production intents when Deckit is invoked:

- "介绍一下..."
- "讲讲..."
- "分析..."
- "总结..."
- "整理..."
- "做一下..."
- "explain..."
- "introduce..."
- "summarize..."
- "analyze..."
- "brief me on..."

Examples:

- `@deckit 介绍一下 F-16 战斗机` → produce an F-16 image-first deck end to end: brief, storyboard, prompts, generated slide PNGs, review, and a non-editable PPTX image container.
- `@deckit summarize this article` → produce an article-summary deck end to end unless the user explicitly asks only for a summary.
- `@deckit 讲讲普卡拉战斗机` → produce a topic-source deck run end to end.

Minimum default output for an explicit Deckit invocation is a complete Deckit deliverable:

1. `work/deck-brief.md`
2. `work/storyboard.md`
3. `prompts/README.md` and `prompts/<slide-id>.md`
4. `assets/generated-slides/<slide-id>.png` from the official `$imagegen` skill
5. `dist/<deck-name>.pptx` as a non-editable image container when packaging is available
6. `dist/review.md` and, for PPTX, an audit result

Do not stop at prose, a brief, a storyboard, or a prompt pack merely to ask whether to continue. Continue through `$imagegen` and packaging by default. Stop early only when the user explicitly requests a partial artifact, explicitly forbids slides/images/PPTX, or a required tool is unavailable.

Exceptions: answer directly instead of starting a deck run when the user asks what Deckit can do, asks to install/debug/inspect/review Deckit, explicitly requests text-only output, or explicitly says not to create slides/deck artifacts.

## No Continuation Gate

Deckit should not insert a user-confirmation checkpoint between normal production stages.

Forbidden during an explicit Deckit run:

- Ending the turn after a plain topic explanation with "I can turn this into slides next."
- Ending the turn after `work/storyboard.md` / `prompts/*.md` with "Say continue to generate images."
- Asking the user to confirm image generation when `$imagegen` is available and the run is not explicitly text-only.
- Asking whether to package as PPTX after all slide PNGs exist and packaging tools are available.

Instead, announce the route briefly in commentary, then continue. Budget mode may change slide count and critique depth, but it must not silently downgrade an explicit Deckit invocation into "outline only" or "prompt pack only".

## Native PPTX Firewall

PPTX is allowed only as a delivery container, never as a production method.

Never satisfy ambiguous requests such as "make a PPT", "create a PowerPoint", "make slides", "produce a presentation", "制作 PPT", "做 PPT", "帮我做个演示文稿", or "生成 PowerPoint" by creating editable native PowerPoint shapes, text boxes, charts, or layouts. Interpret ambiguous presentation requests as Deckit's image-first route:

> Create an image-first presentation: brief, storyboard, image prompts, and generated full-slide images.

Do not ask the user to choose between image-first and native-PPTX. Native-PPTX is not an active option. If the user asks for a `.pptx` file, treat it only as an optional package after `$imagegen` has produced slide PNGs; the package must contain one generated full-slide image per page and must not contain native editable slide construction.

If the user explicitly requires editable PowerPoint objects, state the limitation and do not switch routes:

> Deckit does not produce editable native-PPTX decks in the active route. I can continue with image-first full-slide images, optionally packaged into a non-editable `.pptx` container.

## No Substitute Visual PPTX

Visual polish does not make a deck image-first. A visually designed PowerPoint file is still native-PPTX if its slides contain editable text boxes, PowerPoint shapes, lines, charts, tables, or layout objects.

If `$imagegen` is unavailable or fails and `assets/generated-slides/<slide-id>.png` does not exist for every storyboard slide, do not deliver a PPTX. Stop at the prompt pack and say generated slide images are pending. Do not choose this branch merely because the user has not written a separate "continue" message.

Do not create native PowerPoint layouts as a substitute for generated images. Do not create a native-PPTX first and then backfill Deckit artifacts (`run.json`, `work/`, `prompts/`, or `dist/review.md`) to make it look like a Deckit run. Deckit artifacts must precede delivery and control the production path.

When a PPTX exists, audit it:

```powershell
deckit-dev audit-pptx --pptx <file.pptx>
```

The audit must pass with exactly one full-slide picture per slide. If it reports `PPTX-NATIVE-CONTENT`, the file is not a valid Deckit image-first deliverable.

## PPTX Packaging Discipline

A `.pptx` deliverable is allowed only after generated slide PNGs exist. Use the stable packaging route instead of inventing a PPTX writer during the run:

```powershell
deckit-dev package-images --run <run-folder>
```

Packaging requirements:

- Source images must be `assets/generated-slides/<slide-id>.png`, one for every storyboard slide.
- The package must contain one slide per storyboard slide, in storyboard order.
- Each PPTX slide must contain exactly one generated full-slide image sized to the slide canvas.
- Each PPTX slide must include speaker notes in PowerPoint's notes pane, sourced from `Speaker notes` / `Presenter notes` / `Presenter intent` in `work/storyboard.md` or synthesized from the slide's claim and support points.
- Do not hand-write minimal OpenXML `.pptx` zip packages for delivery; PowerPoint may reject or repair them.
- Do not add editable text boxes, native charts, native tables, or PowerPoint shape layouts.
- After packaging, run `deckit-dev review --run <run-folder>` and keep `dist/review.md`.

## Debug Evidence Mode

When the user asks to debug a Deckit run, investigate a failed output, or compare expected vs actual routing, preserve evidence instead of only summarizing. Record:

- the exact user prompt or routing trigger;
- the resolved production route and budget;
- the exact commands run (`new-run`, `package-images`, `audit-pptx`, `review`);
- paths to `run.json`, source, brief, storyboard, prompts, generated PNGs, PPTX, review, and audit output;
- whether `$imagegen` was invoked, skipped, unavailable, or simulated;
- any failed quality gates and the concrete file/line or slide that caused them.

Prefer writing this into `dist/debug-evidence.md` when a run folder exists. Do not overwrite failing artifacts until the evidence has been captured.

## Workflow

1. Identify the user's source material and desired output. If Deckit was explicitly invoked and the source is only a topic or instruction, treat it as a source seed for a complete deck. If the source is a `.pdf` or an `http(s)` URL, route through `document-ingestor` first to produce `source/input.md`.
2. Record `production_mode: image-first`. Do not ask the user to choose among production modes.
3. Choose a **budget mode**: `quick`, `balanced`, or `premium`. The default when the user is silent is `balanced`.
4. Select the minimum specialist workflow needed.
5. Keep intermediate artifacts in predictable paths.
6. Invoke the official `$imagegen` skill to generate full-slide images from the prompt pack unless the user explicitly asked for a partial/text-only artifact or `$imagegen` is unavailable.
7. Package generated slide images into a non-editable PPTX image container when packaging is available.
8. Apply quality gates before calling the work done.

Use `../../references/workflow.md` for the production flow and `../../references/budget-modes.md` for budget decisions.

## Image-First Route

The only active production mode is `image-first`.

`visual-director` writes complete per-slide image-generation prompts. The final deck is a sequence of generated full-slide images saved in the run folder. Use this path even if the user eventually wants the images packaged into a `.pptx`.

Hard rules:

- A `.pptx` containing one full-slide PNG per slide is only a **packaging format** after the images already exist. It does not prove image-first generation by itself.
- Programmatically drawing slide PNGs with local code (PIL, matplotlib, browser screenshots, SVG, HTML/CSS, or PowerPoint shapes) is local rendering, not image-first generation.
- Do not invoke third-party presentation/PPTX skills or plugins during Deckit runs, including Codex `Presentations` and Anthropic `pptx`. They tend to produce native PowerPoint elements and will pull the workflow back into a route v0.3 intentionally disables.
- If the user explicitly invokes Deckit, or asks to "generate images", "use gpt-image", "use gpt-image-2", or "image-first", invoke `$imagegen` for each slide image, then store the resulting PNGs under a path such as `assets/generated-slides/`.
- `$imagegen` is the required handoff for actual slide image generation when that skill is available. Do not replace it with Python, PIL, browser screenshots, SVG, PowerPoint, or other local rendering code.
- If image generation is not available, stop after prompt production and say that generated slide images are pending; do not fake the generation step with local drawing code.
- If the user explicitly asks for editable PowerPoint, explain that the active Deckit route is image-first and produces non-editable slide images; do not switch to an editable shape-by-shape deck workflow.

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
uv run deckit-dev new-run --source ..\path\to\source.md --name run-name --mode image-first --budget balanced
uv run deckit-dev new-run --source ..\path\to\source.pdf --name run-name --mode image-first --budget balanced
uv run deckit-dev new-run --source https://example.com/post --name run-name --mode image-first --budget balanced
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
- `assets/generated-slides/<slide-id>.png` after an actual image-generation step has run
- `dist/<deck-name>.pptx` as a container around generated images, not as the primary image-generation method

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

Run the gate by either reading every artifact and checking each item by hand, or (preferred when available) by running `deckit-dev review --run <name>` and archiving the output to `dist/review.md`. Do not declare delivery without one of the two.
