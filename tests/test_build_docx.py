import docx
from report.build_docx import render_markdown_to_docx


def test_render_markdown_to_docx_creates_valid_doc(tmp_path):
    md = tmp_path / "sample.md"
    md.write_text(
        "# Title\n\n## 1. INTRODUCTION\n\nBody text with **bold**.\n\n| A | B |\n|---|---|\n| 1 | 2 |\n",
        encoding="utf-8",
    )
    out = tmp_path / "out.docx"
    render_markdown_to_docx(str(md), str(tmp_path), str(out))
    d = docx.Document(str(out))
    assert any("INTRODUCTION" in p.text for p in d.paragraphs)
    assert len(d.tables) == 1
