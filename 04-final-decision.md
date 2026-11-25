# Final Decision: MTI ResearchOS — Idea & Architecture

**Status:** definitive version, standalone (no need to read files 01–03). Concept and architecture only; nothing is built.
**Fact-checked:** 25 Nov 2026. Every research claim was opened at its source, and every price was checked on the vendor's own pricing page (see §14 Evidence base). Prices change, so re-check them on submission day.
**Currency:** USD throughout. **1 USD ≈ LKR 332** (Wise mid-market, Nov 2026).

---

## 0. About MTI and the problem

MTI Consulting is an international strategy consultancy founded in 1997 (now in its 30th year). It has completed **760+ assignments in 56 countries** and runs **7 regional offices** (Colombo, Melbourne, London, Manama, Kigali, Canada, Mumbai). Every assignment depends on desk research: market sizing, competitors, regulation and trade data, often for frontier markets where data is thin and scattered.

**Today:** a typical desk research brief takes an analyst **16–24 hours** (2–3 days). This is an assumption to confirm with MTI in Phase 0.
**Target:** about **1.5 hours of human time per brief**, with every fact traceable and audited.

---

## 1. The decision in six lines

1. **Architecture:** a supervisor-led multi-agent pipeline (LangGraph). Every fact is stored as an **evidence card** in a PostgreSQL **ledger**. The report is written **only** from the ledger.
2. **Accuracy:** a **three-stage validation cascade**: code checks on 100% of cards, then a different-vendor LLM judge on about 25%, then independent corroboration on about 8%. Facts run on **two tracks**: *published* facts and *labelled estimates*.
3. **Automation:** humans touch only **three gates** (approve the plan, clear the exception queue, sign off), about **1.2 hours per brief plus about 0.4 hours of audit**. That is **about 92% of analyst time automated**.
4. **Proof:** automation is always reported **together with audited accuracy**. A severity-weighted error budget tightens automation automatically if accuracy slips.
5. **Models:** a **hybrid**. Claude does planning, research and writing. Gemini Flash-Lite judges Claude's work, because a model shouldn't grade its own family. **Free and local models** are used for the prototype and for confidential documents.
6. **Cost:** **≈ USD 0 for the prototype**, **≈ USD 21 per brief** in production (**≈ USD 13 with caching and batching, same quality**), about **USD 770 a month at 30 briefs**. The build costs about USD 5,600 and pays back **within about 2 months of go-live**.

---

## 2. End-to-end flow

```text
 BRIEF (email / web form / PDF / Word)
   │
 [1] INTAKE AGENT ─► Research Plan (JSON): objective, MECE issue tree, key questions,
   │                 required metrics + units, geography, period, source types,
   │                 output format, open ambiguities (as questions, never guessed)
   ▼
 ◆ GATE 1 — consultant approves / edits plan (≈10 min)
   │   └─ every edit stored → Intake learning loop (few-shot examples + regression tests)
   ▼
 [2] FACT BASE LOOKUP ─ reuse public facts already verified and still fresh
   ▼
 [3] SUPERVISOR ─► N parallel RESEARCH SUBAGENTS, effort-scaled:
   │     simple lookup = 1 agent (3–10 tool calls) · comparison = 2–4 · multi-country = 5–10
   │     source priority: Country Source Registry → MTI licensed DBs (if licence allows)
   │       → World Bank / IMF / UN Comtrade APIs → 2 web-search indexes → news (leads only)
   │     queries in English AND the local language; original-language quote kept
   ▼
 [4] EXTRACTION AGENT ─► EVIDENCE CARDS in the LEDGER (+ stored source snapshot)
   ▼
 [5] ESTIMATION AGENT (separate track) ─ top-down / bottom-up / analogue, Python only,
   │     inputs must be verified cards
   ▼
 [6] VALIDATION CASCADE  S1 (100%) → S2 (~25%) → S3 (~8%) ─► confidence + status label
   ▼
 [7] WRITER AGENT (reads ledger only) ─► [8] FORMATTER (code; MTI template)
   ▼
 ◆ GATE 2 — Exception queue: only flagged items (≈45 min)
 ◆ GATE 3 — Sign-off by the accountable consultant (≈15 min)
   ▼
 DELIVERABLES: PPT deck · Word report · Excel data book · Source register · Validation log
   ▼
 WRITE-BACK: verified public facts → Fact Base; reviewer reason codes → tiers / prompts / thresholds
```

---

## 3. Step 1: Receiving, researching, extracting and presenting

### 3.1 Receiving and interpreting the brief
- **Intake channels:** Outlook mailbox, a web form, or an uploaded PDF or Word file (via SharePoint / Power Automate).
- **Output:** a fixed JSON schema, never free text. It is turned into a **MECE issue tree**, so research coverage can be measured ("14 of 15 sub-questions answered").
- **Ambiguities become Gate-1 questions.** Misreading the brief is the costliest error and the cheapest one to prevent.
- **Intake learning loop:** each Gate-1 edit is stored next to the original brief. These pairs become few-shot examples and regression tests, so Gate-1 edits fall over time.

### 3.2 Conducting research
This follows the documented production pattern from Anthropic's research system and LangChain's Open Deep Research:
- **Lead agent and parallel subagents.** In Anthropic's internal evaluation, this beat a single agent by 90.2%, and parallel tool calls cut research time by up to 90% on complex queries.
- **Effort scaling.** Early versions of Anthropic's system spawned 50 subagents for simple queries.
- **A task card for every subagent:** objective, output format, source guidance and boundaries. Vague delegation causes duplicated work.
- **Source-quality heuristics.** Early agents preferred SEO content farms over authoritative sources.
- **Perspective prompts** (investor, regulator, customer, competitor) for broader coverage. Stanford's STORM showed perspective-guided questioning improves coverage and organisation.
- **Country Source Registry:** a curated, versioned list of Tier-1 sources for each country (statistics office, central bank, regulators, exchange, trade ministry). It is drafted automatically, reviewed once, and reused on every brief across MTI's 56 countries.

### 3.3 Extracting and organising: the evidence card
```json
{
  "card_id": "BD-TEA-0042",
  "claim": "Bangladesh imported 4,100 tonnes of packaged tea in FY2024",
  "metric": "packaged_tea_imports", "value": 4100, "unit": "tonnes",
  "period": "FY2024", "geography": "Bangladesh",
  "source_url": "https://…", "source_tier": 1, "page": 37,
  "exact_quote": "…imports of packaged tea stood at 4,100 MT…",
  "snapshot_id": "snap_8f2c…", "archive_url": "https://web.archive.org/…",
  "published": "2025-06-30", "retrieved": "2026-11-25",
  "language": "en", "track": "published",
  "checks": {"S1": "pass", "S2": "skipped", "S3": "pass"},
  "confidence": 0.94, "status": "Verified"
}
```
*(The figures are illustrative and show the format only.)*

- PDFs and annual reports are parsed with **Docling** (MIT licence, runs locally, so confidential documents never leave MTI).
- **All arithmetic** (CAGR, shares, FX conversion, sizing) is done in **Python**, never by the LLM.

### 3.4 Presenting quantitative and qualitative data
| Output | Contents | Built by |
|---|---|---|
| **Slide deck (MTI template)** | Action titles ("Imports meet ~40% of demand → local processing is the entry route"), charts drawn from ledger values, footnote and confidence badge on every number | python-pptx |
| **Word report** | Qualitative synthesis: themes, competitor profiles, regulation. Every sentence cited | python-docx |
| **Excel data book** | One sheet per workstream; conflicting values side by side; status column | openpyxl |
| **Source register** | Every source with tier, dates, URL and archive link | openpyxl |
| **Validation log** | Everything flagged and how it was resolved | openpyxl |

A **single writer agent** writes at the end. LangChain found that writing sections in parallel produced disjointed reports.

---

## 4. Step 2: Verifying accuracy and credibility

### 4.1 Why this layer exists
| Evidence | Finding |
|---|---|
| DeepResearch Bench | Citation accuracy of commercial deep-research agents: **77.96%** (OpenAI) to **90.24%** (Perplexity) |
| Reference-hallucination study | **3–13%** of citation URLs hallucinated. Deep-research agents 10.7% vs search-augmented LLMs 4.8%. Automated URL checking cut non-resolving links **6–79×** |
| Web-search credibility study | Share of credible cited sources ranged from **71%** (GPT-5) to **86%** (Perplexity) |

**Conclusion:** off-the-shelf output is wrong or weakly supported 10–20% of the time. That is unacceptable in a client deliverable, so validation is the core of the system, not an add-on.

### 4.2 The validation cascade
| Stage | What it checks | Share of cards | Who runs it |
|---|---|---|---|
| **S1 Deterministic** | URL resolves (Wayback fallback); **exact quote found in the stored source snapshot** (not in the extractor's output, which would be circular); quoted value = card value; unit, currency, period and geography consistent; recency threshold; tier rule; derived numbers recomputed | **100%** | Code (free) |
| **S2 Cross-vendor LLM judge** | "Does this quote support this claim?"; contradiction check against other cards | **~25%**: borderline after S1, all qualitative claims, all numbers from charts, scans or translations | **Gemini Flash-Lite** (not Claude) |
| **S3 Independent corroboration** | Fresh search for a second independent source, compared within tolerance (±10% market size; exact for official statistics) | **~8%**: headline numbers, single-source numbers, all estimates' inputs | Claude Sonnet + search |

**Why a different vendor judges:** LLM judges recognise and favour their own outputs (Panickssery et al. 2024), and similar models make similar mistakes (Goel et al., ICML 2025). Having a different vendor judge costs about $0.26 more per brief (§10).

**Hard cases:**
- **Numbers in charts or scans:** OCR through Docling, then always sent to S2 and S3. They can never be auto-approved on S1 alone.
- **Translated sources:** the quote is matched in the **original language**, and the translation is shown alongside.

### 4.3 Source credibility tiers
| Tier | Sources | May supply |
|---|---|---|
| **1 Official** | Statistics offices, central banks, regulators, audited filings | Hard numbers |
| **2 Institutional** | World Bank, IMF, UN agencies, licensed databases MTI holds | Hard numbers, cross-checks |
| **3 Reputable media / industry** | Established business press, industry associations | Numbers **only if corroborated**; qualitative context |
| **4 Routing only** | Wikipedia, blogs, forums, social media, SEO sites | Leads to better sources; **never cited** |

**Conflict rule:** higher tier wins, then more independent sources, then the most recent. **Losing values are never deleted.** They stay in the data book with a conflict note. The tier-first rule is backed by a 2026 AWS preprint (Trust-Tiered Librarian). Its results come from the authors' own corpus and haven't been independently replicated, so we use it as design support, not proof.

### 4.4 When data is outdated
| Data type | Flag as "Outdated" if older than |
|---|---|
| Exchange rates, commodity prices | 3 months |
| Macro statistics (GDP, inflation, trade) | 2 years after the reference year |
| Market size / industry reports | 3 years |
| Company financials | Not the latest published financial year |
| Regulation | Always re-checked for current status |

### 4.5 Status labels and direct references
| Label | Rule | Human sees it? |
|---|---|---|
| ✅ **Verified** | ≥2 independent sources, ≥1 Tier 1–2, within tolerance | No |
| ✅ **Verified – official** | One Tier-1 source, quote matched in snapshot | No (unless headline) |
| 🟡 **Estimated – triangulated** | 2–3 methods agree; assumptions listed | Yes, if headline |
| 🟠 **Conflicting** | Sources differ beyond tolerance | **Yes** |
| 🟠 **Outdated** | Older than the threshold in §4.4 | **Yes** |
| 🔴 **Unverified** | Tier 3–4 only, or any check failed | **Yes** |

**Direct references:** every number in every deliverable carries source, page, exact quote, date accessed and an archive link.

### 4.6 When no data exists: the Estimation Agent (second track)
Frontier markets often have no published figure for exactly what the client asks. Today a consultant builds an estimate by hand. The Estimation Agent does the same:
1. **Top-down:** total category × segment share.
2. **Bottom-up:** units × price × penetration.
3. **Analogue:** a comparable country, scaled by GDP per capita or consumption ratios.

**Rules:**
- **Inputs must be verified cards.**
- The arithmetic runs in Python.
- Assumptions are listed.
- If the methods agree within ±20%, the figure is labelled **Estimated – triangulated**. If not, it goes to the exception queue.
- An estimate **can never become Verified** unless a real source is found later.
- Any estimate used as a headline needs explicit consultant sign-off.

---

## 5. Defining and proving "90–95% automation"

### 5.1 The metric tree
| Level | Metric | Target |
|---|---|---|
| **Headline** | **Process automation = 1 − (human minutes ÷ baseline minutes)** | **≥ 90%** |
| Supporting | Claim auto-approval rate | ≥ 90% |
| **Guardrail** | **Audited accuracy**: numbers ≥ 98%, qualitative ≥ 95% | Must hold, or automation tightens |

**Human time per brief (central case):**
- Gate 1: 10 min.
- Gate 2: 45 min.
- Gate 3: 15 min.
- Audit share: 25 min (3 hours a week spread across about 7 briefs).
- **Total ≈ 95 min, against a 20-hour baseline (1,200 min). That is ≈ 92% automated.**

**Range:** about 88% (16-hour baseline, slow review) to about 95% (24-hour baseline). Headlining a defined range is more credible than claiming a flat "95%".

### 5.2 The audit: a severity-weighted error budget
- **Sample:** each week, **40 numeric and 20 qualitative** auto-approved claims are drawn at random. Checking them takes about **3 hours** (about 3 minutes per claim).
- **Each error is graded:**
  - **Critical:** a wrong number or claim that would reach the client.
  - **Major:** a wrong supporting figure or attribution.
  - **Minor:** rounding or formatting.
- **When thresholds tighten:** on a **rolling 8-week** window (320 numeric, 160 qualitative claims), the auto-approval threshold rises if the critical-plus-major error count exceeds what the target would explain at 95% confidence:
  - **more than 11 numeric errors** out of 320 (target ≤2%), or
  - **more than 13 qualitative errors** out of 160 (target ≤5%).

  One unlucky mistake doesn't collapse automation, but a real drift is caught within weeks.
- **Any critical error** triggers a root-cause review of that source or prompt the same week.
- **Kill switch:** if accuracy is still below target after two tightenings, the system falls back to **assist mode** (drafts plus full human review) until the cause is fixed.

### 5.3 Levers that raise automation over time
1. Confidence-based routing: only uncertain items reach humans. Selective prediction lets a system trade coverage for a guaranteed error rate (Geifman & El-Yaniv 2017). Confidence weights are calibrated on MTI's gold set, because LLM self-confidence generalises only partly to new tasks (Kadavath et al. 2022).
2. The Estimation Agent removes "no data found" handoffs.
3. The Fact Base: repeat markets reuse verified facts.
4. The Country Source Registry finds Tier-1 sources first time.
5. Self-repair loops fix dead links and unsupported claims before a human sees them.
6. Reviewer reason codes feed back into tiers, prompts and thresholds.

---

## 6. Human-in-the-loop design: the exception card
Each flagged item appears as **one card** in a review screen (a Streamlit app, or a Teams/Excel view in the pilot). It shows:
- the claim and its status (e.g. 🟠 Conflicting);
- **the exact quote highlighted in the source snapshot**;
- alternative values with tier, date and source;
- buttons: **Accept** · **Pick alternative** · **Edit** · **Reject**;
- a **reason code** (wrong source / stale / misread / out of scope), which feeds the learning loop.

**Time box:** if Gate 2 exceeds 60 minutes, the brief is tagged for a root-cause review. That keeps "90%" honest.

---

## 7. Step 3: Implementation approach

### 7.1 Why this approach, and build vs buy
| Option | Pros | Cons | Decision |
|---|---|---|---|
| **Buy** (ChatGPT / Gemini / Perplexity enterprise deep research) | Instant, no engineering | Citation accuracy 78–90%; can't enforce MTI's source tiers; no evidence ledger or audit trail; no MTI templates | Benchmark on the gold set in Phase 0 |
| **Build from scratch** | Full control | Slow, expensive, reinvents standard parts | ✗ |
| **Hybrid (chosen)** | A thin custom layer (ledger, validation, gates, templates) on open-source orchestration; commercial engines plugged in as tools (e.g. Gemini Deep Research at about $1–3 per task) | Needs one engineer | ✅ |

**Rule:** if a bought tool meets the targets on MTI's gold set in Phase 0, buy it. This decision is made on evidence, not taste.

### 7.2 Agents, models and hand-offs
| Agent | Model | Tools | Hands to |
|---|---|---|---|
| Intake | Claude Opus 5.5 | Document parser | Plan → Gate 1 |
| Supervisor | Claude Opus 5.5 | Plan, Fact Base, ledger | Research subagents; decides when research is done |
| Research (×N) | Claude Sonnet 5.5 | Search APIs, page reader, World Bank/IMF/UN Comtrade APIs, Country Registry, MCP connectors | Raw sources + snapshots |
| Extraction | Claude Haiku 5.5 (public docs) / **local Qwen via Ollama** (confidential docs) | Docling, Python | Evidence cards |
| Estimation | Claude Sonnet 5.5 + Python | Ledger (verified cards only) | Estimated cards |
| Validator S1 | Code only | URL check, Wayback, quote matcher, unit/date rules | Pass/fail |
| Validator S2 | **Gemini 3.1 Flash-Lite** | Snapshot + claim | Support/contradiction verdict |
| Validator S3 | Claude Sonnet 5.5 | Second search index | Corroboration |
| Writer | Claude Opus 5.5 | Ledger (read-only) | Draft |
| Formatter | Code only | python-pptx/docx, openpyxl, MTI template | Deliverables → Gate 2 |

**Interaction:** agents never pass free text to each other. They read and write **typed ledger records**. LangGraph holds state, so a failed run resumes from its last checkpoint, and `interrupt()` pauses at each gate for a human. MCP (an open-source standard for connecting AI applications to external systems) plugs in new data sources without changing the agents.

### 7.3 Minimum viable stack (four core vendors)
**Anthropic** (Claude) · **Google** (Gemini judge and Deep Research tool) · **one search provider and one reader** (Tavily, Firecrawl) · **open source** (LangGraph, PostgreSQL, Docling, Langfuse, Ollama). Integration uses MTI's existing **Microsoft 365**: SharePoint for files, Power Automate for intake, Teams for notifications. Fewer vendors means fewer data-processing agreements and less for a 0.25-FTE maintainer to look after.

### 7.4 Rollout plan (16 weeks, with go/no-go gates)
| Phase | Weeks | Deliverable | Go/no-go criterion |
|---|---|---|---|
| **0 Discovery** | 1–2 | Gold set of 20–30 past briefs with final outputs; baseline analyst hours; licence inventory; source tiers; buy-option benchmark | Baseline measured; build-vs-buy decided |
| **1 Core pipeline** | 3–6 | Intake → research → ledger → S1 → writer → deck, on free tiers (prototype) | Cited draft for 5 gold briefs |
| **2 Validation + Estimation** | 7–9 | Full cascade, confidence calibration, Estimation Agent, exception-card UI | Gold set: ≥98% numeric / ≥95% qualitative accuracy |
| **3 Integrations** | 10–11 | Licensed DBs (where terms allow), Country Registry for the first 10 countries, SharePoint, MTI templates | Full pack generated automatically |
| **4 Shadow pilot** | 12–16 | Live briefs run in parallel with analysts | **≥90% automation and accuracy targets held for 5 weeks** → go live |
| **5 Scale** | ongoing | More countries; Fact Base growth; monthly gold-set re-runs | Flag rate and cost per brief falling |

**RACI:**
- **Engineer:** builds and runs the system (R).
- **Research lead:** owns source tiers and the audit (A).
- **Analysts:** review at the gates (R).
- **Partner:** signs off deliverables and stays accountable to the client (A).
- **IT:** security and access (C).

**Change management:** two analyst champions, a shadow pilot so nobody's work is at risk, and a visible evidence trail on every claim, so trust is earned rather than demanded.

---

## 8. Data governance
| Data class | Example | Allowed models | Enters shared Fact Base? |
|---|---|---|---|
| **Public** | Statistics office tables, news, filings | Any approved paid model | ✅ Yes |
| **Licensed** | Statista, Euromonitor, EMIS extracts | Only where the licence permits automated or AI use (checked in Phase 0) | Only if the licence allows |
| **Client-confidential** | Client briefs, client-supplied data | **Local model (Ollama)** or paid API with no training and zero retention | ❌ Never; isolated per client |

- **Free API tiers are never used with client data.** Google's terms state free-tier content may be used to improve products and read by human reviewers, and tell users not to submit confidential information. On paid tiers, prompts are not used for training.
- **Personal data:** desk research avoids personal data. Anything incidental is handled under Sri Lanka's **Personal Data Protection Act No. 9 of 2022**.
- **Client disclosure:** AI-assisted research is disclosed in the engagement letter. The accountable consultant signs every deliverable.
- **Prompt injection:** following OWASP LLM01:2025, web content is treated as untrusted data, agents get least privilege, nothing is sent or published without human approval, and external content is segregated.

---

## 9. Step 4: Challenges and mitigation
| # | Challenge | Type | Mitigation |
|---|---|---|---|
| 1 | Hallucinated numbers | Technical | Writer reads the ledger only; quote matched in snapshot; cross-vendor judge; maths in Python |
| 2 | Fake or dead citations | Technical | URL check + Wayback archive; self-repair loop |
| 3 | Unreliable or biased sources | Technical | Tier lattice; Tier 4 = leads only; S3 for headline numbers |
| 4 | Conflicting data | Technical | Fixed conflict rule; alternatives kept; sent to a human |
| 5 | Outdated data | Technical | Thresholds by data type (§4.4); "latest available" noted |
| 6 | No published data (frontier markets) | Technical | Estimation track with labels and sign-off |
| 7 | Paywalls, bot blocking, scanned PDFs | Operational | Official APIs first; licensed APIs; Docling OCR; "inaccessible" flag for human sourcing |
| 8 | Non-English sources | Technical | Local-language queries; original-language quote matching |
| 9 | Automation failures (API errors, timeouts) | Technical | LangGraph checkpoints, retries, resume from last step |
| 10 | Cost blow-outs or agent loops | Technical | Effort scaling; token and search budgets per run; Langfuse alerts |
| 11 | Quality drift after model changes or deprecation | Technical | Model-agnostic config; gold-set regression test before any switch |
| 12 | Prompt injection | Security | OWASP controls (§8) |
| 13 | Client confidentiality and leakage between clients | Operational | Data classes; per-client isolation; local models; no free tiers |
| 14 | Database licence terms | Legal | Phase-0 licence review; connectors only where permitted |
| 15 | Over-automation hiding errors | Operational | Error budget + kill switch (§5.2) |
| 16 | Key-person risk (one engineer) | Operational | Documented runbooks; managed services; a second trained person |
| 17 | Analyst resistance | People | Champions; shadow pilot; framed as more capacity, not headcount cuts |

---

## 10. Step 5: Models and the free-LLM question

### 10.1 Verified model prices (per million tokens, input / output)
| Model | Price | Role |
|---|---|---|
| Claude Opus 5.5 | $4 / $20 | Plan, supervise, write |
| Claude Sonnet 5.5 | $2 / $10 | Research, S3, estimation |
| Claude Haiku 5.5 | $0.10 / $0.50 (prompts ≤100K tokens; $0.50 / $2.50 above) | Extraction (documents chunked under 100K) |
| Gemini 3.1 Flash-Lite (paid tier) | $0.25 / $1.50 | S2 cross-vendor judge |
| Qwen3-235B (open-weight, DeepInfra) | $0.09 / $0.55 | Optional, for Scenario C |
| Qwen / Llama via **Ollama** (local) | $0 | Prototype; confidential documents |
| Alternatives | GPT-6.2-astra $8/$40 (top), GPT-6.2-sol $2/$10 (mid), Gemini 3.1 Pro $2/$12 | Model-agnostic: can swap via config |

Cost levers: the **Batch API** is 50% off (for S2/S3, which aren't urgent), and **prompt caching** reads cost 0.05–0.1× input. Neither is counted in the budget below, so they are pure upside.

### 10.2 Should we use free LLMs?
**Yes, where accuracy risk and data sensitivity are low. No for client-facing reasoning.**

| "Free" option | Verdict |
|---|---|
| **Free API tiers** (Gemini free tier; OpenRouter `:free` at 20 requests/min and 50–1,000/day) | ✅ Prototype with public data only. ❌ Client work: data may be used for training or human review, and the rate limits stall long research runs |
| **Local open-weight models (Ollama)** | ✅ Confidential document extraction: data never leaves MTI |
| **Hosted open-weight** (Qwen3 / Llama / DeepSeek, about $0.07–0.26 in per Mtok) | ✅ Optional cost lever (Scenario C), if the gold set proves research quality holds |
| **Rented GPU, self-hosted** | ❌ Costs more than APIs at MTI's volume |

**The key insight:** the cheap models already handle about **half the tokens but only about 6% of the cost**. Cost is driven by the *research* model. Switching everything to free models therefore saves at most about **$10 per brief**, roughly $300 a month at 30 briefs. One wrong number in a client deck costs MTI more than that. The real saving is **about 18 analyst hours per brief**.

### 10.3 Cost per brief (standard brief, about 6 workstreams, about 150 evidence cards)
| Line | Volume (in / out tokens) | B. Hybrid ✅ | C. Max open-weight | D. All-Claude |
|---|---|---|---|---|
| Plan, supervise, write (Opus) | 0.6M / 0.1M | $4.40 | $4.40 | $4.40 |
| Research subagents | 2.5M / 0.25M | $7.50 (Sonnet) | $0.36 (Qwen3-235B) | $7.50 |
| Extraction | 3.0M / 0.3M | $0.45 (Haiku) | $0.44 (Qwen3-235B) | $0.45 |
| S2 judge (~25% of cards) | 0.8M / 0.08M | $0.32 (Gemini FL) | $0.32 (Gemini FL) | $0.12 (Haiku ✗ same family) |
| S3 corroboration (~8%) | 0.3M / 0.03M | $0.90 (Sonnet) | $0.90 | $0.90 |
| Web search (~300 at ~$0.0075) | — | $2.25 | $2.25 | $2.25 |
| **Subtotal** | | **$15.82** | **$8.67** | **$15.62** |
| **+30% buffer** (retries, re-checks) | | **≈ $21** | **≈ $11** | **≈ $20** |

- **Scenario A (prototype):** Gemini free tier + Ollama + Tavily's 1,000 free credits a month + Exa's $10 free monthly credits + Jina Reader + Docling = **$0**. Public data only.
- **Why B over D:** an independent judge costs only about **$0.26 more per brief**.
- **Why B over C for now:** Scenario C is cheaper but unproven on research tool use. Phase 2 runs a gold-set bake-off, and if C matches B, switching is a config change.

### 10.4 Cost optimisation without reducing quality
**Where the money goes:** across Claude usage, **input is about 63% of the bill** ($8.30 input vs $4.95 output per brief). Output is 5× more expensive per token, but research agents read far more than they write. The biggest single cost is **research agents re-reading their own history and web pages**, so the savings come from cutting input, not output.

**Tier 1: no effect on quality (identical model output)**
| Lever | How | Saving per brief |
|---|---|---|
| Prompt caching | Agent loops resend their history each step. The repeated part (instructions, tools, plan, earlier steps) is billed at 0.05× input on Opus and Sonnet 5.5 | ≈ $3.40 |
| Batch API (50% off) | Extraction and S2 judging run as batch jobs; same-day delivery still holds | ≈ $0.40 |
| Shared page and search cache | Each page or search is fetched once per brief (and across briefs); free official APIs first | ≈ $0.75 |
| Code-built deliverables | Charts, tables and slides come from Python templates, not LLM tokens | (already in design) |

**Tier 2: quality held, confirmed on the gold set before switching**
| Lever | How | Saving per brief |
|---|---|---|
| Send only relevant text | Clean text, dedupe, relevant PDF pages only. **S1 still matches quotes against the full stored snapshot** | ≈ $0.50 |
| Short structured outputs | Compact JSON notes; output caps per step | ≈ $0.50 |
| Opus only for planning and final writing | Supervisor runs on Sonnet | ≈ $0.80 (not counted below) |
| Strict effort scaling and stop rules | 1 agent for simple briefs; stop when every sub-question has verified answers | Varies |

**Tier 3: savings that grow over time:** Fact Base reuse on repeat markets, better S1 rules (fewer S2 calls), and fewer retries (buffer 30% → 20%).

| | Baseline (§10.3 B) | Optimised (Tier 1 + Tier 2 text and output levers) |
|---|---|---|
| Opus (plan/write) | $4.40 | $3.50 |
| Research subagents | $7.50 | $4.00 |
| Extraction | $0.45 | $0.23 |
| S2 judge | $0.32 | $0.16 (if Gemini batch pricing applies; check) |
| S3 corroboration | $0.90 | $0.75 |
| Web search | $2.25 | $1.50 |
| **Subtotal** | **$15.82** | **$10.14** |
| **+30% buffer** | **≈ $21** | **≈ $13 (≈ 37% lower)** |
| Monthly usage at 30 briefs | $617 | ≈ $396 |

With Tier 3 over time, the cost could fall toward **$10–11 per brief** (an estimate to confirm on the gold set). The budget in §12 deliberately stays on the **unoptimised $21**, so the optimisation is upside, not an assumption the ROI depends on.

**Never cut, because accuracy depends on these:** S3 corroboration on headline numbers; the cross-vendor judge (switching to a same-family judge saves only about $0.20); frontier-quality client writing without gold-set proof; the no-free-tier rule for client data; the weekly audit sample.

**Website vs API:** the system runs on the **Claude API**, not the claude.ai website. The website can't be automated (consumer terms forbid scripted access), has message caps, runs one chat at a time and can't feed the ledger. Claude Team seats remain optional for consultants' own ad hoc work.

**Browser automation vs search APIs:** reading a page by Claude browsing (computer use) takes a screenshot at every step, which uses roughly 10–50× the tokens of a search API plus page reader and is much slower. It is used only as a fallback for the under 5% of pages APIs can't read (click-through government portals, JavaScript dashboards).

---

## 11. Tools, purpose, free alternatives and prices
| Category | Tool | Why needed | Price (checked 25 Nov 2026) | Free alternative |
|---|---|---|---|---|
| Orchestration | LangGraph | State, resume, human gates | Free (MIT) | CrewAI, Microsoft Agent Framework |
| LLMs | Claude / Gemini (§10) | Reasoning, extraction, judging | §10.1 | Gemini free tier, Ollama |
| Web search ×2 | Tavily + Exa | Two independent indexes for corroboration | Tavily $0.008/credit (1k free/mo); Exa $7/1k on the default mode ($4 lite) | Free tiers; Brave $5 free/mo |
| Page reader | Firecrawl | Clean text from pages and PDFs | Hobby $19/mo (5k pages); Standard $99/mo (100k) | Jina Reader; Firecrawl 1k free/mo |
| Document parsing | Docling | Tables + OCR, runs locally | Free (MIT) | — |
| Official data | World Bank, IMF, UN Comtrade, national statistics offices | Tier-1 numbers | Free | — |
| Licensed data | MTI's subscriptions; Statista Connect API | Tier-2 market data | Statista: by quote, not published | Official statistics |
| Managed research (optional) | Gemini Deep Research | Extra engine for long tasks | ~$1–3 per task (token-billed) | — |
| Search grounding (optional) | Google Search grounding | Grounded Gemini answers | 5,000 free/mo, then $14 per 1k | — |
| Ledger + Fact Base | PostgreSQL + pgvector | Evidence store, reuse | Free | — |
| Observability | Langfuse | Tracing, cost, evaluations | Self-host free; Core $29/mo | LangSmith free developer seat |
| Review UI | Streamlit (or Teams/Excel in pilot) | Exception queue | Free | — |
| Triggers | Power Automate (in M365) / n8n | Email and form intake | M365 existing; n8n €20/mo billed annually | n8n self-hosted |
| Outputs | python-pptx / docx / openpyxl | MTI-template deliverables | Free | — |
| Archive | Wayback Machine API | Link preservation | Free | — |
| Hosting | Hetzner CCX13 (2 dedicated vCPU / 8 GB) | Runs agents and database | €36.99–43.49/mo (≈ $50) | Local server during pilot |

---

## 12. Budget

### 12.1 One-off build cost (16 weeks)
| Item | Basis | USD |
|---|---|---|
| AI engineer, weeks 3–16 (~3.25 months) | LKR 350k/month mid-level (market sources range ~LKR 90k–390k; confirm locally) | ≈ 3,450 |
| Phase-0 analyst time (gold set, baseline timing) | ~40 h × $10/h | ≈ 400 |
| API + hosting during build and pilot | Gold-set runs, bake-offs, shadow briefs | ≈ 1,000 |
| Contingency 15% | — | ≈ 730 |
| **Total build** | | **≈ USD 5,600 (≈ LKR 1.85M)** |

The prototype phase alone (weeks 3–6, free tiers) costs **≈ USD 0–50** in tools.

### 12.2 Monthly running cost (Scenario B)
| Item | 10 briefs/mo | **30 briefs/mo** | 50 briefs/mo |
|---|---|---|---|
| Per-brief usage (× $20.57) | 206 | **617** | 1,029 |
| Firecrawl | 19 (Hobby, 5k pages) | **99** (Standard) | 99 |
| Hosting (Hetzner) | 50 | **50** | 50 |
| Langfuse (self-hosted) | 0 | **0** | 0 |
| **Running total** | **≈ 275** | **≈ 770** | **≈ 1,180** |
| Maintenance: 0.25 FTE (≈ $265) + monthly gold-set re-runs ($50) | 315 | **315** | 315 |
| **All-in monthly** | **≈ 590** | **≈ 1,085** | **≈ 1,495** |

### 12.3 Value (framed as capacity, not cash)
| | 10 briefs/mo | **30 briefs/mo** | 50 briefs/mo |
|---|---|---|---|
| Analyst hours freed (20 h → 1.6 h per brief) | 184 h | **552 h** | 920 h |
| Capacity value at a conservative $10/h | $1,840 | **$5,520** | $9,200 |
| Net monthly benefit | $1,250 | **$4,435** | $7,705 |
| **Payback on the $5,600 build** | ~4.5 months after go-live | **~1.3 months after go-live (≈ 5 months from kickoff)** | < 1 month after go-live |

Freed hours become **capacity**: more proposals, more briefs per analyst, and faster turnaround (**same day instead of 2–3 days**). They are not a headcount cut. All volumes and rates are confirmed with MTI in Phase 0.

---

## 13. Worked example (illustrative, for the presentation)
**Brief:** *"Assess Bangladesh as an export market for a Sri Lankan packaged-tea brand."*

| Stage | What happens | Human time | Est. cost |
|---|---|---|---|
| Intake | Plan: market size, imports by origin, top brands, tariffs and regulation, retail channels, consumer trends. One ambiguity raised: "premium segment only?" | **10 min** (Gate 1) | $0.60 |
| Research | 5 subagents. Bangladesh Bureau of Statistics, Bangladesh Bank, UN Comtrade, tariff schedule, Bengali-language news | — | $9.50 |
| Extraction | ~150 evidence cards | — | $0.45 |
| Estimation | Premium-segment size triangulated three ways (import data × premium share; retail store audit proxy; Sri Lanka analogue). Methods within 15% → *Estimated* | — | $0.30 |
| Validation | S1 catches 1 dead link (repaired via Wayback). S2 flags a stale 2019 tariff figure → *Outdated*. S3 finds two import figures 22% apart → *Conflicting*, Tier-1 customs value chosen | — | $1.25 |
| Write + format | 18-slide deck, Word report, data book | — | $3.50 |
| Exception queue | 12 cards (8% of 150): 1 conflict, 1 outdated, 3 qualitative, 7 headline confirmations | **45 min** (Gate 2) | — |
| Sign-off | Partner reviews the headline estimate and its assumptions | **15 min** (Gate 3) | — |
| **Total** | | **70 min + audit share** | **≈ $16 + buffer** |

---

## 14. Evidence base (each source opened 25 Nov 2026)
| Claim used | Source |
|---|---|
| Multi-agent beat single agent by 90.2% (Claude Opus 4 lead + Sonnet 4 subagents vs Opus 4 alone, internal eval); up to 90% faster; ~15× tokens; effort scaling; SEO-farm and 50-subagent lessons; ~20-query evals; LLM-judge rubric | https://www.anthropic.com/engineering/multi-agent-research-system |
| Scope → research → write; supervisor + subagents; parallel writing was disjointed | https://blog.langchain.com/open-deep-research/ |
| Citation accuracy 77.96–90.24% (FACT framework, Table 1) | https://arxiv.org/html/2506.11763 |
| 3–13% hallucinated URLs; 10.7% vs 4.8%; URL checking 6.4–79× fewer non-resolving links | https://arxiv.org/abs/2604.03173 |
| Trust-Tiered Librarian (AWS preprint): tier-first 22/22 vs 9/22; ledger 6,845 → 0 contradictions | https://arxiv.org/abs/2608.12984 |
| Credible-source share 71% (GPT-5) – 86% (Perplexity) (EACL 2026) | https://arxiv.org/abs/2510.13749 |
| SAFE: 72% agreement with humans, wins 76% of disagreements, >20× cheaper | https://arxiv.org/abs/2403.18802 |
| Chain-of-Verification: FactScore 55.9 → 71.4 | https://arxiv.org/html/2309.11495 |
| STORM: perspective-guided questioning improves coverage and organisation | https://arxiv.org/abs/2402.14207 |
| LLM judges favour their own outputs | https://arxiv.org/abs/2404.13076 |
| Similar models share errors, which undermines oversight (ICML 2025) | https://arxiv.org/abs/2502.04313 |
| LLMs (mostly) know what they know, with partial generalisation | https://arxiv.org/abs/2207.05221 |
| Selective prediction guarantees an error rate | https://arxiv.org/abs/1705.08500 |
| OWASP LLM01:2025 Prompt Injection | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ |
| LangGraph `interrupt()` and checkpointers | https://docs.langchain.com/oss/python/langgraph/interrupts |
| Model Context Protocol | https://modelcontextprotocol.io/docs/getting-started/intro |
| MTI facts (1997, 760+ assignments, 56 countries, 7 offices) | https://www.mtiworldwide.com/ |
| Prices | Anthropic, OpenAI, Google AI Studio (pricing and terms), DeepInfra, OpenRouter, Exa, Tavily, Brave, Firecrawl, Jina, LlamaIndex, Langfuse, n8n, Hetzner, Statista pages, checked 25 Nov 2026 |

---

## 15. Suggested presentation storyline (15 slides)
1. **Desk research costs 16–24 analyst hours per brief; we can return over 90% of that.** *Visual:* baseline vs target bar.
2. **"90% automation" is defined, measured and guarded by audited accuracy.** *Visual:* metric tree (§5.1).
3. **Brief in, audited research pack out, with humans at just three gates.** *Visual:* end-to-end flow (§2).
4. **Specialised agents, each with one job and a typed hand-off.** *Visual:* agent swimlane (§7.2).
5. **Every number is an evidence card; the writer can only cite the ledger.** *Visual:* annotated card (§3.3).
6. **A three-stage cascade catches fake, stale and conflicting data cheaply.** *Visual:* funnel, 100% → 25% → 8% (§4.2).
7. **Conflicts are settled by rule, and losing values stay visible.** *Visual:* tier lattice and conflict example (§4.3).
8. **When no data exists, we triangulate and label honestly.** *Visual:* three-method estimate chart (§4.6).
9. **Worked example: one brief, 70 minutes of human time, about $16.** *Visual:* stage timeline (§13).
10. **What the consultant actually sees.** *Visual:* mock deck slide, data-book tab and exception card (§3.4, §6).
11. **Accuracy is audited weekly, and automation tightens itself if it slips.** *Visual:* control chart (§5.2).
12. **Client data never touches a free tier.** *Visual:* data-class matrix (§8).
13. **Seventeen risks, each with a built-in control.** *Visual:* risk heat map and table (§9).
14. **Free where it's safe, frontier where the client sees it: about $21 per brief.** *Visual:* scenario bars and tool table (§10–11).
15. **USD 5.6k build, payback about 5 months from kickoff, on a 16-week rollout with go/no-go gates.** *Visual:* Gantt, ROI at 10/30/50 briefs, and our asks of MTI: volumes, licences, template.

*Appendix:* build vs buy (§7.1), full price table, evidence base, assumptions register.

---

## 16. Assumptions and open questions for MTI
- Brief volume, typical scope and current analyst hours (drives the ROI).
- Data subscriptions held, and their terms on automated or AI use.
- Client rules on AI use and data residency.
- MTI's slide template and style guide.
- Microsoft 365 setup (SharePoint, Power Automate, Teams).
