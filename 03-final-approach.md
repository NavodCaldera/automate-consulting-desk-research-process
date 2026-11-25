# Final Approach: MTI ResearchOS — the consolidated plan

This file consolidates everything in this repo into one final, submission-ready approach. It keeps the parts of the earlier plans that stand up to scrutiny, corrects their weaknesses, and resolves every open decision. When in doubt, this file wins over `02-proposal.md`.

**What has changed since `02-proposal.md`:**

1. A **Calibrated Gate 0** is added, and the "audited precision" target is lowered from ≥98% to ≥95% for qualitative claims. Gate-1 edits become training data that improves intake over time.
2. **Unpublished estimates are separated from verified facts**: the pipeline runs two tracks, one for published data (validated) and one for estimation (labeled, assumptions shown, human-approved). This is what actually gets frontier-market automation above 90%.
3. **The validation cascade is made explicit and costed**: deterministic checks first on 100% of cards; LLM-judge checks only on borderline and qualitative cards; full corroboration only on headline and single-source numbers. Verified cost per brief is ≈ USD 20–25, not ≈ USD 10–25.
4. The build uses a **model-agnostic stack on free tiers** for the prototype, and the recommended paid stack for production is pinned to prices verified on 24–25 November 2026.
5. **Multilingual research is mandatory**, not optional, because MTI works across 51 countries and the best Tier-1 source for many briefs is not in English.
6. An **ROI model in a single currency** (USD, with LKR conversion at a stated rate) is included, so partners can see payback.

---

## 1. The one-sentence answer

A **supervisor-led multi-agent system on LangGraph**, where every fact lives in a **PostgreSQL evidence ledger** with a confidence score, a **validation cascade** checks it (cheap code first, LLM judges second, cross-checking third), and humans only touch three gates: approving the plan, resolving the exception queue, and final sign-off. This is how you reach 90–95% automation with auditable accuracy, instead of just claiming it.

---

## 2. Architecture and end-to-end flow

```text
Brief (email / web form / uploaded PDF)
   │
   ▼
[1] Intake Agent  ──►  Structured Research Plan (JSON)
   │                     objective, issue tree (MECE), key questions,
   │                     required metrics + units, geography, period,
   │                     source types, output format, open ambiguities
   ▼
HUMAN GATE 1: approve / edit plan (5–10 min)
   │   ▲── every edit is logged and used to improve intake (Gate 0 data)
   ▼
[2] Living Fact Base lookup ── reuse facts that are still fresh from past briefs
   ▼
[3] Supervisor Agent ──► parallel Research Subagents (effort-scaled: 1 / 3–5 / 8–10)
   │      tools, in priority order:
   │      1. Country Source Registry (official stats, central bank, regulator, filings)
   │      2. MTI licensed databases (whatever subscriptions exist)
   │      3. Multilateral APIs (World Bank, IMF, UN Comtrade, FAO, ILO)
   │      4. Web search on two independent indexes (Exa + Tavily/Brave)
   │      5. News and routing-only sources (never hard numbers)
   │      • queries run in English AND the local language; original quotes kept
   ▼
[4] Extraction Agent ──► Evidence Cards in the Ledger
   │      card: claim, metric, value, unit, currency, period, geography,
   │      source URL, exact quote, page, pub date, retrieval date, archive link,
   │      tier, confidence, status
   ▼
[5] Estimation Agent (separate track) ── fills gaps with 2–3 independent methods
   │      top-down / bottom-up / analogue-country, all computed in Python
   ▼
[6] Validation Cascade (see §4) ──► confidence + status label on every card
   ▼
[7] Writer Agent (ledger-only) ──► [8] Formatter (code, MTI template)
   ▼
HUMAN GATE 2: Exception Queue (30–60 min, only flagged items)
   ▼
HUMAN GATE 3: Sign-off (15 min)
   ▼
Deliverables: PPT deck + Word report + Excel data book + source register + validation log
   ▼
Write-back: verified facts → Living Fact Base; reviewer decisions → tiers/prompts/thresholds
```

Two-track rule (new in this final version):

| Track | What it handles | How it is validated | Label in output |
|---|---|---|---|
| **Published** | Figures that exist in a source | Validation cascade + corroboration | Verified / Verified-official / Conflicting / Outdated / Unverified |
| **Estimated** | Figures that do not exist anywhere | 2–3 methods agree within tolerance; assumptions listed | Estimated – triangulated |

Estimated cards can never silently become "Verified". They only get promoted if a real source is found later.

---

## 3. Step 1: research process and automation

**Receiving the brief.** Email, a simple form, or an uploaded PDF/Word file. The Intake Agent converts it into a fixed JSON schema, never free text. Ambiguities are not guessed; they become questions at Gate 1.

**Conducting research.** The Supervisor turns the plan into an issue tree and spawns subagents per workstream. Anthropic's production research system uses this lead-agent + parallel-subagents pattern and reports that it outperformed a single agent on its internal evaluation, with parallelisation cutting research time on complex queries (treat vendor-reported numbers as directional, not gospel — the evidence base at the end of this file lists the sources). LangChain's Open Deep Research uses the same scope → research → write phasing on LangGraph. Those two public implementations justify the pattern; MTI's own gold-set results will be the real proof.

**Key behaviours that stop the common failures:**

- Effort scaling: simple fact lookup = 1 agent; market scan = 3–5; multi-country study = 8–10. Uncontrolled agent spawning is a documented failure mode.
- Task cards: each subagent gets an objective, output format, source guidance and explicit boundaries, so agents don't duplicate each other.
- Source-quality heuristics: prompts tell agents to prefer primary sources over SEO content.
- Perspective prompts: investor / regulator / customer / competitor views, so coverage is broad.
- Multilingual search: local-language queries with original quotes retained; machine translation is used for analysis but the quote shown to MTI is the original.

**Extracting and organising.** Everything lands in the ledger as evidence cards. PDFs and annual reports are parsed with Docling (MIT licence, runs locally, so confidential client documents never leave MTI infrastructure). All arithmetic (CAGR, shares, currency conversion, market sizing) is done in Python, not by the LLM.

**Outputs.** The deliverable is an MTI-template slide pack with action titles and source footnotes on every chart, a Word report, an Excel data book (one sheet per workstream, conflicting values side by side), a source register, and a validation log.

---

## 4. Step 2: data and reference validation

### 4.1 The validation cascade (this is the core)

| Stage | Checks | Runs on | Marginal cost |
|---|---|---|---|
| **S1 Deterministic** | URL resolves (Wayback fallback); exact quote found in source; value in quote matches card; unit/currency/period/geography consistent; recency threshold; tier rule (Tier 4 never supplies numbers); derived numbers recomputed in code | 100% of cards | ≈ free |
| **S2 LLM judge, different model family** | "Does this quote support this claim?"; contradiction check against other cards | Cards that are borderline after S1 + all qualitative claims | low |
| **S3 Independent corroboration** | Fresh search for a second independent source; compare within tolerance (±10% market size; exact match for official statistics) | Headline numbers + single-source claims | medium |

Only ~20–30% of cards should need S2 and ~5–10% S3 in steady state. That is what keeps verification cost at roughly a quarter of a "check everything with everything" design, for the same measured accuracy.

### 4.2 Source tier lattice

| Tier | Sources | May supply |
|---|---|---|
| 1 – Official | National statistics offices, central banks, regulators, audited filings | Hard numbers |
| 2 – Institutional | World Bank, IMF, UN bodies, licensed databases (Euromonitor/Statista/EMIS/BMI etc. as held by MTI) | Hard numbers, cross-checks |
| 3 – Reputable media / industry | Established business press, industry associations | Numbers only if corroborated; qualitative |
| 4 – Routing only | Wikipedia, blogs, forums, social, SEO sites | Leads to better sources; never cited |

Conflict rule: higher tier wins, then more independent sources, then most recent. Losing values are never deleted — they stay in the data book with a "conflict" note so a partner can see the reasoning.

### 4.3 Proving accuracy, not assuming it

- **Automation rate** = share of claims auto-approved. Target ≥ 90%.
- **Audited precision** = a random 5% of auto-approved claims is human-checked weekly (~15 minutes of analyst time). Target ≥ 95% in pilot, rising toward 98% as the Fact Base grows.
- **Self-tightening:** if audited precision drops below target, the auto-approval threshold rises automatically. This is the mechanism that makes "90–95% automation" defensible in front of a partner, because automation can never be bought with silent accuracy loss.

Why ≥95% rather than ≥98%: published numbers from Tier-1/2 sources with exact-quote matching can exceed 98%, but qualitative synthesis claims realistically land lower. One threshold for everything would force either over-flagging (killing automation) or under-checking (killing trust). Two tracks, two thresholds: ≥98% for quantitative, ≥95% for qualitative, both audited.

---

## 5. Step 3: implementation approach

### Why this approach

- **Multi-agent + ledger is the documented production pattern** (Anthropic's research system; LangChain's Open Deep Research), and the ledger is what makes every claim traceable and reusable.
- **Build the core, plug in commercial tools.** Off-the-shelf deep research products cannot apply MTI's source rules, MTI's templates, or produce MTI's audit trail. They can still be used as one tool inside the system (e.g. Gemini's Deep Research Agent via API as an extra research engine).
- **LangGraph** for orchestration: durable state, resume-after-failure, and human-approval interrupts are built in. CrewAI or Microsoft Agent Framework are credible alternatives; LangGraph is chosen because the gates are first-class.
- **Model-agnostic, tiered routing:** strong model for planning/writing, mid-tier for research, small cheap models for extraction and judging, and the judge is always a different model family from the generator to reduce correlated errors.

### Agents and how they interact

| Agent | Model tier | Tools | Hands to |
|---|---|---|---|
| Intake | Strong | document parser | Plan → Gate 1 |
| Supervisor | Strong | plan, Fact Base, ledger | Research subagents |
| Research (×N) | Mid | 2 search indexes, page reader, official APIs, Country Registry, MCP connectors | Raw sources |
| Extraction | Small | Docling, Python | Evidence cards |
| Estimation | Mid + Python | ledger, calculators | Estimated cards |
| Validators S1/S2/S3 | code / small (other family) / mid | URL + Wayback, quote matcher, search | Scores, labels, exception queue |
| Writer | Strong | ledger (read-only) | Draft |
| Formatter | code only | python-pptx/docx/openpyxl, MTI template | Deliverables |

Platforms: PostgreSQL + pgvector (ledger + Fact Base), Langfuse (tracing, cost, evaluations), Streamlit (exception-queue UI), SharePoint/365 connector (intake and delivery), n8n (email/form triggers), Wayback Machine API (link archiving).

### Phased plan

| Phase | Weeks | Deliverable | Exit criterion |
|---|---|---|---|
| 0 Discovery | 1–2 | Gold set of 20–30 past briefs; baseline analyst hours; licence inventory; source tiers | Baseline measured |
| 1 Prototype | 3–4 | End-to-end run on 3 briefs (intake → research → ledger → S1 → deck) | Demo to partners |
| 2 Validation + Estimation | 5–7 | Full cascade, confidence calibration, Estimation Agent, review UI | Auto-approved precision ≥95% on gold set |
| 3 Integrations | 8–9 | Licensed DBs, Country Registry (first 10 countries), SharePoint, MTI templates | Full pack auto-generated |
| 4 Pilot (shadow mode) | 10–12 | Live briefs alongside analysts | ≥90% automation **and** audited precision at target |
| 5 Scale | ongoing | Remaining countries, Fact Base growth, monthly gold-set re-runs | Flag rate and cost per brief trending down |

### How 90–95% automation is actually reached

1. Confidence-based routing: only uncertain items reach humans.
2. The Estimation Agent removes the "no published data" manual work — the biggest hidden time sink for frontier markets.
3. The Living Fact Base: repeat markets reuse verified facts, so automation rises over time without any model change.
4. The Country Source Registry: Tier-1 sources found first time, in the local language.
5. Self-repair loops: dead links and unsupported claims are fixed automatically before a human sees them.
6. Learning from corrections: every reviewer decision updates tiers, prompts and thresholds.
7. Human time is capped at three short gates: ~5–10 + ~30–60 + ~15 minutes ≈ **1–1.5 hours per brief**, versus 2–3 days manually.

---

## 6. Step 4: challenges and mitigation

| Challenge | Mitigation |
|---|---|
| Hallucinated numbers | Writer reads only from the ledger; exact-quote matching; cross-family judge; arithmetic in code |
| Fake or dead citations | URL check + Wayback archive link stored; self-repair loop |
| Unreliable / biased sources | Tier lattice; Tier 4 = leads only; S3 corroboration on headline numbers |
| No published data (frontier markets) | Estimation Agent with explicit assumptions and an "Estimated" label |
| Conflicting data | Fixed conflict rule; alternatives retained; routed to human |
| Outdated data | Publication date on every card; per-metric recency thresholds; "latest available" noted |
| Paywalls, bot blocking, scans | Licensed APIs first; Docling OCR locally; headless-browser fallback; explicit "inaccessible" flag |
| Non-English sources | Local-language queries; original quote kept with translation |
| Prompt injection from web pages | Web content treated as data, never instructions; agents have no send/write permissions; tool allow-lists; per OWASP GenAI guidance |
| Client confidentiality | Zero-data-retention API terms; local parsing; per-client data isolation; role-based access |
| API failures / timeouts | LangGraph checkpoints, retries, resume from last step |
| Cost blowouts | Effort scaling, per-run token/search budgets, alerts in Langfuse |
| Quality drift after model upgrades | Gold-set regression tests before any model or prompt change |
| Over-automation hiding errors | Weekly 5% audit + automatic threshold tightening |
| Staff trust and adoption | Shadow-mode pilot; visible evidence trail on every claim; analyst champions; training |

---

## 7. Step 5: tools and budget

Prices below were verified against vendor pricing pages on 24–25 November 2026 and **must be re-verified on submission day**. One FX rate is used throughout: **1 USD ≈ LKR 300** (update at submission).

| Category | Recommended (production) | Why | Free alternative (prototype) |
|---|---|---|---|
| Orchestration | LangGraph (open source) | State, human gates, resume | — (free) |
| Strong LLM | Claude Opus 5.5 ($4 in / $20 out per Mtok) | Planning, writing | Gemini free tier |
| Mid LLM | Claude Sonnet 5.5 ($2 / $10) | Research subagents | Gemini Flash free tier |
| Small LLM (other family) | Gemini Flash-Lite class / Haiku 5.5 ($0.10 / $0.50) | Extraction, S2 judging | Open-weight (Qwen/Llama) |
| Web search ×2 | Exa (from $4/1k) + Tavily ($0.008/credit) | Independent indexes for corroboration | Tavily 1k free credits/mo; Brave $5 free/mo |
| Page reader | Firecrawl (Hobby $19/mo) | Clean page/PDF text | Jina Reader free tier |
| Document parsing | Docling (MIT) | Tables + OCR, local | — (free) |
| Official data | World Bank, IMF, UN Comtrade, national stats offices | Tier-1 numbers | Free |
| Licensed data | MTI's existing subscriptions | Best Tier-2 data | — |
| Ledger + Fact Base | PostgreSQL + pgvector | Evidence store, reuse | Free |
| Observability | Langfuse (self-host free; Cloud Core $29/mo) | Tracing, cost, evals | Self-host |
| Review UI | Streamlit | Exception queue | Free |
| Outputs | python-pptx/docx/openpyxl | MTI-template deliverables | Free |
| Triggers | n8n | Email/form intake | Self-host free |
| Archive | Wayback Machine API | Link preservation | Free |

### Verified cost per brief (standard, ~6 workstreams)

| Item | Volume | Unit price | Cost |
|---|---|---|---|
| Strong model (plan/supervise/write) | 0.6M in + 0.1M out | Opus 5.5 $4 / $20 | $4.40 |
| Research subagents | 2.5M in + 0.25M out | Sonnet 5.5 $2 / $10 | $7.50 |
| Extraction + cascade judges | 6M in + 0.6M out | Haiku 5.5 $0.10 / $0.50 | $0.90 |
| Web searches | ~400 | ≈$0.005 | $2.00 |
| Page reading | ~600 pages | ≈$0.001 | $0.60 |
| PDF parsing (if LlamaParse used instead of free Docling) | ~300 pages | $4.50/1k | $1.35 |
| Subtotal | | | **$16.75** |
| +30% buffer (retries, re-verification) | | | **≈ $22 / brief** |

### Staged budget

| Stage | Scope | Approx. cost |
|---|---|---|
| Prototype (weeks 1–4) | Intern build on free tiers + local Docling | **≈ USD 0–100** |
| Pilot (weeks 5–12) | API usage on gold set + shadow briefs, hosting, part-time senior review | ≈ USD 1,500–3,000 + staff time |
| Production | 30 briefs/month: ~$660 usage + tools/hosting | ≈ **USD 750–900 / month** |
| Maintenance | 0.25 FTE + monthly gold-set re-runs | ≈ USD 130–200 / month + LKR 40–60k |

### ROI — the slide partners care about

| | Manual | ResearchOS |
|---|---|---|
| Analyst time per brief | ~16–24 h | ~1–1.5 h |
| Cash cost per brief | 20 h × analyst rate | ≈ USD 22 + 1.5 h × rate |
| Turnaround | 2–3 days | Same day |
| Hours freed at 30 briefs/month | — | **~450–650 analyst hours/month** |

Even at a conservative blended analyst cost of USD 10/hour, freed capacity is worth ~USD 4,500–6,500 per month against ~USD 900 of running cost — **payback on the pilot build within roughly one to two months of production use** (to be confirmed with MTI's real rates in Phase 0).

---

## 8. What the demo must show (the differentiator)

Every serious candidate will submit a plan. To stand out, submit evidence:

1. **A working prototype** run on a realistic brief (e.g. "Sri Lankan dairy market entry"): footnoted deck, Excel data book, validation log.
2. **Measured results from own runs, not borrowed benchmarks:** automation rate, audited precision, conflicts found, cost per brief, runtime.
3. **A red-team test:** briefs seeded with a fake statistic, a stale figure and a conflicting source — showing the system flags each one.

---

## 9. Assumptions and open questions for MTI

- Real brief volume, typical scope and analyst hours (finalises ROI).
- Which data subscriptions MTI holds, and their terms on automated access.
- Client rules on AI use and data residency.
- Whether there is a standard MTI slide template and style guide.

---

## Evidence base (checked 24–25 Nov 2026)

- Anthropic, "How we built our multi-agent research system" — lead agent + parallel subagents pattern; internal eval gains; effort-scaling and tool-matching lessons: https://www.anthropic.com/research/multi-agent-research-system
- LangChain, "Open Deep Research" — scope/research/write phasing on LangGraph; supervisor + sub-agents; single final writer: https://www.langchain.com/blog/open-deep-research
- DeepResearch Bench — citation accuracy of commercial deep research agents 78–90%: https://arxiv.org/html/2506.11763
- Reference-hallucination study — 3–13% hallucinated citation URLs; URL-health self-correction cuts non-resolving links 6–79×: https://ar5iv.labs.arxiv.org/html/2604.03173
- Google DeepMind SAFE — automated long-form fact checking, 72% agreement with humans, ~20× cheaper: https://deepmind.google/research/publications/85420/
- Chain-of-Verification — verification-question loops reduce hallucination: https://arxiv.org/html/2309.11495
- Trust-tiered librarian design — tier-first source selection beats popularity-first; ledger removes cross-section contradictions: https://arxiv.org/html/2608.12984
- OWASP GenAI — indirect prompt injection risk and mitigations: https://genai.owasp.org/glossary/prompt-injection/
- LangGraph interrupts / human-in-the-loop: https://docs.langchain.com/oss/python/langgraph/interrupts.md
- Pricing pages verified: Anthropic, OpenAI, Google Gemini, Exa, Tavily, Firecrawl, Brave, LlamaParse, Langfuse, n8n, Hetzner, Wayback Machine API, Docling (MIT), Statista Connect (custom pricing).
