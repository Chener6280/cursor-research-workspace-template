# AGENTS.md - Template Repository Instructions

This repository contains a reusable Cursor research workspace template and bootstrap/validation scripts.

When modifying this repository:

- It is acceptable to inspect and edit Python bootstrap/validation code.
- Preserve the generated workspace's non-coding research behavior.
- Do not put real API keys, cookies, tokens, or personal paths in templates, tests, or docs.
- Keep template files line-based and valid for Cursor parsing.
- Preserve default-deny `.cursorignore` and `.cursorindexingignore` behavior.
- Keep `claim_ledger.status` as the canonical evidence status axis: supported, mixed, insufficient_evidence, contradicted.
- Keep local-only / document-first literature tasks from forcing external search unless the user asks for current verification or corroboration.
- Run `python -m pytest` after changes.
