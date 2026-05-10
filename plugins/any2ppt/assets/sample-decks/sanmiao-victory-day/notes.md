# Notes — Why This Deck Worked

This sample documents an image-first deck that successfully turned a 30-minute Mandarin-language podcast into an 8-slide lecture deck. The full run lives outside this repository (it includes raw audio, a long transcript, and the generated 4K slide images). Only the brief, storyboard, and four representative prompts are kept in-tree as teaching material.

## What Worked

### 1. The thesis fits in one slide

`01_core_thesis` is a single-slide compression of the entire talk. Every other slide just unpacks one piece of that thesis. This is the discipline `story-architect` is supposed to enforce: a thesis is not a section heading, it is a sentence that survives the rest of the deck being deleted.

### 2. The argument is anchored on a concrete dispute

`02_date_dispute` (May 8 vs May 9) gives the audience a small, factual entry point before the deck starts arguing. Abstract claims about "narrative authority" land much better when the next slide already showed a concrete artifact of that authority. This is the slide-storyboarder pattern of "anchor abstract claims on concrete evidence early".

### 3. Image-first was the right mode for this content

The deck is consumed visually (podcast viewer, screen-shared on social media). Editability did not matter; visual polish did. The choice of `image-first` was deliberate and recorded; it was not a default fall-through.

### 4. Visual style stayed consistent across all eight slides

The same palette (off-white, charcoal, muted red, steel gray) and the same lecture-deck typography were specified in `prompts/README.md` and repeated in every per-slide prompt. This is what stopped the deck from looking like eight unrelated images glued together.

### 5. Visuals supported the argument; they were never decorative

Every per-slide prompt contains a "Negative" block that explicitly forbids cinematic empty backgrounds, decorative pseudo-text, and stock-photo people. This is what made the slides usable as teaching material rather than as wallpaper.

## What to Reuse in New Decks

When `visual-director` writes a new image-first prompt pack, copy these patterns:

- A `prompts/README.md` that fixes palette, typography, and a hard "Negative direction" list **before** any per-slide prompt is written.
- A per-slide structure of: Meta / Visual Concept / Composition / Text to Render / Style / Negative.
- Explicit "Text to Render" blocks that name the exact characters the image should contain. Vague "render the title" instructions are the most common failure mode.
- Negative blocks that ban the most common generator failures (logos, real people, decorative pseudo-text, cinematic emptiness).

## What Not to Copy Blindly

- The Traditional Chinese rendering succeeded only because the prompts repeated the exact characters in a labeled "render exactly" block. For other languages or scripts, expect to need similar exact-match text blocks.
- The `premium` budget allowed multiple regeneration passes per slide. Under `balanced` budget, plan for one good prompt rather than three good attempts.
- The deck used opinionated political analysis as content. The storyboard frames every claim as the host's argument; do not assume neutral framing comes from the model.

## Skill Notes Carried Forward

- `story-architect` should ship a one-sentence thesis that survives the deck being shortened to one slide.
- `slide-storyboarder` should anchor abstract claims on concrete evidence early.
- `visual-director` should fix global style first, write per-slide prompts second, and ban specific generator failure modes by name.
- `deck-producer` should record the chosen production mode in `run.json` and the brief's "Skill Notes". This sample is `image-first` because the audience consumes images, not because `image-first` is the default.

## What Is Excluded From This Sample

To keep the sample slim and rights-clean:

- The original audio file.
- The full transcript.
- The 8 generated 4K slide images.
- The final delivery PPTX/PDF container.
- Any third-party media references (book covers, photographs, archive material).

The full run remains in `local-runs/sanmiao-victory-day/` (gitignored) for the project owner.
