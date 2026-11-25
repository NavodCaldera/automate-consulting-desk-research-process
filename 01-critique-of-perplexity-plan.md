# Critique of the Perplexity Plan ("MTI Agentic Desk-Research Plan")

This is a point-by-point review: what the plan gets right, what is wrong or weak, and what is missing. My proposal (`02-proposal.md`) fixes each of these.

---

## 1. Where I agree, and why

| # | Perplexity design choice | Why I agree |
|---|---|---|
| A1 | **Supervisor + parallel research subagents** | Desk research breaks into independent workstreams (market size, competitors, regulation, consumers). Running them in parallel is faster, and giving each subagent its own context stops one long context from losing focus. |
| A2 | **Brief converted into a structured JSON research plan, with a human approval step** | Misreading the brief is the most expensive error, and it is cheapest to catch before any research runs. Five minutes of consultant time here saves hours later. |
| A3 | **Evidence ledger (database of claim cards) instead of free text** | This is the most important idea in the plan. A report built from a ledger can be traced, checked, reused and exported to Excel. Free text can't. |
| A4 | **Source tiers (official > institutional > media > routing-only)** | This matches how consultants already rank sources. Wikipedia and blogs can point to better sources but should never supply a number. |
| A5 | **Numbers computed in Python, not by the LLM** | LLMs make arithmetic mistakes. CAGR, market shares and currency conversion should be done in code. |
| A6 | **Review by exception** | This is the only realistic way to reach 90–95% automation: humans look only at flagged items, not the whole report. |
| A7 | **One writer agent at the end** | Separate section writers produce reports that read as disjointed. One writer working from the ledger keeps the voice consistent. |
| A8 | **URL health checks + Wayback archive links** | Cheap, deterministic, and it removes the most embarrassing failure: a dead or made-up link in a client deliverable. |
| A9 | **MCP for tool and data connectors; model-agnostic design** | New data sources and new models can be added later without a rewrite. |
| A10 | **Prompt-injection and confidentiality controls** | Web pages are untrusted input. Client briefs are confidential. Both need controls from day one. |

---

## 2. Where I disagree, and why

### D1. The evidence leans too hard on one obscure paper and on vendor claims
About half of the hard numbers ("99.5% numeric grounding", "22/22 vs 9/22", "6,845 contradictory figures → 0", "973 of 2,132 conflicts", "0.793 vs 0.714") come from a single "Trust-Tiered Librarian" arXiv paper. The "90.2% better" figure is Anthropic's internal evaluation of its own product. If an MTI interviewer asks "who replicated this?", the plan has no answer.
**Fix:** treat these as design inspiration, not proof. Show MTI **our own measured numbers** from a prototype run on real MTI-style briefs (see proposal §7).

### D2. "90–95% automation" is defined only as time saved, and the metric can be gamed
The plan defines automation as analyst hours (2–3 days down to 1–2 hours). It never says how MTI would know the 90% of claims that were auto-approved are actually correct. A system that auto-approves everything scores 100% "automation" and is still useless.
**Fix:** use two metrics that must both pass:
1. **Automation rate** = share of claims auto-approved (target ≥ 90%).
2. **Audited precision of auto-approved claims** = a random 5% sample is checked by a human every week (target ≥ 98%).
If precision drops, the approval threshold tightens automatically. That makes the 90–95% figure defensible.

### D3. "Flag data gaps, don't fill them" contradicts the 90–95% target
For Sri Lanka and other frontier markets, the number a client most wants (for example, "the size of the premium dairy segment") often isn't published anywhere. The plan's answer is to flag the gap for a human. In real consulting work, a consultant then builds an **estimate** (top-down, bottom-up, proxy or analogue country). That is hours of manual work on every brief, and it quietly breaks the automation target.
**Fix:** add a **Triangulation / Estimation Agent** that builds market-sizing models in code, using 2–3 independent methods with explicit assumptions, and labels the result **"Estimated"** rather than "Verified". This is the single biggest gap in the plan.

### D4. The validation layer is redundant and expensive
Seven checks run on every claim, including SAFE-style fresh searches *and* Chain-of-Verification *and* a citation re-fetch. These overlap heavily, and running all of them on every claim multiplies cost and latency.
**Fix:** a **cascade**. Cheap deterministic checks run first on every claim (URL health, exact-quote match, unit/period/geography consistency, recency, tier rule). Only claims that fail or are borderline go to LLM checks. Only headline numbers get full independent re-search. That cuts verification cost by roughly 60–80% for the same accuracy.

### D5. The same model family checks its own work
The plan uses Claude or GPT for generation and the same model families as judges. Errors from the same family are correlated: the judge tends to accept the kind of mistake its own family makes.
**Fix:** **cross-family verification.** If Claude writes a claim, a Gemini or open-weight model judges it (and the reverse).

### D6. It ignores the paid databases MTI almost certainly already uses
Consultancies normally hold subscriptions to sources such as Euromonitor, Statista, EMIS, Fitch Solutions/BMI, Bloomberg or Capital IQ. The plan mentions only Statista, with price unknown. The best Tier-1/2 data for a client brief is usually behind these logins.
**Fix:** Phase 0 includes an **inventory of MTI's existing licences**, with connectors built for those first. Check licence terms on automated access before building.

### D7. The world is treated as "Sri Lanka + global APIs"
MTI works in **51 countries**. The plan only hard-wires CBSL and DCS. Each country has its own statistics office, central bank, regulators, exchange filings and language.
**Fix:** a **Country Source Registry**: a curated, versioned list of Tier-1 sources per country. It is built once (and largely auto-generated, then reviewed) and reused on every brief. Add multilingual search and translation, so queries run in the local language as well as English.

### D8. Every brief starts from zero, so nothing compounds
After 30 years and thousands of assignments, MTI's main asset is accumulated knowledge. In the plan, each run is independent.
**Fix:** a **Living Fact Base**. Verified ledger entries are kept across projects, with freshness dates. The second brief on Sri Lankan dairy reuses already-verified facts, so it is faster, cheaper and needs less human review. Automation rises over time without changing the model.

### D9. The budget has errors and unverifiable assumptions
- Model prices such as "Haiku 5.5 at $0.10 / $0.50" and "GPT-6.2-sol" must be re-checked on the vendors' pricing pages on submission day. A wrong price in front of an interviewer costs credibility.
- Development is costed as **2 full-time engineers for 3 months**. That isn't realistic for an intern-led initiative, and it hides the option of a cheap staged rollout.
- The budget mixes LKR and USD without stating an exchange rate.
- It omits licences MTI may already pay for (Microsoft 365 / Copilot, data subscriptions), which change the build-vs-buy answer.
**Fix:** a staged budget (prototype ≈ free → pilot → production) in one currency with a stated FX rate, plus a cost-per-brief vs analyst-cost-per-brief **ROI** comparison. The plan has no ROI section at all.

### D10. Unverified factual claims inside the plan
"Open Deep Research repository archived in August 2026" and similar statements are presented as fact without checking. Any one of them being wrong would undermine trust in the whole document.
**Fix:** verify every factual claim, or remove it.

### D11. Output doesn't match how consultants actually deliver
The plan generates generic Word/PPT. MTI deliverables are slides in **MTI's own template**, with "so-what" headlines, source footnotes on every chart, and an appendix.
**Fix:** a slide generator that writes action titles ("Imports supply ~40% of dairy demand → entry via local processing"), puts the source footnote on every chart and table, and uses MTI's master template.

---

## 3. What is missing entirely

| Missing element | Why it matters |
|---|---|
| **Working prototype / demo** | Every candidate will submit a plan. A plan plus a live run on a real brief, with measured accuracy, is what separates the top submission. |
| **ROI / payback** | MTI's partners will ask "what do we save?". The plan gives cost but not value. |
| **Calibrated confidence scores** | Status labels are rule-based only. Scores calibrated on a gold set let MTI tune the automation vs. accuracy trade-off with one dial. |
| **Change management** | Adoption fails if analysts don't trust it. Needs champions, training and a visible evidence trail. |
| **Governance and accountability** | Who signs off? What is disclosed to clients about AI use? Is data residency required for some clients? |
| **Failure-mode testing (red team)** | Deliberately feed briefs with conflicting, stale or fake sources, and prove the system flags them. |

---

## 4. Verdict

The Perplexity plan is a **solid generic architecture** (roughly 70% of the right answer) built from well-known public patterns. Because it is generic, other candidates using AI tools will submit something very similar.

The ways to stand out are:
1. **Estimation and triangulation** (closes the real automation gap).
2. **A metric that can't be gamed:** automation rate + audited precision.
3. **Compounding knowledge:** Living Fact Base + Country Source Registry.
4. **A cheaper, smarter validation cascade** with cross-family verification.
5. **Proof:** a working prototype with measured results and an ROI case.
