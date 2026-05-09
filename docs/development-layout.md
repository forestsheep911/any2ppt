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
