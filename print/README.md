# Print edition

Revised 20 November 2026. The primary digest is **68 pages at 5.5 × 8.5 inches**,
with mirrored glue margins and 0.125-inch bleed. A new printer-calculated spine
is required; the 0.14-inch wrap is retained only as `Horizons-77-digest-cover-48pp.pdf`
for the previous 48-page order. Do not pair that wrap with the revised interior.

Read the [current design compass](../devlog/20261120-editorial-and-design-compass.md)
and [current proof evidence](../devlog/20261120-spreads-as-worlds/README.md).
The web now has 67 folios. The Letter edition and its imposition are preserved
as the earlier layout, not equivalent exports of the redesigned digest.

The three features use explicit physical-point compositions in `digest-features.py`:
sharp serif ocean headlines, condensed industrial headings for hillside and flight,
large plates and different arrangements of text, notes and illustration. Body type
is fixed at 9.4/12.2 pt in these features; column splitting is measured rather than
solved by shrinking. The contributor compositor in `digest-contributors.py` replaces the old article
and office templates, uses fixed 9–10.4 pt reading type, and draws panoramic art
in trim coordinates. The inhabited ocean, six-page Alexander essay and four-page architectural exchange
use `digest-worlds.py`, including measured columns that change width beside the art.
Atlas and document leaves retain their earlier body settings via logical legacy mapping. The whole-book proof has 72 pages including front/back and two blank
inside covers. The facing-spread PDF is for review, not printer imposition.

## Rebuild

Requires Node with `sharp`, and Python with `reportlab`, `pypdf`, `Pillow`, `lxml`.
The print fonts are bundled in `assets/fonts/`, with the publisher’s license.

```sh
node print/export.cjs
python3 print/build-digest.py
python3 print/verify-digest.py
# Optional: rebuild the earlier Letter layout separately
python3 print/build.py
```

`HORIZONS_PRINT_TMP` overrides the temporary cache directory;
`HORIZONS_ROOT` overrides the repository root. `NODE_PATH` may be used when
`sharp` is supplied by a bundled workspace runtime rather than a local install.
The build reads the current magazine source, including `workshop-leaves.js` and `edition-inserts.js`, and writes the PDFs and pagination
record to `output/pdf/`. Rendering and proofing are separate steps.

The imposed PDF is a convenience for basic duplex printing. A shop should
usually use the reader-order PDF and its own imposition software. Check a
physical folded proof, particularly duplex orientation, before a full run.

The digest-spreads PDF places consecutive facing pages together for screen
reading; it is not a print imposition. The current production body is the digest interior in reader order. The tabloid
imposition belongs to the earlier Letter edition; it is not a digest production file.

The word أُنس is kept in logical reading order in the source and web edition, with a locally bundled Amiri font (SIL OFL). The print paragraph uses a verified joined, visual-order form of this single word in embedded Amiri. The four-line Arabic poem in `edition-inserts.js` likewise retains logical text for the web and a checked, shaped visual-order cache (`printLines`) for the fixed PDF lines. That cache was prepared with arabic-reshaper and python-bidi and visually proofed in Amiri; the regular build does not need those authoring dependencies. Any change to those Arabic lines requires re-shaping and visual proofing. Do not reverse arbitrary Arabic text.

All reading columns use left alignment with a ragged right edge, preserving natural word spacing in the digest as well as Letter. Long words can wrap and URI-aware breaking allows long references to fit without widening spaces. The web edition uses the same alignment throughout, with language-aware hyphenation and emergency wrapping for links.

Illustrations reserve their measured caption height, including wrapped lines, plus a 12-point working gap before following prose. Supporting notes measure the entire title/image/caption/text arrangement before choosing a stacked or side-by-side layout.

The digest compositor in `digest-layout.py` enlarges selected plates and most body
settings, then places measured reading panels in available space. Panels include
Machado, the 1923 wording of Hughes’s “Dreams,” a Rilke stanza, an eight-word Snyder
extract with commentary, original Arabic verse, correspondence and workshop notices.
Existing marginal notes are folded into these panels rather than printed twice.
`digest-pagination.json` records panel bottoms and body fits; overflow stops the build.
The Fuller/Snelson text and its sources remain complete; the web keeps the
tensegrity study, and the digest gives the model and exchange a dedicated page.
