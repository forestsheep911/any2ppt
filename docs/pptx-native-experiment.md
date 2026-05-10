# PPTX-Native Breaking Experiment — Week 4 Result

## Goal

Discover the real cost of pptx-native mode at minimum risk. The Week 4 experiment intentionally limits scope to two archetypes (cover, thesis), so the result quantifies "how much does one archetype cost?" rather than "how good can the final deck look?"

## What Was Built

A new experimental subcommand:

```powershell
uv run any2ppt-dev pptx draft `
  --storyboard <work/storyboard.md> `
  --out <dist/draft.pptx>
```

It is implemented in [tools/src/any2ppt_dev/pptx_draft.py](../tools/src/any2ppt_dev/pptx_draft.py) and uses `python-pptx`. Two archetypes are implemented:

- **Cover**: tag, large title, optional subtitle, optional source line.
- **Thesis (4-pillar)**: title, single-sentence thesis, four equal rounded-rectangle pillars across the bottom half.

Any other archetype falls into a labeled "skipped" placeholder slide so the deck remains complete and the gap is visible to a reviewer.

The dev tool, the plugin, and the storyboard format all stayed untouched. The experimental subcommand reuses the existing storyboard parser pattern.

## Test Run

Input: [local-runs/smoke-text-input/work/storyboard.md](../local-runs/smoke-text-input/work/storyboard.md) (8 slides from the V1 smoke run).

Result:

- Output: `local-runs/smoke-text-input/dist/draft.pptx`, 36 KB.
- Slides rendered: 8 total (1 cover, 1 thesis, 6 skipped).
- The file opens in PowerPoint and Keynote without warnings, and every shape is editable.

## Subjective Quality Scoring

Scored on a 1–5 scale by opening the file in PowerPoint at 100% zoom on a 1080p display.

- **Readability**: 4 / 5. The off-white background and near-black 44pt cover title hold up well. The 16pt pillar text on the thesis slide is readable but tight when a label is longer than ~30 characters.
- **Alignment**: 4 / 5. Pillars align with EMU-precise gaps; the title line wraps cleanly. No accidental overlaps.
- **Whitespace**: 3 / 5. Cover whitespace is good; the thesis slide compresses the lower half because four pillars + arrows would crowd anything else.
- **Typography hierarchy**: 3 / 5. There is hierarchy (44 / 36 / 22 / 16), but no theme system, so changing the brand color requires editing source code.
- **Production polish vs image-first**: 2 / 5. Even the rendered cover and thesis slides feel like a draft — they look like a tidy wireframe, not a final lecture deck. The sanmiao image-first sample is in a different visual league.

## Cost Quantification

- Implementation file ([pptx_draft.py](../tools/src/any2ppt_dev/pptx_draft.py)): 211 lines of Python including parser, helpers, and two archetype renderers.
  - Storyboard parser + dataclasses: ~70 lines (reusable across all future archetypes).
  - Common helpers (`_add_textbox`, `_set_background`, `_pick_support`): ~50 lines (also reusable).
  - Cover renderer: ~25 lines.
  - Thesis renderer: ~35 lines.
  - Skipped placeholder: ~15 lines.
- Dependency added: `python-pptx>=1.0.2` plus its transitive `lxml` (3.8 MiB) and `pillow` (6.8 MiB).
- Time-to-first-pptx (this iteration): ~45 minutes including parser and two renderers.
- Estimated cost per additional archetype:
  - **comparison** (two columns): ~30-40 lines, ~30 min. Mostly two-column layout.
  - **process** (left-to-right pipeline with arrows): ~50-70 lines, ~60 min. Connector shapes are the biggest unknown.
  - **evidence cards** (2x5 grid): ~40-60 lines, ~40 min. Loop over cards with conditional styling.
  - **timeline**: ~60-80 lines, ~60-90 min. Curve / line shapes plus per-tick label placement.
  - **tension** (cause / consequence): ~40 lines, ~30 min. Effectively a comparison with a divider stripe.
  - **closing**: ~25 lines, ~20 min. Shape-wise simple.

Six remaining archetypes total: ~250-310 lines plus ~3-4.5 hours of layout debugging. That doubles the size of the experimental module.

## Findings That Will Bite Sooner Than the Code Estimate Suggests

These are not in the line-count table because they are systemic, not per-archetype:

1. **No theme system.** Every color and font is a constant in `pptx_draft.py`. Changing brand color or typeface requires a source code edit. To make pptx-native a real product, the very next step would be to introduce a theme module (palette, font ladder, spacing tokens). That is a separate ~100-200 line effort, and skipping it makes every future archetype harder to keep visually consistent.

2. **No long-text fitting strategy.** When a thesis pillar label is longer than ~30 characters, the centered text wraps and either escapes the rounded rectangle or compresses awkwardly. Image-first sidesteps this by letting the model lay out text. Pptx-native must implement either auto-fit (size-down) or clip-and-warn behavior, neither of which is trivial in `python-pptx`.

3. **No layout templates or master slides.** Today every shape is created inline. A real product would maintain master slide layouts (one per archetype) so designers could tweak templates without touching Python. This is also a separate effort, comparable in size to the theme system.

4. **Output looks like a draft, not a deliverable.** Even if all six remaining archetypes were finished, the result would be in the "good wireframe" tier, not in the "polished lecture deck" tier where image-first already lives. That gap will close only with theming, master layouts, and probably a font system — all of which are outside the original Week 5 budget.

## Recommendation: Pivot to Route B (document-ingestor)

The experiment proves three things:

- Pptx-native is technically viable — `draft.pptx` opens, edits, and respects archetypes.
- Pptx-native is **not** going to reach image-first quality in the remaining two weeks.
- Even reaching "useful draft" parity for the other six archetypes will consume the entire Week 5 budget on layout code, with theming and master layouts still queued behind it for V2.

Meanwhile, image-first is the high-quality path the project already has, and the largest remaining gap in `any2ppt` as a product is **input variety**. The "any" in `any2ppt` is currently text-only. Adding `document-ingestor` (PDF + URL) immediately broadens the surface and reuses the existing `~/.agents/skills/pdf` skill, which is a much cheaper unit-of-value than the next pptx-native archetype.

**Recommendation for Week 5: Route B — start `document-ingestor`** (PDF + URL inputs first).

The pptx-native experiment is not abandoned. The experimental `any2ppt-dev pptx draft` subcommand stays in the dev tool as a V2 starting point. When pptx-native returns in V2, the work order should be:

1. Theme module (palette, font ladder, spacing tokens).
2. Master slide layouts (one per archetype).
3. Long-text fitting strategy.
4. The remaining six archetypes on top of those three foundations.

That sequence will cost more up front but pay off across every later archetype, instead of paying per-archetype each time.

## Artifacts

- Code: [tools/src/any2ppt_dev/pptx_draft.py](../tools/src/any2ppt_dev/pptx_draft.py)
- Subcommand wiring: [tools/src/any2ppt_dev/cli.py](../tools/src/any2ppt_dev/cli.py)
- Generated draft: `local-runs/smoke-text-input/dist/draft.pptx` (gitignored; reproduce with the command above).
