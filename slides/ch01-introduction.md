---
chapter: '1'
section: Introduction · Research questions
source: 'Thesis Chapter 1 · fig:intro:arc · Two independent research themes'
---

# Scientific accuracy under computational constraints

<p class="subtitle">How should representation, inference, and optimization change when computation is limited?</p>
<div class="cols">
<div class="rule">
<div class="eyebrow">Part I · Neuromorphic algorithms</div>
<h2>Represent and compute with spikes</h2>
<div class="chapter-pair">Spiking representations & marching <span>Chapter 2</span></div>
<div class="chapter-pair">Conversion & hardware deployment <span>Chapter 3</span></div>
<div class="chapter-pair">Forward-mode training <span>Chapter 4</span></div>
</div>
<div class="rule teal">
<div class="eyebrow">Part II · Sequence-to-sequence models</div>
<h2>Infer fields and coordinated trajectories</h2>
<div class="chapter-pair">Energy-based reconstruction <span>Chapter 5</span></div>
<div class="chapter-pair">Sparse-measurement reconstruction <span>Chapter 6</span></div>
<div class="chapter-pair">Multi-agent optimal control <span>Chapter 7</span></div>
</div>
</div>
<div class="takeaway">A shared emphasis on computational structure; separate datasets, objectives, and experiments.</div>

<!-- Explain the two parts independently. Chapters 5 and 6 are reconstruction studies; Chapter 7 is a separate optimal-control study. -->

---
chapter: '1'
section: Introduction · Contributions
source: 'Thesis Chapter 1 · Contributions and dissertation organization'
---

# Three questions guide the evidence

<div class="three" style="margin-top:32px">
<div class="rule"><div class="number">01</div><h2>What is preserved?</h2><p class="small">Continuous fields, temporal evolution, and physical structure under discrete or sparse representations.</p><p class="micro">Spiking encodings · reconstructed spectra</p></div>
<div class="rule"><div class="number">02</div><h2>What does it cost?</h2><p class="small">Simulation horizon, calibration, iterative inference, and hardware replication determine practical efficiency.</p><p class="micro">Accuracy–latency trade-offs · measured hardware</p></div>
<div class="rule"><div class="number">03</div><h2>Where does it generalize?</h2><p class="small">Temporal extrapolation, observation changes, and boundary-condition shifts require distinct tests.</p><p class="micro">Protocol-specific conclusions · explicit limitations</p></div>
</div>
<div class="takeaway">Evaluate scientific fidelity and computational cost together—and retain the conditions under which each result holds.</div>

<!-- These questions organize the talk, while slides remain in thesis chapter order. -->
