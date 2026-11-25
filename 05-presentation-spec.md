# Presentation Build Spec: MTI ResearchOS

**For:** the coding agent (Codex) that will build the PowerPoint file.
**Source of truth for all content:** `04-final-decision.md` in this repo. Don't invent numbers. Every figure below comes from that file. If something here conflicts with `04`, `04` wins.
**Do not build the software system.** Build only the slide deck.

---

## 0. Deliverable

| Item | Value |
|---|---|
| Output file | `presentation/MTI-ResearchOS.pptx` |
| Generator script | `presentation/build_deck.py` (python-pptx) **or** `presentation/build_deck.js` (pptxgenjs). Pick one and commit it |
| Slide size | 16:9, 13.333 in × 7.5 in |
| Slide count | **21 main slides** (1–18, 18A, 19, 20) + **4 appendix** (A1–A4) = 25 |
| Speaker notes | Required on every slide (text given below) |
| Charts | **Native PowerPoint charts** (editable), not images |
| Diagrams | Built from native shapes (rectangles, rounded rectangles, arrows, connectors), not images |
| Fonts | Headings **Cambria**, body **Calibri** (safe on every Office install) |

---

## 1. Design system

### 1.1 Palette ("Ledger Green": evidence, trust, money)
| Token | Hex | Use |
|---|---|---|
| `INK` | `12263A` | Dark backgrounds (title, section, closing), primary text on light |
| `TEAL` | `0F766E` | Primary accent: agent boxes, key numbers, chart main series |
| `MINT` | `CCEFE9` | Light card fill, table header fill on light slides |
| `SLATE` | `475569` | Secondary text, captions, axis labels |
| `CLOUD` | `F1F5F9` | Subtle panel background on white slides |
| `WHITE` | `FFFFFF` | Content slide background |
| `AMBER` | `D97706` | Warnings: Conflicting / Outdated / human gates |
| `RED` | `B91C1C` | Unverified / critical / kill switch |
| `GREEN` | `15803D` | Verified status |

Dominance: INK and TEAL carry about 65% of the visual weight. AMBER is reserved for **human gates and flags**, so it always means "human attention here".

### 1.2 Typography
| Element | Font | Size | Weight / colour |
|---|---|---|---|
| Slide title (action headline) | Cambria | 30 pt | Bold, INK (WHITE on dark slides) |
| Kicker (small label above title) | Calibri | 12 pt | Bold, TEAL, ALL CAPS, e.g. `STEP 2 · VALIDATION` |
| Body | Calibri | 15–16 pt | SLATE / INK |
| Big stat number | Cambria | 54–66 pt | Bold, TEAL |
| Stat label | Calibri | 13 pt | SLATE |
| Table text | Calibri | 12–13 pt | INK; header row bold on MINT |
| Footnote / source line | Calibri | 9–10 pt | SLATE |

Titles are **action headlines**: full sentences that state the conclusion, with no trailing full stop. Keep each to 2 lines or fewer at 30 pt.

### 1.3 Layout grid
- Margins: 0.5 in on all sides.
- Kicker at y = 0.45 in; title at y = 0.7 in (height 1.1 in); content area from y = 1.95 in to y = 6.85 in.
- **Footer** (every slide except title and closing): left `MTI ResearchOS · Concept & Architecture`, right the slide number, Calibri 9 pt, SLATE, at y = 7.1 in.
- **Source line** above the footer at y = 6.85 in where a slide cites evidence (text given per slide).
- Gap between cards: 0.3 in, used consistently.

### 1.4 Visual motif
- **The evidence-card chip:** a small rounded rectangle (0.9 in × 0.32 in, corner radius 0.08 in, MINT fill, TEAL 9 pt bold text) used as a tag throughout: `S1`, `Tier 1`, `Verified`, `Gate 2` and so on. Reuse it on every slide where a status, tier, gate or stage is named.
- **Human gates** are always drawn as AMBER diamonds (◆) in flow diagrams.

### 1.5 Status badge colours (consistent everywhere)
| Status | Fill | Text |
|---|---|---|
| Verified / Verified – official | GREEN | WHITE |
| Estimated – triangulated | `FEF3C7` | `92400E` |
| Conflicting / Outdated | AMBER | WHITE |
| Unverified | RED | WHITE |

### 1.6 Don'ts
- No decorative accent bars or stripes along slide or card edges, and no underline under titles.
- No centred body text (centre only big stats and diagram labels).
- No text-only slides: every slide has a diagram, chart, table, mock or stat block.
- No text below 9 pt. If content doesn't fit, cut words or split. Never shrink below the sizes in §1.2.
- No emoji in the deck (use coloured badges instead).

---

## 2. Slide-by-slide specification

> **Format per slide:** Kicker · Title · Layout · Content (exact text) · Visual build notes · Source line · Speaker notes.

---

### Slide 1: Title (dark)
- **Background:** INK.
- **Title (Cambria 44 pt, WHITE):** `MTI ResearchOS`
- **Subtitle (Calibri 22 pt, MINT):** `An agentic AI system to automate desk research — from brief to validated research pack`
- **Line 3 (Calibri 14 pt, WHITE at 80%):** `Strategy Consulting (Agentic AI) Internship Assignment · Concept & Architecture`
- **Line 4 (Calibri 12 pt, SLATE-light `94A3B8`):** `[Candidate name] · November 2026`
- **Visual:** on the right half, a faint stack of 3 overlapping evidence-card outlines (rounded rectangles, TEAL outline at 60% transparency, slightly rotated −4°, 0°, +4°). Purely decorative and low contrast.
- **Notes:** "This is a concept and architecture proposal for automating MTI's desk research, from receiving a brief to delivering a validated research pack, targeting 90–95% automation without giving up accuracy."

---

### Slide 2: The problem and the prize
- **Kicker:** `THE OPPORTUNITY`
- **Title:** `Desk research costs 16–24 analyst hours per brief — we can return over 90% of that time`
- **Layout:** left 55% chart, right 45% three stat blocks stacked.
- **Chart (native clustered bar, horizontal):** title "Human hours per brief".
  - Categories: `Today (manual)`, `With ResearchOS`
  - Values: `20` (label "16–24 h"), `1.6` (label "≈1.6 h")
  - Colours: today = SLATE, ResearchOS = TEAL. Data labels on. No legend. Light gridlines (`E2E8F0`).
- **Stat blocks (right):**
  1. `≈92%` · "of analyst time automated (central case)"
  2. `Same day` · "turnaround instead of 2–3 days"
  3. `100%` · "of numbers traceable to a source, quote and archive link"
- **Bottom strip (Calibri 13 pt, SLATE):** `MTI: international strategy consultancy since 1997 · 760+ assignments · 56 countries · 7 regional offices`
- **Source line:** `Baseline hours are an assumption to confirm with MTI in Phase 0. MTI facts: mtiworldwide.com`
- **Notes:** "MTI's work depends on desk research across 56 countries, often in frontier markets where data is thin. Today a brief takes 2–3 analyst days. The goal isn't just speed: it's speed with every number traceable."

---

### Slide 3: What "90% automation" means
- **Kicker:** `DEFINITION`
- **Title:** `“90% automation” is defined, measured and guarded by audited accuracy`
- **Layout:** metric tree across the top (3 levels), human-time breakdown bar along the bottom.
- **Metric tree (native shapes, connected by elbow connectors):**
  - Top box (TEAL fill, WHITE text): **Headline: Process automation = 1 − (human minutes ÷ baseline minutes)** · target **≥ 90%**
  - Left child (MINT): **Supporting: Claim auto-approval rate** · target **≥ 90%**
  - Right child (AMBER outline, INK text): **Guardrail: Audited accuracy** · **numbers ≥ 98% · qualitative ≥ 95%** · "If it slips, automation tightens automatically"
- **Bottom: native 100% stacked bar, one row, "Human minutes per brief (≈95 min)":**
  - Segments: `Gate 1 plan approval 10` · `Gate 2 exception queue 45` · `Gate 3 sign-off 15` · `Audit share 25`
  - Colours: Gate segments AMBER at descending shades (`D97706`, `F59E0B`, `FBBF24`), audit SLATE.
  - Data labels inside (`ctr`).
- **Callout chip on the right of the bar:** `95 min vs 1,200 min baseline → ≈92% · range 88–95%`
- **Notes:** "I define automation as the share of analyst time removed, not as a vague claim. It always comes with a guardrail: audited accuracy. A system that auto-approves everything would score 100% automation and be useless. This definition makes that impossible."

---

### Slide 4: End-to-end flow
- **Kicker:** `STEP 1 · HOW IT WORKS`
- **Title:** `Brief in, audited research pack out — humans touch only three gates`
- **Layout:** a full-width horizontal process flow in 2 rows (snake layout), left to right then right to left.
- **Row 1 boxes (rounded rectangles, TEAL outline, WHITE fill, INK 12 pt text, numbered chip top-left):**
  1. `Brief intake` ("email · form · PDF/Word")
  2. `Intake Agent` ("JSON plan + MECE issue tree")
  3. ◆ `Gate 1` (AMBER diamond) ("approve plan · 10 min")
  4. `Fact Base lookup` ("reuse verified facts")
  5. `Supervisor + parallel research` ("1 / 2–4 / 5–10 agents")
- **Row 2 boxes:**
  6. `Extraction` ("evidence cards + snapshots")
  7. `Estimation track` ("when no data exists")
  8. `Validation cascade` ("S1 → S2 → S3")
  9. `Writer + Formatter` ("ledger-only · MTI template")
  10. ◆ `Gate 2 + Gate 3` (AMBER) ("exceptions 45 min · sign-off 15 min")
- **End box (INK fill, WHITE text):** `Deck · Word report · Excel data book · Source register · Validation log`
- **Feedback arrow (dashed TEAL, curved from the end box back to "Fact Base lookup"):** label `Write-back: verified facts + reviewer reason codes → learning loop`
- **Notes:** walk the flow once. Stress that everything between the gates is automatic and that gates are short and focused.

---

### Slide 5: Agents and hand-offs
- **Kicker:** `STEP 3 · AGENTS, TOOLS & PLATFORMS`
- **Title:** `Specialised agents, each with one job and a typed hand-off through the ledger`
- **Layout:** swimlane table (native table), 4 columns × 10 rows, plus a thin platform strip at the bottom.
- **Table columns:** `Agent` · `Model` · `Main tools` · `Hands off to`
- **Rows (exact):**
| Agent | Model | Main tools | Hands off to |
|---|---|---|---|
| Intake | Claude Opus 5.5 | Document parser | Plan → Gate 1 |
| Supervisor | Claude Opus 5.5 | Plan, Fact Base, ledger | Research subagents |
| Research (×N) | Claude Sonnet 5.5 | Search APIs, page reader, World Bank / IMF / UN Comtrade, Country Registry, MCP | Sources + snapshots |
| Extraction | Claude Haiku 5.5 · local Qwen (confidential) | Docling, Python | Evidence cards |
| Estimation | Claude Sonnet 5.5 + Python | Verified cards only | Estimated cards |
| Validator S1 | Code only | URL check, Wayback, quote matcher | Pass / fail |
| Validator S2 | Gemini 3.1 Flash-Lite | Snapshot + claim | Support verdict |
| Validator S3 | Claude Sonnet 5.5 | Second search index | Corroboration |
| Writer | Claude Opus 5.5 | Ledger (read-only) | Draft |
| Formatter | Code only | python-pptx / docx / openpyxl | Deliverables → Gate 2 |
- Highlight the `Validator S2` row's Model cell with a MINT fill and the chip `Different vendor`.
- **Platform strip (row of 6 chips):** `LangGraph · state + human gates` · `PostgreSQL + pgvector · ledger` · `Docling · local parsing` · `Langfuse · tracing & cost` · `MCP · connectors` · `Microsoft 365 · SharePoint / Power Automate / Teams`
- **Notes:** "Agents never pass free text to each other. They read and write typed ledger records. LangGraph keeps state, so a failed run resumes from its checkpoint and pauses at each gate for a human. The judge is deliberately a different vendor."

---

### Slide 6: The evidence card
- **Kicker:** `STEP 1 · EXTRACT & ORGANISE`
- **Title:** `Every number becomes an evidence card — the writer can only cite the ledger`
- **Layout:** left 55% shows a mock evidence card; right 45% has 3 annotation callouts with connector lines pointing to card fields.
- **Mock card (rounded rectangle, CLOUD fill, monospace-style text in Calibri 12 pt, INK). Show these lines:**
```
claim:        Bangladesh imported 4,100 t of packaged tea (FY2024)
value / unit: 4,100 · tonnes · FY2024 · Bangladesh
source:       Tier 1 · page 37 · published 2025-06-30
exact_quote:  “…imports of packaged tea stood at 4,100 MT…”
snapshot:     snap_8f2c…   archive: web.archive.org/…
checks:       S1 pass · S2 skipped · S3 pass
confidence:   0.94          status: [Verified]
```
  - `[Verified]` rendered as a GREEN badge.
- **Callouts (right):**
  1. **Traceable:** "Quote + page + archive link on every number"
  2. **Checkable:** "Quote matched against the stored snapshot, not the AI's own text"
  3. **Reusable:** "Verified public facts enter the Fact Base for future briefs"
- **Bottom line (13 pt):** `All arithmetic (CAGR, shares, FX, sizing) is done in Python — never by the LLM.`
- **Caption (9 pt):** `Illustrative figures — format only.`
- **Notes:** "This is the heart of the design. The report is generated from these cards, so the model can't invent a number. If it isn't in the ledger, it can't appear in the deck."

---

### Slide 7: Why validation matters
- **Kicker:** `STEP 2 · WHY VALIDATE`
- **Title:** `Even the best off-the-shelf research agents get 10–22% of citations wrong`
- **Layout:** left 60% native horizontal bar chart; right 40% two stat blocks.
- **Chart:** title "Citation accuracy — DeepResearch Bench".
  - Categories and values: `Perplexity Deep Research 90.24` · `Grok Deeper Search 83.59` · `Gemini 2.5 Pro Deep Research 81.44` · `OpenAI Deep Research 77.96`
  - Axis min 60, max 100. Bars TEAL. Add a vertical reference line at **98** (draw as a thin AMBER line shape over the chart) labelled `Our target for numbers: 98%`.
- **Stat blocks:**
  1. `3–13%` · "of citation URLs from LLMs and research agents were hallucinated"
  2. `6–79×` · "fewer broken links after automated URL checking"
- **Source line:** `DeepResearch Bench (arXiv 2506.11763); Rao et al., reference hallucination study (arXiv 2604.03173)`
- **Notes:** "This is why I don't recommend just buying a deep-research tool. The best one still gets about 1 in 10 citations wrong, and for consulting that's unacceptable. Validation is the core of the system, not an add-on."

---

### Slide 8: The validation cascade
- **Kicker:** `STEP 2 · VERIFY ACCURACY`
- **Title:** `A three-stage cascade catches fake, stale and conflicting data cheaply`
- **Layout:** left 45% funnel; right 55% three stage descriptions aligned to funnel levels.
- **Funnel (3 stacked trapezoids or decreasing-width rounded rectangles, top to bottom):**
  - `S1 Deterministic · 100% of cards` (TEAL, widest)
  - `S2 Cross-vendor LLM judge · ~25%` (TEAL at 70%)
  - `S3 Independent corroboration · ~8%` (TEAL at 45%, narrowest)
- **Right side text per stage (title bold 15 pt + 13 pt detail):**
  - **S1 · Code (free):** "URL resolves (Wayback fallback) · exact quote in stored snapshot · value, unit, period, geography consistent · recency · tier rule · numbers recomputed"
  - **S2 · Gemini Flash-Lite:** "Does the quote support the claim? Contradictions? Runs on borderline, qualitative, chart / scan / translated numbers"
  - **S3 · Claude Sonnet + 2nd search index:** "Second independent source within tolerance (±10% market size, exact for official stats). Runs on headline and single-source numbers"
- **Bottom callout (MINT panel):** `Why a different vendor judges: LLM judges favour their own outputs, and similar models share errors. Cost of independence: ≈ $0.26 per brief.`
- **Source line:** `Panickssery et al. 2024 (arXiv 2404.13076); Goel et al., ICML 2025 (arXiv 2502.04313)`
- **Notes:** "Cheap checks run on everything; expensive checks run only where needed. That's how we get accuracy without the cost of checking every claim with every method."

---

### Slide 9: Source tiers, conflicts and status labels
- **Kicker:** `STEP 2 · CREDIBILITY & FLAGS`
- **Title:** `Conflicts are settled by rule — and losing values stay visible`
- **Layout:** left 50% tier pyramid; right 50% top = conflict rule, bottom = status-label legend.
- **Pyramid (4 stacked shapes, top narrow → bottom wide):**
  - `Tier 1 Official` — "statistics offices, central banks, regulators, audited filings" → chip `Hard numbers`
  - `Tier 2 Institutional` — "World Bank, IMF, UN, licensed databases" → chip `Hard numbers`
  - `Tier 3 Media / industry` — "business press, associations" → chip `Only if corroborated`
  - `Tier 4 Routing only` — "Wikipedia, blogs, forums, SEO sites" → chip `Never cited` (RED chip)
- **Conflict rule (3 numbered steps with arrows):** `1 Higher tier wins` → `2 More independent sources` → `3 Most recent`. Under it: "Alternatives are kept in the data book with a conflict note."
- **Status legend (6 badges, colours from §1.5, each with a 1-line rule and a "Human?" yes/no):**
  - Verified — ≥2 sources, ≥1 Tier 1–2 — No
  - Verified – official — 1 Tier-1, quote matched — No (unless headline)
  - Estimated – triangulated — 2–3 methods agree — Yes if headline
  - Conflicting — beyond tolerance — Yes
  - Outdated — older than threshold — Yes
  - Unverified — Tier 3–4 only / check failed — Yes
- **Small table (bottom right, 11 pt), "Outdated if older than":** FX and commodity prices 3 months · Macro statistics 2 years · Market size 3 years · Company financials: not the latest FY · Regulation: always re-checked
- **Notes:** "Every claim carries a label, so the consultant sees at a glance what's solid and what needs judgement. Nothing is silently deleted."

---

### Slide 10: When no data exists
- **Kicker:** `STEP 2 · FRONTIER MARKETS`
- **Title:** `When no published figure exists, we triangulate — and label it honestly`
- **Layout:** left 55% native chart; right 45% rules list.
- **Chart (native clustered column with 3 bars + a shaded agreement band):** title "Premium packaged-tea segment, Bangladesh (illustrative, USD m)".
  - `Top-down (imports × premium share) 42` · `Bottom-up (stores × sales × price) 38` · `Analogue (Sri Lanka scaled by GDP/capita) 45`
  - Bars TEAL / TEAL 70% / TEAL 45%. Data labels on.
  - Draw a horizontal translucent AMBER band (rectangle, 70% transparency) from 36 to 47 labelled `Methods within ±20% → "Estimated – triangulated"`.
- **Rules (icon + text rows):**
  1. "Inputs must be verified evidence cards"
  2. "All arithmetic in Python; assumptions listed"
  3. "Never promoted to Verified unless a real source is found"
  4. "Headline estimates need consultant sign-off"
- **Caption:** `Illustrative values — method demonstration only.`
- **Notes:** "This is the biggest gap in generic AI research tools. They either invent a number or say 'not found'. A consultant triangulates. So does this system, transparently."

---

### Slide 11: Worked example
- **Kicker:** `WORKED EXAMPLE`
- **Title:** `One brief, start to finish: 70 minutes of human time and about $16 of compute`
- **Brief banner (MINT panel, top):** `“Assess Bangladesh as an export market for a Sri Lankan packaged-tea brand.”`
- **Layout:** horizontal timeline of 8 stages (chevrons or rounded boxes with arrows). Under each, two chips: human time (AMBER if > 0) and cost (TEAL).
| Stage | Key event (≤ 12 words) | Human | Cost |
|---|---|---|---|
| Intake | Plan + 1 question: "premium segment only?" | 10 min | $0.60 |
| Research | 5 agents: BBS, Bangladesh Bank, UN Comtrade, Bengali news | — | $9.50 |
| Extraction | ~150 evidence cards | — | $0.45 |
| Estimation | Premium segment triangulated 3 ways, within 15% | — | $0.30 |
| Validation | Dead link repaired · 2019 tariff → Outdated · 22% gap → Conflicting | — | $1.25 |
| Write + format | 18-slide deck, Word report, data book | — | $3.50 |
| Exception queue | 12 cards (8%) reviewed | 45 min | — |
| Sign-off | Partner checks headline estimate | 15 min | — |
- **Totals bar (bottom, INK fill, WHITE text):** `Human: 70 min (+ audit share) · Compute: ≈ $16 (+30% buffer ≈ $21)`
- **Caption:** `Illustrative walkthrough.`
- **Notes:** walk the timeline. Point out the three flags the system caught on its own, and that the human only saw 12 of 150 claims.

---

### Slide 12: What the consultant sees
- **Kicker:** `OUTPUTS & HUMAN REVIEW`
- **Title:** `What the consultant actually receives — and the only screen they need to review`
- **Layout:** three mock panels side by side, each about 3.9 in wide, CLOUD background with a subtle shadow.
  1. **Mock MTI slide (thumbnail):** headline `Imports meet ~40% of demand → local processing is the entry route`, a tiny native column chart (3 bars), and a 9 pt footnote `Source: Bangladesh Bureau of Statistics, p.37, accessed 25 Nov 2026 · archived` + GREEN `Verified` badge.
  2. **Mock Excel data book:** a native table, 5 columns (`Metric` · `Value` · `Source` · `Tier` · `Status`), 4 rows. One row shows two values side by side with an AMBER `Conflicting` badge.
  3. **Mock exception card:** title `Packaged tea imports FY2024`; AMBER `Conflicting` badge; quote box with highlighted text; alternatives `4,100 t · Tier 1 customs` vs `5,000 t · Tier 3 press`; 4 button-shaped rectangles `Accept` · `Pick alternative` · `Edit` · `Reject`; dropdown-looking box `Reason code: wrong source / stale / misread / out of scope`.
- **Bottom line:** `Gate 2 is time-boxed: > 60 min triggers a root-cause review. Reason codes feed the learning loop.`
- **Notes:** "This is the human-in-the-loop experience. The consultant doesn't reread a report. They clear a short queue of cards, each with the evidence on one screen."

---

### Slide 13: Audit and self-correction
- **Kicker:** `STEP 3 · STAYING ACCURATE`
- **Title:** `Accuracy is audited every week — automation tightens itself if it slips`
- **Layout:** left 60% control-chart mock; right 40% rule panel.
- **Chart (native line chart):** title "Numeric errors (critical + major) — rolling 8 weeks, n = 320".
  - X: `W1`…`W12`. Series "Errors in window": `5, 6, 4, 6, 7, 5, 8, 9, 12, 13, 9, 6`. TEAL line with markers.
  - Second series "Tighten threshold" constant at `11`, AMBER dashed line.
  - Annotate W9–W10 with a small AMBER callout `Threshold exceeded → auto-tighten`, and W11–W12 with GREEN `Recovered`.
- **Rule panel (numbered):**
  1. "Weekly: 40 numeric + 20 qualitative auto-approved claims sampled · ~3 h"
  2. "Errors graded: Critical · Major · Minor"
  3. "Tighten if rolling 8-week errors > 11 / 320 numeric or > 13 / 160 qualitative"
  4. "Any critical error → root-cause review that week"
  5. RED chip `Kill switch`: "Still below target after 2 tightenings → assist mode (drafts + full review)"
- **Caption:** `Illustrative data.`
- **Notes:** "One unlucky error doesn't collapse automation, but real drift is caught within weeks. Automation can never be bought with silent accuracy loss."

---

### Slide 14: Data governance
- **Kicker:** `GOVERNANCE`
- **Title:** `Client data never touches a free AI tier`
- **Layout:** a 3-row × 3-column matrix (native table) with icons, plus a bottom row of 3 chips.
| Data class | Allowed models | Enters shared Fact Base? |
|---|---|---|
| **Public** (statistics, filings, news) | Any approved paid model | GREEN badge `Yes` |
| **Licensed** (Statista, Euromonitor, EMIS) | Only where the licence permits AI use | AMBER badge `Only if licence allows` |
| **Client-confidential** (briefs, client data) | Local model (Ollama) or paid zero-retention API | RED badge `Never · isolated per client` |
- **Callout (MINT panel):** `Google's free-tier terms: content may be used to improve products and read by human reviewers — "do not submit confidential information". Paid tiers: prompts not used for training.`
- **Bottom chips:** `Sri Lanka PDPA No. 9 of 2022` · `AI use disclosed in engagement letter` · `OWASP LLM01 prompt-injection controls`
- **Source line:** `Google AI Studio terms; OWASP GenAI LLM01:2025`
- **Notes:** "This is where most AI pilots fail in consulting: confidentiality. The rule is simple and enforced by architecture. The data class decides which model may see it."

---

### Slide 15: Challenges and mitigation
- **Kicker:** `STEP 4 · CHALLENGES`
- **Title:** `Seventeen risks — each with a control built into the design`
- **Layout:** left 40% risk heat map (2×2 or 3×3 grid of native squares); right 60% table of the top 8 risks (the full 17 go in the appendix).
- **Heat map:** axes `Likelihood` (low → high) × `Impact` (low → high). Place numbered dots:
  - High/High: 1 Hallucinated numbers · 13 Confidentiality · 6 No published data
  - High/Med: 2 Fake citations · 4 Conflicting data · 7 Paywalls / scans
  - Med/High: 15 Over-automation · 14 Licence terms
  - Med/Med: 10 Cost blow-outs · 11 Model drift · 17 Analyst resistance
- **Table (Challenge · Type · Control):**
  1. Hallucinated numbers · Technical · Ledger-only writer, quote-in-snapshot match, cross-vendor judge
  2. Fake / dead citations · Technical · URL check + Wayback, self-repair
  3. Unreliable sources · Technical · Tier lattice; Tier 4 never cited
  4. Conflicting / outdated data · Technical · Conflict rule, recency thresholds, flags
  5. No published data · Technical · Estimation track, labelled
  6. Paywalls, bot blocking, scans · Operational · Official APIs, licensed APIs, Docling OCR
  7. Automation failures · Technical · LangGraph checkpoints, retries, resume
  8. Confidentiality and licences · Operational / legal · Data classes, local models, Phase-0 licence review
- **Notes:** mention that the full 17-risk register is in the appendix, including prompt injection, key-person risk and analyst adoption.

---

### Slide 16: Models and the free-LLM question
- **Kicker:** `STEP 5 · MODELS`
- **Title:** `Free where it’s safe, frontier where the client sees it`
- **Layout:** left 50% native stacked column chart; right 50% verdict table.
- **Chart (native clustered column): "Cost per brief incl. 30% buffer (USD)"**
  - `A. Free prototype 0` · `B. Hybrid (recommended) 21` · `C. Max open-weight 11` · `D. All-Claude 20`
  - B bar TEAL, the others SLATE. Data labels on. Chip above B: `Recommended`.
- **Key insight panel (MINT, under the chart):** `Cheap models already handle ~50% of tokens but only ~6% of cost. Going all-free saves ≤ $10 per brief — the real saving is ~18 analyst hours.`
- **Verdict table:**
| Option | Use for | Verdict |
|---|---|---|
| Free API tiers (Gemini free, OpenRouter :free) | Prototype, public data only | GREEN `Prototype` / RED `Never client data` |
| Local open-weight (Ollama: Qwen, Llama) | Confidential document extraction | GREEN `Yes` |
| Hosted open-weight (Qwen3, Llama, DeepSeek) | Cost lever if the gold set proves quality | AMBER `After bake-off` |
| Rented GPU, self-hosted | — | RED `Costs more at MTI volume` |
- **Notes:** "I tested the question of free models seriously. Free and local models are in the design, but only where accuracy risk and data sensitivity are low. Cost is driven by the research model, not by the checking models."

---

### Slide 17: Tool stack
- **Kicker:** `STEP 5 · TOOLS`
- **Title:** `A lean stack — four core vendors, a free alternative at every layer`
- **Layout:** native table, 5 columns, about 12 rows. Use 12 pt. Zebra rows (CLOUD).
| Layer | Tool | Why | Price (Nov 2026) | Free alternative |
|---|---|---|---|---|
| Orchestration | LangGraph | State, resume, human gates | Free (MIT) | CrewAI |
| Reasoning / writing | Claude Opus 5.5 / Sonnet 5.5 | Plan, research, write | $4/$20 · $2/$10 per Mtok | Gemini free tier |
| Extraction | Claude Haiku 5.5 · Ollama | Bulk extraction | $0.10/$0.50 · free | Ollama (local) |
| Judge | Gemini 3.1 Flash-Lite | Independent verification | $0.25/$1.50 | Open-weight |
| Search ×2 | Tavily + Exa | Two independent indexes | $0.008/credit · $7/1k | Free monthly credits |
| Page reader | Firecrawl | Clean page / PDF text | $19–99/mo | Jina Reader |
| Parsing | Docling | Tables + OCR, local | Free (MIT) | — |
| Official data | World Bank, IMF, UN Comtrade, NSOs | Tier-1 numbers | Free | — |
| Ledger | PostgreSQL + pgvector | Evidence store | Free | — |
| Observability | Langfuse | Tracing, cost, evals | Self-host free | LangSmith free seat |
| Integration | Microsoft 365 (SharePoint, Power Automate, Teams) | Intake, delivery, alerts | Existing licence | n8n self-hosted |
| Hosting | Hetzner CCX13 | Agents + database | ≈ $50/mo | Local server |
- **Source line:** `Prices checked on vendor pricing pages, 25 Nov 2026 — re-verify before use.`
- **Notes:** "Every layer has a free alternative, which is exactly how the prototype runs at zero cost."

---

### Slide 18: Budget and ROI
- **Kicker:** `STEP 5 · BUDGET`
- **Title:** `About $21 per brief, USD 5.6k to build — payback within about 5 months of kickoff`
- **Layout:** top row = 4 stat blocks; bottom left = build-cost table; bottom right = native chart.
- **Stat blocks:** `$0` "prototype" · `$21` "per brief" · `$770/mo` "running at 30 briefs" · `~5 months` "payback from kickoff"
- **Build-cost table:** AI engineer 3.25 months · $3,450 | Phase-0 analyst time · $400 | API + hosting (build and pilot) · $1,000 | Contingency 15% · $730 | **Total ≈ $5,600 (≈ LKR 1.85M)**
- **Chart (native clustered column): "Monthly: cost vs capacity value (USD)"** for `10`, `30`, `50` briefs/month:
  - Series "All-in monthly cost": `590, 1085, 1495` (SLATE)
  - Series "Capacity value @ $10/h": `1840, 5520, 9200` (TEAL)
  - Data labels on. Legend bottom.
- **Bottom line (13 pt):** `Freed hours = capacity (more briefs, faster turnaround), not headcount cuts. Volumes and rates confirmed in Phase 0. 1 USD ≈ LKR 332.`
- **Notes:** "Even at a conservative $10 an hour and only 10 briefs a month, it pays back within months. At 30 briefs, it frees about 550 analyst hours a month."

---

### Slide 18A: Cost optimisation (insert after slide 18)
- **Kicker:** `STEP 5 · COST OPTIMISATION`
- **Title:** `Caching and batching cut cost by about 37% — accuracy controls are never on the table`
- **Layout:** left 50% native chart; right 50% three-tier lever list; bottom strip of "Never cut" chips.
- **Chart (native stacked column, two columns `Baseline` and `Optimised`), "Cost per brief before buffer (USD)":**
  - Series (stack order bottom to top), Baseline / Optimised:
    - `Research subagents` 7.50 / 4.00 (TEAL)
    - `Opus plan + write` 4.40 / 3.50 (INK)
    - `Web search` 2.25 / 1.50 (SLATE)
    - `S3 corroboration` 0.90 / 0.75 (`5EEAD4`)
    - `Extraction + S2 judge` 0.77 / 0.39 (MINT)
  - Data labels `ctr`. Totals above each column as text boxes: `$15.82 → ≈ $21 with buffer` and `$10.14 → ≈ $13 with buffer`.
  - Chip between the columns: `−37%`.
- **Small insight line under the chart (12 pt):** `Input = 63% of the Claude bill — agents re-read history and pages, so we cut input, not output.`
- **Lever list (right):**
  - GREEN chip `No quality impact`: **Prompt caching** (≈ −$3.40) · **Batch API 50% off** (≈ −$0.40) · **Shared page and search cache** (≈ −$0.75)
  - AMBER chip `Gold-set tested`: **Relevant text only** (≈ −$0.50) · **Short structured outputs** (≈ −$0.50) · **Opus only for writing** (≈ −$0.80)
  - TEAL chip `Grows over time`: **Fact Base reuse** · **Better S1 rules** · **Fewer retries**
- **"Never cut" strip (RED-outline chips):** `S3 on headline numbers` · `Cross-vendor judge` · `Frontier client writing` · `No free tier for client data` · `Weekly audit`
- **Two small comparison chips (bottom right, 11 pt):** `API, not claude.ai website — the website can't be automated` · `Search API + reader, not browser automation — 10–50× fewer tokens`
- **Source line:** `Anthropic pricing: cache reads 0.05× input (Opus/Sonnet 5.5), Batch API −50%, checked 25 Nov 2026. Savings are estimates to confirm on the gold set; the budget uses the unoptimised $21.`
- **Notes:** "The budget I showed uses $21 per brief, without optimisation. Caching alone saves about $3.40 because research agents resend their history on every step. None of these levers touch the accuracy controls. That list is fixed."

---

### Slide 19: Build vs buy and the rollout plan
- **Kicker:** `STEP 3 · IMPLEMENTATION PLAN`
- **Title:** `A 16-week rollout with go/no-go gates, starting with MTI’s own past briefs`
- **Layout:** top 30% build-vs-buy comparison (3 small cards); bottom 70% Gantt.
- **Build-vs-buy cards:**
  - `Buy` (SLATE outline): "Instant, but 78–90% citation accuracy; no MTI source rules, ledger or audit trail" → chip `Benchmark in Phase 0`
  - `Build from scratch` (SLATE outline): "Full control, slow and costly" → RED chip `No`
  - `Hybrid` (TEAL fill, WHITE): "Thin custom layer (ledger, validation, gates, templates) on open source; commercial engines plugged in as tools" → GREEN chip `Chosen`
- **Gantt (native shapes; x-axis weeks 1–16; one bar per phase, TEAL; AMBER diamond at each go/no-go):**
| Phase | Weeks | Go/no-go diamond label |
|---|---|---|
| 0 Discovery: gold set, baseline, licences, buy benchmark | 1–2 | Build-vs-buy decided |
| 1 Core pipeline (free-tier prototype) | 3–6 | Cited drafts for 5 gold briefs |
| 2 Validation + Estimation + review UI | 7–9 | ≥98% numeric / ≥95% qualitative on gold set |
| 3 Integrations: licensed DBs, Country Registry (10 countries), SharePoint, templates | 10–11 | Full pack auto-generated |
| 4 Shadow pilot alongside analysts | 12–16 | ≥90% automation + targets held 5 weeks → Go live |
| 5 Scale (arrow continuing past week 16) | ongoing | — |
- **Footer row of chips:** `RACI: Engineer builds · Research lead owns tiers & audit · Analysts review · Partner signs off` · `2 analyst champions`
- **Notes:** "Each phase has an objective exit criterion. If a bought tool meets the targets in Phase 0, we buy it. That decision is made on evidence."

---

### Slide 20: Closing and asks (dark)
- **Background:** INK.
- **Title (WHITE, Cambria 34 pt):** `Automation you can audit: faster research, every number traceable`
- **Three columns (WHITE text, TEAL number chips 1–3):**
  1. **Accurate:** "Ledger-only writing, a three-stage cascade, cross-vendor judging, weekly audit"
  2. **Automated:** "≈92% of analyst time, humans at three short gates"
  3. **Affordable:** "$0 prototype · ≈$21 per brief (≈$13 optimised) · payback ≈ 5 months"
- **"What we need from MTI" panel (MINT fill, INK text):** `Brief volumes & analyst hours · Data subscriptions & licence terms · Client AI-use rules · MTI slide template · Microsoft 365 setup`
- **Notes:** "My ask is a two-week Phase 0 with 20–30 past briefs. That alone proves or disproves the numbers on MTI's own work."

---

## 3. Appendix slides (after slide 20)

| # | Title | Content |
|---|---|---|
| A1 | `Appendix — Full risk register (17 risks)` | Native table: all 17 rows from `04` §9 (Challenge · Type · Mitigation). Split across 2 slides if needed, never below 11 pt. |
| A2 | `Appendix — Cost per brief, line by line` | Native table from `04` §10.3 (scenarios B / C / D with token volumes) plus the Scenario A note. |
| A3 | `Appendix — Evidence base` | Native table from `04` §14 (Claim · Source URL), 10 pt. |
| A4 | `Appendix — Assumptions & open questions` | Bullet list from `04` §16, plus: "Baseline 16–24 h/brief", "$10/h conservative capacity value", "Engineer LKR 350k/month", "1 USD ≈ LKR 332". |

---

## 4. Build instructions for Codex

1. Create `presentation/` and write the generator script. Define palette constants and helper functions once: `kicker()`, `title()`, `footer()`, `source_line()`, `chip(text, fill, color)`, `stat_block(number, label)`, `badge(status)`, `card(x, y, w, h)`.
2. Build slides in the order above. Use native charts for slides 2, 3, 7, 10, 12 (mini chart), 13, 16 and 18. Use native tables for 5, 9, 11, 12, 14, 15, 16, 17, 18 and the appendix.
3. Add speaker notes to every slide, using the Notes text in this spec.
4. Set chart fonts to Calibri, axis label colour SLATE, gridlines `E2E8F0`, no chart borders, data labels on, legend off for single-series charts.
5. **Hex colours without `#`** if you use pptxgenjs. Don't share option objects between calls in pptxgenjs (they are mutated).
6. Save as `presentation/MTI-ResearchOS.pptx`.

## 5. QA checklist (must pass before committing)

- [ ] 21 main slides (including 18A) + 4 appendix; slide numbers in the footer; no footer on the title or closing slides.
- [ ] Every number matches `04-final-decision.md` (spot-check: 92%, 98% / 95%, 100% / 25% / 8%, $21, $11, $20, $0.26, $770, $5,600, LKR 1.85M, 552 h, ~5 months, 760+ / 56 / 7).
- [ ] No text overflow or overlap: render to PDF/images (LibreOffice or PowerPoint export) and inspect every slide.
- [ ] Titles are in the same position, font and size on every content slide.
- [ ] All charts are native and editable; no chart pasted as an image.
- [ ] Illustrative slides (6, 10, 11, 13) carry the "Illustrative" caption.
- [ ] Every slide has speaker notes.
- [ ] No placeholder text remains except `[Candidate name]` on slide 1 (the candidate fills that in).
- [ ] The file opens in PowerPoint without a repair prompt.
