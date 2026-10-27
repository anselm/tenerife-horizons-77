# Print edition

Recorded 2026-10-27. A separately typeset, 52-page Letter edition of the complete
magazine, with an optional 11 × 17 imposition for 13-sheet saddle stitching.
The 48-sheet web version is unchanged. Finished PDFs and the shop brief are in
[`output/pdf/`](../output/pdf/).

The PDFs use white paper, no simulated seam, no bleed and generous margins.
Typesetting uses embedded Georgia and Arial, balanced columns, and protected
short paragraph endings. Fixed print pagination is generated independently of
web folios. The source illustrations are preserved; simple workshop graphics
are redrawn for the print layout. Source citations print as readable titles and
domains; complete URLs remain in the web edition.

## Rebuild

Requires Node with `sharp`, and Python with `reportlab`, `pypdf`, `Pillow`, `lxml`.
The default font directory is macOS `/System/Library/Fonts/Supplemental/`;
set `HORIZONS_FONT_DIR` for another folder containing the named font files.
Fonts are not redistributed as source assets.

```sh
node print/export.cjs
python3 print/build.py
```

`HORIZONS_PRINT_TMP` overrides the temporary cache directory;
`HORIZONS_ROOT` overrides the repository root. `NODE_PATH` may be used when
`sharp` is supplied by a bundled workspace runtime rather than a local install.
The build reads the current magazine source and writes the PDFs and pagination
record to `output/pdf/`. Rendering and proofing are separate steps.

The imposed PDF is a convenience for basic duplex printing. A shop should
usually use the reader-order PDF and its own imposition software. Check a
physical folded proof, particularly duplex orientation, before a full run.
