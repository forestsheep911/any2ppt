"""Document ingestor — convert PDF and HTTP/HTTPS URLs into Markdown source.

The output is always a Markdown file suitable for the V1 text-input loop
(`<run>/source/input.md`). Extraction quality is intentionally simple; the goal
is reproducibility, not perfection.
"""
from __future__ import annotations

from pathlib import Path


def is_url(value: str) -> bool:
    return value.startswith("http://") or value.startswith("https://")


def ingest_pdf(pdf_path: Path, out_path: Path) -> int:
    from pypdf import PdfReader

    pdf_path = pdf_path.resolve()
    if not pdf_path.is_file():
        raise FileNotFoundError(f"pdf not found: {pdf_path}")

    reader = PdfReader(str(pdf_path))
    pages: list[str] = []
    empty_count = 0
    for page_index, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if not text:
            empty_count += 1
            continue
        pages.append(f"## Page {page_index}\n\n{text}")

    out_path = out_path.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    header = f"# {pdf_path.stem}\n\nSource PDF: `{pdf_path}`\nPages: {len(reader.pages)}\n\n"
    body = "\n\n".join(pages) if pages else "_No extractable text. The PDF may be image-only._\n"
    out_path.write_text(header + body + "\n", encoding="utf-8")

    print(f"wrote: {out_path}")
    print(f"pages: {len(reader.pages)} total ({empty_count} empty)")
    if empty_count == len(reader.pages):
        print("warning: every page was empty — the PDF may need OCR")
    return 0


def ingest_url(url: str, out_path: Path) -> int:
    import httpx
    from bs4 import BeautifulSoup
    from markdownify import markdownify as md

    out_path = out_path.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    headers = {
        "User-Agent": "Mozilla/5.0 (any2ppt-dev ingest)",
    }
    with httpx.Client(timeout=30.0, follow_redirects=True, headers=headers) as client:
        resp = client.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    title_text = ""
    if soup.title and soup.title.string:
        title_text = soup.title.string.strip()
    if not title_text:
        title_text = url

    main = soup.find("main") or soup.find("article") or soup.body
    if main is None:
        raise ValueError(f"could not find a main content area in {url}")

    for tag in main.find_all(["nav", "footer", "script", "style", "aside", "form", "noscript"]):
        tag.decompose()

    body_md = md(str(main), heading_style="ATX", bullets="-").strip()
    body_md = "\n".join(line.rstrip() for line in body_md.splitlines() if line.strip() != "")

    text = f"# {title_text}\n\nSource URL: {url}\n\n{body_md}\n"
    out_path.write_text(text, encoding="utf-8")

    print(f"wrote: {out_path}")
    print(f"title: {title_text}")
    print(f"chars: {len(body_md)}")
    return 0


def ingest(source: str, out_path: Path) -> int:
    if is_url(source):
        return ingest_url(source, out_path)
    suffix = Path(source).suffix.lower()
    if suffix == ".pdf":
        return ingest_pdf(Path(source), out_path)
    raise ValueError(
        f"unsupported source for ingest: {source}. Supported: .pdf files and http(s) URLs."
    )
