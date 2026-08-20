# lvsea-research

> 中文优先的研究、探讨、查证与决策总调度 Skill。它把实时检索、证据账本、前提挑战、时间线/横截面、贝叶斯决策、历史同构和对标分析放进一个可路由、可验证、可继续维护的包。

## 它解决什么问题

研究类请求常见的失败不是“搜得不够多”，而是把简单查证、深度研究、现实决策和历史类比混在一起，最后得到一篇来源不清、结论过强、不能行动的长文。

lvsea-research 的做法是：

- 先判断主任务，再选择一个主路由；
- 先读用户材料，再补实时来源；
- 用来源等级、独立性和反证控制结论强度；
- 严格区分事实、来源解释、推断、假设和未知；
- 只在确有必要时做时间线、竞品、贝叶斯更新或历史案例；
- 先给结论和行动含义，再给证据、限制、下一条信息和复盘条件。

## 安装

~~~bash
npx skills add lhylvsea/lvsea-research --skill lvsea-research
~~~

安装后重启当前 Agent 客户端，然后直接用自然语言触发。

## 你可以这样说

1. 用 $lvsea-research 深度研究膨润土猫砂的工艺路线、成本结构、竞品和工厂落地风险，先给结论，再给来源和验证缺口。
2. 用 $lvsea-research 查证安全生产材料中的数字、法规依据和因果说法，做事实核验表，不要把推测写成事实。
3. 用 $lvsea-research 比较两个设备改造方案，按停机风险、产能、维护、投资回收和可逆试点做决策分析。
4. 用 $lvsea-research 从历史案例研究制造企业如何从老板亲自交付转向流程化管理，同时找失败案例和不能照搬的条件。

## 路由总览

| 路由 | 适合什么 | 主要交付 |
| --- | --- | --- |
| fast-retrieval | 一个事实、URL、定义或当前状态 | 结论与直接来源 |
| fact-check | 数字、日期、因果、法规和真假核验 | 事实核验表 |
| deep-research | 产品、公司、技术、政策或概念的系统研究 | 研究报告/备忘录 |
| timeline-cross-section | 发展历程与当下比较需要交叉解释 | 时间线、比较、交汇洞察 |
| decision-analysis | 是否做、选哪个、先试什么 | 决策报告、阈值和试验 |
| problem-diagnosis | 问题混乱、术语模糊、前提可能错误 | 问题重述、诊断和缺口 |
| benchmark-comparison | 对标、竞品、方案和机制比较 | 矩阵、价值链和迁移边界 |
| historical-analogy | 找历史案例和带条件的标准答案 | 结构指纹、案例和机制 |

## 默认工作流

1. 明确研究问题、范围、用途和交付格式。
2. 建立查询矩阵：定义、机制、当前状态、替代、反证和一手来源。
3. 按环境选择 AnySearch、多引擎、宿主 Web/浏览器或本地文件；记录真实调用与降级。
4. 建立证据账本：来源、日期、等级、独立性、支持关系和局限。
5. 按路由执行分析，避免所有请求都强行长报告。
6. 先给结论，再给证据、推导、反证、未知项和下一步。
7. 交付前检查链接、数字、单位、事实/推断边界、风险和未验证项。

## 运行与验证

在仓库根目录执行：

~~~bash
python scripts/validate_package.py .
python scripts/route_eval.py . --cases evals/route_cases.json --output reports/route-eval.json
python scripts/trigger_eval.py . --cases evals/trigger_cases.json --output reports/trigger-eval.json
python scripts/export_skill_ir.py . --output reports/skill-ir.json
python scripts/context_sizer.py . --output reports/context-budget.json
python scripts/release_check.py . --phase local --run-tests
~~~

Windows PowerShell 可使用 py 替换 python。这些命令验证包结构、触发/路由边界、IR、上下文预算和本地测试；它们不能代替真实来源调用或人工评审。

## 前置条件

- Python 3.9+ 用于本包验证脚本；
- 真实研究需要宿主 Web/浏览器能力，或安装并配置一个可用的检索 provider；
- AnySearch 可匿名使用但有配额/速率限制，API Key 由用户自行配置，不能写入仓库；
- 不需要为了安装本 Skill 自动安装第三方 MCP、浏览器或搜索 API。

## 注意事项、限制与能力边界

- 研究结论只对注明的时间、地域、样本和来源范围负责；动态事实需要重新核验。
- 搜索结果摘要、Stars、下载量、第三方评分不能证明事实或输出质量。
- 没有可靠基准或似然比时，不输出伪精确概率；高风险领域只做决策支持。
- 对标用于理解机制和边界，不鼓励复制商业秘密、受限素材、品牌或侵权内容。
- 用户未授权外部写入时，所有网络、GitHub、文件和账户操作保持只读。
- 静态验证通过不等于 provider 已调用；报告会单独标记 provider 或人工证据状态。

## 故障排查

- 路由结果不符合预期：先运行 python scripts/route_request.py --text "..." --json，检查关键词与显式路由，再修正 references/route-playbook.md 或增加评测用例。
- 触发过宽：把“只解释、翻译、只摘要、只查看、不要查资料”等负例补进 evals/trigger_cases.json。
- provider 不可用：保留来源计划，切换宿主 Web/浏览器或本地文件，并在交付中写明降级。
- 研究内容过长：降低深度为 standard，先交付结论、证据表和缺口，不为字数堆材料。

## 许可证与研究来源

本包原创内容使用 MIT。上游方法与许可证边界见 THIRD_PARTY_NOTICES.md；研究账本见 reports/prior-art-research.md。其中 dbskill 为 CC BY-NC 4.0，本仓库未打包其受限原文、案例或代码。
