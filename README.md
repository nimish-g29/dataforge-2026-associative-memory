# One Synapse, Many Memories
### An interactive explainer on Associative Memory & Synaptic Plasticity, connected to Pathway's Dragon Hatchling (BDH)
**DataForge 2026 — Pathway Track ("Explain the Frontier")**

**Live artifact:** *(see SUBMISSION_STEPS.md — you must host this yourself; instructions are exact)*
**Source repository:** (https://github.com/nimish-g29/dataforge-2026-associative-memory)
**Concept summary (the "blog"):** [`dataforge-concept-summary.pdf`](./dataforge-concept-summary.pdf)

---

## 1. The claim

> A fixed-size memory can store many key→value associations by summing them into the same weights.
> It doesn't fail all at once: as more associations share the same synapses, or as stored keys become
> more alike, retrieval degrades **smoothly** because of interference — not catastrophic collapse.

This is falsifiable and the artifact is built to let a learner try to break it: add memories past the
point where you'd expect failure, correlate the keys, remove the dimension headroom — and watch whether
the claim survives.

## 2. Intended learner & prerequisites

- **Audience:** ML-curious learners and researchers who are comfortable with vectors and the dot product,
  but need no prior exposure to Hebbian learning, associative memory, or BDH specifically.
- **Prerequisites:** vectors, dot product, outer product, matrix-vector multiplication. No linear algebra
  beyond that, no ML background assumed.

## 3. Learning objectives

By the end, a learner should be able to:
1. State the Hebbian write rule (`M ← λM + key⊗value`) and the read rule (`value_est = sign(Mᵀ·key)`) from memory.
2. Predict — before touching a slider — how dimension, decay, and key correlation each change retrieval accuracy, and explain why in terms of signal vs. interference.
3. Name where this exact mechanism appears inside BDH, what's different there (sparsity, locality, graph structure vs. a flat matrix), and which claims about it are developer-reported vs. independently checked.
4. State one concrete limitation of the toy model and one common misconception about memory capacity in larger systems.

## 4. Architecture of the artifact

Single self-contained HTML file (`index.html`) — no backend, no build step, no external JS framework.
All computation is vanilla JavaScript running client-side; all visuals are `<canvas>` and CSS grid, drawn
at runtime. External dependency: Google Fonts (see §10).

```
index.html
├── <nav>            sticky links to this artifact, the concept-summary PDF, and the repo
├── #top (hero)       one-line claim, audience/prerequisites, live preset stats
├── #walkthrough      4-step guided stepper: write 3 memories one at a time, watch one
│                      specific synapse (matrix cell) change value at each step
├── #sandbox           the open lab: dimension / decay / key-correlation / cue-noise
│                      sliders, add/remove memories, live heatmap, multi-pattern
│                      truth-vs-estimate cards, dual capacity curve (orthogonal vs.
│                      current correlation)
├── #bdh               BDH connection: side-by-side write rules, the sparsity↔correlation
│                      argument, an explicit "what this is/isn't" scope disclosure,
│                      and an on-page evidence-level table
├── (limitation)       one stated limitation + common misconception
├── (60-second check)  prediction-then-reveal widget, computed live on click
└── (explain it back)  ungraded free-text reflection box, not stored or sent anywhere
```

## 5. Role of every major component

| Component | What it does | Depends on |
|---|---|---|
| `randBipolar`, `correlatedKey`, `zeroMatrix`, `decayMatrix`, `outerAdd`, `readMemory`, `accuracy` | The entire mathematical substrate — Hebbian write, leaky decay, sign-thresholded read, bit-accuracy scoring | Nothing external; pure JS arithmetic |
| Walkthrough stepper | Drives the 3-step guided write sequence and the single "watched cell" | Substrate functions above |
| Sandbox sliders (`dimSlider`, `decaySlider`, `corrSlider`, `noiseSlider`) | Mutate global state (`SDIM`, `DECAY`, `CORR`) and trigger a full matrix rebuild or fresh simulation | Substrate functions above |
| `drawHeatmap` / `drawGrid` | Render the matrix and vector bit-patterns to `<canvas>` / CSS grid | Canvas 2D API only |
| `computeCurve` / `pointAccuracy` | Run fresh Monte Carlo trials (6–20 trials per point) to compute the capacity curve and the prediction-reveal numbers | Substrate functions above |
| BDH module text and equations | Static, hand-written content paraphrased from primary sources (§9) | — |
| Evidence table | Static, hand-written; each row's evidence-level tag is asserted by a human, not computed | — |

## 6. What's live, precomputed, synthetic, or animated

| Element | Status |
|---|---|
| Memory-matrix heatmap, retrieval grids, accuracy percentages, capacity curve, prediction-reveal numbers | **Live** — recomputed in your browser on every interaction, using a seeded PRNG (`mulberry32`) so results are reproducible run-to-run but not hand-picked |
| Stored keys/values | **Synthetic** — randomly generated bipolar vectors (with optional correlation), not real-world data |
| BDH/BDH-CQ equations and architecture claims | **Precomputed knowledge, paraphrased from primary sources** — not derived or reproduced by this artifact; explicitly labeled as such throughout §7 of the page |
| Walkthrough heatmap outline (the "watched cell") | **Live**, but the three memories shown are fixed (seeded) so the walkthrough is repeatable for every learner |
| Everything else (text, layout) | Static content, not animation |

Nothing in this artifact is a scripted/faked animation standing in for real computation.

## 7. How to reproduce the results

No installation, no dependencies, no build step.

1. Clone or download the repo.
2. Open `index.html` directly in any modern browser (double-click, or `open index.html` / drag into a
   browser window) — **or** serve it locally:
   ```bash
   cd <repo-folder>
   python3 -m http.server 8000
   # then visit http://localhost:8000/index.html
   ```
3. All numbers are computed fresh in-browser using a seeded PRNG. Reloading the page reproduces the same
   walkthrough values every time; sandbox values vary run-to-run by design (they're live simulations, not
   a fixed lookup), but their *statistical shape* (smooth degradation with more memories, worse with higher
   correlation, better with higher dimension) reproduces consistently.
4. To regenerate the concept-summary PDF from source: `python3 make_summary.py` (requires `reportlab`,
   installed via `pip install reportlab`). This is a build tool for the PDF only — it is not part of the
   live artifact.

There is no notebook and no server-side component in this submission.

## 8. Primary papers (2022–2026) used, cited beside their claims

| Paper | Year | Where it's used / what it supports |
|---|---|---|
| Pathway, *"The Dragon Hatchling: The Missing Link between the Transformer and Models of the Brain,"* arXiv:2509.26507 | 2025 | Primary source for BDH's Hebbian synapse mechanism, cited in the BDH module and evidence table |
| Pathway, *"BDH-CQ: In-Context Learning with Recurrent Latent Reasoning,"* arXiv:2608.09888 | 2026 | Primary source for BDH-CQ's demonstration-driven contextual memory and its ARC-AGI-1 result, cited in the BDH module and evidence table |
| Hu, Yang, Wu, Xu, Chen & Liu, *"On Sparse Modern Hopfield Model,"* NeurIPS 2023 (arXiv:2309.12673) | 2023 | Cited beside the sparsity↔correlation claim in the BDH module — independent, peer-reviewed evidence that sparsity provably improves associative-memory capacity, used to support (not fabricate) the BDH analogy |
| Hu, Wu & Liu, *"Provably Optimal Memory Capacity for Modern Hopfield Models: Transformer-Compatible Dense Associative Memories as Spherical Codes,"* NeurIPS 2024 (arXiv:2410.23126) | 2024 | Cited in the evidence table as current, peer-reviewed theory on associative-memory capacity bounds — evidence the core concept is an active research area right now, not settled decades ago |

Classical (pre-2022) sources — Anderson (1972), Kohonen (1972), Hopfield (1982) — are cited for the
original correlation-matrix-memory formulation this toy implements, but are not counted toward the
2022–2026 requirement; the four papers above satisfy it.

## 9. Source and license record

| Item | Source | License |
|---|---|---|
| All JavaScript (memory math, rendering, UI logic) | Written for this submission | This repo's code license (see §12) |
| All HTML/CSS | Written for this submission | This repo's code license |
| Fonts: Spectral, IBM Plex Sans, IBM Plex Mono | Google Fonts CDN (`fonts.googleapis.com`) | SIL Open Font License 1.1 (all three) |
| Concept-summary PDF generator (`make_summary.py`) | Written for this submission, using the `reportlab` Python library | `reportlab`: BSD license (build-time tool only, not shipped to learners) |
| Data (stored key/value vectors) | Synthetically generated at runtime by this artifact | N/A — not external data |
| Model weights | None used | N/A |
| Images | None used — all visuals are `<canvas>`/CSS, generated at runtime | N/A |

No third-party JS libraries, ML frameworks, model checkpoints, or datasets are used anywhere in the
artifact itself.

## 10. AI assistance, code, data, asset, and license disclosure

- **AI assistance:** Substantial portions of the code, page copy, and this README were drafted with AI
  assistance (Claude, Anthropic). The human author selected the topic, directed the design and content of
  every section, tested every interactive feature by hand, requested specific corrections (including the
  mobile-layout fix and the evidence-table overflow fix described in the commit history / conversation
  log), and is responsible for understanding and defending every component live, per the hackathon's
  ownership requirement.
- **Code:** original for this submission (see §9); no forked repository.
- **Data:** none external; all data shown is generated synthetically at runtime.
- **Assets:** no images, icons, or media assets beyond the three Google Fonts listed in §9.
- **License of reused BDH claims:** all BDH/BDH-CQ content is paraphrased explanation of publicly
  published research, with primary-source citations; no BDH source code, weights, or proprietary material
  is reproduced.

> **Before submitting:** replace this paragraph with your own first-person account of what you changed,
> tested, and can defend — judges score "technical ownership and live defense" separately from
> correctness, and a disclosure written entirely by AI about AI assistance undercuts that.

## 11. Known limitations (of the artifact itself)

- Dense, unnormalized Hebbian sums with no cleanup network — real associative-memory systems (see §8)
  add sparsity, normalization, or an explicit cleanup step to push capacity further; this toy shows the
  raw phenomenon underneath those fixes, not a production-grade memory system.
- The sparsity↔correlation connection to BDH (§6 of the page) is a structural analogy supported by
  independent Hopfield-network literature, not a specific measured BDH statistic — this is stated
  explicitly on the page and should stay that way.
- No claim here reproduces BDH's or BDH-CQ's reported benchmark numbers; those are cited, not recomputed.

## 12. Credits & license

- Built by **[YOUR NAME]** for DataForge 2026 (IIT Kharagpur), Pathway track.
- Code in this repository: **[CHOOSE A LICENSE — e.g. MIT]**.
- Written content (README, page copy, concept summary): **[CHOOSE A LICENSE — e.g. CC BY 4.0]**.
- Not affiliated with or endorsed by Pathway; independent educational reimplementation.
