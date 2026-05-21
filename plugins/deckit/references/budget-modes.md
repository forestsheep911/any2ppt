# Budget Modes

Deckit v0.4 has one active route for explicit Deckit invocation: image-first with actual image generation, review, standard preview generation, and packaging of generated PNGs into the requested final delivery target (`pptx` or `pdf`). Budget mode says how large and polished that route is; it must not change the route into "plain prose", "outline only", or "prompt pack only" unless the user explicitly asks for a partial/text-only artifact or `$imagegen` is truly unavailable. The default when the user is silent is `balanced`.

When a prompt is high-risk vague, ask the preflight clarification question set before choosing final budget and slide count. If the user says "use defaults" or answers partially, use `balanced`, a standard 8-slide target, and `pptx` as the final delivery target unless the user chooses `pdf`.

## quick

Use for early exploration or when the user values speed.

Default scope:

- Deck brief.
- Slide storyboard.
- Visual direction and per-slide image prompts.
- Generated slide images through the official `$imagegen` skill.
- Requested final delivery packaging after generated PNGs exist; default is non-editable PPTX image-container packaging.
- Standard preview generation from slide PNGs (`dist/preview.png` up to 32 slides; numbered `dist/preview-XX.png` files above 32 slides).
- Single-pass review; no multi-pass critique.

Target slide count: **4-6**.

## balanced

Use as the default mode.

Default scope:

- Deck brief.
- Slide storyboard.
- Visual direction.
- Per-slide image prompts.
- Generated slide images through the official `$imagegen` skill.
- Requested final delivery packaging after generated PNGs exist; default is non-editable PPTX image-container packaging.
- Standard preview generation from slide PNGs (`dist/preview.png` up to 32 slides; numbered `dist/preview-XX.png` files above 32 slides).
- Lightweight manual or automated quality check archived to `dist/review.md`.

Target slide count: **7-10**.

## premium

Use when the user explicitly asks for high quality and accepts higher time or token cost.

Default scope:

- Deck brief.
- Slide storyboard.
- Visual direction.
- Generated images through `$imagegen`. "Generated images" means images produced by the official `$imagegen` skill, not locally rendered screenshots or PIL/canvas output.
- Requested final delivery packaging after generated PNGs exist; default is non-editable PPTX image-container packaging.
- Standard preview generation from slide PNGs (`dist/preview.png` up to 32 slides; numbered `dist/preview-XX.png` files above 32 slides).
- Render or screenshot review.
- Iteration on weak slides.

Target slide count: **8-14**.

Document an exception when the storyboard's slide count is outside the band (e.g. a narrow technical topic that genuinely fits in fewer slides) in the brief's "Skill Notes".

## Downgrade Choices

When the budget is tight, prefer to reduce:

- Number of slides.
- Visual complexity.
- Number of generated image attempts.
- Critique passes.

Do not quietly reduce argument quality. If the source needs more thinking, say so and propose a smaller deck.
