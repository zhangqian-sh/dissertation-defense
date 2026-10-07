---
name: academic-slide-design
description: Edit this dissertation presentation using academic design preferences established through collaborative revision of the Content, ch2-04 encoding, ch2-05 DeepONet, and ch2-06 spiking marching slides. Apply to wording, typography, equations, figures, and layout while preserving the current page-by-page review scope.
---

# Academic slide design for this presentation

Use the collaboratively revised pages as examples of design reasoning, not templates to impose on every page. Aim for a clear scientific explanation, readable evidence, coherent grouping, and restrained academic typography. More text, boxes, or diagrams do not automatically make a slide more informative.

## Established choices and scope

- Use **Noto Serif for non-math text** and **KaTeX's default LaTeX-style math fonts**. Earlier Noto Sans, Libertinus, New York, and custom MathML font experiments are superseded.
- All main titles are **40px**, including cover and divider titles.
- Font sizes refer to **slide coordinates**, not SVG viewBox units. A label declared as 12px inside an SVG can appear larger or smaller when the figure scales. Compensate for the SVG-to-slide scale, or position text in HTML at the specified slide size. Preserve Slidev's whole-slide zoom; do not compensate for browser/device zoom as though it were figure scaling. The same text role must look the same size across figures with different viewBoxes.
- The current shared hierarchy for ch2-04–ch2-07 is **16px headings and diagram/caption labels**, **14px body text**, and **12px axis labels**. On ch2-06 the LIF equation base is 16px, and variable definitions and algorithm input/output are 14px. Main titles remain 40px. Apply these latest choices over older sizes recorded in the page histories below.
- For SVG axis text, `composables/useSvgAxisText.ts` measures the viewBox scale from the SVG's local dimensions and sets a compensating font size. `CoordinateEncodings.vue` and the ch2-07 `TracePlot` instances use it. Verify visible size rather than counting nominal SVG declarations as slide pixels. Extend compensation to other SVG text when editing it under the same typography requirement.
- Content-page part titles are **20px semibold**, topic titles **16px semibold**, and descriptions **14px regular**. These subordinate sizes belong to that page; choose other sizes according to the scientific content and readability.
- The user explicitly requested **no full-deck rebuilds or checks of other pages unless asked**. Work on the requested page or element. A targeted preview may inspect the current page; small edits do not automatically require a build, browser audit, Slurm job, or rendering task.
- Preserve the user's latest wording and edits. During collaborative calibration, apply these principles without assuming authorization for a deck-wide redesign. No additional approval ritual is needed for requested edits.
- Distinguish source edits, generated figures, and visual verification. The ch2-04 and ch2-06 arrow geometry was inspected in isolated browser renders at 8× zoom; this does not establish full-slide overflow or full-deck correctness. Report only the verification actually performed.

## Content page: changes and lesson

Source: `slides/ch01-introduction.md`; styles: `.content-outline` in `style.css`.

Previously, each entry combined a chapter-number prefix, topic title, processing chain, and implementation or evaluation details. The user replaced the descriptions with short statements of each chapter's central scientific idea and purpose.

- Retain the two research parts: chapters 2–4 on the left, 5–7 on the right. Read down each part, then move to the next. The proposed single-column outline was not adopted.
- Remove `Ch. X ·` prefixes from topic titles.
- Reduce descriptions from 16px to 14px; keep topic titles visually stronger.
- Shorten “Mesh-free RFormer” to “RFormer” and put meshfree reconstruction in its description.
- Use concise descriptions such as “Energy-based model for flow field reconstruction” and “Meshfree reconstruction inspired by language model.” Preserve the user's wording unless asked to edit it.
- Keep this page text-led; it needs no decorative figure.

**Lesson:** An outline establishes scientific identity and navigation. Save detailed mechanisms, ablations, metrics, precision, and memory management for the relevant scientific pages. Choosing the right level of abstraction can communicate more with fewer words. Do not fill space merely to increase density.

## ch2-04: changes and lesson

Title: **From continuous functions to spikes**.

Source: the encoding section of `slides/ch02-spiking-foundations.md`. Generator: `scripts/prepare_encoding_figure.py`. Figures: `public/figures/ch02/encoding_continuous.svg` and `encoding_discrete.svg`. Styles: `.encoding-*` in `style.css`.

Previously, spatial position ran horizontally in the continuous plot but vertically in the spike raster. Two separate formula blocks below the figures did not clearly connect the transformations to their objects.

- Regenerate both figures in Python from the same illustrative function. Put continuous values on the left and binary spikes on the right. Spatial position increases horizontally in both; the raster's vertical axis is spike step.
- Show the decoded approximation against the continuous curve, making quantization visible.
- Use **40 spike steps over [0, 0.2]**, giving a decoded increment of **0.005**. Changing the count requires regenerating the decoded trace as well as the raster.
- Connect the figures with an upper curved encoding arrow, left to right, and a lower curved decoding arrow, right to left.
- Use filled triangular arrowheads aligned with the terminal tangent. The final implementation uses explicit polygons: shafts end inside the heads, while the tips stay at the intended endpoints. A marker positioned at the endpoint alone did not fix protruding shaft pixels. Avoid hand-drawn V-shaped heads, abrupt hooks, and oversized points. See the ch2-06 arrow checks below.
- Position softly shaded, borderless formula annotations beside the arrows. Remove brown overlines from these annotations. Keep “Encoding” or “Decoding” beside its formula as one centered unit: the current gap is 12px, without an expanding spacer.
- Reduce the figures to 190px height and 86% width within their columns. This is a local composition choice, not a universal size cap. Preserve readable labels when adapting other figures.
- Render caption equations through Markdown/KaTeX. Separate Markdown content from surrounding HTML with blank lines. Avoid broad caption `span` rules that alter nested KaTeX spans; style only the intended outer element.
- Shorten the original title to the current one. Keep the note about the illustrative example, range, resolution, and internal versus physical time. Remove “51 spatial samples”: that incidental count distracts when the function itself is not explicitly defined.

**Lesson:** Arrange objects and transformations as one explanation. Matched axes establish correspondence; arrows express direction; nearby formulas explain those arrows. The audience should not need to mentally transpose an image or search a separate block for the meaning of a connection.

## ch2-05: changes and lesson

Title: **Example: DeepONet for 1d Poisson equation**.

Source: the Poisson example section of `slides/ch02-spiking-foundations.md`. Encoding illustrations: `components/CoordinateEncodings.vue`. Result figure: `public/figures/ch02/deeponet_poisson_triangular_long.png`. Styles: `.poisson-*` in `style.css`.

Previously, the results table occupied the upper left and the prediction figure the upper right, with operator and error formulas in separate blocks underneath. The page did not explain the problem or encoding choices before presenting their results.

- Give the left column the explanatory role: **setup above, encoding methods below**. Define the equation, domain, boundary conditions, and the forcing-to-solution learning task. Keep supporting experiment details concise.
- Give the right column the evidence role: **prediction examples above, metric and table below**. Put the relative L2 definition beside its heading and directly above the numerical comparison.
- Retain **all four published examples in one horizontal row**. The intermediate crop to one example was rejected. Identify the illustration as Ours at K=500; do not imply that it illustrates the highlighted K=50 row.
- Illustrate **Rate, Direct, and Ours**. Remove floating point from the illustration and table.
- Rename lower-triangular encoding to **Ours** in the displayed comparison. Highlight **Ours, K=50** with a light fill and stronger text, drawing attention to the comparison at the same horizon as Rate and Direct. Preserve reported values and retain the K=500 result as a separate row.
- Keep the method names above the illustrations. Remove repeated lower descriptions such as “Probabilistic spikes.” Use only explanations that add information; keep the blue-cell key concise.
- Prefer concise text tied to the page's purpose: the learning target, coordinate normalization, and the meaning of the figure. Avoid repeating architecture details or adding a disconnected protocol strip.
- Keep the smoothing qualification beside the evaluation: the reported errors use Savitzky–Golay smoothing with window 51 and order 3.

**Source verification matters:** The initial Direct illustration incorrectly used a diagonal one-hot raster inferred from the manuscript's latency-encoding section. The experiment code instead selects `SpikingDeepONet_Direct`, a learned encoder: coordinate input → learned dense projection → spiking dynamics over K steps → averaged readout. The illustration was corrected to that flow. Verify named methods against the implementation before drawing them; do not equate “direct” with “latency” merely because their names appear near each other in the manuscript.

Verification sources are the local SPINN repository under `/users/qzhang64/Projects/SpikingNN/SPINN`: `tensorflow2/tests/deeponet/run_deeponet_1d.py` selects the direct model; `tensorflow2/tests/deeponet/model/direct_encoding.py` defines its operations; `configs/DeepONet/spiking_de_configs.yaml` supplies its configuration. The schematic depicts those operations, not a measured trained spike raster.

**Lesson:** Assign clear roles to the page's regions. Here, the left explains the experiment and the right shows its evidence and evaluation. Introduce unfamiliar methods visually, group the metric with its table, and emphasize the comparison the audience should notice. Remove captions that only repeat what the figure already communicates. This arrangement is suitable for this example, not a mandatory four-quadrant template for every page.

## ch2-06: changes and lesson

Title: **Spiking marching scheme**.

Source: the method section of `slides/ch02-spiking-foundations.md`. Diagram: `components/SMSMethodDiagram.vue`. Styles: `.sms-*` in `style.css`.

The committed slide placed a large update formula above an embedded workflow image and a prose block. It described decoded predictions feeding the next history. My first redesign repeated that scientific mistake, then added redundant equations, labels, and awkward arrow connections. The collaborative revision corrected the computation and refined the geometry.

- **Verify the recurrence before drawing it.** Encode the two initial states once; predict and feed back thresholded spikes throughout the rollout; decode the saved trajectory after marching. Do not depict encode → SNN → decode inside every iteration. The implementation is the reference for this page: `/users/qzhang64/Projects/SpikingNN/spiking_marching_scheme/src/evaluate.py` performs spike-space feedback, and `src/main.py` decodes the completed trajectory.
- Give the wider left column the diagram and its explanations; give the right column the cascade algorithm and training note. The current column ratio is 1.5:1. Treat that ratio as a local choice rather than a template.
- Show the two input spike histories, the LIF → Dense → Dense network, and the predicted spike raster directly. These rasters are schematic, not measured predictions. Place mathematical state labels beneath the corresponding images.
- Remove “Predict,” “spatial position,” the parameter suffix after SNN, and repeated instructions about encoding or shifting history. State the spatial coordinate with mathematical notation when needed. Explain an operation once, where it helps interpret the diagram or algorithm.
- Explain **LIF** rather than merely naming it. Include the implemented voltage update and threshold equation, with definitions of voltage retention, threshold, input spikes, and output spikes. Its reset gates the next voltage update; verify against `src/nn/sequential/layer.py` rather than substituting an arbitrary textbook recurrence.
- Use a LaTeX-style algorithm block with a ruled heading, input/output, numbered initialization and loop steps, indentation, and final decoding. Remove the two formulas above the algorithm: they repeated the algorithm and weakened its hierarchy.
- Keep one-step evaluation (reference spike histories) and cascade evaluation (predicted spike histories) together beneath the explanation. Distinguish physical marching index n from internal spike index k.

**Arrow geometry is part of the explanation:** Connect the actual image or block boundaries. Do not end arrows at nearby axes, labels, or detached line segments. Keep routes clear of mathematical labels. For this feedback loop, the curved return arrow was rejected; straight segments with 90-degree turns route cleanly around the diagram. This does not replace the curved encoding/decoding arrows on ch2-04.

The thin marker heads and endpoint adjustments still left pixel defects. Both pages now use explicit filled triangles. On ch2-06, each head is 8 SVG units long and 7 units wide, centered on the shaft; the shaft stops 6 units before the tip, overlapping the triangle by 2 units. On curves, derive the triangle orientation from the endpoint tangent and shorten the shaft along that tangent. Ensure rounded or square shaft caps cannot protrude past the tip. Preserve the desired tip position when shortening the shaft.

Inspect the rendered junction and destination at high zoom, not just the SVG coordinates. The targeted checks used isolated component/arrow renders at 8× device scale, without rebuilding other slides. Check both the head–shaft junction and the tip–destination contact; a correct centerline does not guarantee clean visible pixels. Do not claim a fix solely because `refX` equals the marker width.

**Lesson:** Scientific accuracy, meaningful grouping, and careful geometry work together. More useful detail came from explaining LIF and making the recurrence explicit, while removing redundant formulas and labels improved readability. Choose arrow routes around the actual composition; avoid applying a favored curve or column layout mechanically.

## Apply the principles with judgment

- Decide what relationship the audience should see immediately, then choose the layout. In 16:9, side-by-side regions often support comparison, but neither two columns nor horizontal bands are mandatory.
- Group by meaning. A label and equation form one unit; an image and caption form another. Keep within-group spacing smaller than between-group spacing. Avoid scattered miniature cards and accidental pockets of whitespace.
- Use whitespace deliberately. Do not stretch related elements apart to fill a row. Do not enlarge every figure simply to occupy space or shrink result panels until their evidence is unreadable.
- Emphasize selectively with typography, light fills, and grouping. Borderless encoding annotations do not imply removing every rule from the deck. Decoration should clarify hierarchy.
- Typeset real mathematics consistently. Algorithm pages should resemble LaTeX algorithm/pseudocode blocks: clear input/output, aligned steps, and mathematical expressions. Avoid arbitrary Unicode formulas and fragmented promotional-style cards.
- When using `data/references/defense-zer.pdf` and `defense-zz.pdf`, study how particular pages organize definitions, equations, figures, and conclusions. Transfer those relationships, not superficial motifs. Do not claim a full review based on a few selected pages.
- Keep figure generation reproducible and prefer vector output for plots when suitable. Distinguish illustrative data from experimental results. Redraw confusing comparisons when necessary; check their scientific meaning before changing orientation or scale.

For an authorized targeted preview, inspect readable axes, matching orientations, rendered caption math, smooth arrowheads, grouping, and footer clearance on the requested page. Do not expand this into an automatic deck-wide audit.
