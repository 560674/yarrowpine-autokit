import csv
import json

from openpyxl import load_workbook
from pypdf import PdfReader, PdfWriter

from autokit import csvtools, pdftools
from autokit.cli import main


def make_pdf(path, pages):
    w = PdfWriter()
    for _ in range(pages):
        w.add_blank_page(612, 792)
    with open(path, "wb") as f:
        w.write(f)
    return path


def test_clean(tmp_path):
    src = tmp_path / "a.csv"
    src.write_text("Name,Email\n Ann ,a@example.com\nAnn,a@example.com\n,\nBob,b@example.com\n")
    s = csvtools.clean(src, tmp_path / "o.csv")
    assert s == {"input": 4, "empty": 1, "duplicates": 1, "output": 2}


def test_excel_roundtrip(tmp_path):
    src = tmp_path / "n.csv"
    src.write_text("a,b\n1,2.5\nx,y\n")
    x = csvtools.csv_to_excel([src], tmp_path / "n.xlsx")
    assert load_workbook(x)["n"]["B2"].value == 2.5
    out = csvtools.excel_to_csv(x, tmp_path / "back")
    with open(out[0], newline="") as f:
        assert list(csv.reader(f))[2] == ["x", "y"]


def test_pdf_merge_and_cli(tmp_path, capsys):
    a, b = make_pdf(tmp_path / "a.pdf", 2), make_pdf(tmp_path / "b.pdf", 1)
    assert pdftools.merge([a, b], tmp_path / "m.pdf") == 3
    main(["pdf-merge", str(tmp_path / "m2.pdf"), str(a), str(b)])
    assert "3 pages" in capsys.readouterr().out
    assert len(PdfReader(tmp_path / "m2.pdf").pages) == 3


def test_cli_clean(tmp_path, capsys):
    src = tmp_path / "c.csv"
    src.write_text("k\n1\n1\n")
    main(["csv-clean", str(src), str(tmp_path / "o.csv")])
    assert json.loads(capsys.readouterr().out)["output"] == 1
