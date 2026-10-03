# 报告写作标准

用户于 2026-10-03 要求后续报告经过三项 skill 修订。本 BA 项目的报告默认执行，交付格式不替代研究与证据检查。

执行顺序：

1. `writing-analyst-prose`：先做六项简短分析地图，再按判断、证据、含义写正文。把重复边界和研究过程移到方法附录，保留会改变解释的条件。
2. `humanizer`：中文正文按 `patterns-zh.md` 检查，使用 professional 语体、balanced 修改幅度，锁定事实、引用、术语、引语和代码。对原稿与修订稿运行 `integrity_check.py`。
3. `humanize-ai`：用户已授权语言修正，默认直接修订再自检。按商业报告标准判断，保留具体判断和真实不确定性；按密度而非单次关键词识别套话。不编造经历、情绪或作者立场。
4. 回到证据检查：核对数字正负、单位、期间、对象、来源、估计/实际/预测，以及“可能”是否被改成因果或承诺。自动工具不能代替中文语义检查。

声音保护区：用户直接引语、主页原问题及已确认的个人表达。分析师判断可以明确，但只能扎在研究证据中。报告不使用装饰性破折号、不机械排比、不强行加入幽默、语气词或感情色彩。正文交付完整可读的修订版；审校记录留在工作目录，不把诊断模板塞进正文。

路径：

- `/Users/gabrielchen/.codex/skills/writing-analyst-prose/SKILL.md`
- `/Users/gabrielchen/.codex/skills/humanizer/SKILL.md`
- `/Users/gabrielchen/.agents/skills/humanize-ai/SKILL.md`

未要求扩展到其他项目或修改已安装 skill。今后进入该项目先读取本标准和所需 skill。
