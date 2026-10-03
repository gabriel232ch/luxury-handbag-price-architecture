# Manual vs Skill v0.3 — R1 Chinese Report Comparison

## Executive conclusion

Version B, the independently generated `$writing-analyst-prose v0.3` report, is slightly better overall as a reader-facing analyst report. It scores 51/55 versus 49/55 for Version A, a 2-point gap (0.18 points on average per dimension). This is a small quality difference, not a wholesale replacement of the manual pass.

The Skill reproduced the manual pass's core analytical discourse structure: claim-first ordering, positive scope framing, localized evidence boundaries, conditional next steps, and preservation of unresolved states. It also improved boundary economy, natural analyst voice, and report-level consistency. The manual pass remains better at naming exact evidence that would unlock a downstream decision, especially the evidence required for a pricing action, and at retaining a few local provenance details.

No material safety regression was found. The Skill report preserves the facts, numbers, reporting grain, currencies, `limited` status, unresolved-price treatment, `not_computed` comparison state, historical source conflict, and no-price-action boundary. The remaining gap is primarily analytical/editorial specificity, with a minor provenance-compression risk to monitor.

Integrity note: the supplied `BASELINE_SHA` ending in `...e13f3a8` does not resolve in Git. Both frozen commits identify the same parent ending in `...e13f8a3`; that resolvable parent was used as the baseline reference.

## Independent scorecards

Scores were assigned independently before using the sentence-level diff. Difference is `Skill − Manual`.

| Dimension | Manual | Skill | Difference |
| --------- | -----: | ----: | ---------: |
| A. Claim salience | 4 | 5 | +1 |
| B. Positive scope framing | 4 | 5 | +1 |
| C. Boundary precision | 5 | 4 | -1 |
| D. Boundary economy | 4 | 5 | +1 |
| E. Evidence-gate specificity | 5 | 4 | -1 |
| F. Business specificity | 5 | 4 | -1 |
| G. Decision usefulness | 5 | 4 | -1 |
| H. Information density | 4 | 5 | +1 |
| I. Natural analyst voice | 4 | 5 | +1 |
| J. Report-level coherence | 4 | 5 | +1 |
| K. Factual / epistemic integrity | 5 | 5 | 0 |
| **Total** | **49** | **51** | **+2** |

The lower Skill scores are not caused by incorrect analysis. They reflect places where a generic phrase such as “证据门槛” replaces a more exact list of missing evidence, or where a local provenance condition is compressed.

## Functional replacement estimate

**Estimated replacement: 90–95%, closer to 90% than 95%.**

This estimate is based on analytical function rather than lexical overlap:

- The Skill reproduces or improves the principal claim ordering in the executive summary, coverage, price ladder, historical panel, robustness method, interpretation boundary, and decision close.
- It preserves the reporting grain and the main evidence gates: same market/snapshot, local currencies, date alignment, no imputation, signature-flag requirement, source-branch retention, pre-specified independent sensitivity testing, and SKU/attribute/sample thresholds.
- It keeps the report useful for a decision reader by stating three conditional evidence paths and explicitly withholding a new-price or price-increase proposal.
- Remaining manual value is concentrated in a small number of high-specificity phrases, not in a missing analytical structure.

The replacement band is therefore high, but not equivalent to zero review. A targeted analyst pass is still useful for exact unlock evidence and local provenance.

## Full meaningful-difference inventory

Trivial punctuation, whitespace, and wording substitutions with no editorial effect are omitted. The quoted wording is taken from the committed reports: Version A at `1423d1e7` and Version B at `4bd3ff68`.

| # | Section | Manual wording | Skill wording | Category | Reason / relevant dimensions |
| -: | --- | --- | --- | --- | --- |
| 1 | Executive summary | “本轮分析基于公开本地标价观察，研究可见价格架构；品牌全量组合仍需完整 SKU 清单来界定。” | “本轮描绘的是 Chanel 在 2026-08-15 法国与美国公开本地标价样本中的可见价格架构。” | **Skill clearly better** for salience and scope framing; **Manual clearly better** for one explicit coverage boundary | Skill leads with the analytical object and makes the reader’s first sentence a finding. Manual states the full-assortment/SKU boundary more explicitly. (A, B, C, F, I) |
| 2 | Observation range / Dior | “另有 7 条价格待解析，作为缺失值保留，后续需补充可核验价格来源。” | “另有 7 条价格未解析并保留为缺失值，不做插补。” | **Different but neither clearly better** | Skill gives the stronger missing-data rule (“不做插补”); Manual gives the more operational evidence gate (“可核验价格来源”). The unresolved state and count are identical. (C, E, F, K) |
| 3 | Observation range / coverage definition | “‘数值覆盖率’定义为可解析价格行在接受观察中的比例；官网覆盖率还需要完整 SKU 清单与抓取范围记录。” | “数值覆盖率描述接受观察中可解析价格行的比例；官网覆盖率还需要完整 SKU 清单与抓取范围记录。” | **Skill clearly better** | The Skill removes a defensive “不能称为” construction while retaining the exact distinction between numeric coverage and website coverage. (A, B, D, H, I) |
| 4 | Supplementary pairing audit | “主文资格仍按属性、状态和独立家族样本门槛审查，当前证据保留在附加审计中。” | “主文资格仍需同时满足属性、状态和独立家族样本门槛。” | **Different but neither clearly better** | Skill makes the conjunctive eligibility gate more explicit. Manual preserves where the current evidence sits. The latter is useful provenance, but its omission does not change the eligibility decision. (C, D, E, J) |
| 5 | Hermès benchmark | “Hermès 在这里作为价格坐标参照；40 条当前观察均未提供供应商标注的 signature flag。若要做同口径的品牌图标溢价比较，下一步需补齐该字段并统一比较口径。” | “Hermès 的 40 条当前观察可作为价格坐标参照，但没有供应商标注的 signature flag；补齐该字段并统一比较口径后，才可进行同口径的品牌图标溢价比较。” | **Skill clearly better** | Skill states what the benchmark can do before stating the gate, then makes the unlock condition explicit. All 40 observations and the missing flag remain. (A, B, D, E, I) |
| 6 | Snapshot provenance | “执行日新页面需要作为独立刷新，与 8 月 15 日快照对齐后再纳入比较。” | “执行日的新页面不回填到 8 月 15 日快照。” | **Manual clearly better** for the local gate; **Skill equivalent** on the no-backfill rule | Manual states both independent-refresh treatment and date alignment before inclusion. Skill retains no-backfill protection but is less explicit about the condition for later comparison. (C, E, K) |
| 7 | Price ladder opening | “法国样本中，Classic 组最低观察价为……美国样本显示……” followed by “这里的间隔按同一市场、同一快照计算。” | “在同一市场、同一快照内，法国 Classic 组最低观察价为……美国对应观察值为……” | **Skill clearly better** | Skill moves validity-critical grain next to the result and removes a repeated downstream caveat without changing any value or currency. (A, C, D, H, I) |
| 8 | Group membership / sensitivity | “这里的间隔按同一市场、同一快照计算，询价状态单独记录在状态字段；……判断抽样偏差还需完整 SKU 组合与抽样框。” | “询价状态单独保留在状态字段……去变体视图用于检验颜色行重复对间隔的敏感性；抽样偏差仍需完整 SKU 组合与抽样框来判断。” | **Skill clearly better** | The Skill consolidates the repeated grain statement, preserves the inquiry-status boundary, states the sensitivity purpose positively, and keeps the sampling-frame requirement. (B, D, H, I) |
| 9 | Historical observation | “主要历史价格来自二手表格，这一层结果用于有限的方向性判断……” | “主要历史价格来自二手表格，因此结果适合有限的方向性判断……” | **Skill clearly better** | The Skill makes the source-to-interpretation relationship explicit and uses a more natural analytical sentence. Common years, lineages, missing-year treatment, primary-source requirement, and both Hermès branches remain. (C, H, I, J, K) |
| 10 | Robustness method | “这轮保留原始观察、去变体视图、家族汇总，以及价格带 ±10% 的内部边界敏感性。” | “本轮用原始观察、去变体视图、家族汇总和价格带 ±10% 的内部边界敏感性来检验架构描述的稳定性。” | **Skill clearly better** | Skill explains what the robustness views are for instead of merely listing retained artifacts. The post-observation band and pre-specified independent-test boundary remain. (A, B, D, H, I) |
| 11 | Decision implication | “当前有三条有条件的下一步……” | “当前有三条带触发条件的证据路径……” | **Skill clearly better** | “证据路径” and “触发条件” give the closing a clearer analytical identity and decision-gate structure. (G, I, J) |
| 12 | Decision implication / pricing gate | “这三条路径分别定义决策问题与证据需求；定价动作还需要需求、替代、利润和品牌资产证据。” | “它们定义的是决策问题与证据门槛，尚不足以提出新品价位或涨价方案。” | **Different but neither clearly better** | Skill gives the cleaner current decision boundary and prevents an unsupported pricing recommendation. Manual names the exact downstream evidence—demand, substitution, profit, and brand assets—that would be needed for a pricing action. (E, F, G, K) |
| 13 | Interpretation boundary | “本轮样本采用非加权的公开本地标价观察，分析对象是可见价格架构。……属于下一层判断，需要补充相应证据。” | “本报告分析非加权的公开本地标价观察，结果用于描述可见价格架构。……需要相应的独立证据。” | **Skill clearly better** | Skill states the report’s analytical use positively and upgrades the evidence requirement from generic “相应证据” to “独立证据,” while retaining the five unsupported inference categories and cost/continuity boundaries. (A, B, D, E, I) |

### Inventory synthesis

The ten substantive paragraph rewrites are not ten independent quality wins for the Skill. They cluster into three effects:

1. **Structure and voice:** Skill is better in claim-first ordering, positive scope, method-purpose statements, and reduced defensive framing.
2. **Specificity trade-off:** Manual is better when the sentence names the exact evidence or provenance action that unlocks the next step.
3. **Safety-preserving compression:** Skill shortens several boundaries but retains their operative state; the shortened wording should be monitored where it drops an inclusion condition or source location.

## Where manual is better

- **Exact evidence requirements for a pricing decision.** Version A explicitly says that pricing action requires evidence on demand, substitution, profit, and brand assets. Version B says only that a new price or price increase cannot yet be proposed. The Skill preserves the refusal boundary but loses the concrete unlock list.
- **Concrete evidence repair for unresolved Dior prices.** Version A asks for a verifiable price source after identifying the seven unresolved rows. Version B correctly says the rows remain missing and are not imputed, but does not name the source needed to resolve them.
- **Temporal/provenance detail.** Version A says execution-day pages should be treated as an independent refresh, aligned to the 15 August snapshot before being included. Version B keeps the no-backfill rule, but not the full later-inclusion condition.
- **Immediate scope signaling.** Version A puts the full-assortment/SKU-coverage boundary into the executive summary. Version B retains the website-coverage/SKU requirement in Section 1, so this is a salience and locality advantage rather than a material scope error.

## Where Skill is better

- **Claim salience.** The executive summary opens with the object being described rather than with a limitation. The price-ladder grain is also placed before the figures it qualifies.
- **Positive scope framing.** The report says what the sample describes, what the sensitivity views test, and what the evidence path supports before stating its limits.
- **Boundary economy.** Repeated same-market/same-snapshot and defensive “cannot call this…” language is consolidated without removing the operative status fields or thresholds.
- **Analytical identity.** “检验架构描述的稳定性” and “证据路径” explain the role of the analysis more directly than artifact-retention or refusal-style wording.
- **Natural analyst voice.** The Skill reads less like a paper defending itself and more like an analyst stating an observed result, its evidence gate, and the next test.
- **Report-level coherence.** The same pattern—claim, evidence state, gate, next action—appears consistently across the sections.

## Equivalent areas

The two reports are substantively equivalent on the following areas:

- All reported observations and figures: 161 accepted observations, 147 numeric prices, brand counts, Dior 13/20 and seven unresolved rows, 15 candidates, 18 cells, refresh counts, price ladder values, ratios, years, Hermès branch values, ±10% band, and the three-group threshold.
- Numeric-token sequence: identical in the committed Chinese reports.
- Fixed analytical grouping: Classic 11.12 and Small Classic versus Mini Classic, Shopping Bag, and Bowling Bag.
- Measurement grain and currency handling: France/EUR and US/USD remain separate; no FX, tax, duty, or landed-cost standardization is introduced.
- Epistemic status: both retain `limited`, no imputation for unresolved prices, `not_computed` for date-misaligned cross-brand comparison, source branches for the Hermès conflict, missing-year treatment, and the SAME_MODEL_CONTINUOUS / MODEL_SUCCESSOR / EXACT_SKU distinction.
- Decision boundary: neither report claims demand, substitution, profit, brand-equity effect, or an optimal future price from the observed list-price sample.

## Remaining human workload

**Workload: Light.**

If Version B were the first output shown to an analyst, the remaining work to reach Version A’s specific strengths would be a targeted review, not a rewrite:

1. Restore the exact unlock evidence for unresolved Dior prices and for any future pricing action.
2. Restore the full independent-refresh/date-alignment condition and, where useful, the location of evidence held in supplementary audit.
3. Decide whether the full-assortment/SKU boundary should be repeated in the executive summary for the intended audience.

No reordering of the report, numerical correction, or broad prose cleanup is required. These are a few high-value specificity edits across otherwise usable copy.

## Potential future failure families

| Failure family | Evidence count / examples in this comparison | Generalizable? | Classification |
| --- | --- | --- | --- |
| Evidence gate becomes generic after a correct refusal | 2 strong examples: “后续需补充可核验价格来源” becomes “不做插补”; “需求、替代、利润和品牌资产证据” becomes “证据门槛.” | Yes. A writer can preserve the no-go boundary while still failing to name the smallest evidence that unlocks the next decision. | **Monitor only**; no v0.4 commitment from this experiment. |
| Local provenance or inclusion condition is compressed | 2 examples: “当前证据保留在附加审计中” is omitted; “独立刷新、对齐后再纳入比较” becomes “不回填.” | Yes. This can recur whenever audit location, refresh identity, or date alignment is compressed into a shorter boundary. | **Monitor only**; not an immediate safety issue here because the blocked state and no-backfill rule remain. |
| Scope boundary moves away from the first claim | 1 direct example plus a structurally important pattern: the full-assortment/SKU boundary leaves the executive summary but remains in the coverage section. | Yes, but the current instance is not a report-level scope failure. | **Monitor only**; escalate only if future outputs omit the boundary entirely or imply census coverage. |

These are monitoring families, not proposed Skill changes. A future v0.4 candidate would require recurrence across real reports with a material effect on decision interpretation.

## Safety review

| Check | Result | Evidence |
| --- | --- | --- |
| Changes a fact | No | The two reports retain the same claims about the sample, brands, groups, sources, and evidence state. |
| Changes a number | No | Numeric values and numeric-token order are identical. |
| Changes reporting grain | No material change | Same-market/same-snapshot scope is retained in Version B and moved earlier in the price-ladder paragraph. |
| Upgrades correlation to causation | No | Neither version claims that the observed ladder causes demand, willingness to pay, profit, brand equity, or an optimal price. |
| Weakens an evidence boundary | No material weakening | Version B retains the date-misaligned `not_computed` state, no-imputation rule, source-conflict branches, pre-specified independent-test requirement, and eligibility thresholds. |
| Suppresses an unresolved warning | No material suppression | The `limited` status and the three stated strength constraints remain. The Skill omits two concrete unlock details, which is an analytical-specificity gap rather than a hidden change in status. |
| Changes missing-data interpretation | No | “未解析并保留为缺失值，不做插补” is at least as explicit as the manual wording on imputation. |

The only items requiring monitoring are the compressed provenance/inclusion wording and the less specific pricing evidence gate. Neither rises to an immediate safety issue in this frozen report.

## Final recommendation

1. **Which report is better overall?** Version B, Skill v0.3, slightly.
2. **By how much?** 2 points on the 55-point scorecard; the difference is meaningful but small.
3. **What does the manual pass still do better?** Exact missing-evidence lists, business nouns for pricing decisions, and some local provenance detail.
4. **What does the Skill do equally well?** Facts, numbers, reporting grain, unresolved-state preservation, and the principal analytical boundaries.
5. **What does the Skill do better?** Claim ordering, positive scope framing, boundary economy, methodology phrasing, analyst voice, and report-level coherence.
6. **What percentage/band of manual editorial work does the Skill replace?** 90–95%, closer to 90%.
7. **How much human editing remains after the Skill pass?** Light, focused on evidence-unlock specificity and provenance checks.
8. **Are the remaining gaps primarily stylistic, analytical, or safety-related?** Primarily analytical/editorial specificity, with minor provenance compression; not safety-related in this output.
9. **Is immediate v0.4 work justified?** No. Monitor the recurring families; one frozen comparison is not enough to commit a v0.4 change.
10. **Should v0.3 remain the default Business Analysis writing Skill?** Yes, with a light analyst spot-check for exact evidence gates and local provenance.

**SKILL REPLACEMENT: HIGH**
