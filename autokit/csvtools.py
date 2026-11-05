"""CSV / Excel helpers built on the standard library csv module and openpyxl."""
from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook, load_workbook



def read_rows(path: str | Path) -> tuple[list[str], list[dict]]:
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)



def write_rows(path: str | Path, header: list[str], rows: list[dict]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=header, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)



def clean(src, dst, dedupe=True, strip=True, drop_empty=True, key: list[str] | None = None, lower_headers=False) -> dict:
    """Trim whitespace, drop empty rows, remove duplicates (optionally by key columns)."""
    header, rows = read_rows(src)
    if lower_headers:
        mapping = {h: h.strip().lower().replace(" ", "_") for h in header}
        header = [mapping[h] for h in header]
        rows = [{mapping[k]: v for k, v in r.items() if k in mapping} for r in rows]
    out, seen, stats = [], set(), {"input": len(rows), "empty": 0, "duplicates": 0}
    for r in rows:
        if strip:
            r = {k: (v.strip() if isinstance(v, str) else v) for k, v in r.items()}
        if drop_empty and not any((v or "") for v in r.values()):
            stats["empty"] += 1
            continue
        if dedupe:
            sig = tuple(r.get(k, "") for k in (key or header))
            if sig in seen:
                stats["duplicates"] += 1
                continue
            seen.add(sig)
        out.append(r)
    write_rows(dst, header, out)
    stats["output"] = len(out)
    return stats



def excel_to_csv(src, outdir, sheet: str | None = None) -> list[Path]:
    """Export one sheet (or all sheets) of an .xlsx to CSV."""
    wb = load_workbook(src, read_only=True, data_only=True)
    names = [sheet] if sheet else wb.sheetnames
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    for name in names:
        ws = wb[name]
        p = outdir / f"{Path(src).stem}_{name}.csv" if len(names) > 1 or not sheet else outdir / f"{Path(src).stem}.csv"
        with open(p, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for row in ws.iter_rows(values_only=True):
                w.writerow(["" if v is None else v for v in row])
        paths.append(p)
    wb.close()
    return paths



def csv_to_excel(srcs: list, dst) -> Path:
    """Combine one or more CSVs into a workbook, one sheet per file."""
    wb = Workbook()
    wb.remove(wb.active)
    for s in srcs:
        ws = wb.create_sheet(Path(s).stem[:31])
        with open(s, newline="", encoding="utf-8-sig") as f:
            for row in csv.reader(f):
                ws.append([_num(v) for v in row])
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    wb.save(dst)
    return Path(dst)



def _num(v: str):
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v
