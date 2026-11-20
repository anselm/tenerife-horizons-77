# Spreads as inhabited worlds

20 November 2026. A further experiment after the contributed-page revision,
responding to Anselm’s generated magazine references and permission to change
length and abandon settled layouts. The references suggested multiple ways into
a spread, illustrations that determine the reading area, and an ordinary human
life inside extraordinary proposals.

This is the current stage for the ocean, village/Alexander and architectural
gathering. It supersedes their previous compositions, not their writing. The
[design compass](../20261120-editorial-and-design-compass.md) remains the editorial
entry point. Earlier snapshots preserve earlier stages rather than current folios.

## Three experiments

- **Ocean, digest 14–17; web 16–19.** The opening pair is a continuous drawing of
  a submarine tram and an inhabited coastal room. A condensed headline, italic
  Italian line and narrowing prose measure occupy the drawing’s unprinted edge.
  The room contains books, a table, coats and people. The subsequent spread keeps
  the whole argument and the service drawing, objection and amendment.
- **Village, digest 32–37; web 34–39.** A diagonal stair links rooms, neighbours,
  the fisherman and a companion. The first two paragraphs occupy cavities in the
  drawing. Four further leaves preserve Alexander’s full essay. The bucket scene
  has unequal measures; the revelation interrupts two-column reading at a much
  larger scale. The last pair carries the denser argument in readable 9.4/12.2 type.
- **Gathering, digest 54–57; web 57–60.** An imagined halftone working table crosses
  the binding. The digest then gives Fuller/Snelson a page, with the Arabic poem
  and local respondents opposite. The web introduces the argument on recto 57,
  ensuring the picture actually faces across 58–59. This is an illustrative
  reconstruction, not a recovered photograph or a verified engineering model.

The main edition grows from 64 to **68 interior pages**, including its blank last
endpaper. The whole-book reading proof has **72 pages**, including outside covers
and two blank inside covers. The web has **67 folios** and independent references.
No replacement spine width is guessed: the prior 0.14-inch cover wrap belongs to
48 pages. A fresh Mixam template is required before the next production cover.

## Art and composition

[Exact generation prompts](prompts.json) record the built-in image-generation
method. New assets are `ocean-inhabited-spread.png`, `village-stair-spread.png` and
`architects-working-table.png` in `assets/`. Original assets are retained. No essay
text was baked into the pictures. The new paintings are 1470 × 1070 pixels and
the table image 1536 × 1024; the two full-spread paintings are approximately
122 ppi at their placed size. They are texture-rich design proofs, not a claim
of 300 ppi reproduction. Judge a physical 100% sample on the chosen uncoated stock.

`print/digest-worlds.py` composes the three experiments in physical points.
Its shaped-column helper splits actual paragraphs across changing measures;
fixed line spacing and final-word protection prevent the gaps and isolated
last words found in the first proof. Background illustration overlap requires
visual inspection in addition to the text-box collision check. `world-pages.js`
and `worlds.css` carry the corresponding web compositions; narrow screens put
prose beneath the art without shrinking it to the illustrated page’s dimensions.

## Evidence

- [Ocean opening](ocean-14-15.png)
- [Village opening](village-32-33.png)
- [Architectural gathering](gathering-54-55.png)
- [Tensegrity and translation table](tensegrity-56-57.png)
- [All facing spreads](contact-sheet.png)

The PDF preservation check finds all **198 essay/report paragraphs** and all
**11 reading panels**. The browser’s rendered text was independently compared
with the same source paragraphs and reading-panel prose: none missing. Print
checks pass for trim/bleed boxes, safe text bounds, composed-element collisions,
facing-page parity and blank inside covers/endpaper. All eleven print font faces
are embedded. Desktop and 390-pixel mobile previews have no horizontal overflow,
no broken page references, and no clipped new prose. Lazy-loaded images are not
misreported as failures before loading. The new openings and continuations were
visually reviewed, along with a contact sheet of the whole issue.

The next useful judgment is artistic: which of these spatial compositions feels
most like an object worth inhabiting? Further changes should follow that reading,
not merely add more illustrations or make every remaining page imitate these.

Small editorial follow-up: the edition notes now credit Amber Case’s influence
through calm technology directly, without the sentence about having built many
projects together. The web and digest proofs carry the quieter acknowledgment.
