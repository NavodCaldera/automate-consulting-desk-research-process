# Proposal: "MTI ResearchOS": an Agentic Desk-Research System

**Goal:** turn a research brief into a structured, validated, client-ready research pack, with 90–95% of the work automated and **audited** accuracy of at least 98% on auto-approved facts.

**One-line idea:** keep the proven multi-agent and evidence-ledger core, and add the three things real consulting needs that generic deep-research tools lack: **estimation when data doesn't exist, knowledge that compounds across projects, and an automation metric that can be audited.**

---

## 1. End-to-end flow

```
Brief (email / form / PDF)
   │
   ▼
[1] Intake Agent ──► Structured Research Plan (JSON) ──► HUMAN GATE 1 (5–10 min: approve / edit)
   │
   ▼
[2] Fact-Base Lookup ── reuse already-verified, still-fresh facts from past projects
   │
   ▼
[3] Supervisor ──► parallel Research Subagents (one per workstream; effort scaled to brief)
   │                 tools: Country Source Registry, official APIs, MTI licensed DBs,
   │                        web search (2 independent indexes), page/PDF reader, multilingual search
   ▼
[4] Extraction Agent ──► Evidence Cards in the Ledger (value, unit, period, geo, quote, page, URL, tier)
   │
   ▼
[5] Triangulation / Estimation Agent ── fills gaps with 2–3 independent sizing methods (code-computed)
   │
   ▼
[6] Validation Cascade ──► confidence score + status label on every card
   │
   ▼
[7] Writer Agent (ledger-only) ──► [8] Slide/Report Generator (MTI template, footnoted)
   │
   ▼
HUMAN GATE 2: Exception Queue (30–60 min: only flagged items) ──► HUMAN GATE 3: Sign-off (15 min)
   │
   ▼
Delivery: PPT deck + Word report + Excel data book + Source register + Validation log
   │
   ▼
Write-back: verified facts → Living Fact Base; reviewer corrections → source tiers, prompts, thresholds
```

---

## 2. Step 1: Research process and automation

**Receiving and interpreting the brief**
- Intake from email, a web form, or an uploaded PDF/Word file.
- The Intake Agent produces a fixed schema: objective, key questions, required metrics (with units), geography, time period, required source types, output format, and *open ambiguities*.
- Ambiguities become questions at Gate 1. The system never guesses the scope.
- An **issue tree** (MECE breakdown of key questions into sub-questions) is generated, so research coverage can be checked and reported.

**Conducting the research**
- The Supervisor splits the issue tree into workstreams and scales effort: 1 agent for a fact lookup, 3–5 for a market scan, 8–10 for a multi-country study.
- Source priority order: **(1) Living Fact Base → (2) Country Source Registry (official stats, central bank, regulator, exchange filings) → (3) MTI's licensed databases → (4) multilateral APIs (World Bank, IMF, UN Comtrade, FAO, ILO) → (5) web search across two independent indexes → (6) news.**
- Queries run in English **and the local language** for non-English markets, with results translated and the original-language quote kept.
- Subagents use perspective prompts (investor, regulator, customer, competitor) so coverage is broad.

**Extracting, organising and presenting the data**
- Every fact becomes an **evidence card**: claim, metric, value, unit, currency, period, geography, source URL, exact quote, page, publication date, retrieval date, archive link, tier, confidence, status.
- Tables in PDFs and annual reports are parsed with Docling (runs locally, so confidential files never leave MTI).
- **Outputs:** an MTI-template slide deck with action titles and source footnotes, a Word report, an Excel data book (one sheet per workstream, conflicts shown side by side), a source register, and a validation log.

**New: Triangulation / Estimation Agent**
When a required metric has no published figure, the agent builds it the way a consultant would:
- **Top-down:** total category × segment share (for example, total dairy imports × premium share).
- **Bottom-up:** units × price × penetration.
- **Proxy / analogue:** a comparable country adjusted by GDP per capita or consumption ratios.

All calculations run in Python. Assumptions are listed explicitly. If the methods agree within a tolerance, the result is labelled **"Estimated – triangulated"**. If they diverge, it goes to the exception queue. Without this agent, every data gap becomes manual work.

---

## 3. Step 2: Data and reference validation

### 3.1 Validation cascade (cheap checks first)
| Stage | Checks | Runs on | Cost |
|---|---|---|---|
| **S1 Deterministic** | URL resolves (Wayback fallback); exact quote found on page/PDF; value in quote matches card; unit/currency/period/geo consistent; recency threshold; tier rule (Tier 4 can't supply numbers); derived numbers recomputed in code | 100% of cards | ~free |
| **S2 LLM judge, different model family** | "Does this quote support this claim?"; contradiction check against other cards | Cards that pass S1 but are borderline + all qualitative claims | low |
| **S3 Independent corroboration** | Fresh search for a second independent source; compare within tolerance (e.g. ±10% for market size, exact for official statistics) | Headline numbers + single-source claims | medium |

### 3.2 Confidence score and status labels
Each card gets a 0–1 confidence score from the tier, the number of independent sources, agreement, recency, and the S1–S3 results. The weights are **calibrated on a gold set** of past MTI briefs.

| Label | Rule | Human sees it? |
|---|---|---|
| ✅ Verified | ≥2 independent sources, ≥1 Tier 1–2, within tolerance | No |
| ✅ Verified – official | 1 Tier-1 source, quote matched | No (unless headline) |
| 🟡 Estimated | Triangulated, methods agree | Shown with assumptions |
| 🟠 Conflicting | Sources differ beyond tolerance; all values kept | **Yes** |
| 🟠 Outdated | Latest data older than threshold | **Yes** / auto-noted |
| 🔴 Unverified | Only Tier 3–4, or a check failed | **Yes** |

**Conflict rule:** higher tier wins, then more independent sources, then the most recent. Alternatives always stay in the data book.
**Direct references:** every number in the deck has a footnote (source, page, date accessed, archive link).

### 3.3 Proving accuracy: the audit loop
- Each week, a random **5% of auto-approved claims** is checked by an analyst. That takes about 15 minutes.
- Measured precision is shown on a dashboard. **If it falls below 98%, the auto-approval threshold tightens automatically.**
- This is what makes the 90–95% claim honest: automation is never bought at the expense of accuracy without anyone noticing.

---

## 4. Step 3: Implementation approach (outline for the PowerPoint)

### Why this approach
- **Multi-agent + ledger:** this is the documented production pattern for deep research systems, and it makes the output traceable.
- **Build the core, plug in tools:** commercial deep-research products can't apply MTI's source rules or templates, or produce an audit trail. They can still be used *as one tool* inside the system.
- **LangGraph orchestration:** durable state, resume after failure, and built-in human-approval pauses. CrewAI or the Claude Agent SDK are alternatives.
- **Model-agnostic, tiered models:** a strong model for planning and writing, mid-tier for research, small and cheap for extraction. Verification uses a different model family from generation.

### Agents and how they interact
| Agent | Model tier | Tools | Output → |
|---|---|---|---|
| Intake | Strong | Doc parser | Plan → Gate 1 |
| Supervisor | Strong | Plan, Fact Base, ledger | Spawns subagents, decides when research is done |
| Research (×N) | Mid | Search ×2, reader, APIs, Registry, MCP connectors | Raw sources |
| Extraction | Small | Docling, Python | Evidence cards |
| Triangulation | Mid + Python | Ledger, calculators | Estimated cards |
| Validators S1/S2/S3 | Code / other-family small / mid | URL check, Wayback, quote matcher, search | Scores, labels, exception queue |
| Writer | Strong | Ledger (read-only) | Draft |
| Formatter | Code | python-pptx / docx / openpyxl, MTI template | Deliverables |

**Platforms:** PostgreSQL (ledger + Fact Base + pgvector), Langfuse (tracing, cost, evaluations), a Streamlit review UI (exception queue with accept / pick alternative / edit buttons), SharePoint connector (inputs and delivery), n8n (email triggers).

### Phased plan
| Phase | Weeks | Deliverable | Exit criterion |
|---|---|---|---|
| **0 Discovery** | 1–2 | Gold set of 20–30 past briefs + final outputs; baseline analyst hours; licence inventory; source tiers | Baseline measured |
| **1 Prototype** | 3–4 | End-to-end run on 3 briefs: intake → research → ledger → S1 checks → deck | Demo to partners |
| **2 Validation + Estimation** | 5–7 | Full cascade, confidence calibration, Triangulation Agent, review UI | Auto-approved precision ≥ 95% on gold set |
| **3 Integrations** | 8–9 | Licensed DBs, Country Registry (first 10 countries), SharePoint, MTI templates | Full pack generated automatically |
| **4 Pilot** | 10–12 | Live briefs run alongside analysts (shadow mode) | ≥ 90% automation **and** ≥ 98% audited precision |
| **5 Scale** | ongoing | Remaining countries, Fact Base growth, monthly gold-set re-runs | Flag rate and cost per brief trending down |

### How 90–95% automation is reached
1. Confidence-based routing: only uncertain items reach humans.
2. The Estimation Agent removes the "data not found" manual work.
3. The Living Fact Base: repeat markets need fewer new checks.
4. The Country Source Registry: Tier-1 sources found first time.
5. Self-repair loops: dead links and unsupported claims are fixed before a human sees them.
6. Learning from corrections: each reviewer decision updates tiers, prompts and thresholds.
7. Human time is limited to three short gates (about 1–1.5 hours vs. 2–3 days manually).

---

## 5. Step 4: Challenges and mitigation

| Challenge | Mitigation |
|---|---|
| Hallucinated numbers | Writer reads only from the ledger; exact-quote match; cross-family judge; numbers computed in code |
| Fake or dead citations | URL check + Wayback; self-repair loop; archived link stored |
| Unreliable or biased sources | Tier lattice; Tier 4 = leads only; S3 corroboration for headline numbers |
| No published data (frontier markets) | Triangulation Agent with explicit assumptions + "Estimated" label |
| Conflicting data | Fixed conflict rule; all alternatives retained; routed to human |
| Outdated data | Publication date on every card; thresholds by metric type; "latest available" noted |
| Paywalls, bot blocking, scanned PDFs | MTI licensed APIs first; Docling OCR; headless browser fallback; "inaccessible" flag |
| Non-English sources | Local-language queries; translation with the original quote kept |
| Prompt injection from web pages | Web content treated as data; agents have no send/write permissions; tool allow-lists |
| Client confidentiality | Zero-data-retention API terms; local parsing; role-based access; per-client data isolation |
| API failures / timeouts | LangGraph checkpoints, retries, resume from last step |
| Cost blowouts | Effort scaling, per-run token and search budgets, alerts |
| Quality drift after model upgrades | Gold-set regression tests before any model or prompt change |
| Over-automation hides errors | Weekly 5% audit + automatic threshold tightening |
| Staff trust and adoption | Shadow-mode pilot, a visible evidence trail on every claim, analyst champions, training |

---

## 6. Step 5: Tools and budget

> All prices must be re-verified on the vendors' pricing pages before submission. They are planning estimates. Use one FX rate throughout (state it, e.g. 1 USD ≈ LKR 300).

| Category | Recommended | Why | Free alternative |
|---|---|---|---|
| Orchestration | LangGraph | State, human gates, resume after failure | CrewAI, Claude Agent SDK |
| Strong LLM | Claude Opus / GPT top tier | Planning, writing | Gemini free tier (prototype) |
| Mid LLM | Claude Sonnet / Gemini Pro | Research subagents | Gemini Flash free tier |
| Small LLM (other family) | Haiku / Gemini Flash-Lite | Extraction, S2 judge | Open-weight (Qwen, Llama) self-hosted |
| Web search ×2 | Exa + Tavily/Brave | Two independent indexes for corroboration | Free monthly tiers |
| Page reader | Firecrawl / Jina Reader | Clean page and PDF text | Jina free tier |
| Document parsing | Docling | Tables + OCR, runs locally | (free, MIT) |
| Official data | World Bank, IMF, UN Comtrade, national statistics offices | Tier-1 numbers | Free |
| Licensed data | MTI's existing subscriptions | Best Tier-2 data | — |
| Ledger + Fact Base | PostgreSQL + pgvector | Evidence store, reuse | Free |
| Observability | Langfuse | Tracing, cost, evaluations | Self-host free |
| Review UI | Streamlit | Exception queue | Free |
| Outputs | python-pptx / docx / openpyxl | MTI-template deliverables | Free |
| Triggers | n8n | Email/form intake | Self-host free |
| Archive | Wayback Machine API | Link preservation | Free |

### Budget (staged)
| Stage | Scope | Approx. cost |
|---|---|---|
| **Prototype (weeks 1–4)** | Intern build on free tiers + local Docling | **≈ USD 0–100** |
| **Pilot (weeks 5–12)** | 1 engineer (or intern + part-time senior), API usage on gold set and shadow briefs, hosting | ≈ USD 1,500–3,000 in API/hosting + staff cost |
| **Production running cost** | Per brief: ≈ USD 10–25 (the validation cascade and Fact Base reuse cut the Perplexity estimate of ~22) | 30 briefs/month ≈ USD 400–800/month incl. tools & hosting |
| **Maintenance** | 0.25 FTE + monthly gold-set re-runs | ≈ LKR 40–60k/month + ~USD 50 |

### ROI (the section partners care about most)
| | Manual | ResearchOS |
|---|---|---|
| Analyst time per brief | ~16–24 h | ~1–1.5 h |
| Cost per brief | 20 h × analyst rate | ~USD 20 API + 1.5 h × rate |
| Turnaround | 2–3 days | Same day |

At 30 briefs a month, roughly **450–650 analyst hours a month are freed** for higher-value client work. Payback on the build should be **within a few months** (to be confirmed with MTI's real rates and volumes in Phase 0).

---

## 7. What I will demonstrate (my differentiator)

1. **A working prototype** run on a realistic brief (e.g. "Sri Lankan dairy market entry"). The output is a footnoted deck, an Excel data book and a validation log.
2. **Measured results, not borrowed benchmarks:** automation rate, audited precision, conflicts found, cost per brief and runtime, all from my own runs.
3. **A red-team test:** briefs seeded with a fake statistic, a stale figure and a conflicting source, showing that the system flags each one.

---

## 8. Assumptions and open questions for MTI
- Real brief volume, typical brief scope and analyst hours (needed to finalise ROI).
- Which data subscriptions MTI holds, and their terms on automated access.
- Client rules on AI use and data residency.
- Whether there is a standard MTI slide template and style guide.
