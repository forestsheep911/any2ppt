# Development Layout

This repository separates product artifacts, plugin source, development tools, and release output.

## Directory Roles

```text
any2ppt/
├── .agents/plugins/       # Local marketplace metadata for plugin install testing
├── docs/                  # Vision, architecture, and development notes
├── plugins/               # Codex plugin source directories
│   └── any2ppt/           # Source of the Any2PPT plugin
├── tools/                 # Repo-local development tools managed by uv
├── local-runs/            # Ignored one-off experiments and working artifacts
└── dist/                  # Ignored generated release artifacts
```

## Plugin Source

`plugins/any2ppt/` is the canonical plugin source directory.

Keep files here limited to plugin runtime contents:

- `.codex-plugin/plugin.json`
- `skills/`
- `references/`
- `assets/`
- `scripts/` when scripts are part of the plugin itself
- Future plugin files such as `.mcp.json` or `.app.json`

Do not store local experiments, raw media, generated prompt packs, or release zip files inside the plugin source.

## Sample Decks

`plugins/any2ppt/assets/sample-decks/<deck-name>/` holds slim, in-tree teaching examples that specialist skills can reference. A sample deck typically contains:

- `brief.md`: the slim deck brief (no raw transcript or external content).
- `storyboard.md`: the per-slide plan.
- `prompts/<slide-id>.md`: a small selection (cover plus 2-3 representative slides), not the full prompt pack.
- `notes.md`: explanation of why the deck worked and what to reuse or avoid.

Inclusion rules (must hold for every sample deck added here):

- **Slim**: keep total sample size well under 200 KB. Plain text only. Strip raw transcripts, full audio, and full prompt packs; reference them as living in `local-runs/` (gitignored) instead.
- **Rights-clean**: no third-party photographs, book covers, archive material, or trademarked logos. No identifiable real people in prompts. No copyrighted source content embedded inline.
- **Teachable**: every sample must include a `notes.md` explaining what worked and what not to copy blindly. A sample without `notes.md` is not yet a sample.
- **Stable**: sample decks change only when their teaching value changes. Do not chase the latest production output; pick a stable, exemplary version and freeze it.

Skills that reference samples (currently `story-architect` and `visual-director`) link to `../../assets/sample-decks/<deck-name>/` from inside their `SKILL.md`. New samples should be linked from at least one skill, otherwise they will not be discoverable.

## Local Marketplace

`.agents/plugins/marketplace.json` is the repo-local plugin marketplace used for install-flow testing.

It points to the source plugin with:

```json
{
  "name": "any2ppt",
  "source": {
    "source": "local",
    "path": "./plugins/any2ppt"
  }
}
```

Use this marketplace to test the future workflow where Any2PPT is discovered, installed, and then used from another working directory. Keep marketplace paths relative to the repository root.

## Development Tools

Use `tools/` for utilities that help build, inspect, validate, package, or test the plugin.

Python tooling should be managed with `uv` from inside `tools/`:

```powershell
cd tools
uv run any2ppt-dev --help
```

Development tools may read `../plugins/any2ppt/`, but should not be required for the plugin to load at runtime.

## Local Runs

`local-runs/` is ignored by git. Use it for:

- Prior one-off deck experiments.
- Raw audio/video.
- Transcripts.
- Generated slide images.
- Prompt packs produced during testing.

This keeps successful examples available locally without making them plugin source.

Create a standard text-input run with:

```powershell
cd tools
uv run any2ppt-dev new-run --source ..\path\to\source.md --name topic-name
```

The command creates:

```text
local-runs/topic-name/
├── run.json
├── source/
│   └── input.md
├── work/
├── prompts/
└── dist/
```

Use `work/` for `deck-brief.md` and `storyboard.md`, `prompts/` for visual prompt packs, and `dist/` for generated deliverables from that run.

## Release Artifacts

`dist/` is ignored by git. Use it for generated plugin packages, export bundles, or other publication artifacts.

The source of truth remains `plugins/any2ppt/`. Release artifacts should be reproducible from committed source and development tools.

## Practical Rule

When adding a file, decide its role first:

- Product decision or architecture note: `docs/`
- Plugin behavior used by Codex: `plugins/any2ppt/`
- Build, validation, or packaging helper: `tools/`
- One-off experiment or generated run output: `local-runs/`
- Generated release package: `dist/`
