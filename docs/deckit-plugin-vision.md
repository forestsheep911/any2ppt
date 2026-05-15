# Deckit Plugin Vision

## Purpose

Deckit is a Codex plugin for turning source material into presentation-ready decks.

The plugin should not start as a large automation system. Its first job is to preserve a repeatable creative workflow: understand the source, shape the argument, plan the slides, direct the visuals, and check whether the result is actually usable as a presentation.

The long-term product can grow into a configurable local tool with style systems, budget choices, source adapters, PPTX assembly, and review loops. Version 1 should stay small enough to use, inspect, and improve.

Current direction: Deckit v0.3 is image-first only. Historical notes about alternate production modes remain in `docs/production-mode-insights.md`, but they are not active plugin guidance.

## Product Principle

Deckit should behave like a practical production team, not like an unconstrained generator.

The plugin must balance:

- Quality: the deck should have a clear thesis, coherent slide sequence, readable text, and useful visuals.
- Cost: token use, image generation count, time, and review depth are real constraints.
- Scope: each run should choose the minimum workflow needed for the requested output.
- Traceability: important intermediate artifacts should be kept so a user can revise the deck without restarting.

This is why the main entry skill is called `deck-producer`.

## Core Role: deck-producer

`deck-producer` is the plugin's main entry point and production owner.

It is responsible for:

- Interpreting the user's goal.
- Identifying the source material type.
- Choosing an appropriate workflow.
- Setting a realistic production budget.
- Deciding which specialist skills are needed.
- Naming and organizing intermediate artifacts.
- Enforcing quality gates before delivery.
- Choosing downgrade paths when budget or time is limited.

`deck-producer` should not do every specialist task itself. It should coordinate smaller skills and keep the overall deck production coherent.

Examples of budget-aware decisions:

- For a quick draft, produce a deck brief and storyboard only.
- For a balanced run, produce storyboard plus per-slide visual prompts.
- For a premium run, add visual generation, PPTX assembly, render review, and iteration.
- When the source is long, summarize into a brief before planning slides.
- When the user already provides a clear outline, skip source analysis and move directly to slide planning.

## V1 Scope

Version 1 should prove the workflow, not the full product.

V1 supports:

- Markdown, transcript, or plain text as the primary input.
- Deck brief generation.
- Slide storyboard generation.
- Per-slide visual direction and image prompt generation.
- A lightweight critique checklist.
- Explicit budget modes: quick, balanced, premium.
- Work artifacts saved in predictable paths.

V1 does not need to support:

- A local website UI.
- Full YouTube download and transcription.
- Full PDF, PPTX, XLSX ingestion.
- Automatic editable PPTX assembly.
- Style marketplace or template library.
- Fully automated multi-pass visual review.

Those are extension points, not first-version requirements.

## Suggested V1 Plugin Structure

```text
plugins/deckit/
├── .codex-plugin/
│   └── plugin.json
├── skills/
│   ├── deck-producer/
│   │   └── SKILL.md
│   ├── story-architect/
│   │   └── SKILL.md
│   ├── slide-storyboarder/
│   │   └── SKILL.md
│   └── visual-director/
│       └── SKILL.md
├── references/
│   ├── workflow.md
│   ├── budget-modes.md
│   ├── slide-archetypes.md
│   └── critique-checklist.md
└── assets/
    └── sample-decks/
```

## Specialist Skills

### deck-producer

Main coordinator. It receives the user request and decides how to run the production.

Inputs:

- User goal.
- Source material path or pasted content.
- Desired output, if specified.
- Budget mode, if specified.

Outputs:

- Production plan.
- Work artifact paths.
- Calls to specialist skills.
- Final delivery summary.

### story-architect

Turns raw material into a deck-level argument.

Responsibilities:

- Extract the central thesis.
- Identify the audience and presentation purpose.
- Choose the narrative arc.
- Select the main sections.
- Remove tangents that do not serve the deck.

Output:

- `work/deck-brief.md`

### slide-storyboarder

Turns the deck argument into a page-by-page plan.

Responsibilities:

- Assign one purpose to each slide.
- Write slide titles and core claims.
- Choose 2-4 support points per slide.
- Recommend slide archetypes.
- Add speaker notes for every slide so packaged PowerPoint decks include presenter guidance in the notes pane.

Output:

- `work/storyboard.md`

### visual-director

Turns the storyboard into visual treatment and generation prompts.

Responsibilities:

- Choose visual style and layout direction.
- Write per-slide image prompts when image-first output is requested.
- Avoid decorative-only visuals.
- Keep generated text large, short, high-contrast, and readable.
- Keep slide visuals tied to the argument.

Outputs:

- `prompts/README.md`
- `prompts/<slide-id>.md`

## Budget Modes

Budget modes should guide workflow depth.

### quick

Use when the user wants speed or early exploration.

Default output:

- Deck brief.
- Slide storyboard.
- No image generation unless explicitly requested.

### balanced

Use as the default mode.

Default output:

- Deck brief.
- Slide storyboard.
- Per-slide visual direction.
- Per-slide image prompts.
- Lightweight critique pass.

### premium

Use when the user explicitly asks for high quality and accepts higher cost.

Default output:

- Deck brief.
- Slide storyboard.
- Visual prompts.
- Generated slide images or assembled PPTX when tools are available.
- Render or screenshot review.
- Iteration on weak slides.

## Quality Gates

Before a deck is treated as done, check:

- The deck has a clear central thesis.
- Each slide has one primary job.
- Slide titles are specific and presentable.
- The sequence has a logical arc.
- No slide is only decorative.
- Text is readable at presentation scale.
- Visuals support the argument rather than replacing it.
- Language style is consistent.
- The chosen workflow fits the budget.
- The final output path is clear.

## Future Extensions

Future modules should be added only after V1 proves the basic production loop.

Candidate skills:

- `youtube-ingestor`: download YouTube audio and produce transcripts.
- `document-ingestor`: read PDF, DOCX, PPTX, XLSX, and web pages into briefs.
- PowerPoint packaging: optionally place already generated slide images into a `.pptx` container.
- `deck-critic`: perform deeper review and recommend slide-level revisions.
- `style-director`: manage presentation styles, templates, palettes, and typography.
- `speaker-notes-writer`: generate presenter notes and talk tracks.
- `local-studio`: provide a local web UI for choosing parameters and reviewing outputs.

Candidate product parameters:

- Budget: quick, balanced, premium.
- Output: brief, storyboard, prompts, images, PPTX.
- Production mode: image-first only in v0.3.
- Style: editorial, consulting, academic, cinematic, product pitch.
- Language: Simplified Chinese, Traditional Chinese, English, bilingual.
- Editability: visual artifact, editable native deck, mixed editable overlays.
- Review depth: none, checklist, rendered visual review, multi-pass critique.

## Non-Goals

Avoid turning V1 into a large platform.

Do not require a UI before the command-line and skill workflow are useful.
Do not duplicate mature PDF, PPTX, XLSX, or document skills unless the Deckit workflow needs a stable wrapper.
Do not hide cost: when an output requires many generated images, multiple critique passes, or heavy transcription, `deck-producer` should make that visible.
Do not let visual polish outrun argument quality.

## First Implementation Milestone

The first usable milestone is:

1. Scaffold the `deckit` plugin.
2. Implement `deck-producer`, `story-architect`, `slide-storyboarder`, and `visual-director`.
3. Move the successful Sanmiao deck flow into `assets/sample-decks/` or references as an example.
4. Validate that a new transcript can produce:
   - `work/deck-brief.md`
   - `work/storyboard.md`
   - `prompts/README.md`
   - `prompts/*.md`
5. Keep YouTube ingestion, PPTX assembly, and local UI out of the first milestone unless they become necessary to test the core workflow.
