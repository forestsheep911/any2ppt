from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PLUGIN = REPO_ROOT / "plugins" / "any2ppt"
DEFAULT_RUNS_DIR = REPO_ROOT / "local-runs"
DEFAULT_MARKETPLACE = REPO_ROOT / ".agents" / "plugins" / "marketplace.json"
TEXT_SOURCE_SUFFIXES = {".md", ".markdown", ".txt"}


def _load_skill_frontmatter(skill_md: Path) -> dict[str, object]:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{skill_md} is missing YAML frontmatter")
    try:
        _, frontmatter, _ = text.split("---\n", 2)
    except ValueError as exc:
        raise ValueError(f"{skill_md} has malformed YAML frontmatter") from exc
    data = yaml.safe_load(frontmatter)
    if not isinstance(data, dict):
        raise ValueError(f"{skill_md} frontmatter is not a mapping")
    return data


def inspect_plugin(plugin: Path) -> int:
    manifest_path = plugin / ".codex-plugin" / "plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    skills_dir = plugin / "skills"
    skill_files = sorted(skills_dir.glob("*/SKILL.md"))

    print(f"plugin: {manifest.get('name')}")
    print(f"version: {manifest.get('version')}")
    print(f"skills: {len(skill_files)}")

    for skill_md in skill_files:
        data = _load_skill_frontmatter(skill_md)
        name = data.get("name")
        description = data.get("description")
        if not name or not description:
            raise ValueError(f"{skill_md} must include name and description")
        print(f"- {name}: {skill_md.parent.relative_to(plugin)}")

    return 0


def inspect_marketplace(marketplace: Path) -> int:
    marketplace = marketplace.resolve()
    data = json.loads(marketplace.read_text(encoding="utf-8"))
    plugins = data.get("plugins")
    if not isinstance(plugins, list):
        raise ValueError(f"{marketplace} must contain a plugins list")

    print(f"marketplace: {data.get('name')}")
    print(f"plugins: {len(plugins)}")

    root = marketplace.parents[2]
    for plugin in plugins:
        name = plugin.get("name")
        source = plugin.get("source", {})
        path_value = source.get("path")
        if not name or not path_value:
            raise ValueError(f"marketplace plugin entry is missing name or source.path: {plugin}")
        plugin_path = (root / path_value).resolve()
        manifest_path = plugin_path / ".codex-plugin" / "plugin.json"
        if not manifest_path.is_file():
            raise FileNotFoundError(f"plugin manifest not found for {name}: {manifest_path}")
        print(f"- {name}: {plugin_path.relative_to(root)}")

    return 0


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    slug = re.sub(r"-{2,}", "-", slug)
    if not slug:
        raise ValueError("run name must contain at least one letter or digit")
    return slug


def _ensure_inside(parent: Path, child: Path) -> None:
    parent = parent.resolve()
    child = child.resolve()
    if child != parent and parent not in child.parents:
        raise ValueError(f"path is outside expected directory: {child}")


def new_run(source: Path, name: str | None, runs_dir: Path, force: bool) -> int:
    source = source.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"source file does not exist: {source}")
    if source.suffix.lower() not in TEXT_SOURCE_SUFFIXES:
        allowed = ", ".join(sorted(TEXT_SOURCE_SUFFIXES))
        raise ValueError(f"source must be a text file with one of: {allowed}")

    run_name = _slugify(name or source.stem)
    runs_dir = runs_dir.resolve()
    run_dir = runs_dir / run_name
    _ensure_inside(runs_dir, run_dir)

    if run_dir.exists() and not force:
        raise FileExistsError(f"run already exists: {run_dir}. Use --force to reuse it.")

    for child in ("source", "work", "prompts", "dist"):
        (run_dir / child).mkdir(parents=True, exist_ok=True)

    target_source = run_dir / "source" / f"input{source.suffix.lower()}"
    if target_source.exists() and not force:
        raise FileExistsError(f"source already exists: {target_source}. Use --force to replace it.")
    shutil.copy2(source, target_source)

    manifest = {
        "name": run_name,
        "source": {
            "original_path": str(source),
            "local_path": str(target_source.relative_to(run_dir)),
            "type": "text",
        },
        "artifacts": {
            "deck_brief": "work/deck-brief.md",
            "storyboard": "work/storyboard.md",
            "prompt_readme": "prompts/README.md",
            "prompt_files": "prompts/<slide-id>.md",
            "dist": "dist/",
        },
    }
    (run_dir / "run.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"created run: {run_dir}")
    print(f"source: {target_source}")
    print("next artifacts:")
    for artifact in manifest["artifacts"].values():
        print(f"- {artifact}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Any2PPT development tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect the plugin manifest and skills")
    inspect_parser.add_argument("--plugin", type=Path, default=DEFAULT_PLUGIN)

    marketplace_parser = subparsers.add_parser("inspect-marketplace", help="Inspect repo-local plugin marketplace")
    marketplace_parser.add_argument("--marketplace", type=Path, default=DEFAULT_MARKETPLACE)

    new_run_parser = subparsers.add_parser("new-run", help="Create a standard local run directory from a text source")
    new_run_parser.add_argument("--source", type=Path, required=True, help="Markdown or plain text source file")
    new_run_parser.add_argument("--name", help="Run name. Defaults to the source filename stem.")
    new_run_parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    new_run_parser.add_argument("--force", action="store_true", help="Reuse an existing run directory and replace source copy")

    args = parser.parse_args()

    if args.command == "inspect":
        return inspect_plugin(args.plugin.resolve())
    if args.command == "inspect-marketplace":
        return inspect_marketplace(args.marketplace)
    if args.command == "new-run":
        return new_run(args.source, args.name, args.runs_dir, args.force)

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
