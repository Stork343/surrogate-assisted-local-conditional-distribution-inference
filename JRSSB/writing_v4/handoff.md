# JRSSB 写作交接说明（writing_v4）

更新日期：2026-09-30，语料蒸馏与第一轮修订后。本页给协助改写正文的外部助手阅读。

## 目录定位

- `paper/` 是 `JRSSB_revision_v3/paper/` 的工作稿副本；`figures/` 与 V3 相同。
- 权威数值、逐次结果、代码与审计记录在作者本地的 `JRSSB_revision_v3` 包中。本目录只改文字、结构与图表归属，数值一律不得改动。
- V3 交付包仍是正式版本；`JRSSB/submission_v5/` 是协作方发布的 V5 快照（29 页），不含本目录后续编辑。

## 必读材料

- `output/`：语料蒸馏与审计交付物。`JRSSB_STYLE_PROFILE.md` 是 20 篇样本的画像，`JRSSB_STYLE_RULES.yaml` 是机器可读规则，`MANUSCRIPT_JRSSB_AUDIT.md` 是修订后的逐项审计，`REVISION_PLAN.md` 是剩余工作清单。
- `output/JRSSB_STYLE_MODEL.md`：语料定性提炼的写作风格模型，含开场、贡献、定理引入与解释、结果报告、过渡、动词表与可套用句式。
- `style_findings.md`：样本共性与维度分析的叙述版。
- 本页其余部分是状态、规则与文件地图。

## 已完成的改动

第一轮（结构）：引言重写、理论评注删减、模拟 7 并 4 小节、应用 6 并 4 小节、原第六图移入补充材料、讨论删减、表格改单倍行距。

第二轮（12 篇样本）：短段合并；`we` 密度 2.2 到 4.2。

第三轮（20 篇样本）：语料扩容与深度度量，产出画像与规则。

第四轮（追加维度）：引导句、note/recall、Remark、limitation、证明组织。

第五轮（语料蒸馏后修订，2026-09-30）：
1. 参考文献从 27 条扩到 50 条；新增 19 条为语料库双核对条目，其余来自原 bib 的真实条目；提交版删除 `doi` 字段（官方允许任意可读格式）。
2. 引言从 586 词扩到 897 词，文献分四组，每段以缺口收尾。
3. 3.2 节条件改为 Assumption 1--5。
4. 新增 Remark 1--3。
5. 02 节新增 Algorithm 1 伪代码框（procedurebox，无新宏包）。
6. `eq:identity` 移入补充材料 S3，02 节公式从 11 条降到 9 条。
7. 表 3 移入补充材料成为 Table S5，正文保留两张表，内部横线改为空行。
8. 摘要改为情境句开场。
9. 引导句 5 处、`note that / recall that` 4 处、情态词 1.1 每千词、显式 limitation 一句。
10. `we` 密度 4.2 到 6.7。
11. 正文 34 页，补充材料 54 页，均无溢出框与未定义引用。

## 度量基线（20 篇样本对照，修订后）

| 指标 | V3 | 当前 | 样本中位 |
|---|---|---|---|
| 正文页数 | 34 | 34 | - |
| 正文词数 | 6,687 | 6,583 | 11,682 |
| 引言词数 | - | 897 | 1,524 |
| 参考文献条数 | 27 | 50 | 46 |
| 正文图数 | 7 | 6 | 8 |
| 正文表数 | 3 | 2 | 1 |
| `we` 密度（每千词） | 2.2 | 6.7 | 12.9 |
| 情态词密度（每千词） | 0.3 | 1.1 | 2.3 |
| 引导句 | 0 | 5 | 9.5 处 |
| `note that / recall that` | 0 | 4 | 8.5 处 |
| 编号假设 | 0 | 5 | 16/20 篇有 |
| 编号 Remark | 0 | 3 | 11/20 篇有 |
| 算法框 | 0 | 1 | 10/20 篇有 |
| 希腊字母种类 | 16 | 15 | 10.5 |
| 编号公式条数 | 25 | 23 | 20 |
| 摘要词数 | 157 | 159 | 191 |

## 待办

1. R06：把绘图代码的面板字母从坐标区上沿移到面板内部左上角，重新生成六幅图（官方合规项）。
2. R02/R03/R04 收尾：引言再扩约 200 词、`we` 再加约 10 处、引导句再加 1--2 处，或接受当前值。
3. R14：把式 (11) 的卡方记号与 $\mathcal K_{\kappa,B}$ 并入文字，希腊字母降到 14 种。
4. R17：标题用词 certified 对 guarantees，由作者裁决。
5. R12 的最终确认：正文 34 页（语料一致性优先的默认）；如需回到 30 页，删约 1,200 词或再移展示项。
6. R18：定稿后同步 V3 包记录并重跑 `release_audit_v3.py`。

## 改写规则

### 立场
- 直接陈述结论。必要的适用范围与限制写一次，放在定理后的 Remark 或限制小节。
- 用正面范围替代否定式免责；避免 `not X but Y`、`rather than`、`to be clear`、`it should be noted that`。

### 句法（英文）
- 句长目标 10--30 词；超过 30 词拆分。每句一个核心命题。
- 不用破折号连接句子。
- 结果段报告"发生了什么"，解释放到讨论。

### 语气
- 经验与设定句用 `we` 主语；定义与公式陈述可保留非人称形式。
- 解释句允许 `may reflect`、`could indicate`；数值结论不加情态。
- 摘要以情境句开场。每节开头用一句引导句；回引定义用 `recall that` 或 `note that`。

### 记号
- 运算符用简写：`E`、`Var`、`Cov`、`argmin`、`tr`。
- 帽子只标估计量，同一字母的装饰族只在定义处出现，后文用 `c(λ)` 与 `g(λ)`。
- 不引入新的希腊字母；需要新记号时优先复用已有字母加下标。

### 术语与数值
- 一人一名：Paired、Anchor、Full、Trace、Plug-in、Projection、Unpaired、gate、evaluation、audit frame 全文统一。
- 缩略语首次出现给全称。
- 正文、表格、`results_macros.tex` 的数值不得改动，也不得新增；新增参考文献必须真实可核对。
- 改动后必须重新编译，核对页数与无未定义引用。

## JRSSB 硬性要求（摘要）

正文 12pt 双倍行距 A4，含全部内容低于 30 页、超过约 35 页招致负面评审；摘要不超过 200 词；英式拼写；定理按类型编号；表格无竖线与内部横线；图例正下方 `Alt text:`；补充材料每份不超过 2MB 且正文引用；数据可用性在致谢之前；录用前代码须有 DOI；单盲评审。

## 文件地图

| 文件 | 内容 | 状态 |
|---|---|---|
| `paper/manuscript.tex` | 主文件 | 摘要开场已改 |
| `paper/01_introduction.tex` | 引言 | 897 词，四组文献 |
| `paper/02_method.tex` | 方法与算法 | 语态、算法框、公式说明句 |
| `paper/03_theory.tex` | 定理与解释 | Assumption 1--5、Remark 1--3 |
| `paper/04_simulation.tex` | 模拟 | 4 小节 |
| `paper/05_application.tex` | EPA 应用 | 4 小节 |
| `paper/06_discussion.tex` | 讨论与声明 | 含 limitation 句 |
| `paper/tables_and_figures.tex` | 两张表 | 表 3 已移入补充材料 |
| `paper/S3_feasible.tex` | 补充材料 S3 | 收纳 eq:identity |
| `paper/S10_results.tex` | 补充材料 S10 | 收纳 Table S5 |
| `paper/references.bib` | 参考文献 | 59 条，提交版无 doi 字段 |
| `paper/results_macros.tex` | 数值宏 | 勿改 |
| `output/` | 语料交付物与审计 | 必读 |

正文在用的图：`figure_separation_v2`、`figure_simulation_v2`、`figure_validation_v3`、`figure_binary_v2`、`figure_epa_science_v2`、`figure_epa_budget_v3`。

## 编译

在 `paper/` 内执行 pdflatex、bibtex、pdflatex ×2（manuscript 与 supplement）。图形路径 `../figures/`。当前基线：正文 34 页，补充材料 54 页，均无溢出框、无未定义引用。

