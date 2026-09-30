# Presentation implementation

The deck contains 47 slides: 41 main slides following Chapters 1–8 and six
chapter-ordered backups. The academic layout uses a white 16:9 canvas,
locally bundled serif headings and sans-serif body text, restrained Brown-red
accents, chapter progress, source footers, and speaker notes.

The original four interactive figures use verified, versioned data: SMS physical-time
rollout, Burgers reference/SNN/difference at recorded T values, ET vortex-street reconstruction
history, and the OCFormer 3D swarm. Playback pauses when leaving a slide. Linked traces
seek the corresponding recorded frame; input controls do not advance slides.
Printing and data/WebGL failures use source-consistent static figures.

Additional dynamic views include the two RFormer flow sequences, paired weather
maps, recorded optimized physical trajectories beside straight latent references,
and a default 128-agent 2D tab beside the 3D swarm. Blood now uses two original
static 2×2 u/v snapshot figures. Splitting the former slide 30 shifts subsequent
pages: latent map is now 33 and swarm inspection is 38.

## Deliverables and verification

The 2026-09-30 manuscript update adds a static hybrid Spiking RFormer slide
(slide 40) in the Chapter 8 outlook, using the manuscript's original reconstruction
PNG without modification. It explains the u/v/p rows, truth/observation/SNN columns,
T=32 hybrid calibration, and matched ANN/SNN relative RMSE results. The deck now
contains 47 slides, including 41 main slides and six backups.
Slurm job `6850232` passed the build and 47-slide/47-page browser/PDF audit,
with nine existing interactive figures and no detected overflow or missing images.
The new slide was visually reviewed; figure provenance and checksums are recorded
in `figure_conversions.json`. The hybrid results establish preliminary software
feasibility; energy and latency require hardware measurements.

The latest requested revisions passed Slurm job `6249173` on 2026-09-11:
16 Python tests, three raster tests, and the 46-slide/46-page browser/PDF
audit with nine interactive figures. No overflow was detected. Static and
live views of slides 30, 31, 33, and 38 were visually reviewed. Weather now
has paired reference/reconstructed panels; blood uses the original u/v
2×2 snapshots; the physical illustration uses saved L-BFGS trajectories;
and the default 2D swarm uses the paper's seeded palette and gray past paths.
Exports and validation ran on compute nodes using the submit-slurm-jobs skill.

The 2026-09-11 additions were collected in Slurm job `6244400` and verified in
`6244719`: all 16 Python tests, three raster tests, 46-slide / 46-page checks,
and 10 interactive-view checks passed. New views passed seeking, playback,
pause-on-exit and missing-data fallbacks. No detected overflow, missing images,
browser exceptions or external requests. Changed static and interactive layouts
were visually reviewed. `added_sequences.md` records scientific qualifications.
Final labeling rebuild `6244908` repeated the same successful 46-slide,
46-page and 10-view checks after updating the swarm heading/footer to cover
both its 2D and 3D datasets.

- `dist/`: offline browser presentation, including a downloadable PDF.
- `artifacts/defense.pdf`: audited copy of the build-time PDF export.
- `artifacts/slides/`: full-resolution browser screenshots of every slide.
- `artifacts/layout-audit.json`: machine-readable layout and interaction audit.
- `artifacts/pdf-contact-*.png`: contact sheets rendered from the PDF.
- `docs/slide_inventory.csv`: slide titles, chapter/source labels and assets.

Generated outputs are ignored, not committed. Run the commands in `README.md`
to reproduce them; compute-heavy conversion and browser verification run through
Slurm on Oscar. The audit checks image availability and footer/horizontal
boundaries on every slide, four interactive controls and linked traces,
populated field canvases, playback pause on exit, presenter routing, failure
fallbacks, external requests, browser exceptions, and PDF page count.

### Initial release verified 2026-09-10 (superseded by the history/error revision)

Slurm job `6192371` passed the browser/PDF audit: 44 slides, 44 PDF pages,
zero detected overflow, missing images, browser exceptions, or external
requests. All three interactions, linked seeking, pause-on-exit, presenter
route, data-failure and WebGL-failure fallbacks passed. Conversion fields
passed the populated-canvas check. Every PDF page was visually reviewed using
the rendered contact sheets; PDF text extraction independently confirmed all
44 titles in the correct order. The presentation-scoped whitespace check and
JavaScript/shell syntax checks passed. Unrelated thesis edits were preserved.

### Earlier history/error revision verified 2026-09-10 (superseded examples)

Slurm job `6192894` passed: 45 slides / PDF pages, four interactive figures,
zero detected overflow or missing images, zero browser exceptions and zero
external requests. ET playback, slider, mouse-wheel stepping, changing
reconstruction and error toggle passed. SNN first/last error fields differ,
both panels are populated, and linked traces / pause-on-exit still work.
All PDF page titles and their order were checked, and all exported pages plus
the two revised live figures were visually reviewed. The native-mesh raster
passed three tests for coverage without seams, exact linear interpolation,
and changing error colors under a fixed scale.

### Vortex-street / Burgers revision verified 2026-09-10

Slurm job `6195396` completed successfully: four assets validated against raw
captures, 11 numerical contract tests, three raster tests, and the complete
45-slide / 45-page browser/PDF audit. No detected overflow, clipped SVG labels,
missing images, browser exceptions or external requests. Burgers has exactly
three native-grid panels: changing T preserves reference and changes both SNN
and difference. ET native canvas dimensions, disabled smoothing, wheel steps,
playback and error toggle pass. Changed live figures and exported pages were
visually reviewed. Reference-range ET colors retain contrast; saturation
fractions are labeled and raw values/metrics remain unchanged.

### Burgers intermediate fields verified 2026-09-10

GPU job `6195542` captured all 128 actual emitted-output prefixes after fresh
advanced-CAA calibration. Publication/build job `6195567` completed successfully:
four raw-linked assets, 13 numerical contract tests, three raster tests and
45-slide / 45-page browser/PDF checks passed. Slide 11 loads in approximately
1.6 seconds in the audit environment. The interaction check explicitly verifies
T=64→65 changes SNN and difference but not reference; playback and navigation
isolation pass. No detected overflow, browser errors or external requests.
The live three-panel layout was visually reviewed.

## Remaining limits

Layout restoration verified by Slurm job `6195875` on 2026-09-10: CH6–27 now
has a 3×3 matrix (u/v/p rows; reference/observations/RFormer columns). CH6–29
has reference/observations/RFormer velocity-vector panels, including measured
vectors in the observation panel. Fixed scales and physical-time playback
are retained. All 14 Python tests, three raster tests and the complete
45-slide/45-page, six-interaction browser/PDF audit passed. Updated live and
static layouts were visually reviewed with no detected overflow.

Latest RFormer update: Slurm job `6195742` completed on 2026-09-10. Slides 27
and 29 now provide physical-time playback of 20 vortex and 40 jet snapshots.
All 14 Python tests, three raster tests, and the 45-slide / 45-page audit passed;
six interactive figures are checked. Both new figures pass seeking, playback,
pause-on-exit and missing-data fallback checks. No detected overflow, missing
images, browser errors or external requests. Static and live changed slides
were visually reviewed. Source ordering, blind-target recovery and display
interpolation are documented in `conditional_views.md`.

Target-laptop, projector, and dual-display rehearsal remain manual checks.
The active Burgers sequence contains all actual prefixes T=1–128 from a fresh
fixed-horizon-128 calibration, not independently recalibrated models at each T
or reproduction of the historical archived calibrated state. The corrected reference/coordinate layout and original
training-grid evaluation scope are documented in the Burgers collection README.
The source defense date is still a placeholder, so the cover omits it.
ET iterations now come from a fresh 2D vortex-street saved-checkpoint replay.
It differs from the archived output by 0.111% relative L2; the cause remains unresolved and
the deck explicitly qualifies it. No synthetic temporal progression is used.
RFormer physical-time playback is enabled for vortex and jet snapshots;
3D rotation/movable slicing remain disabled. Jet test times have gaps and
are labeled as source indices, not seconds. See `conditional_views.md`.
The exploratory conversion case, unrecovered Loihi RMS normalization, and
sampled—not continuous-time—swarm constraints are explicitly qualified in
the slides. These limits must remain visible when presenting the results.
