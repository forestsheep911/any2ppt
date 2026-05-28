# Deckit

Deckit is a Codex plugin for producing image-first presentation decks end to end.

Current release: **v0.4.3**.

## What Deckit Does

Deckit turns a topic, note, Markdown document, PDF, or URL into a presentation workflow:

1. Ingest or frame the source material.
2. Build a deck brief and narrative arc.
3. Create a slide-by-slide storyboard.
4. Write image-generation prompts for each full-slide visual.
5. Generate actual slide images through the official image generation capability when available.
6. Package generated slide PNGs into the requested final delivery target.
7. Produce standard preview artifact(s): `dist/preview.png` for decks up to 32 slides, or numbered `dist/preview-XX.png` files for longer decks.
8. Review and audit the output before delivery.

## Current Production Route

Deckit v0.4 has one active production route: **image-first**.

That means:

- slide visuals are generated as bitmap images first;
- `.pptx` output is a non-editable image-container deck, with one full-slide image per slide;
- `.pdf` output is image-only delivery built from generated slide images;
- generated slide PNGs are retained as intermediate artifacts;
- Deckit should not substitute native PowerPoint shapes, browser-rendered slides, SVG screenshots, or generic presentation plugins for the image-generation step.

If the user asks for editable PowerPoint, Deckit should explain that the current plugin produces generated slide images packaged into PPTX, not native editable PowerPoint layouts.

## Marketplace Installation

Deckit is distributed through the 2water Codex plugin marketplace:

```text
forestsheep911/codex-plugin-marketplace-2water
```

The marketplace entry should point to this repository as a git subdirectory source:

```json
{
  "name": "deckit",
  "source": {
    "source": "git-subdir",
    "url": "forestsheep911/deckit",
    "path": "plugins/deckit",
    "ref": "v0.4.3"
  }
}
```

Useful verification commands:

```powershell
git ls-remote --tags https://github.com/forestsheep911/deckit.git refs/tags/v0.4.3
```

```powershell
Invoke-WebRequest -UseBasicParsing `
  https://raw.githubusercontent.com/forestsheep911/codex-plugin-marketplace-2water/main/.agents/plugins/marketplace.json |
  Select-Object -ExpandProperty Content
```

## Local Development Layout

The installable plugin lives under:

```text
plugins/deckit/
```

Key files:

```text
plugins/deckit/.codex-plugin/plugin.json
plugins/deckit/skills/deck-producer/SKILL.md
plugins/deckit/skills/story-architect/SKILL.md
plugins/deckit/skills/slide-storyboarder/SKILL.md
plugins/deckit/skills/visual-director/SKILL.md
plugins/deckit/skills/document-ingestor/SKILL.md
plugins/deckit/references/workflow.md
plugins/deckit/references/budget-modes.md
```

Development docs live under:

```text
docs/
```

Generated and smoke-test artifacts are local working outputs and should not be treated as the plugin source of truth.

## Release Checklist

When publishing a new Deckit version:

1. Update `plugins/deckit/.codex-plugin/plugin.json`.
2. Commit and push the Deckit repository changes.
3. Create and push a matching tag, for example `v0.4.1`.
4. Update `forestsheep911/codex-plugin-marketplace-2water` so `.agents/plugins/marketplace.json` points Deckit's `ref` to the new tag.
5. Commit and push the marketplace change.
6. Verify that the remote tag exists and the raw marketplace JSON points at the same tag.

See `AGENTS.md` for the detailed release and Windows marketplace-upgrade troubleshooting notes.

## More Documentation

- `docs/install-and-use.md` — local install and workflow notes.
- `docs/development-layout.md` — repository layout and dev-tool notes.
- `docs/v1-status.md` — current V1 status, updated for v0.4.3.
- `docs/production-mode-insights.md` — archived production-mode research.
- `docs/pptx-native-experiment.md` — archived native-PPTX experiment notes.
