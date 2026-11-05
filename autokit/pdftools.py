"""PDF merge built on pypdf (BSD)."""
from __future__ import annotations

from pypdf import PdfWriter


def merge(srcs: list, dst) -> int:
    w = PdfWriter()
    for s in srcs:
        w.append(str(s))
    with open(dst, "wb") as f:
        w.write(f)
    return len(w.pages)
