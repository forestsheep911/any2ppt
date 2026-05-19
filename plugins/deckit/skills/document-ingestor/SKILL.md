---
name: document-ingestor
description: Convert non-text inputs (PDF or http(s) URL) into the V1 text-source format. Use when the user provides a PDF, a web page URL, or a similar document that needs to become a Markdown file before story-architect can analyze it. Produces source/input.md inside the run folder, preserving structure where possible.
---

# Document Ingestor

Convert non-text inputs into the standard V1 text source so the rest of the workflow (`story-architect`, `slide-storyboarder`, `visual-director`) does not need to know about the original format.

## Supported Inputs (V1)

- `.pdf` files. Extracted text is preserved page by page (one `## Page N` heading per non-empty page). Complex layout is approximated.
- `http(s)` URLs. The page is fetched, scoped to its main content area, and converted to Markdown.

Other formats (DOCX, PPTX, XLSX, video, audio) are not supported in V1; defer to V2 ingestors (`youtube-ingestor`, `audio-transcriber`, `office-ingestor`).

## When To Use

- The user provides a PDF path or a URL instead of a Markdown file.
- The source is too long or layout-heavy to paste; the ingestor saves a reproducible source file.
- A new run needs `<run>/source/input.md` before `story-architect` can begin.

## Output

Always writes `<run>/source/input.md` (Markdown). The original source path or URL is recorded in `run.json` under `source.original_path` and `source.type` is set to `pdf` or `url`. This keeps the run traceable back to the original input.

## Execution

In installed-plugin runs, create `<run>/source/input.md` directly in the user's run folder. Do not require repository development tools.

For PDFs, use an available PDF text-extraction library or existing document/PDF capability, preserve page breaks where possible, and write one Markdown file. For URLs, fetch the page once, keep the main readable content, strip navigation/scripts/footers where practical, and write one Markdown file.

If a source-repository development helper is available, it may be used as a convenience, but its absence must not block ingestion. Do not mention development helper commands to normal users unless they are debugging Deckit itself or working from the source repository.

## Quality Notes

- PDF extraction loses layout. Tables and multi-column text often arrive as merged paragraphs. The ingested Markdown should be reviewed before being treated as a clean brief input.
- URL extraction targets `<main>`, then `<article>`, then `<body>`. Navigation, ads, scripts, and footers are stripped, but site-specific quirks may bleed through. Re-check long-form pages before relying on them as a single source of truth.
- The ingestor does **not** summarize or interpret. That is the job of `story-architect` running on the produced Markdown.

## Limitations

- No OCR. Image-only PDFs return empty pages and emit a warning.
- No login flow. URLs requiring authentication will fail with the underlying HTTP error.
- No JavaScript rendering. Sites that need a headless browser to expose their main content are out of scope for V1.
- No video / audio transcription. Defer to V2.
- No URL allowlist or rate limiting. The ingestor performs a single HTTP GET with a generic user agent.
