#!/usr/bin/env python3
"""
Regenerates index.html's text from content.md.

Usage:
    python3 build.py

Edit content.md, run this script, and index.html is updated in place.
Everything else about index.html (layout, styling, structure) is untouched —
this script only ever rewrites the text between "<!--c:...-->" markers.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT_MD = ROOT / "content.md"
INDEX_HTML = ROOT / "index.html"

# Fields that aren't plain text: maps "section-slug|field-slug" -> kind.
# Anything not listed here defaults to "text" (a single run of text dropped
# straight between its <!--c:KEY:start--> / <!--c:KEY:end--> markers).
FIELD_KINDS = {
    "about-me|quick-facts": "fact-list",
    "acquisition-criteria|financial-profile": "dl",
    "acquisition-criteria|business-characteristics": "ul",
    "acquisition-criteria|industries-of-interest-tags": "ul",
    "for-brokers|side-card-checklist": "ul",
    "contact|email": "email",
    "contact|phone": "phone",
}
for _n in range(1, 7):
    FIELD_KINDS[f"frequently-asked-questions|question-{_n}"] = "faq"

# Fields that live in an HTML attribute rather than as visible text, and
# which attribute they occupy.
ATTR_FIELDS = {
    "browser-tab-search-preview|search-engine-description": "content",
    "browser-tab-search-preview|social-share-title": "content",
    "browser-tab-search-preview|social-share-description": "content",
    "about-me|photo-alt-text": "alt",
    "contact|linkedin-url": "href",
}


def slugify(text):
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def esc_attr(text):
    return esc(text).replace('"', "&quot;")


def collapse(text):
    return re.sub(r"\s+", " ", text).strip()


def parse_content_md(path):
    """Returns {(section_slug, field_slug): raw_body_text}."""
    fields = {}
    section = None
    field = None
    body_lines = []

    def flush():
        if section and field:
            body = "\n".join(body_lines).strip("\n")
            lines = body.split("\n")
            # Drop a leading italic description line, e.g. "_Shown at the top._"
            if lines and re.match(r"^_.*_$", lines[0].strip()):
                lines = lines[1:]
            fields[(section, field)] = "\n".join(lines).strip()

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip("\n")
        if line.startswith("## "):
            flush()
            section = slugify(line[3:])
            field = None
            body_lines = []
        elif line.startswith("### "):
            flush()
            field = slugify(line[4:])
            body_lines = []
        elif line.strip() == "---":
            continue  # section divider, not content
        elif section and field is not None:
            body_lines.append(line)
    flush()
    return fields


def render_ul(body, indent):
    items = [line[2:].strip() for line in body.splitlines() if line.strip().startswith("- ")]
    sep = "\n" + indent
    return sep.join(f"<li>{esc(item)}</li>" for item in items)


def render_labeled(body, template, indent):
    items = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("- "):
            continue
        label, _, value = line[2:].partition(":")
        items.append(template.format(label=esc(label.strip()), value=esc(value.strip())))
    sep = "\n" + indent
    return sep.join(items)


def render_faq(body):
    question = ""
    answer_lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("Q:"):
            question = stripped[2:].strip()
        elif stripped.startswith("A:"):
            answer_lines.append(stripped[2:].strip())
        elif stripped:
            answer_lines.append(stripped)
    answer = collapse(" ".join(answer_lines))
    return (
        f"<summary>{esc(question)}</summary>\n"
        f"            <p>\n"
        f"              {esc(answer)}\n"
        f"            </p>"
    )


def digits_only(text):
    return re.sub(r"\D", "", text)


def apply_text_field(html, key, body, warnings):
    kind = FIELD_KINDS.get(key, "text")

    if kind == "text":
        replacement = esc(collapse(body))
    elif kind == "ul":
        replacement = render_ul(body, indent=" " * 12)
    elif kind == "fact-list":
        replacement = render_labeled(body, "<li><strong>{label}</strong> {value}</li>", indent=" " * 12)
    elif kind == "dl":
        replacement = render_labeled(body, "<div><dt>{label}</dt><dd>{value}</dd></div>", indent=" " * 14)
    elif kind == "faq":
        replacement = render_faq(body)
    elif kind == "email":
        replacement = esc(collapse(body))
    elif kind == "phone":
        replacement = esc(collapse(body))
    else:
        raise ValueError(f"unknown kind {kind!r} for {key}")

    pattern = re.compile(
        r"(<!--c:" + re.escape(key) + r":start-->)([\s\S]*?)(<!--c:" + re.escape(key) + r":end-->)"
    )
    new_html, count = pattern.subn(lambda m: m.group(1) + replacement + m.group(3), html, count=1)
    if count == 0:
        warnings.append(f"no marker found in index.html for '{key}' (heading may have been renamed)")
        return html
    return new_html


def apply_attr_field(html, key, body, warnings):
    attr = ATTR_FIELDS[key]
    value = esc_attr(collapse(body))
    pattern = re.compile(
        attr + r'="[^"]*"([^>]*>\s*<!--c:attr:' + re.escape(key) + r"-->)"
    )
    new_html, count = pattern.subn(lambda m: f'{attr}="{value}"' + m.group(1), html, count=1)
    if count == 0:
        warnings.append(f"no attribute marker found in index.html for '{key}'")
        return html
    return new_html


def apply_email_href(html, key, body, warnings):
    email = collapse(body)
    pattern = re.compile(
        r'href="mailto:[^"]*"(\s*[^>]*>\s*<!--c:' + re.escape(key) + r':start-->)'
    )
    new_html, count = pattern.subn(lambda m: f'href="mailto:{email}"' + m.group(1), html, count=1)
    if count == 0:
        warnings.append(f"couldn't update the mailto: link for '{key}'")
        return html
    return new_html


def apply_phone_href(html, key, body, warnings):
    digits = digits_only(body)
    tel = f"+1{digits}" if len(digits) == 10 else f"+{digits}"
    pattern = re.compile(
        r'href="tel:[^"]*"(\s*[^>]*>\s*<!--c:' + re.escape(key) + r':start-->)'
    )
    new_html, count = pattern.subn(lambda m: f'href="tel:{tel}"' + m.group(1), html, count=1)
    if count == 0:
        warnings.append(f"couldn't update the tel: link for '{key}'")
        return html
    return new_html


def main():
    if not CONTENT_MD.exists():
        sys.exit(f"Missing {CONTENT_MD.name} next to build.py")
    if not INDEX_HTML.exists():
        sys.exit(f"Missing {INDEX_HTML.name} next to build.py")

    fields = parse_content_md(CONTENT_MD)
    html = INDEX_HTML.read_text(encoding="utf-8")
    warnings = []

    for (section, field), body in fields.items():
        key = f"{section}|{field}"
        if key in ATTR_FIELDS:
            html = apply_attr_field(html, key, body, warnings)
        else:
            html = apply_text_field(html, key, body, warnings)
            if FIELD_KINDS.get(key) == "email":
                html = apply_email_href(html, key, body, warnings)
            elif FIELD_KINDS.get(key) == "phone":
                html = apply_phone_href(html, key, body, warnings)

    INDEX_HTML.write_text(html, encoding="utf-8")

    print(f"Updated {INDEX_HTML.name} from {len(fields)} fields in {CONTENT_MD.name}.")
    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  - {w}")


if __name__ == "__main__":
    main()
