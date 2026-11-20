# Horizons ’77

[Read the magazine →](https://anselm.github.io/tenerife-horizons-77/)

**Friendship and the art of seeing together**

Papers, drawings, walks and conversations among friends new and old.

An alternative-history magazine assembled at the close of an imagined Tenerife futures conference in 1977. Architecture, communal life, undersea habitats, cooperative finance, energy, and personal gliders raised by skyscraper lift stations. English, Spanish, French, Italian and German, with a small Arabic contribution.

The complete issue is one continuous numbered sequence, shown as facing pages on wide screens and single pages on smaller screens. Printed “see page…” references work quietly as links. Viewer controls sit outside the magazine paper. All articles, translations, atlas annotations and conference inserts appear in the reading flow.

## Print edition — digest first

The principal edition is a **68-page, 5.5 × 8.5-inch digest**, including a blank
endpaper. The newest experiments compose inhabited worlds across the binding:
the ocean room and tram (pp. 14–15), Alexander’s village stair (32–33), and an
imagined architectural working table (54–55). The village essay now has six pages;
the architectural exchange has four, including Fuller/Snelson and the Arabic poem.
The full writing remains, with live type following the shapes of the drawings.

These sit among the French coastal photomontage (6–7), the Drago excursion (12–13),
hillside section (28–31), flight proposal (42–45), and film-desk fantasy (50–51).

- [Facing-spread design proof](output/pdf/Horizons-77-digest-spreads.pdf) — best for reviewing the new compositions.
- [Whole-book reading proof](output/pdf/Horizons-77-digest-proof.pdf) — front/back and blank inside covers included.
- [Digest interior](output/pdf/Horizons-77-digest-interior.pdf) — 68 single pages with trim and bleed boxes.
- [Print setup and cover status](output/pdf/DIGEST-MIXAM.txt).

**A new cover spine measurement is needed for 68 pages.** The previous
[48-page cover wrap](output/pdf/Horizons-77-digest-cover-48pp.pdf) is preserved
for the earlier order and must not be paired with this revised interior.
The target stock remains 50lb uncoated text and 80lb uncoated outside-only cover.

The web edition has 67 folios and its own page references. The earlier
[Letter edition](output/pdf/Horizons-77-print-letter.pdf),
[tabloid imposition](output/pdf/Horizons-77-booklet-tabloid.pdf), and
[Letter spreads](output/pdf/Horizons-77-reader-spreads.pdf) remain available
as the previous layout. They do not contain this digest redesign.
See [print source notes](print/README.md).

## Current editorial and design guidance

Read the [20 November design compass](devlog/20261120-editorial-and-design-compass.md)
before changing type, layouts or tone. It replaces the fixed-page-count and
uniform-template assumptions in earlier print notes. [Anselm's note on the
dreamers](devlog/20261120-the-dreamers.md) preserves the emotional intent:
friendships, quixotic hopes, mortality, and sympathy for those who keep imagining.
[Spreads as worlds: prompts, decisions and proof evidence](devlog/20261120-spreads-as-worlds/README.md)
records the current experiments. [Contributed pages](devlog/20261120-contributed-pages/README.md)
preserves the preceding broader revision. The [earlier three-feature pass](devlog/20261120-restored-spreads/README.md)
is retained as an earlier stage, not the current page map.

## View locally

Open `index.html`, or serve this folder:

```sh
python3 -m http.server 8777 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8777`. No build, dependencies, accounts or external fonts are required.

## GitHub Pages

The magazine is published at [anselm.github.io/tenerife-horizons-77](https://anselm.github.io/tenerife-horizons-77/). GitHub Pages serves the `main` branch from the repository root; pushed changes update the site automatically.



## Reading order

The in-magazine contents and numbered links are generated from the current
web sequence. Ocean begins on 16, hillside on 30, the village on 34, flight on 44,
Clarke on 48, and the architecture discussion on 57 (its picture spans 58–59).
The French panorama is 8–9; the film-desk panorama is 54–55; edition notes begin on 67.
These differ from the digest’s printed folios. `output/pdf/digest-pagination.json`
records the print mapping; use the contents in the edition you are reading.

The magazine and conference are fictional. Real luminaries appear as imagined contributors without fabricated authentic quotations or claims of historical attendance. The landscape and Bocacangrejo plate are newly generated images; the maps and technical drawings are original graphics. See the final edition notes and `ART-DIRECTION.txt`, `BOCACANGREJO-ART.txt` and `OCEAN-OBSERVATORY-ART.txt` and `COAST-NOTEBOOK-ART.txt` and `COAST-NOTEBOOK-ART-V2.txt` for provenance.

Conceived in a 2025 conversation; digital edition made in October 2026.

The Alexander essay, coastal excursion, revelation and influence on the completion of *The Timeless Way of Building* are fictional additions to this alternative timeline. The real Alexander archive contains a 1970 draft; no actual book-origin claim or authentic quotation is represented.

Cousteau, Goodall and Gilliam conference features are original alternative-history fiction grounded in their 1977 work. All visits, conversations and Tenerife influences are invented; historical sources are linked in the final edition notes.

The horse photograph was supplied for this edition and is a contemporary image, not a recovered 1977 photograph.

## Development log

The current dated guidance and restoration snapshot are linked above. Earlier entries below are grouped by year and numbered in reading order. Numbers mark the narrative sequence, not months or separate workdays. The original conversation began March 30, 2025; the web edition was built October 22, 2026. These notes were assembled on October 22, 2026 from the surviving conversation and repository history. No activity is implied in the intervening gap.

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

- [31 · Natural word spacing](devlog/2026/31-natural-word-spacing.md)

- [Different days at sea](devlog/2026/32-different-days-at-sea.md)

- [Room for captions](devlog/2026/33-room-for-captions.md)

- [34 · The digest comes first](devlog/2026/34-the-digest-comes-first.md)

- [35 · A table that can travel](devlog/2026/35-a-table-that-can-travel.md)
