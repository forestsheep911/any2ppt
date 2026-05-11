# Week 1 Smoke Report — smoke-text-input

> Current note: v0.3 makes image-first generation the only active route. Mentions of earlier production-mode ambiguity below are historical context, not current guidance.

## Run Summary
- Source: `docs/any2ppt-plugin-vision.md` (~250 lines, structured markdown)
- Run folder: `local-runs/smoke-text-input/`
- Produced artifacts:
  - `work/deck-brief.md`
  - `work/storyboard.md`
  - `prompts/README.md`
  - `prompts/00_cover.md` ... `prompts/07_closing.md` (8 files)
- Production mode used: image-first (default)
- Budget mode used: balanced

## Walk-through Findings (Week 1 Checklist)

### 1. Was production mode actively chosen?

**No.** The current `deck-producer/SKILL.md` does not require picking a production mode. The walk-through fell into image-first because `visual-director` defaults to writing prompts and nothing else asked.

**Fix**: this is exactly the second Week 1 deliverable. Add a Production Mode section to `deck-producer/SKILL.md` requiring the mode to be picked before budget, and add a "Mode-aware Flow" paragraph to `references/workflow.md`.

**Severity**: high. Without this, every default run silently consumes the visual-direction step even when the user wanted only a brief or a pptx-native deck.

### 2. Is the section-to-slide cutting rule clear?

**Partially.** The brief produced 7 sections; the storyboard collapsed them into 8 slides (cover + 6 body + closing). The mapping was hand-tuned because no skill states "one section per slide" or "merge problem and principle into one slide if budget is quick".

**Fix**: add to `slide-storyboarder/SKILL.md` a guideline "default one slide per section; merge or split only when an explicit reason is recorded in the storyboard". Also add a target slide-count band per budget mode: quick = 5-7, balanced = 7-10, premium = 8-14.

**Severity**: medium. Today the storyboarder works because a human is tuning; a fully automated run could drift.

### 3. Slide ID consistency between storyboard and prompts

**Held.** Storyboard slide IDs (`00_cover` ... `07_closing`) match the eight prompt filenames one-to-one. No mismatch in this run.

However, no skill enforces the convention `<two-digit-index>_<snake_case_slug>`. It happened to be consistent because one author wrote both. A fully decoupled run could produce `cover` vs `00_cover` mismatches.

**Fix**: add to `slide-storyboarder/SKILL.md` an explicit slide-ID format rule (`NN_slug`, two-digit zero-padded index, lowercase snake_case slug). `visual-director/SKILL.md` should reference it.

**Severity**: low (will not break this run, will break a coordinated run later). Defer to the Week 6 sweep.

### 4. Quality gate executor

**Unclear.** `deck-producer/SKILL.md` lists quality gates but does not say who runs the checklist or how to record the result. In this walk-through the gate ran as a manual scan and was logged into this report. Without this report, the gate would have been silent.

**Fix**: this is the second-week deliverable. The `any2ppt-dev review` subcommand will turn the checklist into a callable action. In the meantime `deck-producer/SKILL.md` should require either the checklist run or the `review` tool, with the result archived under `dist/review.md`.

**Severity**: high. Without a callable gate, "quality gate" is decorative.

### 5. Specialist boundary discipline

**Mostly held.**

- `story-architect` was tempted to suggest slide titles inside the brief's section outline; the brief here was kept to section-level claims only.
- `visual-director`'s `prompts/README.md` was tempted to restate the deck argument; it was kept to global style only.

The skill text already says "does not write slide titles" (story-architect) and "does not change the argument" (visual-director), and both held. No fix needed beyond restating these rules in the Week 6 sweep.

**Severity**: low.

## Other Findings (Beyond the Five Points)

### Negative tone in the source

The source document leans on "what not to do". The brief explicitly flagged this risk; the storyboard rephrased into positive claims ("Four things we balance on every run"). This rephrasing is currently judgment, not a skill rule. Consider adding to `story-architect/SKILL.md`: *"If the source is dominated by negation, propose at least one positive framing in the brief."*

### Budget mode default not codified

The walk-through used `balanced` because the reference lists it as default. `deck-producer/SKILL.md` should restate this so a skim-reader of the skill alone knows the default.

### The brief's "Skill Notes" section was useful

The brief ended with a "Skill Notes" section noting the mode-not-chosen issue. This was not in the `story-architect` spec but proved useful for traceability. Consider adding "Skill Notes" as an optional last section in the brief template.

### Production mode is mentioned in the source but never propagated

Ironically, the source document itself names the production-mode trade-off (image-first / pptx-native / hybrid), yet the run produced from it failed to ask which mode to use. This validates the urgency of finding 1.

## Action Items Feeding Later Weeks

- **W1 second deliverable** (next): implement the production-mode requirement in `deck-producer` + `workflow.md` (severity high, finding 1).
- **W1 minor**: add slide-ID format rule (finding 3) — small change, can fold into the same W1 commit.
- **W2 review tool**: makes findings 1, 2, 4 enforceable. The tool can check that mode is recorded in `run.json`, slide ID format is right, and that `dist/review.md` exists.
- **W6 skill sweep**: fold finding 5 (boundary restatement) and the two minor "other findings" into the one-pass refresh.

## Verdict

The walk-through ran end-to-end. All four artifact families exist and are coherent. The skills hold their boundaries. The two real-blocking issues (mode not chosen, gate not enforced) are exactly what the rest of the roadmap addresses. The smoke run is a green light to proceed with the W1 second deliverable and W2.

## 2026-05-11 Image-First Generation Follow-up

A later smoke run, `local-runs/smoke-current/` (gitignored), extended the original image-first artifact loop into actual bitmap generation:

- Source: `docs/any2ppt-plugin-vision.md`.
- Production mode: `image-first`.
- Budget mode: `balanced`.
- Generated artifacts:
  - `work/deck-brief.md`
  - `work/storyboard.md`
  - `prompts/README.md`
  - `prompts/00_cover.md` ... `prompts/07_closing.md`
  - `assets/generated-slides/00_cover.png` ... `assets/generated-slides/07_closing.png`
  - `dist/review.md`
  - `dist/image-first-review.md`

Result:

- `any2ppt-dev review --run local-runs/smoke-current` passed with 0 errors and 0 warnings.
- Eight slide PNGs were generated with external image generation and copied into the run folder.
- The first cover generation misspelled `Storyboard`; one regeneration fixed it. This confirms the known image-first risk: generated text must be checked, and prompt-side spelling constraints reduce but do not remove the risk.

Boundary:

- This follow-up validates the full image-first production loop for testing.
- It does not mean the plugin itself now calls an image-generation API. Automatic image generation remains outside V1; the V1 plugin produces prompt packs and expects an external generation step.
