# Print edition

Recorded 2026-10-27. A separately typeset, 44-page Letter edition of the complete
magazine, with an optional 11 × 17 imposition for 11-sheet saddle stitching.
The 48-sheet web version retains its numbered sequence and now opens in facing spreads. Finished PDFs and the shop brief are in
[`output/pdf/`](../output/pdf/).

The PDFs use white paper, no simulated seam, no bleed and generous margins.
Typesetting uses embedded URW Bookman, Nimbus Roman and Nimbus Sans, balanced columns, and protected
short paragraph endings. Fixed print pagination is generated independently of
web folios. The cover image appears only once. A new terrace plate, a screening-room
illustration and original working diagrams provide subject-specific artwork. Source citations print as readable titles and
domains; complete URLs remain in the web edition.

## Rebuild

Requires Node with `sharp`, and Python with `reportlab`, `pypdf`, `Pillow`, `lxml`.
The print fonts are bundled in `assets/fonts/`, with the publisher’s license.

```sh
node print/export.cjs
python3 print/build.py
```

`HORIZONS_PRINT_TMP` overrides the temporary cache directory;
`HORIZONS_ROOT` overrides the repository root. `NODE_PATH` may be used when
`sharp` is supplied by a bundled workspace runtime rather than a local install.
The build reads the current magazine source, including `workshop-leaves.js`, and writes the PDFs and pagination
record to `output/pdf/`. Rendering and proofing are separate steps.

The imposed PDF is a convenience for basic duplex printing. A shop should
usually use the reader-order PDF and its own imposition software. Check a
physical folded proof, particularly duplex orientation, before a full run.

The new reader-spreads PDF places consecutive facing pages together for screen
reading; it is not a print imposition. The production files remain the ordinary
reader-order PDF and the separately imposed tabloid PDF.
