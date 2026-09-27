# Zeta Agentic Upgrade — Project Plan

**Extending [pronzzz/zeta](https://github.com/pronzzz/zeta) with agentic AI/LLM tooling — not a rewrite.**

## 0. Where this starts from

Zeta today: a local-first agent (Python 3.10+, Typer/Rich CLI + FastAPI + React dashboard) with an **Intent Router** dispatching to skills (web search via `ddgs`, finance, system control, notes), an **Ollama** LLM backend, and a **Memory Manager** split across SQLite (session history) and ChromaDB (long-term vector facts). Config lives in one `config.yaml`. Development has run in verified phases (`verify_phase1.py`…`verify_phase8.py`). Current deps: `typer, rich, psutil, pyyaml, ollama, cryptography, pydantic, chromadb, ddgs, fastapi, uvicorn`.

Everything below plugs into that shape: new capabilities are **skills registered with the existing Intent Router**, new config lives in the **same `config.yaml`**, ChromaDB is **reused** rather than duplicated, and each phase ships its own `verify_phaseN.py`, continuing the existing numbering (9→12) instead of introducing a separate testing convention.

## 1. Principles

- **One Intent Router.** MCP tools, RAG retrieval, and the triage pipeline are all reachable as Zeta skills, not standalone scripts the router doesn't know about.
- **One memory store.** ChromaDB is already a dependency — it's the vector store for RAG, not a second Chroma/FAISS instance.
- **Local-first by default, cloud as an explicit opt-in.** Tool-calling and multi-agent hand-offs are meaningfully more reliable on strong function-calling models. Add an `llm.fallback_provider` key to `config.yaml` (unset by default) so Zeta stays "100% local" out of the box, but Phase 12 in particular can be pointed at a hosted model without a code change.
- **The eval harness is infrastructure, not a phase you do last.** Building it first means Phases 10–12 each ship with regression tests from day one.

## 2. Sequencing

| Phase | Feature | Est. duration | Depends on |
|---|---|---|---|
| 9 | Evaluation harness | ~1 week | — |
| 10 | MCP retail inventory server | ~1.5 weeks | 9 (to grade it) |
| 11 | RAG tutor (AWS/ITIL) | ~1.5–2 weeks | 9 |
| 12 | Multi-agent support triage | ~2 weeks | 9, reuses 11's retriever |

**Why this order:** the harness (item 5 in your list) is explicitly the highest-leverage piece — build it first and every later phase is provably tested, not just demoed. The MCP server is self-contained and maps straight onto your actual merchandising work, so it's next. The RAG tutor's retrieval layer (keyword/dense/hybrid) then becomes the **retriever node** Phase 12 reuses instead of rebuilding — that reuse is itself a good "extend, don't duplicate" story for a portfolio.

Total: ~6–7 weeks part-time.

---

## Phase 9 — Evaluation Harness for Zeta

**Goal:** turn Zeta from "a 2-commit demo" into a system with a real, reusable regression suite.

**New structure:**
```
eval/
  tasks/            # task prompts as YAML/JSONL: input, expected behavior, pass criteria
  grader.py         # rule-based checks (skill invoked? key fact in output?) + LLM-judge fallback
  runner.py         # executes tasks against live Zeta, records pass/fail
  report.py         # pass-rate trend across commits/models, rendered with `rich`
verify_phase9.py
```

**Build steps:**
1. Write 20–40 task prompts covering existing skills (web search, finance, system control, memory recall) — e.g. "What's the price of NVDA?" with a pass criterion of "response contains a numeric price and cites the finance skill."
2. Rule-based grading first (did it call the right skill, is a regex/field present); fall back to LLM-as-judge (using the local Ollama model, keeping it free) only for open-ended tasks.
3. Persist each run (JSON or a new SQLite table) tagged with git commit hash + Ollama model name, so `report.py` can plot pass-rate over time.
4. Expose `zeta eval run` and `zeta eval report` as Typer subcommands — reusing the CLI framework already in the repo.
5. Package it so it's presentable as its own tool (separate README section, importable module) rather than buried in `main.py`.

**Stack:** Python, `pydantic` (task schema, already a dep), `rich` (already a dep), no new heavyweight dependency needed.

**Portfolio angle:** "Built a regression-test harness for a local LLM agent — rule-based + LLM-judge grading, tracked across commits" is a concrete, provable line, and every phase below cites it as their test method.

---

## Phase 10 — MCP Server for Retail Inventory

**Goal:** expose retail-merchandising tools over MCP against a synthetic dataset modeled on real patterns — maps directly onto your JB Hi-Fi merchandising duties.

**New structure:**
```
mcp_servers/retail_inventory/
  seed_data.py      # Faker-generated SKUs, stores, on-hand qty, reorder point, sell-through
  db.py             # SQLite (Postgres-ready via SQLAlchemy)
  tools.py          # check_stock_level, flag_slow_movers, draft_restock_suggestion
  server.py         # MCP server entrypoint
verify_phase10.py
```

**Tools to expose:**
- `check_stock_level(sku, store)` → on-hand qty, reorder point, days-of-cover
- `flag_slow_movers(store, window_days, threshold)` → SKUs under a sell-through threshold
- `draft_restock_suggestion(sku, store)` → structured JSON *and* a human-readable draft, mirroring what you'd actually write

**Two integration wins, not one:** register this MCP server as a client inside Zeta's own Intent Router (Zeta talks to its own server over MCP). That demonstrates both **building** an MCP server and **consuming** one — more interesting than either alone.

**Stack choice:** Python MCP SDK, to stay in one codebase with the rest of Zeta (the TypeScript SDK is a fine alternative only if you're specifically targeting JS-first MCP clients). `sqlite3`/SQLAlchemy, `Faker` for synthetic data.

**Testing:** add eval tasks to Phase 9's harness — "what's the stock level of SKU 4471 at the Belconnen store," graded against the seeded ground truth.

---

## Phase 11 — RAG Tutor over AWS/ITIL Study Material

**Goal:** a scoped tutor over your own certification notes, with a documented retrieval ablation — the write-up is what makes this different from a generic "chat with your PDF" project, and it doubles as real exam prep.

**New structure:**
```
rag_tutor/
  ingest.py         # chunking (document chunk-size/overlap choices)
  retrievers.py      # keyword (BM25), dense (embeddings + ChromaDB), hybrid (RRF fusion)
  ablation.py        # runs all three against a labeled Q&A set, computes recall@k / MRR
  api.py             # FastAPI endpoint (sibling to Zeta's existing FastAPI app)
ABLATION.md          # the write-up: chunking choices + comparison table
verify_phase11.py
```

**Build steps:**
1. Chunk your own AWS Cloud Practitioner / ITIL notes; document the chunk size/overlap decisions (not just the final numbers — the *reasoning*).
2. Implement three retrievers: keyword (`rank_bm25`), dense (embeddings — an Ollama embedding model like `nomic-embed-text`, or `sentence-transformers`, into the existing ChromaDB), and hybrid (reciprocal rank fusion of both).
3. Hand-label ~20–30 Q&A pairs with known-correct source chunks; score each retriever on recall@k and MRR, not just end-answer correctness.
4. Write `ABLATION.md` with the comparison table and a short discussion of when each retriever wins/loses on this material.
5. Serve via FastAPI — either a new tab on the existing React dashboard or a minimal standalone page.

**Stack:** ChromaDB (reused), `rank_bm25`, an embedding model, `fastapi` (reused).

**Reuse note:** `retrievers.py`'s hybrid retriever is what Phase 12 imports directly for its retriever node.

---

## Phase 12 — Multi-Agent Support-Ticket Triage

**Goal:** classifier → retriever → drafter → reviewer pipeline producing a structured, human-approved response — ties directly to "handled escalations, refunds" on your resume.

**New structure:**
```
agents/support_triage/
  tickets_synth.py   # synthetic tickets (refund, escalation, fault, price-match) — reuse Phase 10's retail data for realism
  classifier.py       # ticket category + urgency
  drafter.py           # LLM drafts a reply
  reviewer.py          # guardrail pass: policy compliance, tone, no unapproved refunds
  graph.py              # orchestration
verify_phase12.py
```

**Orchestration choice:** LangGraph over hand-rolled — an explicit state graph is easier to demo and diagram, and it's a framework interviewers commonly ask about, which hand-rolled agents don't buy you.

**Guardrails as a feature, not an afterthought:** the reviewer agent should actively block/edit drafts that promise unapproved refunds or invent policy, and every block gets logged — a "guardrail catch-rate" metric is a strong, concrete eval-harness tie-in.

**Stack:** `langgraph`, an LLM (local Ollama model, or the `llm.fallback_provider` from Section 1 if tool-calling reliability is a problem), `pydantic`.

**Testing:** end-to-end pipeline tasks *and* guardrail-catch tasks added to Phase 9's harness.

---

## 3. Cross-cutting changes

**`requirements.txt` additions across all phases:** `mcp` (or the TS SDK if you switch), `Faker`, `rank_bm25`, `sentence-transformers` (skip if using an Ollama embedding model instead), `langgraph`, `sqlalchemy` (optional, only if moving past SQLite).

**`config.yaml` additions:** new `mcp:`, `rag:`, `agents:` sections alongside the existing `llm:` and `safety:` blocks — one config file stays the source of truth.

**`README.md`:** add one section per phase as it ships, matching the existing style, and extend the architecture diagram with the new nodes (MCP server, retriever, agent graph).

**CI (cheap, high visibility):** a GitHub Actions workflow that runs `verify_phase*.py` plus `zeta eval run` on every push — "CI-gated regression suite" is a good, checkable resume line once Phase 9 exists.

## 4. Immediate next action

Start Phase 9: write the first 10 task prompts against skills that already exist (web search, finance, memory recall) and get `runner.py` executing them against a live Zeta instance end to end before writing the grader. A thin, working loop beats a complete grading rubric with nothing to run it on.
