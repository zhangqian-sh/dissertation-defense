# Brown APMA dissertation defense

A locally served Slidev presentation for Qian Zhang's dissertation, with a
white academic theme, local Inter / Latin Modern fonts, chapter citations,
speaker notes, 41 main slides, and six chapter-ordered backup slides.

## View the built presentation

```bash
./present.sh
```

The launcher serves `dist/` on `http://127.0.0.1:3030` and stays running until
Ctrl-C. It requires Node.js and curl; it installs nothing and makes no external
requests. Set `PORT` to use another port. The presenter view is
`http://127.0.0.1:3030/presenter/1`. Use the on-screen Slidev navigation or arrow
keys; interactive controls keep their keyboard events within the figure.

For transfer to a laptop, copy `dist/`, `scripts/serve.mjs`, `present.sh`, and
`artifacts/defense.pdf` while preserving the directory structure. Node.js must
already be installed. The PDF works independently of JavaScript and WebGL.

## Edit and build

```bash
npm ci
npm run dev
npm run build
npm run export:pdf
```

Edit the title/frontmatter in `slides.md`, scientific content in `slides/`,
the `layouts/academic.vue` layout, and `style.css`. The canvas is 1200 × 675
(16:9). Body typography and explicit image heights reserve room for a source
footer. Do not reduce font sizes to force additional content onto a slide;
split the argument or comparison instead. The title is sourced from thesis
metadata. The defense date is omitted because the thesis date is a placeholder.

The repository includes the figures, fonts, and active browser data needed to
build the deck. A normal build does not require the parent thesis repository,
model repositories, checkpoints, or raw experiment captures. Dependencies and
generated output in `node_modules/`, `dist/`, `artifacts/`, and `data/staging/`
are ignored. Superseded browser exports and scratch notes remain local.

Research-data regeneration is a separate workflow: collection and figure
preparation scripts use the external thesis/model sources identified in the
provenance documents and may require their Python environments. Raw payloads
and checkpoints are intentionally excluded from Git; collection scripts, run
indexes, and metadata are retained. The full Python contract test suite checks
those raw captures and requires them locally, whereas `npm run validate:assets`
and the build/browser audit validate the included presentation bundle.

On Oscar, figure preparation and browser audits run in Slurm:

```bash
mkdir -p data/staging
sbatch scripts/setup_deck_job.sh
sbatch scripts/build_deck_job.sh
```

Submit the build after setup finishes. The setup script converts publication
PDFs and installs dependencies/Chromium. Subsequent builds do not need setup.
The build script produces the offline site, screenshots, audit report and PDF.
The browser audit blocks external requests, checks layout boundaries/missing
images, exercises the four controls and linked trace seeking, verifies pause
on slide exit and static fallback on data or WebGL failure, checks populated
conversion heatmaps, and visits the presenter route. `export:pdf` audits and
copies the build-time PDF, checking that all 48 pages are present; run the
build first after editing slides. `scripts/contact_sheets.py --pdf` creates visual
review sheets from the exported PDF (run on a compute node on Oscar).

Outputs in `dist/`, `artifacts/`, and `data/staging/` are generated and ignored.
`artifacts/slides/` contains per-slide screenshots;
`artifacts/layout-audit.json` records the checks. `docs/figure_conversions.json`
records the original PDF and converted PNG checksums.

## Publish with GitHub Pages

The GitHub Actions workflow builds and audits the deck on pushes to `master`,
then publishes `dist/` to GitHub Pages. In the `dissertation-defense` repository,
select **Settings → Pages → Build and deployment → Source → GitHub Actions**
before the first deployment. Commit and push the source; generated output stays
ignored. The intended site is `https://zhangqian-sh.github.io/dissertation-defense/`
(or the project path under an existing personal-site custom domain).

The Pages build uses `/dissertation-defense/` and hash routing, so direct slide
links such as `/dissertation-defense/#/7` and presenter links such as
`/dissertation-defense/#/presenter/1` work without server rewrites. Public data
paths in manifests remain unchanged; the browser adds the deployment prefix.
The PDF download and speaker notes are included, as in the local deck.

To test the hosted build locally (run builds and audits in Slurm on Oscar):

```bash
npm run build:pages
npm run test:pages
BASE_PATH=/dissertation-defense/ npm run preview
```

Open `http://127.0.0.1:3030/dissertation-defense/`. For a local defense at the
server root, run `npm run build` and `./present.sh` as usual. Both deployment
paths are supported. The Pages workflow tests the included browser bundle;
it does not run Python tests that require ignored raw experiment captures.

## Interactive figures

- SMS: linked physical-time prediction and error views; reference-fed versus recursive cascade.
- Burgers (slide 11): exactly three panels—reference, SNN, SNN−reference.
  Play or select every integer prefix T=1–128; only SNN and difference
  change. Fixed scales and native pixels preserve the actual solution.
  These are actual emitted-output prefixes of a fresh SNN calibrated at
  horizon 128, not interpolated fields or independently recalibrated models.
- Energy Transformer (slide 20): 2D vortex street, native 128×256 v field,
  no display smoothing, 12 decoded checkpoint-replay updates, slider,
  playback, wheel stepping, error toggle, and linked error/energy traces.
  Replay differs from the archived prediction by 0.111% relative L2.
- OCFormer: orbitable 3D geometry, linked clearance/time trace, closest-pair
  jump and camera reset. The scene reports sampled position constraints only.
  Slide 38 defaults to **2D · 128 drones**, left of 3D, with all 200 saved
  frames, the paper's seeded colors, hollow circles and cumulative gray trails.
- Latent/physical paths (slide 33): straight endpoint reference beside the
  paper's saved L-BFGS optimized trajectories; no hand-designed detour.
- Weather (slide 30): static station distribution and a smooth, US-masked
  reference/reconstructed temperature comparison from 54 recorded 2024 dates;
  both use identical spatial interpolation and shared colors, not gridded truth.
- Blood flow (slide 31): original static u/v snapshots, each 2×2, distinguishing
  sparse observations, raw/full targets, reconstruction and averaged references.
- RFormer (slides 27 and 29): physical-time playback of reference, observations,
  and RFormer; vortex uses a 3×3 u/v/p matrix, jet uses native velocity arrows.
  There are 20 vortex frames and 40 chronologically sorted
  jet frames. Jet times are nonuniform source indices, not seconds. The jet
  spectrum remains a labeled static published comparison.

All four consume the versioned manifest and local data described in
[interactive_data.md](docs/interactive_data.md). Loading or WebGL failure uses
a source-consistent PNG fallback. Add `?static=1` to a slide URL to show its
print fallback explicitly. Print mode uses the same fallbacks.

RFormer spatial inspection remains disabled; ET history is now enabled.
See [conditional_views.md](docs/conditional_views.md) for the evidence reviewed
and the limits of the current static treatment.

## Rehearsal still requires the target laptop

The automated browser audit is a compute-node check. Before the defense,
inspect the deck on the actual projector, test two-display presenter mode,
and rehearse with Wi-Fi off. Source qualification on Loihi RMS units remains
visible: its original normalization/physical units were not independently
recovered. No universal energy-saving or continuous-time safety claim is made.

Implementation references: [Slidev layouts](https://sli.dev/guide/write-layout),
[slide context](https://sli.dev/guide/global-context), and
[exporting](https://sli.dev/guide/exporting.html).
