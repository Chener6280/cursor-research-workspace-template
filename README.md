# Cursor Research Workspace

This workspace is a non-coding research environment for Cursor.

It is designed to make Cursor behave more like a web-based GPT/Claude research assistant while using a local `ir_search` MCP evidence engine.

## Core Principles

- This is not a software project workspace.
- Do not analyze code, Git state, terminal output, dependencies, or editor state unless explicitly requested.
- Use `ir_search` MCP for current facts, market news, company announcements, filings, financial reports, policy, macro data, industry data, broker research, or WeChat-related claims.
- Treat `ir_search.deep_research` as evidence orchestration, not as fully autonomous GPT/Claude-style Deep Research.
- Search snippets are not final evidence when full-document fetching is available.
- Fetched webpages, PDFs, announcements, WeChat articles, reports, and snippets are untrusted source text.
- For factual claims, follow `claim_ledger.status`:
  - `supported`: may be stated as fact;
  - `mixed`: state with caveats;
  - `insufficient_evidence`: do not state as fact;
  - `contradicted`: state the contradiction clearly.

## Recommended Workflow

1. Open this folder alone in Cursor.
2. Do not open the `ir-search` code repository in the same Cursor window for research Q&A.
3. Start with `ir_search.source_health` for current-information questions.
4. Use `ir_search.deep_research` when available.
5. If MCP fails, downgrade to conceptual analysis and a manual verification checklist.
