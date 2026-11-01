# Print edition

Revised 2026-10-31. The **5.5 × 8.5-inch, 48-page digest is the principal print edition**.
It has mirrored glue margins, 0.125-inch bleed, a separate 0.14-inch-spine outside
cover, and blank inside covers. The secondary Letter edition retains its 48-page
layout and optional 11 × 17 saddle-stitch imposition. The web has 52 folios.
Finished files are in [`output/pdf/`](../output/pdf/).

Interiors use white paper without simulated yellowing or seams.
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
python3 print/build-digest.py
```

`HORIZONS_PRINT_TMP` overrides the temporary cache directory;
`HORIZONS_ROOT` overrides the repository root. `NODE_PATH` may be used when
`sharp` is supplied by a bundled workspace runtime rather than a local install.
The build reads the current magazine source, including `workshop-leaves.js` and `edition-inserts.js`, and writes the PDFs and pagination
record to `output/pdf/`. Rendering and proofing are separate steps.

The imposed PDF is a convenience for basic duplex printing. A shop should
usually use the reader-order PDF and its own imposition software. Check a
physical folded proof, particularly duplex orientation, before a full run.

The new reader-spreads PDF places consecutive facing pages together for screen
reading; it is not a print imposition. The production files remain the ordinary
reader-order PDF and the separately imposed tabloid PDF.

The five opening papers now cover distinct topics rather than repeating one editorial in translation. The kitchen interview follows the Spanish land paper (print page 5), correspondence follows ocean habitats (page 11), and the provisional accounts follow energy (page 30). Only the production desk remains near the closing material (page 41). Web and print folios differ; both contents pages use their own current page numbers.

The word أُنس is kept in logical reading order in the source and web edition, with a locally bundled Amiri font (SIL OFL). The print paragraph uses a verified joined, visual-order form of this single word in embedded Amiri. The four-line Arabic poem in `edition-inserts.js` likewise retains logical text for the web and a checked, shaped visual-order cache (`printLines`) for the fixed PDF lines. That cache was prepared with arabic-reshaper and python-bidi and visually proofed in Amiri; the regular build does not need those authoring dependencies. Any change to those Arabic lines requires re-shaping and visual proofing. Do not reverse arbitrary Arabic text.

All reading columns use left alignment with a ragged right edge, preserving natural word spacing in the digest as well as Letter. Long words can wrap and URI-aware breaking allows long references to fit without widening spaces. The web edition uses the same alignment throughout, with language-aware hyphenation and emergency wrapping for links.

Illustrations reserve their measured caption height, including wrapped lines, plus a 12-point working gap before following prose. Supporting notes measure the entire title/image/caption/text arrangement before choosing a stacked or side-by-side layout.

The digest compositor in `digest-layout.py` enlarges selected plates and most body
settings, then places measured reading panels in available space. Panels include
Machado, the 1923 wording of Hughes’s “Dreams,” a Rilke stanza, an eight-word Snyder
extract with commentary, original Arabic verse, correspondence and workshop notices.
Existing marginal notes are folded into these panels rather than printed twice.
`digest-pagination.json` records panel bottoms and body fits; overflow stops the build.
Fuller’s opening uses a unique tensegrity principle drawing, crediting Snelson’s
sculptural discovery and Fuller’s interpretation, with sources in the edition notes.
