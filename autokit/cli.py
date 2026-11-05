"""autokit (free edition): csv-clean, excel-to-csv, csv-to-excel, pdf-merge."""
from __future__ import annotations

import argparse
import json

from . import __version__, csvtools, pdftools


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="autokit", description="File automation toolkit (free edition).")
    ap.add_argument("--version", action="version", version=__version__)
    sp = ap.add_subparsers(dest="cmd", required=True)
    p = sp.add_parser("csv-clean", help="trim, drop empty rows, dedupe")
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--key", nargs="+", help="dedupe only on these columns")
    p.add_argument("--keep-duplicates", action="store_true")
    p = sp.add_parser("excel-to-csv", help="export xlsx sheets to CSV")
    p.add_argument("src"); p.add_argument("outdir"); p.add_argument("--sheet")
    p = sp.add_parser("csv-to-excel", help="CSV files -> one xlsx (sheet per file)")
    p.add_argument("dst"); p.add_argument("srcs", nargs="+")
    p = sp.add_parser("pdf-merge", help="merge PDFs in order")
    p.add_argument("dst"); p.add_argument("srcs", nargs="+")
    return ap


def main(argv=None) -> int:
    a = build_parser().parse_args(argv)
    if a.cmd == "csv-clean":
        print(json.dumps(csvtools.clean(a.src, a.dst, dedupe=not a.keep_duplicates, key=a.key)))
    elif a.cmd == "excel-to-csv":
        for p in csvtools.excel_to_csv(a.src, a.outdir, a.sheet):
            print(p)
    elif a.cmd == "csv-to-excel":
        print(csvtools.csv_to_excel(a.srcs, a.dst))
    elif a.cmd == "pdf-merge":
        print(f"{pdftools.merge(a.srcs, a.dst)} pages -> {a.dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
