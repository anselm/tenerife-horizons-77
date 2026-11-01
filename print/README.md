# Print edition

Revised 2026-10-31. A separately typeset, 48-page Letter edition of the complete
magazine, with an optional 11 × 17 imposition for 12-sheet saddle stitching.
The 52-sheet web version retains its numbered sequence and now opens in facing spreads. Finished PDFs and the shop brief are in
[`output/pdf/`](../output/pdf/).

The PDFs use white paper, no simulated seam, no bleed and generous margins.
Typesetting uses URW Gothic display capitals, URW Bookman, Nimbus Roman and Nimbus Sans, balanced columns, and protected
short paragraph endings. Fixed print pagination is generated independently of
web folios. Every placed image is used once. Four new editorial pages use three narrow columns, interview exchanges, correspondence, boxed notices and a dedicated editorial cartoon. A new terrace plate, a screening-room
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

The five opening papers now cover distinct topics rather than repeating one editorial in translation. The kitchen interview follows the Spanish land paper (print page 5), correspondence follows ocean habitats (page 11), and the provisional accounts follow energy (page 30). Only the production desk remains near the closing material (page 41). Web and print folios differ; both contents pages use their own current page numbers.

The word أُنس is kept in logical reading order in the source and web edition, with a locally bundled Amiri font (SIL OFL). The print paragraph uses a verified joined, visual-order form of this single word in embedded Amiri. Adding more Arabic will require a general shaping and bidirectional layout pass; do not reverse arbitrary Arabic text.
