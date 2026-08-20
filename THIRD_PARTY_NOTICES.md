# 第三方方法与许可证边界

本仓库是原创的研究路由和证据工作流实现。它没有打包上游仓库的代码、案例、模板、图片或逐段文字；以下记录仅说明研究来源和方法启发。

| 来源 | 本次检查的内容 | 许可证/边界 | 处理方式 |
| --- | --- | --- | --- |
| [anysearch-skill](https://github.com/anysearch-ai/anysearch-skill) | 实时检索、垂直子域、批量搜索、全文提取、运行时降级 | Apache-2.0，含 NOTICE | 只吸收工具选择原则，不复制 CLI 或服务代码 |
| [yao-bayesian-skill](https://github.com/yaojingang/yao-open-skills/tree/main/skills/yao-bayesian-skill) | 决策简报、证据分级、更新、敏感性、行动阈值、多轮日志 | MIT | 重新表述为本包的通用决策模块，不复制源文件 |
| [hv-analysis](https://github.com/KKKKhazix/khazix-skills/blob/main/hv-analysis/SKILL.md) | 纵向时间轴、横向截面、交汇洞察、情景推演 | MIT | 只采用抽象分析结构，按本包路由重写 |
| [multi-search-engine](https://github.com/openclaw/skills/tree/main/skills/gpyangyoujun/multi-search-engine) | 用户指定的多引擎搜索来源 | 2026-08-20 直接仓库与 raw 路径均未能取到，见研究报告 | 不复制；仅把“来源多样性、地区/语言/时间对照”作为待验证设计线索 |
| [dbskill](https://github.com/dontbesilent2025/dbskill) | 问题消解、对标过滤、历史同构、成功/失败/反例比较的高层研究启发 | CC BY-NC 4.0 | 不复制其原文、案例、代码或专有表达；本包只保留独立、通用的研究问题结构，并保留来源致谢 |

此外，Skill 封装流程参考本机 [lvsea-zao-skill](https://github.com/lhylvsea/lvsea-zao-skill) 及其上游方法来源 [qiaomu-meta-skill](https://github.com/joeseesun/qiaomu-meta-skill) 和 [yao-meta-skill](https://github.com/yaojingang/yao-meta-skill)。本包采用语义吸收策略，不是上游镜像。
