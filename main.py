"""Entry program for news-image-20261122 (zech).

Copies the pre-drawn magazine cover entry.png next to this script into
the make.fun output directory, after validating the PNG header, its
dimensions (<=1024x1024) and its size (<=1 MiB). Pure standard library,
no network, fully deterministic: the same bytes come out every run.
"""

import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576
MAX_DIM = 1024
SRC_NAME = "entry.png"


def read_png_size(path):
    with open(path, "rb") as fh:
        head = fh.read(33)
        fh.seek(-12, os.SEEK_END)
        tail = fh.read(12)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("entry.png is not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("entry.png has no IHDR chunk")
    if tail[4:8] != b"IEND":
        raise ValueError("entry.png is truncated: no IEND chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    size = os.path.getsize(src)
    if size > MAX_BYTES:
        raise ValueError(f"entry.png is {size} bytes, over the 1 MiB limit")
    width, height = read_png_size(src)
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"entry.png is {width}x{height}, over 1024x1024")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, SRC_NAME)
    shutil.copyfile(src, dst)
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    print(f"wrote {dst} ({width}x{height}, {size} bytes, sha256 {digest})")


if __name__ == "__main__":
    main()
