# Final Decision: MTI ResearchOS

This is the definitive version. It supersedes `03-final-approach.md` and fixes the seven issues found in review (listed at the end). Where any earlier file disagrees, this file wins.

---

## 1. The decision in five lines

1. **Architecture:** a supervisor-led multi-agent pipeline on LangGraph. Every fact is stored as an evidence card in a PostgreSQL ledger, and the report is written **only** from that ledger.
2. **Accuracy:** a three-stage validation cascade (code checks → LLM judge from a *different* model family → independent corroboration), with two tracks: **published facts** and **labelled estimates**.
3. **Automation:** humans touch only three gates (plan approval, exception queue, sign-off), about **1–1.5 hours per brief** instead of 2–3 days.
4. **Proof:** automation rate **and** audited accuracy are measured every month. Thresholds tighten automatically if accuracy drops.
5. **Cost:** a **hybrid model stack**. Free and open-weight models do the bulk work (extraction and checking, about 70% of tokens). A frontier model does planning and client-facing writing. That gives **≈ USD 0 for the prototype and ≈ USD 20 per brief in production.**

---

## 2. Architecture (unchanged from 03 except where noted)

```text
Brief ─► [1] Intake Agent ─► Research Plan (JSON + issue tree)
                         └─► GATE 1: consultant approves/edits (5–10 min)
     ─► [2] Living Fact Base lookup (reuse fresh, verified facts)
     ─► [3] Supervisor ─► N parallel Research Subagents (1 / 3–5 / 8–10, effort-scaled)
              sources in priority order: Country Source Registry → MTI licensed DBs
              → World Bank/IMF/UN Comtrade → 2 web indexes → news (leads only)
              queries in English AND the local language
     ─► [4] Extraction Agent ─► Evidence Cards (value, unit, period, geo, quote, page, URL, tier)
     ─► [5] Estimation Agent (separate track: top-down / bottom-up / analogue, in Python)
     ─► [6] Validation Cascade S1 → S2 → S3 ─► confidence + status label
     ─► [7] Writer (ledger-only) ─► [8] Formatter (MTI template, code only)
     ─► GATE 2: exception queue (30–60 min) ─► GATE 3: sign-off (15 min)
     ─► Deck + Word report + Excel data book + source register + validation log
     ─► Write-back: verified facts → Fact Base; reviewer decisions → tiers/prompts/thresholds
```

**Intake learning loop** (this replaces the undefined "Gate 0" in 03): every edit a consultant makes at Gate 1 is stored with the original brief. These pairs become few-shot examples and a regression test for the Intake Agent, so plan edits fall over time. It is a feedback loop, not an extra human step.

**Two-track rule:** *Published* figures go through the cascade and get Verified / Verified-official / Conflicting / Outdated / Unverified. *Estimated* figures need 2–3 methods to agree within tolerance, with assumptions listed, and are labelled **Estimated – triangulated**. An estimate is never promoted to Verified unless a real source is found later.

---

## 3. Validation cascade (with consistent volumes, used in the budget)

| Stage | What it checks | Share of cards | Who runs it |
|---|---|---|---|
| **S1 Deterministic** | URL resolves (+ Wayback archive), exact quote present, quoted value = card value, unit/currency/period/geography consistent, recency, tier rule, derived numbers recomputed in Python | **100%** | Code (free) |
| **S2 LLM judge** | "Does the quote support the claim?" + contradiction check against other cards | **~25%** (borderline after S1 + all qualitative) | **Open-weight model** (different family from the Claude writer) |
| **S3 Corroboration** | Fresh search for a second independent source, compared within tolerance (±10% for market size, exact for official stats) | **~8%** (headline + single-source numbers) | Mid-tier model + search |

**Cross-family rule:** the writer and research models are Claude. The S2 judge is an open-weight model (Qwen / Llama / DeepSeek class) or Gemini. A model never grades its own family's work.

### Accuracy targets (one definition, used everywhere)

| Claim type | Target (audited) |
|---|---|
| Quantitative (numbers) | **≥ 98%** |
| Qualitative (statements, synthesis) | **≥ 95%** |
| Automation rate (claims auto-approved) | **≥ 90%** |

### Audit method (fixed and realistic)

- Each week an analyst checks a **random fixed sample of 40 numeric + 20 qualitative auto-approved claims** (about 1 hour a week).
- Accuracy is judged on a **rolling 4-week window** (~240 claims). The test uses the **lower 95% confidence bound**, not the raw rate, so a lucky week can't hide a problem.
- If the lower bound falls below target, the auto-approval threshold for that claim type rises automatically and more items go to the exception queue until accuracy recovers.

---

## 4. The cost approach: can we use free LLMs?

### Short answer
**Yes, for most of the work, but not for everything.** Free and open-weight models are good enough for extraction and fact-checking, which is where most of the tokens are. Planning and client-facing writing should stay on a frontier model, because that is where quality is visible to the client and where a mistake costs the most.

### The four kinds of "free" and what each is good for

| Option | Examples | Cost | Strengths | Limits | Verdict |
|---|---|---|---|---|---|
| **Free API tiers** | Gemini API free tier, Groq free tier, OpenRouter `:free` models, Mistral free tier | USD 0 | Zero cost, fast to start | Rate limits; **free tiers may use your prompts to improve the vendor's models** (check each vendor's terms); no service guarantee | ✅ Prototype with public data only. ❌ Never with client briefs |
| **Open-weight, self-hosted on a laptop / small server** | Qwen3 8–14B, Llama 3.x 8B, Gemma via Ollama | USD 0 software; existing hardware | Data never leaves MTI, so it suits confidential documents | Small models are weaker at long reasoning; slower | ✅ Extraction from confidential PDFs |
| **Open-weight, hosted inference** | Qwen / Llama / DeepSeek class on Groq, Together, DeepInfra, Fireworks | ~USD 0.1–0.9 per million tokens (assumption, varies by model) | 5–20× cheaper than frontier; a different family from Claude (ideal judge) | Weaker tool use; check data-retention terms | ✅ **S2 judging and bulk extraction in production** |
| **Open-weight on a rented GPU** | 70B-class on a cloud GPU | ~USD 700–1,500/month always-on (assumption) | Full control | **More expensive than APIs at MTI's volume** (~30 briefs/month); needs ops skills | ❌ Not worth it below ~100+ briefs/month |

### Recommended stack: the hybrid

| Job | Share of tokens | Model choice |
|---|---|---|
| Plan, supervise, write the client report | ~7% | Frontier strong (Claude Opus class) |
| Research subagents (tool use, reading) | ~28% | Frontier mid (Claude Sonnet class). Tested against open-weight on the gold set; switch if quality matches |
| Extraction + S2 judging | ~65% | Open-weight hosted (cheap, different family) or local Ollama for confidential files |

### Cost per brief: four scenarios

**Price assumptions** (planning figures; re-verify on vendor pricing pages on submission day):
- Strong model: $4 in / $20 out per million tokens.
- Mid model: $2 / $10.
- Open-weight hosted: $0.20 / $0.60.

**Volumes:**
- Strong model: 0.6M in + 0.1M out.
- Research: 2.5M in + 0.25M out.
- Extraction + judges, after the cascade: 4.5M in + 0.5M out (down from 6M + 0.6M, because only ~25% of cards reach S2 and ~8% reach S3).
- Search and reading: ~300 searches + ~500 pages ≈ $2.
- Docling is free.

| Scenario | Plan/write | Research | Extract + judge | Search/read | Subtotal | +30% buffer |
|---|---|---|---|---|---|---|
| **A. Zero-cost prototype** (free tiers + Ollama, public data only) | $0 | $0 | $0 | $0 (free credits) | **$0** | **$0** |
| **B. Hybrid (RECOMMENDED)** | $4.40 | $7.50 | $1.20 | $2.00 | $15.10 | **≈ $20** |
| **C. Max open-weight** (research also open-weight; only if the gold set shows equal quality) | $4.40 | $0.65 | $1.20 | $2.00 | $8.25 | **≈ $11** |
| **D. All frontier** (the original Perplexity design) | $4.40 | $7.50 | $0.90* | $2.60 | $16.75* | ≈ $22 |

\*D uses a cheap Claude model for checking, which breaks the cross-family rule. It is cheaper on paper than B for that line, but less trustworthy.

### Why I don't push to "all free" in production
- **The LLM is not the expensive part.** At 30 briefs a month, moving from B to C saves about USD 270 a month. One wrong number in a client deck costs MTI far more than that in credibility.
- **Free tiers can't hold client data.** The terms and the rate limits rule them out for live briefs.
- **The real saving is analyst time** (~20 hours per brief), not tokens. Optimise for accuracy first, then cut token cost where the gold set proves quality holds.
- **The design stays model-agnostic**, so as open-weight models improve, more jobs move to scenario C through configuration, with no rebuild.

---

## 5. Budget (one currency: USD; 1 USD ≈ LKR 300, update at submission)

| Item | Estimate |
|---|---|
| **Prototype (weeks 1–4)** | Scenario A: **≈ USD 0–50** |
| **Build + pilot (weeks 5–12)**: 1 engineer × 3 months (≈ LKR 159k/month) + part-time senior review + pilot API usage | ≈ LKR 480k staff + ≈ USD 500–1,000 API/hosting → **≈ USD 2,500–3,500 total** |
| **Production running cost (30 briefs/month, Scenario B)** | Usage ≈ $600 + Firecrawl $19 + Tavily ~$30 + VM ~$40 + Langfuse self-hosted $0 → **≈ USD 690/month** |
| **Maintenance** | 0.25 FTE (≈ LKR 40–60k ≈ USD 130–200) + gold-set re-runs ~$50 → **≈ USD 180–250/month** |
| **Total monthly run** | **≈ USD 870–940/month** |

### ROI, now including the build cost

| | Manual | ResearchOS |
|---|---|---|
| Analyst time per brief | ~16–24 h | ~1–1.5 h |
| Turnaround | 2–3 days | Same day |
| Hours freed (30 briefs/month) | — | **~435–675 h/month** |
| Value of freed hours at a conservative USD 10/h | — | ≈ USD 4,350–6,750/month |
| Net monthly benefit (minus ≈ USD 900 run cost) | — | ≈ **USD 3,450–5,850/month** |
| **Payback on ≈ USD 3,500 build** | — | **~1 month after go-live ≈ 4 months from kickoff** |

To be confirmed with MTI's real brief volume, analyst rates and hours in Phase 0.

---

## 6. Implementation plan (12 weeks)

| Phase | Weeks | Deliverable | Exit criterion |
|---|---|---|---|
| 0 Discovery | 1–2 | Gold set of 20–30 past briefs; baseline hours; licence inventory; source tiers | Baseline measured |
| 1 Prototype | 3–4 | End-to-end on 3 briefs, **Scenario A (free)** | Demo to partners |
| 2 Validation + Estimation | 5–7 | Full cascade, Estimation Agent, review UI; open-weight vs frontier bake-off on the gold set | ≥98% quant / ≥95% qual on gold set |
| 3 Integrations | 8–9 | Licensed DBs, Country Registry (first 10 countries), SharePoint, MTI templates | Full pack auto-generated |
| 4 Pilot (shadow mode) | 10–12 | Live briefs alongside analysts, **Scenario B** | ≥90% automation **and** audited targets met |
| 5 Scale | ongoing | More countries; move jobs to Scenario C where the gold set allows | Flag rate and cost per brief falling |

---

## 7. Challenges and mitigation (unchanged from 03 §6, plus two additions)

| New challenge | Mitigation |
|---|---|
| Free-tier data terms / rate limits | Free tiers used only in the prototype with public data; production uses paid or zero-retention endpoints or local models |
| Open-weight quality gaps | Swap decided per job by a gold-set bake-off, never by price alone |

---

## 8. Fixes applied from the review of `03-final-approach.md`

| # | Issue in 03 | Fix here |
|---|---|---|
| 1 | Claimed the cascade cuts cost to ~¼, but the budget table was unchanged | Volumes recomputed from cascade shares (§3, §4) |
| 2 | Cross-family rule broken (Claude Haiku judging Claude output) | S2 judge = open-weight or Gemini |
| 3 | "Gate 0" announced but never defined | Replaced by a defined Intake learning loop |
| 4 | Three different accuracy targets | One table: 98% quant / 95% qual / 90% automation |
| 5 | 5% audit in 15 minutes was impossible and statistically weak | 60 claims a week (~1 h), rolling 240, lower confidence bound |
| 6 | Prices labelled "verified" | Labelled as assumptions to re-verify on submission day |
| 7 | ROI ignored the build cost | Payback includes the build: ≈ 4 months from kickoff |
