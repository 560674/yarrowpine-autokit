# autokit — File Automation CLI

*for the Python® programming language, 3.9+ · free edition: CSV cleanup, Excel↔CSV, PDF merge*

A tiny command-line toolkit for three everyday chores.

```bash
pip install -e .
autokit csv-clean examples/customers_dirty.csv out/clean.csv --key Email   # trim, drop empty rows, dedupe
autokit excel-to-csv examples/report.xlsx out/                             # every sheet -> CSV
autokit csv-to-excel out/book.xlsx examples/orders_q1.csv                  # CSVs -> one workbook
autokit pdf-merge out/all.pdf examples/invoice_a.pdf examples/invoice_b.pdf
```

Run tests: `pip install -e ".[test]" && pytest -q`

Dependencies: openpyxl (MIT), pypdf (BSD-3-Clause).

## Want more?

**autokit Pro — 15 commands ($12):** column mapping, CSV split/merge, PDF split/watermark/compress/text
extraction, safe batch rename with dry run, image resize/convert/EXIF strip, sample data and docs.

## Notes

- Maintained with AI assistance; every release passes its test suite.
- Independent project, not affiliated with or endorsed by the Python Software Foundation. Python is a registered trademark of the Python Software Foundation.
- License: MIT © 2026 Yarrowpine Studio
