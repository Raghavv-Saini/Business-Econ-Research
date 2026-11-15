from __future__ import annotations

import argparse
import re
from pathlib import Path

import docx
from docx.shared import Inches, Pt


def _add_formatted_runs(paragraph: docx.text.paragraph.Paragraph, text: str) -> None:
    """Render **bold** and *italic* inline spans into docx runs."""
    tokens = re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text)
    for tok in tokens:
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            run = paragraph.add_run(tok[2:-2])
            run.bold = True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            run = paragraph.add_run(tok[1:-1])
            run.italic = True
        else:
            paragraph.add_run(tok)


def _flush_table(doc: docx.Document, rows: list[list[str]]) -> None:
    if not rows:
        return
    clean_rows = [r for r in rows if not all(re.fullmatch(r":?-+:?", cell.strip()) for cell in r)]
    if not clean_rows:
        return
    n_cols = max(len(r) for r in clean_rows)
    table = doc.add_table(rows=len(clean_rows), cols=n_cols)
    table.style = "Table Grid"
    for r_idx, row in enumerate(clean_rows):
        for c_idx in range(n_cols):
            cell_text = row[c_idx].strip() if c_idx < len(row) else ""
            cell = table.cell(r_idx, c_idx)
            cell.text = ""
            p = cell.paragraphs[0]
            _add_formatted_runs(p, cell_text)
            if r_idx == 0:
                for run in p.runs:
                    run.bold = True


def render_markdown_to_docx(md_path: str, figures_dir: str, out_docx: str) -> None:
    """Convert a structured Markdown research report into a formatted Word (.docx) document."""
    md_file = Path(md_path)
    fig_dir = Path(figures_dir)
    lines = md_file.read_text(encoding="utf-8").splitlines()

    doc = docx.Document()
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Calibri"
    normal_style.font.size = Pt(11)

    table_buf: list[list[str]] = []
    in_code_block = False
    code_lang = ""
    code_buf: list[str] = []

    def flush_pending_table() -> None:
        nonlocal table_buf
        if table_buf:
            _flush_table(doc, table_buf)
            table_buf = []

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_pending_table()
            if not in_code_block:
                in_code_block = True
                code_lang = stripped[3:].strip()
                code_buf = []
            else:
                in_code_block = False
                label = f"[{code_lang.upper()} DIAGRAM]" if code_lang else "[CODE]"
                p_lbl = doc.add_paragraph()
                r_lbl = p_lbl.add_run(label)
                r_lbl.bold = True
                p_code = doc.add_paragraph("\n".join(code_buf))
                for run in p_code.runs:
                    run.font.name = "Consolas"
                    run.font.size = Pt(9)
                code_buf = []
            continue

        if in_code_block:
            code_buf.append(line)
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            table_buf.append(cells)
            continue
        flush_pending_table()

        img_match = re.match(r"^!\[(.*?)\]\((.+?)\)$", stripped)
        if img_match:
            caption, rel_path = img_match.group(1), img_match.group(2)
            cand1 = md_file.parent / rel_path
            cand2 = fig_dir / Path(rel_path).name
            img_path = cand1 if cand1.exists() else cand2
            if img_path.exists():
                doc.add_picture(str(img_path), width=Inches(6.0))
                if caption:
                    p_cap = doc.add_paragraph()
                    r_cap = p_cap.add_run(caption)
                    r_cap.italic = True
            else:
                doc.add_paragraph(f"[Missing figure: {rel_path}]")
            continue

        if not stripped:
            continue

        if stripped.startswith("# "):
            doc.add_heading(stripped[2:].strip(), level=0)
        elif stripped.startswith("## "):
            doc.add_heading(stripped[3:].strip(), level=1)
        elif stripped.startswith("### "):
            doc.add_heading(stripped[4:].strip(), level=2)
        elif stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            _add_formatted_runs(p, stripped[2:].strip())
        else:
            p = doc.add_paragraph()
            _add_formatted_runs(p, stripped)

    flush_pending_table()
    out_p = Path(out_docx)
    out_p.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(out_p))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build BE_Research_Report.docx from Markdown.")
    parser.add_argument("--md", default="report/BE_Research_Report.md")
    parser.add_argument("--figures-dir", default="results/figures")
    parser.add_argument("--out", default="report/BE_Research_Report.docx")
    args = parser.parse_args()
    render_markdown_to_docx(args.md, args.figures_dir, args.out)
    print(f"Built {args.out}")


if __name__ == "__main__":
    main()
