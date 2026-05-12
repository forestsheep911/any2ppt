# Production Mode Insights

> Archive note: this document records historical research. It is not active plugin guidance for v0.3. The active Deckit route is image-first generation only, using the official image generation capability for slide PNGs. `pptx-native` and `hybrid` should not be offered during normal plugin runs.

## Context

This note records an early Deckit plugin test from:

- Test workspace: `C:\Users\fores\Documents\New project 2`
- Native PPTX output: `C:\Users\fores\Documents\New project 2\dist\eutectic-one-slide.pptx`
- Earlier image-first sample: `C:\Users\fores\dev\trytry\deckit\local-runs\sanmiao-victory-day\assets\generated-slides`

The test prompt asked Deckit to explain the eutectic phenomenon in one slide. The reasoning trace showed a deck/slide workflow and generated a `.pptx` output that PowerPoint can edit directly.

The output file was inspected as a PPTX package:

- Slides: 1
- Embedded media files: 0
- Native slide shapes: 48
- Text runs: 23

This confirms the test followed a PPTX-native production mode rather than an image-first mode.

## Key Finding

Deckit should not mean "always create a native PowerPoint file."

The project name is a product shorthand for creating presentation material. The production mode can vary:

- Image-first slides: generate full-slide visual images, then optionally package them into PPTX or PDF.
- PPTX-native slides: create editable PowerPoint elements such as shapes, text boxes, lines, charts, and diagrams.
- Hybrid slides: combine native PPTX structure with generated images, charts, or visual panels.

These are different production logics and should be treated as explicit choices, not accidental implementation details.

## Image-First Mode

Image-first mode uses image generation to produce complete 16:9 slide visuals. The earlier Sanmiao deck is the reference sample.

Strengths:

- Highest current artistic ceiling.
- Stronger atmosphere, composition, texture, documentary feeling, and visual density.
- Better suited for editorial, cinematic, historical, or visually expressive decks.
- Can produce polished slides quickly when the model follows the visual direction well.

Trade-offs:

- Slide content is not directly editable in PowerPoint.
- Fixing text or layout often requires generating the image again.
- Small text, factual labels, and exact typography can be fragile.
- A later PPTX or PDF is mostly a container unless additional editable overlays are added.

Use when:

- Visual impact matters more than downstream manual editing.
- The deck is closer to a polished visual artifact or narrative presentation.
- The user accepts regeneration as the main revision path.

## PPTX-Native Mode

PPTX-native mode creates PowerPoint-recognized elements directly. The eutectic one-slide test is the first observed example.

Strengths:

- Elements remain editable in PowerPoint.
- Users can manually adjust text, shapes, colors, lines, and layout later.
- Good for technical explainers, diagrams, consulting-style drafts, classroom material, and work that expects human revision.
- Can become more useful as layout heuristics, charting, and diagram patterns improve.

Trade-offs:

- Current artistic quality appears lower than image-first generation.
- Native elements tend to look more mechanical unless layout and typography are carefully tuned.
- Achieving polished design may require many handcrafted layout rules or a stronger template system.
- It may be better as a controllable draft mode before it becomes a final-art mode.

Use when:

- Editability is a primary user requirement.
- The user wants to continue work in PowerPoint.
- The slide is diagrammatic, technical, or text-and-structure driven.
- The production budget cannot afford repeated image regeneration.

## Hybrid Mode

Hybrid mode should be considered a future route.

Possible patterns:

- Use generated images as hero panels, backgrounds, or visual evidence cards.
- Keep titles, subtitles, annotations, and diagrams as editable PPTX elements.
- Generate visual assets per slide, but compose them with native PowerPoint layout.
- Use PPTX-native mode for draft and image-first mode for final visual passes.

Hybrid may eventually offer a better balance between visual quality and editability.

## Product Implication

`deck-producer` should eventually ask or infer a production mode:

- `image-first`: prioritize visual quality and generated slide screenshots.
- `pptx-native`: prioritize editability and PowerPoint-native elements.
- `hybrid`: balance generated visuals with editable structure.

This choice belongs near budget selection because it affects cost, revision strategy, and final artifact quality.

Example user-facing decision:

```text
Production mode:
- Visual polish: image-first
- Editable deck: PPTX-native
- Balanced: hybrid
```

## Development Direction

Do not remove PPTX-native mode. It is strategically valuable even if the current aesthetic quality is weaker.

Do not make PPTX-native the only definition of Deckit. The stronger current path for artistic expression is image-first generation.

Near-term development should keep both paths visible:

- Treat image-first as the high-visual-quality baseline.
- Treat PPTX-native as the editable-output path.
- Record examples and compare them honestly.
- Let `deck-producer` preserve this trade-off instead of hiding it.

Longer term, PPTX-native output may become more competitive through:

- Better slide archetype templates.
- Stronger typography rules.
- Layout validation and screenshot review.
- Reusable chart and diagram builders.
- A style-director skill or style parameter system.

## Updated View — Field Validation (Codex Presentations Plugin)

A second native-PPTX run was performed on 2026-05-10 using the official Codex `Presentations` plugin (a different system than Deckit) on the sanmiao Victory Day topic, and compared head-to-head with the Deckit image-first sample under `local-runs/sanmiao-victory-day/`.

Test workspace: `C:\Users\fores\Documents\New project 3`.

### What the Side-by-Side Said

The Codex plugin's own self-assessment, recorded for honesty:

- Image-first wins on first impression: visual completeness, per-page "visual subject" (May-8/9 timeline, anti-fascism balance, discourse-tool callout, legacy-depletion gauge), and narrative coverage. The image-first deck includes a dedicated "anti-fascism as discourse tool" slide that the native deck does not.
- PPTX-native wins on editability, source restraint (no AI-fabricated historical imagery, no badges, no parade reconstructions), and structural simplicity as a continuable skeleton.
- The Codex plugin's recommended next step: merge — take the image-first visual direction, reimplement as editable PPTX, and replace source-risky AI imagery with abstract but textured editable graphics.

The project owner's verdict on the native output was sharper: roughly "the level of an undergraduate intern who could not present this on stage". The native draft is not stage-ready as-is.

### The Sharper Question This Raised

The "editability" advantage of pptx-native rests on a hidden assumption: the human will actually edit the draft into something usable. The field run challenges that assumption.

When a native-PPTX draft lands below stage quality, editability is mostly theoretical. A human cannot rescue a deck that has the wrong visual idea by tweaking shapes; they would have to restart. At that point editability stops being an advantage and becomes a sunk asset.

By contrast, image-first regeneration with a fixed, well-written prompt is a concrete revision path. It costs more tokens per pass, but the mechanism for "make this slide better" is well-defined.

In short: **a low-quality editable artifact is not necessarily more useful than a higher-quality non-editable one**, because human revision capacity is itself a constraint.

### Implication for V2

This does **not** delete pptx-native from the roadmap, but it does weaken the case for investing heavily in it as currently scoped:

- The Week 4 experiment ([pptx-native-experiment.md](pptx-native-experiment.md)) already concluded V1 should not push pptx-native further without first building theme + master-layout + text-fitting.
- This field validation adds a second, harder question for V2: **even with those foundations, will pptx-native produce a draft good enough that "editability" becomes a real advantage rather than a theoretical one?**
- If V2 still wants to pursue pptx-native, the answer needs to be more concrete than "it is editable". Suggested concrete bars before reopening pptx-assembler work:
  - **Draft-quality threshold**: a draft good enough that a non-designer would not feel the need to redo it from scratch.
  - **Edit-faster-than-regenerate**: a revision flow (change this label, swap this archetype) that is genuinely faster than image-first regeneration on the same edit.
  - **Source-risk parity**: handle the AI-imagery risk that the field comparison flagged, without falling back to "draw nothing".

### What to Reuse Regardless

The Codex Presentations comparison validated three image-first patterns that should stay:

- One strong diagrammatic visual subject per slide (not just a background).
- Strong narrative coverage — every section earns a slide; do not collapse mid-arc sections that carry the argument.
- Source restraint via prompt-side negative blocks (the sanmiao sample's per-slide "Negative" sections do this; keep reinforcing in `visual-director`).

Hybrid mode remains the most likely route for "editability that survives contact with a real audience" — but only after pptx-native draft quality clears the bars above.
