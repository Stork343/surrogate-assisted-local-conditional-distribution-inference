# JRSSB 写作交接说明（writing_v4）

更新日期：2026-09-30。本页给协助改写正文的外部助手阅读。

## 目录定位

- `paper/` 是 `JRSSB_revision_v3/paper/` 的工作稿副本，已完成两轮凝练；`figures/` 与 V3 相同。
- 权威数值、逐次结果、代码与审计记录在作者本地的 `JRSSB_revision_v3` 包中，没有进入本仓库。本目录只改文字、结构与图表位置，数值一律不得改动。
- V3 交付包（34 页、七图）仍是正式版本；`JRSSB/submission_v5/` 是协作方发布的 V5 快照（29 页），不含本目录后续编辑。

## 必读材料

- `style_findings.md`：20 篇 Series B 样本的共性分析，覆盖正文规模、引言、参考文献、措辞语气、标题、章节骨架、叙事逻辑、绘图、表格、编号假设、算法框，以及追加的读者引导句、note/recall、Remark、limitation、证明组织等维度，含行动清单。
- 本页其余部分是状态、规则与文件地图。

## 已完成的改动

第一轮（结构）：引言重写、理论评注删减、模拟 7 并 4 小节、应用 6 并 4 小节、原第六图移入补充材料、讨论删减、表格改单倍行距。

第二轮（按 12 篇样本）：模拟与应用短段合并；语态转换使 `we` 密度从 2.2 提高到 4.2 每千词。

第三轮（样本扩到 20 篇）：样本库扩到 20 篇，深度度量新增引言规模、参考文献规模、编号假设、算法框、摘要开场。

第四轮（追加维度）：度量读者引导句、note/recall 提醒、编号 Remark、定理命名、limitation 表述、证明组织；结论并入 `style_findings.md`。

`02_method.tex` 与 `manuscript.tex` 未改动。

## 度量基线（20 篇样本对照）

| 指标 | V3 | 当前 | 样本中位 |
|---|---|---|---|
| 正文页数 | 34 | 30 | - |
| 正文词数 | 6,687 | 5,910 | 11,682（同口径 6,593） |
| 引言词数 | - | 586 | 1,524 |
| 引言占正文 | - | 8.9% | 14% |
| 参考文献条数 | 27 | 27 | 46 |
| 正文图数 | 7 | 6 | 8 |
| 正文表数 | 3 | 3 | 1 |
| `we` 密度（每千词） | 2.2 | 4.2 | 12.9 |
| 情态词密度（每千词） | 0.3 | 0.3 | 2.3 |
| 摘要词数 | 157 | 157 | 191 |
| 编号假设 | 0 | 0 | 16/20 篇有 |
| 算法框 | 0 | 0 | 10/20 篇有 |
| 引导句 | - | 0 | 9.5 处 |
| `note that / recall that` | - | 0 | 8.5 处 |
| 编号 Remark | - | 0 | 11/20 篇有 |

## 待办（按差距大小排列）

1. 参考文献从 27 条扩到 45--60 条，集中在引言与相关工作；只加真实可核对的条目，新条目先经作者确认。
2. 引言从 586 词扩到 1,100--1,500 词：情境段加长、文献分三组、贡献句保持显式。
3. 语态继续转换，`we` 密度从 4.2 提到 8--12 每千词。
4. 加引导句 6--10 处（In this section / We now / The remainder），放在每节首段与理论节各小节开头。
5. 把 3.2 节的条件段落改成编号的 Assumption 1--5。
6. 恢复 `note that / recall that` 4--6 处，用于定义回引与定理适用范围；`it should be noted` 继续排除。
7. 情态词恢复到 1--2 每千词，只用于解释句。
8. 摘要开场改为情境句。
9. 为配对选择器补 Algorithm 伪代码框。
10. 定理后的解释段改为编号 Remark。
11. 讨论加一句显式 limitation。
12. 页数：扩引言与文献约需 2--2.5 页，需同步压缩 04/05 或移表入补充材料，或者接受 31--32 页；由作者裁决。
13. 定稿后把 `paper/` 移回 `JRSSB_revision_v3`，同步更新 `claim_code_map.csv`、`修改与验收记录_V3.md`、`README.md`、`FILE_INVENTORY.csv`，并重跑 `release_audit_v3.py`。
14. 标题用词：样本用 `guarantees`，`certified` 不在样本词汇内；是否改动由作者决定。

## 改写规则

### 立场
- 直接陈述结论。必要的适用范围与限制写一次，放在定理后的解释段或限制小节。
- 用正面范围替代否定式免责；避免 `not X but Y`、`rather than`、`to be clear`、`it should be noted that`，除非对比本身是论证的一部分。
- 段落一个主题句加支撑；删去只复述本段的收尾句。

### 句法（英文）
- 句长目标 10--30 词；超过 30 词拆分。每句一个核心命题。
- 不用破折号连接句子，用逗号、括号或拆句。
- 结果段报告"发生了什么"，解释放到讨论。

### 语气
- 经验与设定句用 `we` 主语：`We separate`、`We generate`、`We draw`、`We model`。定义与公式陈述可以保留非人称形式。
- 解释句允许 `may reflect`、`could indicate` 一类的适度情态；数值结论不加情态。
- 摘要以情境句开场，再给缺口与贡献。
- 每节开头用一句引导句告诉读者本节做什么；回引定义时用 `recall that` 或 `note that`。

### 术语
- 一人一名：Paired、Anchor、Full、Trace、Plug-in、Projection、Unpaired、gate、evaluation、audit frame 全文统一，不为行文变化引入同义词。
- 缩略语首次出现给全称；EPA、CDF、RH 这类尚未定义的缩略语补上首次定义。

### 数值
- 正文、表格、`results_macros.tex` 的数值不得改动，也不得新增。需要核对时向作者索取 `results` 摘要。
- 新增参考文献必须真实可核对；不得生成条目。
- 改动后必须重新编译，并核对页数与无未定义引用。

## JRSSB 硬性要求（来自官方 Instructions to Authors）

- 正文 12pt、双倍行距（每页 28 行）、A4；含附录、参考文献、表格与图在内低于 30 页，超过约 35 页会在初审招致负面评审。
- 摘要不超过 200 词；五到六个关键词按字母序；摘要内不用引文与缩略语。
- 英式拼写。
- 定理按类型顺序编号（theorem 1, 2, ...；proposition 1, ...）。
- 表格放正文末尾；无竖线、表身内无横线；数字右对齐。
- 图题与图例写在正文文件内；每幅图单独文件；多面板合并为一个文件；面板左上角标 A、B、C。
- 图例正下方写一行 `Alt text: ...`，这是期刊的强制要求，且不会进入排版版。
- 补充材料单独在线发布，每份不超过 2MB，正文必须引用；数据不放进补充材料。
- 数据可用性声明作为独立小节放在致谢之前；录用前代码须有 DOI，并在正文与参考文献中给出。
- 投稿系统 ScholarOne；单盲评审，正文可含作者信息。

## 文件地图

| 文件 | 内容 | 状态 |
|---|---|---|
| `paper/manuscript.tex` | 主文件 | 未改 |
| `paper/01_introduction.tex` | 引言 | 重写并转语态，待扩写 |
| `paper/02_method.tex` | 方法与算法 | 未改，待语态转换与算法框 |
| `paper/03_theory.tex` | 定理与解释 | 评注已删减，待编号假设与 Remark |
| `paper/04_simulation.tex` | 模拟 | 4 小节，并段并转语态 |
| `paper/05_application.tex` | EPA 应用 | 4 小节，并段并转语态 |
| `paper/06_discussion.tex` | 讨论与声明 | 已删减，待 limitation 句 |
| `paper/tables_and_figures.tex` | 三张表 | 表内改单倍行距 |
| `paper/results_macros.tex` | 数值宏 | 勿改 |
| `paper/S6_design.tex` | 补充材料 S6 | 末尾新增 Figure S1 |
| 其余 `paper/S*.tex` | 补充材料各节 | 未改 |
| `style_findings.md` | 20 篇样本共性分析 | 必读 |

正文在用的图：`figure_separation_v2`、`figure_simulation_v2`、`figure_validation_v3`、`figure_binary_v2`、`figure_epa_science_v2`、`figure_epa_budget_v3`。`figure_epa_budget_v2.tex` 沿自 V3，未被引用。

## 编译

在 `paper/` 内执行：

```sh
pdflatex -interaction=nonstopmode manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode manuscript.tex
pdflatex -interaction=nonstopmode manuscript.tex
```

补充材料同理，编译对象换成 `supplement.tex`。图形路径为 `../figures/`。当前基线：正文 30 页，补充材料 53 页，均无溢出框、无未定义引用。
