# Deckit V1 Status — v0.3.5

This is the closing report for the six-week V1 validation roadmap defined in [v1-roadmap.md](v1-roadmap.md). It records what shipped, what did not, and what is queued for V2+.

> Current release note: v0.3.5 keeps the active plugin route image-first only, preserves the native-PPTX firewall for ambiguous "make a PPT" requests, treats explicit Deckit invocations such as `@deckit 介绍一下 F-16 战斗机` as deck-production requests by default, and adds PPTX auditing to reject substitute visual native-PPTX decks. Historical alternate-output research remains in archived docs, but those routes are no longer offered by the plugin skills or dev CLI.

> Packaging note: image-first `.pptx` delivery is allowed only as a non-editable container around generated PNG slides. Use `deckit-dev package-images --run <run-folder>` for this stable packaging path and `deckit-dev audit-pptx --pptx <file.pptx>` to verify the result; do not hand-author minimal OpenXML PPTX packages or substitute visual native-PPTX layouts.

> Routing note: topic-only Deckit requests should produce deck artifacts rather than plain prose answers unless the user explicitly asks for text-only output.

## V1 At a Glance

- Plugin version: **0.3.5** (was 0.1.0 at the start of the roadmap; v0.3.x makes image-first generation the only active path).
- Specialist skills: **5** (was 4).
  - `deck-producer`, `story-architect`, `slide-storyboarder`, `visual-director` (V1 originals).
  - `document-ingestor` (added in Week 5 as the post-W4 route).
- Production mode recognized by the active workflow: `image-first` only.
- Source kinds accepted by `new-run`: text / Markdown, `.pdf`, `http(s)` URL.
- Quality gate: `deckit-dev review --run <name>` writes `dist/review.md` with structural checks for run.json validity, brief sections, storyboard slide blocks, slide-id format, per-archetype support-point band, archetype-name validation, slide-count band per budget, and prompts ↔ storyboard mapping.

### Inspect Output Snapshot

```text
=== INSPECT ===
plugin: deckit
version: 0.3.5
skills: 5
- deck-producer: skills\deck-producer
- document-ingestor: skills\document-ingestor
- slide-storyboarder: skills\slide-storyboarder
- story-architect: skills\story-architect
- visual-director: skills\visual-director

=== INSPECT-MARKETPLACE (in-repo) ===
marketplace: deckit-local
plugins: 1
- deckit: plugins\deckit

=== INSPECT-MARKETPLACE (cross-repo) ===
marketplace: deckit-local
plugins: 1
- deckit: C:\Users\fores\dev\trytry\deckit\plugins\deckit
```

## What V1 Ships

### Plugin

- Five specialist `SKILL.md` files with explicit roles, outputs, do-nots, and (where relevant) reference samples.
- Four references: [workflow](../plugins/deckit/references/workflow.md), [budget-modes](../plugins/deckit/references/budget-modes.md), [slide-archetypes](../plugins/deckit/references/slide-archetypes.md), [critique-checklist](../plugins/deckit/references/critique-checklist.md). Terminology is unified across files (e.g. `production_mode` vs `budget_mode` are named consistently).
- One in-tree teaching sample: `plugins/deckit/assets/sample-decks/sanmiao-victory-day/` (image-first), referenced from `story-architect` and `visual-director`.

### Documentation

- [v1-roadmap.md](v1-roadmap.md) — the six-week schedule and per-week deliverables.
- [v1-smoke-report.md](v1-smoke-report.md) — Week 1 walk-through findings (5 checklist items + minor findings).
- [install-and-use.md](install-and-use.md) — minimum repeatable steps to install and use the plugin from a fresh working directory; includes findings from the Week 2 install loop.
- Archived Week 4 alternate-output experiment — cost quantification and the route-B pivot recommendation. Historical only, not current plugin guidance.
- [development-layout.md](development-layout.md) — repo layout, with new "Sample Decks" inclusion rules added in Week 3.

### Dev Tool (`deckit-dev`)

Six subcommands:

- `inspect` — verify plugin manifest and skills.
- `inspect-marketplace` — verify a marketplace JSON; cross-repo paths handled.
- `new-run` — scaffold a run folder; accepts text / PDF / URL; records `production_mode` and `budget_mode` in `run.json`; auto-routes to the ingestor for PDF / URL.
- `review` — rule-based check on a run folder; writes `dist/review.md`.
- `ingest` — standalone PDF or URL → Markdown ingestion, useful when you want to inspect the extracted source before creating a run.
- `package-images` — stable image-first packaging command; turns `assets/generated-slides/<slide-id>.png` into a non-editable one-image-per-slide `.pptx` container.
- `audit-pptx` — audits any PPTX for Deckit compliance; it passes only when each slide contains exactly one full-slide picture and no native editable slide content.

### Tested Run Loops

- Text source end-to-end: `local-runs/smoke-text-input/` (W1).
- Image-first generation smoke: `local-runs/smoke-current/` (2026-05-11; gitignored). This validated source → brief → storyboard → prompts → 8 generated slide PNGs → visual review, using external image generation rather than plugin-internal API calls.
- Cross-repo install + small deck: `C:\Users\fores\dev\trytry\deckit-install-test\pin-python-version\` (W2; gitignored).
- Sanmiao image-first sample: in-tree slim version (W3).
- PPTX-native experimental draft: `local-runs/smoke-text-input/dist/draft.pptx` (W4; historical only, removed from the active v0.3 CLI).
- PDF + URL ingest end-to-end: `deckit-install-test/ingest-test/{pdf,url}-end-to-end/` with deck-brief produced for both (W5).

## What V1 Did Not Ship (deferred, as planned)

- Editable PowerPoint assembly — removed from the active V1/V0.3 route. Historical experiments remain archived, but this route should not be offered by the plugin until it can clear a separate product-quality bar.
- `style-director` skill — palette / typography / template management, beyond the in-prompt style guidance image-first decks already use.
- `youtube-ingestor`, `audio-transcriber`, DOCX / PPTX / XLSX ingestion.
- Local web UI / studio.
- Editable overlays on top of image-first slides.
- Multi-pass critique loops (`deck-critic` skill).
- Automatic image generation calls inside the plugin (image-first runs still expect external generation; a manual external-generation smoke passed on 2026-05-11).
- LLM-based content checks in `review` (current rules are structural only).

## V2 Candidates, Ranked by Expected Value

The Week 4 decision and Week 5 result reorder the V2 backlog from the original vision:

1. **Image-first generation discipline** — make the official `$imagegen` step explicit, improve prompt strength, and add visual review rubrics so the plugin does not fall back to local rendering or shape-by-shape deck construction.
2. **`document-ingestor` v2** — add OCR fallback for image-only PDFs and a JavaScript-rendered URL fetcher (likely Playwright-backed). Both came up as W5 limitations.
3. **`style-director`** — palette / typography / visual-system management for stronger image-first prompts and more consistent generated slides.
4. **`youtube-ingestor`** — high user value but requires audio pipeline + transcription; treat as a separate vertical.
5. **`deck-critic`** — turn the structural `review` rules into LLM-based judgment passes. Cheap to start once the LLM-call boundary is defined.
6. **Local web UI** — last; only after at least three of the above ship and benefit from a UI.

## Verification Standards Met

- A new reader can produce the first deck-brief and storyboard within one hour using `install-and-use.md`. (Validated in W2; the actual time was under 15 minutes for a 5-slide topic.)
- No conflicting terminology between SKILL.md and references (`production_mode` vs `budget_mode` are uniformly named after the W6 sweep).
- Both `deckit-dev inspect` and `inspect-marketplace` pass with the v0.3.5 manifest.
- The quality gate is callable, not aspirational: `deckit-dev review` produced findings on every test run during the roadmap.
- The image-first artifact loop has been exercised through actual bitmap generation once: 8 PNG slides were generated from `prompts/*.md`, copied into the run folder, and reviewed in `dist/image-first-review.md`.

## Outstanding Items Worth Recording

- `local-runs/smoke-text-input/run.json` is the only run created before W1 added `--mode` / `--budget` to `new-run`. It still has `production_mode = null`. Left intentionally to keep the W1 finding visible; will be regenerated when the smoke run is re-validated against the V2 plugin.
- The `review` tool's content-rule warnings on existing storyboards are useful diagnostics, not red flags. They say "this slide is genuinely outside the standard band" rather than "this slide is broken".
- The cross-repo install flow is verified up to `inspect-marketplace`; the actual click-to-install in Cursor is still UI-only. If the install protocol changes, this gap will be visible to users before maintainers.
