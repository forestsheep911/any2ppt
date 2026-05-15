# Budget Modes

Deckit v0.3 has one active route for explicit Deckit invocation: image-first with actual image generation, review, and PPTX image-container packaging. Budget mode says how large and polished that route is; it must not change the route into "plain prose", "outline only", or "prompt pack only" unless the user explicitly asks for a partial/text-only artifact or a required tool is unavailable. The default when the user is silent is `balanced`.

## quick

Use for early exploration or when the user values speed.

Default scope:

- Deck brief.
- Slide storyboard.
- Visual direction and per-slide image prompts.
- Generated slide images through the official `$imagegen` skill when available.
- Non-editable PPTX image-container packaging when packaging is available.
- Single-pass review; no multi-pass critique.

Target slide count: **4-6**.

## balanced

Use as the default mode.

Default scope:

- Deck brief.
- Slide storyboard.
- Visual direction.
- Per-slide image prompts.
- Generated slide images through the official `$imagegen` skill when available.
- Non-editable PPTX image-container packaging when packaging is available.
- Lightweight quality check via `deckit-dev review`.

Target slide count: **7-10**.

## premium

Use when the user explicitly asks for high quality and accepts higher time or token cost.

Default scope:

- Deck brief.
- Slide storyboard.
- Visual direction.
- Generated images when `$imagegen` is available. "Generated images" means images produced by the official `$imagegen` skill, not locally rendered screenshots or PIL/canvas output.
- Non-editable PPTX image-container packaging when packaging is available.
- Render or screenshot review.
- Iteration on weak slides.

Target slide count: **8-14**.

The `deckit-dev review` tool warns when the storyboard's slide count is outside the band. Document an exception (e.g. a narrow technical topic that genuinely fits in fewer slides) in the brief's "Skill Notes".

## Downgrade Choices

When the budget is tight, prefer to reduce:

- Number of slides.
- Visual complexity.
- Number of generated image attempts.
- Critique passes.

Do not quietly reduce argument quality. If the source needs more thinking, say so and propose a smaller deck.
