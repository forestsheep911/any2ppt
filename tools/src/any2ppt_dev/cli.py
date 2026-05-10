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
PRODUCTION_MODES = ("image-first", "pptx-native", "hybrid")


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
        try:
            display_path = plugin_path.relative_to(root)
        except ValueError:
            display_path = plugin_path
        print(f"- {name}: {display_path}")

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


def _classify_source(source: str) -> str:
    """Return one of: 'url', 'pdf', 'text'."""
    from any2ppt_dev.ingest import is_url

    if is_url(source):
        return "url"
    suffix = Path(source).suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    if suffix in TEXT_SOURCE_SUFFIXES:
        return "text"
    raise ValueError(
        f"unsupported source: {source}. Supported: text files ({sorted(TEXT_SOURCE_SUFFIXES)}), .pdf files, and http(s) URLs."
    )


def _slug_from_source(source: str, kind: str) -> str:
    if kind == "url":
        from urllib.parse import urlparse

        parsed = urlparse(source)
        host = parsed.netloc.replace(".", "-")
        path = parsed.path.strip("/").replace("/", "-") or "index"
        return _slugify(f"{host}-{path}")
    return _slugify(Path(source).stem)


def new_run(
    source: str,
    name: str | None,
    runs_dir: Path,
    force: bool,
    mode: str | None,
    budget: str | None,
) -> int:
    kind = _classify_source(source)

    if kind == "text":
        source_path = Path(source).resolve()
        if not source_path.is_file():
            raise FileNotFoundError(f"source file does not exist: {source_path}")
    elif kind == "pdf":
        source_path = Path(source).resolve()
        if not source_path.is_file():
            raise FileNotFoundError(f"pdf source does not exist: {source_path}")
    else:
        source_path = None

    run_name = _slugify(name) if name else _slug_from_source(source, kind)
    runs_dir = runs_dir.resolve()
    run_dir = runs_dir / run_name
    _ensure_inside(runs_dir, run_dir)

    if run_dir.exists() and not force:
        raise FileExistsError(f"run already exists: {run_dir}. Use --force to reuse it.")

    artifacts: dict[str, str] = {
        "deck_brief": "work/deck-brief.md",
        "storyboard": "work/storyboard.md",
    }
    if mode in (None, "image-first", "hybrid"):
        artifacts["prompt_readme"] = "prompts/README.md"
        artifacts["prompt_files"] = "prompts/<slide-id>.md"
    if mode in ("pptx-native", "hybrid"):
        artifacts["layouts"] = "work/layouts.md"
    artifacts["dist"] = "dist/"
    artifacts["review"] = "dist/review.md"

    children: list[str] = ["source", "work", "dist"]
    if mode in (None, "image-first", "hybrid"):
        children.append("prompts")
    for child in children:
        (run_dir / child).mkdir(parents=True, exist_ok=True)

    if kind == "text":
        target_source = run_dir / "source" / f"input{source_path.suffix.lower()}"
        if target_source.exists() and not force:
            raise FileExistsError(f"source already exists: {target_source}. Use --force to replace it.")
        shutil.copy2(source_path, target_source)
        original_path = str(source_path)
    else:
        target_source = run_dir / "source" / "input.md"
        if target_source.exists() and not force:
            raise FileExistsError(f"source already exists: {target_source}. Use --force to replace it.")
        from any2ppt_dev.ingest import ingest_pdf, ingest_url

        if kind == "pdf":
            ingest_pdf(source_path, target_source)
            original_path = str(source_path)
        else:
            ingest_url(source, target_source)
            original_path = source

    manifest: dict[str, object] = {
        "name": run_name,
        "source": {
            "original_path": original_path,
            "local_path": str(target_source.relative_to(run_dir)),
            "type": kind,
        },
        "production_mode": mode,
        "budget_mode": budget,
        "artifacts": artifacts,
    }
    (run_dir / "run.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"created run: {run_dir}")
    print(f"source ({kind}): {target_source}")
    if mode is None:
        print("production_mode: not set (deck-producer must record it before delivery)")
    else:
        print(f"production_mode: {mode}")
    if budget is None:
        print("budget_mode: not set")
    else:
        print(f"budget_mode: {budget}")
    print("next artifacts:")
    for artifact in artifacts.values():
        print(f"- {artifact}")
    return 0


SLIDE_ID_PATTERN = re.compile(r"^\d{2}_[a-z0-9_]+$")
SLIDE_HEADING_PATTERN = re.compile(r"^##\s+(\S+)\s*$", re.MULTILINE)

TITLE_LENGTH_MAX = 80

KNOWN_ARCHETYPES = {
    "cover", "thesis", "timeline", "comparison", "evidence cards",
    "process", "map", "data chart", "tension", "closing",
}

SUPPORT_COUNT_BANDS: dict[str, tuple[int, int] | None] = {
    "cover": None,
    "closing": None,
    "process": (2, 7),
    "evidence cards": (2, 10),
    "timeline": (2, 10),
    "thesis": (2, 6),
}
SUPPORT_COUNT_DEFAULT = (2, 4)

SLIDE_COUNT_BANDS = {
    "quick": (5, 7),
    "balanced": (7, 10),
    "premium": (8, 14),
}


def _scan_brief(brief_path: Path) -> list[tuple[str, str, str]]:
    findings: list[tuple[str, str, str]] = []
    if not brief_path.is_file():
        findings.append(("error", "BRIEF-001", "work/deck-brief.md missing"))
        return findings
    text = brief_path.read_text(encoding="utf-8").lower()
    for token, rule_id, label in (
        ("thesis", "BRIEF-THESIS", "thesis"),
        ("audience", "BRIEF-AUDIENCE", "audience"),
        ("arc", "BRIEF-ARC", "arc"),
    ):
        if not re.search(rf"^##\s+[^\n]*{token}", text, re.MULTILINE):
            findings.append(("warn", rule_id, f"deck-brief.md missing a heading mentioning '{label}'"))
    return findings


def _parse_storyboard(sb_path: Path) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
    """Return (slide_blocks, findings). Each slide_block is (slide_id, body_text)."""
    findings: list[tuple[str, str, str]] = []
    if not sb_path.is_file():
        findings.append(("error", "SB-001", "work/storyboard.md missing"))
        return [], findings
    text = sb_path.read_text(encoding="utf-8")
    slide_blocks: list[tuple[str, str]] = []
    matches = list(SLIDE_HEADING_PATTERN.finditer(text))
    if not matches:
        findings.append(("error", "SB-002", "no slide sections (## headings) found in storyboard"))
        return [], findings
    for idx, match in enumerate(matches):
        slide_id = match.group(1)
        if slide_id.lower() in {"deck", "meta"} or slide_id.startswith("Deck"):
            continue
        body_start = match.end()
        body_end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[body_start:body_end]
        if not SLIDE_ID_PATTERN.match(slide_id):
            findings.append(("warn", "SLIDE-ID-FORMAT", f"slide id '{slide_id}' does not match NN_slug format"))
        slide_blocks.append((slide_id, body))
    return slide_blocks, findings


def _extract_field_value(body: str, name: str) -> str:
    pattern = rf"^-\s+\*\*{re.escape(name)}\*\*:\s*(.+)$"
    m = re.search(pattern, body, re.MULTILINE | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _normalize_archetype(value: str) -> str:
    """Strip parenthetical clarifications and lowercase. 'Thesis (four pillars)' -> 'thesis'."""
    cleaned = re.sub(r"\([^)]*\)", "", value).strip().lower()
    return cleaned


def _scan_slide(slide_id: str, body: str) -> list[tuple[str, str, str]]:
    findings: list[tuple[str, str, str]] = []
    body_lower = body.lower()
    for token, rule_id, label in (
        ("title", "SLIDE-TITLE", "Title"),
        ("primary job", "SLIDE-JOB", "Primary job"),
        ("core claim", "SLIDE-CLAIM", "Core claim"),
        ("support", "SLIDE-SUPPORT", "Support points"),
    ):
        if token not in body_lower:
            findings.append(("warn", rule_id, f"slide {slide_id}: missing '{label}' field"))

    title_value = _extract_field_value(body, "Title")
    if title_value and len(title_value) > TITLE_LENGTH_MAX:
        findings.append(
            (
                "warn",
                "SLIDE-TITLE-LENGTH",
                f"slide {slide_id}: title length {len(title_value)} exceeds {TITLE_LENGTH_MAX} chars",
            )
        )

    archetype_value = _extract_field_value(body, "Archetype")
    archetype_norm = _normalize_archetype(archetype_value)
    if archetype_value and archetype_norm not in KNOWN_ARCHETYPES:
        findings.append(
            (
                "warn",
                "SLIDE-ARCHETYPE-UNKNOWN",
                f"slide {slide_id}: archetype '{archetype_value}' is not in slide-archetypes.md",
            )
        )

    sp_match = re.search(
        r"\*\*support points?\*\*[^\n]*\n((?:[ \t]*[-*][ \t]+[^\n]*\n)+)",
        body,
        re.IGNORECASE,
    )
    if sp_match:
        bullets = re.findall(r"^[ \t]*[-*][ \t]+", sp_match.group(1), re.MULTILINE)
        band_key = archetype_norm if archetype_norm in SUPPORT_COUNT_BANDS else None
        band = SUPPORT_COUNT_BANDS.get(band_key, SUPPORT_COUNT_DEFAULT) if band_key is not None else SUPPORT_COUNT_DEFAULT
        if band is None:
            return findings
        low, high = band
        if not (low <= len(bullets) <= high):
            findings.append(
                (
                    "warn",
                    "SLIDE-SUPPORT-COUNT",
                    f"slide {slide_id} ({archetype_norm or 'no-archetype'}): support points count {len(bullets)} outside {low}-{high} range",
                )
            )
    return findings


def _scan_slide_count(budget: str | None, slide_count: int) -> list[tuple[str, str, str]]:
    if not budget:
        return []
    band = SLIDE_COUNT_BANDS.get(budget)
    if band is None:
        return []
    low, high = band
    if low <= slide_count <= high:
        return []
    return [
        (
            "warn",
            "DECK-SLIDE-COUNT",
            f"slide count {slide_count} is outside the {budget} band ({low}-{high})",
        )
    ]


def _scan_prompts(run_dir: Path, storyboard_ids: list[str]) -> list[tuple[str, str, str]]:
    findings: list[tuple[str, str, str]] = []
    prompts_dir = run_dir / "prompts"
    if not prompts_dir.is_dir():
        findings.append(("error", "PROMPTS-001", "prompts/ directory missing"))
        return findings
    prompt_ids = sorted(p.stem for p in prompts_dir.glob("*.md") if p.name != "README.md")
    storyboard_set = set(storyboard_ids)
    for sid in storyboard_ids:
        if sid not in prompt_ids:
            findings.append(("error", "PROMPT-MISSING", f"slide {sid} has no prompt file at prompts/{sid}.md"))
    for pid in prompt_ids:
        if pid not in storyboard_set:
            findings.append(("warn", "PROMPT-ORPHAN", f"prompt prompts/{pid}.md has no matching storyboard slide"))
    return findings


def _scan_layouts(run_dir: Path) -> list[tuple[str, str, str]]:
    layouts_path = run_dir / "work" / "layouts.md"
    if not layouts_path.is_file():
        return [("error", "LAYOUTS-001", "work/layouts.md missing (required for pptx-native or hybrid mode)")]
    return []


def review(run_dir: Path) -> int:
    run_dir = run_dir.resolve()
    if not run_dir.is_dir():
        raise NotADirectoryError(f"run directory does not exist: {run_dir}")

    findings: list[tuple[str, str, str]] = []

    run_json_path = run_dir / "run.json"
    manifest: dict[str, object] = {}
    if not run_json_path.is_file():
        findings.append(("error", "RUN-001", "run.json missing"))
    else:
        try:
            manifest = json.loads(run_json_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(("error", "RUN-002", f"run.json is not valid JSON: {exc}"))

    mode = manifest.get("production_mode") if isinstance(manifest, dict) else None
    if mode is None:
        findings.append(("warn", "MODE-001", "production_mode is null in run.json"))
    elif mode not in PRODUCTION_MODES:
        findings.append(("error", "MODE-002", f"production_mode '{mode}' is not one of {PRODUCTION_MODES}"))

    findings.extend(_scan_brief(run_dir / "work" / "deck-brief.md"))

    slide_blocks, sb_findings = _parse_storyboard(run_dir / "work" / "storyboard.md")
    findings.extend(sb_findings)
    for slide_id, body in slide_blocks:
        findings.extend(_scan_slide(slide_id, body))

    storyboard_ids = [sid for sid, _ in slide_blocks]
    budget = manifest.get("budget_mode") if isinstance(manifest, dict) else None
    if storyboard_ids and isinstance(budget, str):
        findings.extend(_scan_slide_count(budget, len(storyboard_ids)))
    if mode in (None, "image-first", "hybrid"):
        findings.extend(_scan_prompts(run_dir, storyboard_ids))
    if mode in ("pptx-native", "hybrid"):
        findings.extend(_scan_layouts(run_dir))

    counts = {"error": 0, "warn": 0}
    for sev, _, _ in findings:
        counts[sev] = counts.get(sev, 0) + 1

    dist_dir = run_dir / "dist"
    dist_dir.mkdir(parents=True, exist_ok=True)
    review_path = dist_dir / "review.md"

    lines: list[str] = []
    lines.append(f"# Review Report — {run_dir.name}\n\n")
    lines.append(f"- Production mode: `{mode if mode else 'unset'}`\n")
    lines.append(f"- Slides found in storyboard: {len(storyboard_ids)}\n")
    lines.append(f"- Findings: {counts['error']} error(s), {counts['warn']} warning(s)\n\n")
    if not findings:
        lines.append("All checks passed.\n")
    else:
        lines.append("## Findings\n\n")
        for sev, rule_id, msg in findings:
            lines.append(f"- **{sev.upper()}** `{rule_id}` — {msg}\n")
    review_path.write_text("".join(lines), encoding="utf-8")

    print(f"wrote: {review_path}")
    print(f"errors: {counts['error']}; warnings: {counts['warn']}")
    return 0 if counts["error"] == 0 else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Any2PPT development tools")
    subparsers = parser.add_subparsers(dest="command", required=True)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect the plugin manifest and skills")
    inspect_parser.add_argument("--plugin", type=Path, default=DEFAULT_PLUGIN)

    marketplace_parser = subparsers.add_parser("inspect-marketplace", help="Inspect repo-local plugin marketplace")
    marketplace_parser.add_argument("--marketplace", type=Path, default=DEFAULT_MARKETPLACE)

    new_run_parser = subparsers.add_parser("new-run", help="Create a standard local run directory from a text, PDF, or URL source")
    new_run_parser.add_argument("--source", required=True, help="Path to a text/Markdown file, a .pdf file, or an http(s) URL")
    new_run_parser.add_argument("--name", help="Run name. Defaults to the source filename stem (or URL host+path).")
    new_run_parser.add_argument("--runs-dir", type=Path, default=DEFAULT_RUNS_DIR)
    new_run_parser.add_argument("--force", action="store_true", help="Reuse an existing run directory and replace source copy")
    new_run_parser.add_argument("--mode", choices=PRODUCTION_MODES, help="Production mode (recorded in run.json). If omitted, deck-producer must record it before delivery.")
    new_run_parser.add_argument("--budget", choices=("quick", "balanced", "premium"), help="Budget mode (recorded in run.json).")

    review_parser = subparsers.add_parser("review", help="Run rule-based quality checks on a run folder and write dist/review.md")
    review_parser.add_argument("--run", type=Path, required=True, help="Path to the run directory to review.")

    pptx_parser = subparsers.add_parser("pptx", help="Experimental pptx-native helpers")
    pptx_sub = pptx_parser.add_subparsers(dest="pptx_command", required=True)
    pptx_draft_parser = pptx_sub.add_parser("draft", help="Render a storyboard into an experimental .pptx (cover + thesis archetypes only)")
    pptx_draft_parser.add_argument("--storyboard", type=Path, required=True, help="Path to work/storyboard.md")
    pptx_draft_parser.add_argument("--out", type=Path, required=True, help="Output .pptx path")

    ingest_parser = subparsers.add_parser("ingest", help="Convert a PDF or URL into source/input.md (Markdown)")
    ingest_group = ingest_parser.add_mutually_exclusive_group(required=True)
    ingest_group.add_argument("--pdf", type=Path, help="Path to a .pdf file")
    ingest_group.add_argument("--url", help="An http(s) URL")
    ingest_parser.add_argument("--out", type=Path, required=True, help="Output Markdown path (e.g. source/input.md)")

    args = parser.parse_args()

    if args.command == "inspect":
        return inspect_plugin(args.plugin.resolve())
    if args.command == "inspect-marketplace":
        return inspect_marketplace(args.marketplace)
    if args.command == "new-run":
        return new_run(args.source, args.name, args.runs_dir, args.force, args.mode, args.budget)
    if args.command == "review":
        return review(args.run)
    if args.command == "pptx" and args.pptx_command == "draft":
        from any2ppt_dev.pptx_draft import draft as pptx_draft

        return pptx_draft(args.storyboard, args.out)
    if args.command == "ingest":
        from any2ppt_dev.ingest import ingest_pdf, ingest_url

        if args.pdf is not None:
            return ingest_pdf(args.pdf, args.out)
        return ingest_url(args.url, args.out)

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
