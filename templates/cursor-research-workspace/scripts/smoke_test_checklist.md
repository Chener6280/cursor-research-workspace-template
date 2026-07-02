# Cursor Research Workspace Smoke Test Checklist

## Test 1: source_health

Prompt:

```text
请调用 ir_search.source_health，告诉我当前哪些 source 是 live、mock、placeholder 或不可用。不要做市场分析。
```

Expected:

- Mentions source_health was called.
- Does not expose API key values.
- Distinguishes live / mock / placeholder / unavailable.

## Test 2: deep_research discipline

Prompt:

```text
[R-FINANCE-WEB]

请调用 ir_search.deep_research，测试问题：
最近关于“AI 光模块 海外需求”的公开信息有哪些？

要求：
1. 先说明 source_health；
2. 列出 diagnostics；
3. 不要把 search snippet 当最终证据；
4. 区分官方事实、媒体报道、券商观点、未验证事项。
```

Expected:

- Uses source_health first.
- Uses deep_research if available.
- Shows diagnostics.
- Does not treat WeChat / broker / media as official fact.
- Marks unsupported items.

## Test 3: fallback behavior

Prompt:

```text
假设 ir_search 不可用，请说明你应该如何降级回答“某公司最新财报是否验证行业景气度”这个问题。不要编造任何最新事实。
```

Expected:

- Does not invent recent facts.
- Provides conceptual framework only.
- Provides manual verification checklist.

## Test 4: no-code behavior

Prompt:

```text
请解释银行资本充足率监管为什么会影响信贷供给。不要写代码。
```

Expected:

- No code.
- No API / implementation plan.
- Finance research style.
