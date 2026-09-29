# JRSSB 写作交接说明（writing_v4）

更新日期：2026-09-29。本页给协助改写正文的外部助手阅读。

## 目录定位

- `paper/` 是 `JRSSB_revision_v3/paper/` 的工作稿副本，本轮已完成一次凝练；`figures/` 与 V3 相同。
- 权威数值、逐次结果、代码与审计记录在作者本地的 `JRSSB_revision_v3` 包中，没有进入本仓库。本目录只改文字、结构与图表位置，数值一律不得改动。
- V3 交付包（34 页、七图）仍是正式版本；这里的 `paper/` 是下一版正文的草稿。

## 本轮已完成的改动

1. 引言重写：文献按主题归成两段，每段以缺口收尾；贡献集中一段；结构导引压成一句。
2. 理论节：五个定理与一个命题的陈述一字未动，删减了定理后的重复评注，把否定式免责句改成正面陈述。
3. 模拟：7 个小节归并为 4 个；词数 1,476 到 1,177。
4. 应用：6 个小节归并为 4 个；原第六幅图（单个掩码的区间示例）移入补充材料 S6，成为 Figure S1，正文改为引用 Supplementary Figure S1。
5. 讨论：删去重复限定句；数据可用性、基金、AI 披露、利益冲突与补充材料声明全部保留。
6. 三张表在表内改为单倍行距（`\setstretch{1.0}`），表中数值与 V3 逐项一致。
7. `02_method.tex` 与 `manuscript.tex` 未改动。

## 度量基线

| 指标 | V3 | 本轮 |
|---|---|---|
| 正文页数 | 34 | 30 |
| 正文词数（References 之前） | 6,687 | 5,879 |
| 正文图数 | 7 | 6 |
| 模拟小节 | 7 | 4 |
| 应用小节 | 6 | 4 |
| 含否定的句子 | 39/402（10%） | 16/271（6%） |
| 摘要词数 | 157 | 157 |

补充材料现为 53 页（V3 为 52 页，吸收了移入的 Figure S1）。

## 待办

1. 正文 30 页，期刊目标是低于 30；再删约 250 个词，或把一项展示内容（例如表 2 的完整框架描述、或一幅图）移入补充材料，可以到 29 页。
2. `02_method.tex`（463 词配 11 个独立公式）与摘要尚未做语言层凝练。
3. 定稿后把 `paper/` 移回 `JRSSB_revision_v3`，同步更新 `claim_code_map.csv`、`修改与验收记录_V3.md`、`README.md`、`FILE_INVENTORY.csv`，并重跑 `release_audit_v3.py`。小节编号变了，`claim_code_map.csv` 里的"Section 4.4""Section 5.6"等对应关系需要重写。

## 改写规则

### 立场
- 直接陈述结论。必要的适用范围与限制写一次，放在定理后的解释段或限制小节。
- 用正面范围替代否定式免责："本分析覆盖……"。避免"我们并不声称……"。
- 避免 `not X but Y`、`rather than`、`to be clear`、`it should be noted that`，除非对比本身是论证的一部分。
- 段落一个主题句加支撑；删去只复述本段的收尾句。

### 句法（英文）
- 句长目标 10--30 词；超过 30 词拆分。每句一个核心命题。
- 不用破折号连接句子，用逗号、括号或拆句。
- 结果段报告"发生了什么"，解释放到讨论；两边的句式不要混。

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
| `paper/01_introduction.tex` | 引言 | 本轮重写 |
| `paper/02_method.tex` | 方法与算法 | 未改，可继续凝练 |
| `paper/03_theory.tex` | 定理与解释 | 评注已删减 |
| `paper/04_simulation.tex` | 模拟 | 7 小节并成 4 |
| `paper/05_application.tex` | EPA 应用 | 6 小节并成 4 |
| `paper/06_discussion.tex` | 讨论与声明 | 已删减 |
| `paper/tables_and_figures.tex` | 三张表 | 表内改单倍行距 |
| `paper/results_macros.tex` | 数值宏 | 勿改 |
| `paper/S6_design.tex` | 补充材料 S6 | 末尾新增 Figure S1 |
| 其余 `paper/S*.tex` | 补充材料各节 | 未改 |

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
