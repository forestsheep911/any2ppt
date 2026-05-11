# Budget Modes

Any2PPT v0.3 has one active route: image-first with actual image generation when generated slides are requested. Budget mode says how thoroughly that route is executed. The default when the user is silent is `balanced`.

## quick

Use for early exploration or when the user values speed.

Default scope:

- Deck brief.
- Slide storyboard.
- No image generation.
- No multi-pass critique.

Target slide count: **5-7**.

## balanced

Use as the default mode.

Default scope:

- Deck brief.
- Slide storyboard.
- Visual direction.
- Per-slide image prompts.
- Lightweight quality check via `any2ppt-dev review`.

Target slide count: **7-10**.

## premium

Use when the user explicitly asks for high quality and accepts higher time or token cost.

Default scope:

- Deck brief.
- Slide storyboard.
- Visual direction.
- Generated images when `$imagegen` is available. "Generated images" means images produced by the official `$imagegen` skill, not locally rendered screenshots or PIL/canvas output.
- Render or screenshot review.
- Iteration on weak slides.

Target slide count: **8-14**.

The `any2ppt-dev review` tool warns when the storyboard's slide count is outside the band. Document an exception (e.g. a narrow technical topic that genuinely fits in fewer slides) in the brief's "Skill Notes".

## Downgrade Choices

When the budget is tight, prefer to reduce:

- Number of slides.
- Visual complexity.
- Number of generated image attempts.
- Critique passes.

Do not quietly reduce argument quality. If the source needs more thinking, say so and propose a smaller deck.
