# JRSSB 写作交接说明（writing_v4）

更新日期：2026-09-29。本页给协助改写正文的外部助手阅读。

## 目录定位

- `paper/` 是 `JRSSB_revision_v3/paper/` 的工作稿副本，已完成两轮凝练；`figures/` 与 V3 相同。
- 权威数值、逐次结果、代码与审计记录在作者本地的 `JRSSB_revision_v3` 包中，没有进入本仓库。本目录只改文字、结构与图表位置，数值一律不得改动。
- V3 交付包（34 页、七图）仍是正式版本；这里的 `paper/` 是下一版正文的草稿。

## 必读材料

- `style_findings.md`：12 篇 Series B 样本的共性分析，含措辞语气、标题、章节骨架、叙事逻辑、绘图、表格六个维度的对照数字与可执行改动。
- 本页其余部分是状态、规则与文件地图。

## 已完成的改动

第一轮（结构）：
1. 引言重写：文献按主题归成两段，每段以缺口收尾；贡献集中一段；结构导引压成一句。
2. 理论节：五个定理与一个命题的陈述一字未动，删减了定理后的重复评注，把否定式免责句改成正面陈述。
3. 模拟：7 个小节归并为 4 个。
4. 应用：6 个小节归并为 4 个；原第六幅图移入补充材料 S6，成为 Figure S1。
5. 讨论：删去重复限定句；声明部分全部保留。
6. 三张表在表内改为单倍行距，数值与 V3 逐项一致。

第二轮（按样本对照）：
7. 模拟与应用的短段合并：04 每段约 106 词，05 每段约 117 词，接近样本中位 113。
8. 语态转换：引言、模拟、应用改为 we 主语，`we` 密度从 2.2 提高到 4.7 每千词。

`02_method.tex` 与 `manuscript.tex` 未改动。

## 度量基线

| 指标 | V3 | 当前 | 样本中位 |
|---|---|---|---|
| 正文页数 | 34 | 30 | - |
| 正文词数（References 之前） | 6,687 | 5,910 | 10,431 |
| 正文图数 | 7 | 6 | 约 7--9 |
| 模拟小节 | 7 | 4 | - |
| 应用小节 | 6 | 4 | - |
| 含否定的句子 | 10% | 6% | 7.1% |
| 每段词数 | 76 | 约 105 | 113 |
| `we` 密度（每千词） | 2.2 | 4.7 | 约 14 |
| 情态词密度（每千词） | 0.3 | 0.3 | 约 2.6 |
| 摘要词数 | 157 | 157 | - |

补充材料现为 53 页（吸收 Figure S1）。

## 待办

1. 语态：`we` 密度从 4.7 提高到 8--12 每千词。优先转换 02 与 03 的非人称句（`Write ...`、`A second sample estimates ...`、`Consider ...`），再补 04/05 的报告句。
2. 情态词：解释句恢复 `may / could / suggest`，目标 1--2 每千词；样本的解释段允许适度情态。
3. 算法框：为配对选择器补一个 Algorithm 伪代码框，放在 02 节规则之后；样本中的方法论文普遍带算法框。
4. 图注：把结论性句子压缩到样本中位长度（约 50 词），Alt text 行保留。
5. 页数：从 30 降到 29。候选做法是把表 3 图化或移入补充材料，或把表 2 的完整框架描述移入补充材料；由作者确认后执行。
6. 摘要与 `02_method.tex` 的语言层凝练。
7. 定稿后把 `paper/` 移回 `JRSSB_revision_v3`，同步更新 `claim_code_map.csv`、`修改与验收记录_V3.md`、`README.md`、`FILE_INVENTORY.csv`，并重跑 `release_audit_v3.py`；小节编号变了，对应关系需要重写。
8. 标题用词：样本标题使用 `guarantees`，`certified` 不在样本词汇内；是否改为 `guaranteed` 由作者决定，属于全文术语级改动。

## 改写规则

### 立场
- 直接陈述结论。必要的适用范围与限制写一次，放在定理后的解释段或限制小节。
- 用正面范围替代否定式免责；避免 `not X but Y`、`rather than`、`to be clear`、`it should be noted that`，除非对比本身是论证的一部分。
- 段落一个主题句加支撑；删去只复述本段的收尾句。

### 句法（英文）
- 句长目标 10--30 词；超过 30 词拆分。每句一个核心命题。
- 不用破折号连接句子，用逗号、括号或拆句。
- 结果段报告"发生了什么"，解释放到讨论；两边的句式不要混。

### 语气
- 经验与设定句用 `we` 主语：`We separate`、`We generate`、`We draw`、`We model`。定义与公式陈述可以保留非人称形式。
- 解释句允许 `may reflect`、`could indicate` 一类的适度情态；数值结论不加情态。

### 术语
- 一人一名：Paired、Anchor、Full、Trace、Plug-in、Projection、Unpaired、gate、evaluation、audit frame 全文统一，不为行文变化引入同义词。
- 缩略语首次出现给全称；EPA、CDF、RH 这类尚未定义的缩略语补上首次定义。

### 数值
- 正文、表格、`results_macros.tex` 的数值不得改动，也不得新增。需要核对时向作者索取 `results` 摘要。
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
| `paper/01_introduction.tex` | 引言 | 重写并转语态 |
| `paper/02_method.tex` | 方法与算法 | 未改，待语态转换与算法框 |
| `paper/03_theory.tex` | 定理与解释 | 评注已删减，待语态转换 |
| `paper/04_simulation.tex` | 模拟 | 4 小节，并段并转语态 |
| `paper/05_application.tex` | EPA 应用 | 4 小节，并段并转语态 |
| `paper/06_discussion.tex` | 讨论与声明 | 已删减 |
| `paper/tables_and_figures.tex` | 三张表 | 表内改单倍行距 |
| `paper/results_macros.tex` | 数值宏 | 勿改 |
| `paper/S6_design.tex` | 补充材料 S6 | 末尾新增 Figure S1 |
| 其余 `paper/S*.tex` | 补充材料各节 | 未改 |
| `style_findings.md` | 样本共性分析 | 必读 |

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
