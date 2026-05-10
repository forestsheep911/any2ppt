# Critique Checklist

Use this checklist before treating a deck plan or prompt pack as ready. The `any2ppt-dev review` subcommand automates the structural items (artifact presence, slide-ID format, archetype names, slide-count band, per-archetype support-point band, prompt-to-storyboard mapping). The judgement items below still require a human read.

## Argument

- The deck has one central thesis.
- Each slide contributes to that thesis.
- The slide order has a clear narrative arc.
- Important source nuance is preserved or explicitly compressed.
- Unsupported claims are flagged.

## Slide Design

- Each slide has one primary job.
- Titles are specific and presentable.
- Support points are short enough to become slide text.
- Visual archetypes fit the slide purpose.
- The deck avoids repetitive layouts unless intentional.

## Visual Direction

- Visuals support the argument rather than decorate it.
- Text is large, readable, and high contrast.
- Charts, tables, timelines, or diagrams are used when they communicate better than images.
- Language style is consistent.
- The prompt pack does not rely on vague cinematic atmosphere.

## Production

- The output matches the selected budget mode.
- Production mode is recorded in `run.json` and the brief's "Skill Notes".
- Intermediate artifact paths are clear.
- Expensive steps are explicit.
- Future work is separated from v1 deliverables.
- `any2ppt-dev review --run <name>` was run and `dist/review.md` is archived in the run folder.
