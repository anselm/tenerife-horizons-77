# Horizons ’77

[Read the magazine →](https://anselm.github.io/tenerife-horizons-77/)

**Friendship and the art of seeing together**

Papers, drawings, walks and conversations among friends new and old.

A 52-page alternative-history magazine assembled at the close of an imagined Tenerife futures conference in 1977. Architecture, communal life, undersea habitats, cooperative finance, energy, and personal gliders raised by skyscraper lift stations. English, Spanish, French, Italian and German.

The complete issue is one continuous numbered sequence, shown as facing pages on wide screens and single pages on smaller screens. Printed “see page…” references work quietly as links. Viewer controls sit outside the magazine paper. All articles, translations, atlas annotations and conference inserts appear in the reading flow.

## Print today

A separate **48-page Letter print edition**, with clean white pages and fixed
pagination, is ready for small-run printing. The complete 52-sheet web edition
retains its numbered sequence.

- [Reader-order PDF — preferred for a print shop](output/pdf/Horizons-77-print-letter.pdf)
- [Already-imposed 11 × 17 booklet PDF](output/pdf/Horizons-77-booklet-tabloid.pdf)
- [Facing reader spreads — for screen reading](output/pdf/Horizons-77-reader-spreads.pdf)
- [Print instructions for twelve copies](output/pdf/PRINTING.txt)

Finished size: 8.5 × 11 inches. Folded booklet: 12 tabloid sheets per copy.
Choose **one** PDF workflow; do not apply booklet mode to the imposed file.
Ask for a folded duplex proof before the run. See [print source notes](print/README.md).

## View locally

Open `index.html`, or serve this folder:

```sh
python3 -m http.server 8777 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8777`. No build, dependencies, accounts or external fonts are required.

## GitHub Pages

The magazine is published at [anselm.github.io/tenerife-horizons-77](https://anselm.github.io/tenerife-horizons-77/). GitHub Pages serves the `main` branch from the repository root; pushed changes update the site automatically.


## Mixam digest edition

A separate **5.5 × 8.5-inch digest** is prepared for 10 colour PUR-bound copies:
48 interior pages on 50lb uncoated text, separate outside-only 80lb uncoated cover,
and the cart’s 0.14-inch spine. It keeps the two-column layout, with reflowed text,
mirrored binding margins and printer bleed.

- [Interior — upload as body](output/pdf/Horizons-77-digest-interior.pdf)
- [Outside cover wrap — upload as cover](output/pdf/Horizons-77-digest-cover.pdf)
- [Whole-book reading proof — do not upload](output/pdf/Horizons-77-digest-proof.pdf)
- [Mixam setup and upload instructions](output/pdf/DIGEST-MIXAM.txt)

Rebuild with `python3 print/build-digest.py` after the usual content export.
The Letter editions and website pagination are unchanged.

## Reading order

| Pages | Material |
| --- | --- |
| 1–2 | Cover and contents |
| 3–4 | An island is a beginning / English editorial |
| 5–6 | La isla no está vacía / land, water and staying / Spanish |
| 7 | Kitchen interview / questions and amendments |
| 8–9 | Rêver à plusieurs / human scale, reef and village / French |
| 10–11 | Una porta da chiudere / communal and private life / Italian |
| 12–13 | Unter dem Drachenbaum / El Drago, Humboldt and friendship / German |
| 14–15 | Ocean habitats |
| 16 | Letters, objections and editorial cartoon |
| 17–18 | Cousteau and the new odyssey |
| 19–20 | Montaña Amarilla and the coastal notebook |
| 21 | Oleaje / a future of his own |
| 22–23 | Goodall and the new institute |
| 24–25 | Maathai and the new Green Belt Movement |
| 26–27 | Hillside settlements |
| 28–31 | Alexander and Bocacangrejo |
| 32 | Rahman and the right to refuse |
| 33–34 | Island energy |
| 35 | Provisional conference accounts |
| 36–37 | Personal gliders and lift stations |
| 38–39 | Island atlas and annotations |
| 40–41 | Cooperative finance |
| 42–43 | Gilliam after Jabberwocky |
| 44–45 | Architectural portraits |
| 46 | The closing desk |
| 47–49 | Programme, delegate credential and cooperative certificate |
| 50–51 | Closing editorial |
| 52 | Edition notes and provenance |

The magazine and conference are fictional. Real luminaries appear as imagined contributors without fabricated authentic quotations or claims of historical attendance. The landscape and Bocacangrejo plate are newly generated images; the maps and technical drawings are original graphics. See page 52 and `ART-DIRECTION.txt`, `BOCACANGREJO-ART.txt` and `OCEAN-OBSERVATORY-ART.txt` and `COAST-NOTEBOOK-ART.txt` and `COAST-NOTEBOOK-ART-V2.txt` for provenance.

Conceived in a 2025 conversation; digital edition made in October 2026.

The Alexander essay, coastal excursion, revelation and influence on the completion of *The Timeless Way of Building* are fictional additions to this alternative timeline. The real Alexander archive contains a 1970 draft; no actual book-origin claim or authentic quotation is represented.

Cousteau, Goodall and Gilliam conference features are original alternative-history fiction grounded in their 1977 work. All visits, conversations and Tenerife influences are invented; historical sources are linked in the final edition notes.

The horse photograph was supplied for this edition and is a contemporary image, not a recovered 1977 photograph.

## Development log

Small steps through the project, grouped by year and numbered in reading order. Numbers mark the narrative sequence, not months or separate workdays. The original conversation began March 30, 2025; the web edition was built October 22, 2026. These notes were assembled on October 22, 2026 from the surviving conversation and repository history. No activity is implied in the intervening gap.

### 2025

- [01 · An island is a beginning](devlog/2025/01-an-island-is-a-beginning.md)
- [02 · Specific islands and a common sea](devlog/2025/02-specific-islands-and-a-common-sea.md)

### 2026

- [01 · Returning to the magazine](devlog/2026/01-returning-to-the-magazine.md)
- [02 · An object from another timeline](devlog/2026/02-an-object-from-another-timeline.md)
- [03 · One continuous issue](devlog/2026/03-one-continuous-issue.md)
- [04 · Fifty years ahead](devlog/2026/04-fifty-years-ahead.md)
- [05 · Restoring the fold](devlog/2026/05-restoring-the-fold.md)
- [06 · A home for the issue](devlog/2026/06-a-home-for-the-issue.md)
- [07 · The village that built us](devlog/2026/07-the-village-that-built-us.md)
- [08 · People at the table](devlog/2026/08-people-at-the-table.md)
- [09 · The sky, by lift](devlog/2026/09-the-sky-by-lift.md)
- [10 · An afternoon without a shore](devlog/2026/10-an-afternoon-without-a-shore.md)
- [11 · The place teaches](devlog/2026/11-the-place-teaches.md)
- [12 · A future of his own](devlog/2026/12-a-future-of-his-own.md)
- [13 · Less detail, more print](devlog/2026/13-less-detail-more-print.md)
- [14 · Keeping the sea in its time](devlog/2026/14-keeping-the-sea-in-its-time.md)
- [15 · Whose future?](devlog/2026/15-whose-future.md)
- [16 · First edition](devlog/2026/16-first-edition.md)
- [17 · Contributors](devlog/2026/17-contributors.md)
- [18 · The fool’s privilege](devlog/2026/18-the-fools-privilege.md)
- [19 · Paragraph endings](devlog/2026/19-paragraph-endings.md)
- [20 · A copy to carry](devlog/2026/20-a-copy-to-carry.md)
- [21 · Typeset as a magazine](devlog/2026/21-typeset-as-a-magazine.md)
- [22 · Lettering and captions](devlog/2026/22-lettering-and-captions.md)
- [23 · A harder heading](devlog/2026/23-a-harder-heading.md)
- [24 · Blackwater and thanks](devlog/2026/24-blackwater-and-thanks.md)
- [25 · Oleaje](devlog/2026/25-oleaje.md)
- [26 · After Habitat](devlog/2026/26-after-habitat.md)
- [27 · Five openings, one conversation](devlog/2026/27-five-openings-one-conversation.md)
- [28 · Dreaming at scale](devlog/2026/28-dreaming-at-scale.md)
- [29 · A digest to carry](devlog/2026/29-a-digest-to-carry.md)
- [30 · The art of seeing together](devlog/2026/30-the-art-of-seeing-together.md)
