# Smoke Test Checklist

Run these prompts after creating the workspace:

1. `prompts/R-SOURCE-HEALTH.md`
2. `prompts/R-DEEP-RESEARCH-SMOKE.md`
3. `prompts/R-FINANCE-WEB.md`
4. `prompts/R-LITERATURE.md`

Expected behavior:

- Source health is reported before current-information research.
- API key values are never printed.
- Search snippets are not treated as final evidence when full documents are available.
- Key claims use `claim_ledger.status`: supported / mixed / insufficient_evidence / contradicted.
- If MCP is unavailable, the answer downgrades to a framework and manual verification checklist.
