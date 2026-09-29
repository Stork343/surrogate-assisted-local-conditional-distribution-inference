# 样本共性分析（12 篇 Series B）

度量对象：`../writing_samples/` 的 12 篇 arXiv 版，正文截到 References 之前；对照对象为本稿 `paper/manuscript.pdf`。度量脚本为 PDF 文本提取，图表说明与小节标题的识别有少量噪声，结论以可核对的数字为准。

## 一、措辞语气与文字风格（差距最大）

- 第一人称密度：样本 `we` 每千词 6.8--20.7，中位约 14，占全文词数约 1.4\%；本稿每千词 2.2，全文 10 处，`our` 为 0。
- 样本句式以 `we propose / we consider / we show / we now / our method` 为主；本稿以 `The experiments separate / The target is / Table X reports` 的非人称句为主。
- 情态词：样本 `may / might / could / suggest` 每千词 0.8--4.6，中位约 2.6；本稿 0.3。
- 论证动词：样本 `show / establish / prove / demonstrate / guarantee` 每千词 0.8--8.6，中位约 4.4；本稿 2.2。
- 判断：本稿的语态与期刊常态偏离最大。Series B 的语气是"人称加适度情态"，本稿是"非人称加绝对语气"。
- 行动：把经验部分的非人称句改成 `we` 主语，解释句恢复适度情态词；目标 `we` 密度 8--12 每千词，情态词 1--2 每千词。

## 二、标题组织形式

- 词数：样本 5--15 词，中位 9--10；本稿 9 词，在范围内。
- 冒号副标题：12 篇中 4 篇使用，副标题陈述性质或保证，如 `randomization enables robust guarantees`、`Prediction, Estimation, and Minimax Optimality`。
- 用词：样本标题出现 `guarantees` 两次、`efficient / efficiency` 三次；`certified / certificate` 出现零次。本稿 `certified simultaneous gains` 在样本词汇之外，`guaranteed` 更接近期刊习惯。
- 行动：是否把 certified 改为 guaranteed 属于全文术语级改动，由作者决定；若改用冒号副标题，副标题应陈述保证本身。

## 三、章节骨架

样本骨架：Introduction → 问题设定或方法 → 理论 → 数值研究 → 真实数据 → Discussion。数值节的命名包括 `Numerical Studies`、`Simulation Studies`、`Simulations`、`Experiments`、`Empirical studies`；应用节以数据域命名，如 `Application to EMR Studies`、`Example: EHR Study of Diabetic Neuropathy`、`Application example: biological high-throughput data`。

本稿骨架与之一致；应用节以科学问题命名，属于可接受的变体。无需改动。

## 四、叙事逻辑

- 引言开场：至少 6 篇以 `In many ... the outcome is expensive or difficult to observe` 一类的普遍情境开场，随后立刻给出本文动作 `we propose / we consider / we develop`。
- 贡献句用显式的 `We propose / We develop` 陈述，随后一段给出理论结果的白话含义，再给数值与真实数据。
- 方法论文普遍带 Algorithm 伪代码框：Gibbs 等、Jin 与 Ren、Sesia 等、Ignatiadis 与 Huber 都有；本稿的配对选择器只有公式与文字，没有算法框。
- 定理后的解释段：样本更短，且允许 `may reflect / could indicate` 一类的情态。
- 行动：为配对选择器补一个 Algorithm 伪代码框，放在 02 节规则之后；引言的贡献段改成 `We` 主语。

## 五、绘图形式

- 每篇正文图数 0--20，中位约 7--9；本稿 6 幅，在范围内。
- 图注词数：样本中位约 50，区间 14--107；本稿含 Alt text 行约 73 词。去掉 Alt text 行后接近样本中位。
- 面板标注：样本图注普遍以小写 (a)(b)(c) 引用面板；期刊要求面板左上角标 A、B、C。本稿的图注用 (A)(B)，绘图代码把字母画在坐标区上沿左端，需要确认是否移到面板内部左上角。
- 常见图型：覆盖率或功效随样本量变化的曲线、方法间的宽度对比、示例区间图；本稿的图形类型与之一致。
- 行动：压缩图注里的结论性句子，保留 Alt text 行；核对面板角标位置。

## 六、表格表达

- 样本正文表格数 0--3，中位 0--1；有 3 篇各带 3 张表。本稿 3 张表，在观察范围内。
- 表注词数：样本约 33--61；本稿 30--60，接近。
- 样本更多把方法对比交给图形；本稿的 Table 3（覆盖与宽度）是候选的图化对象，同时可以省页数。
- 行动：保持三张表；若需要再省一页，把 Table 3 改为双子图的对比图，或将其移入补充材料。

## 汇总：按优先级排列的可执行改动

1. 人称与语态：经验部分改 `we` 主语，目标密度 8--12 每千词。
2. 情态词：解释句恢复 `may / could / suggest`，目标 1--2 每千词。
3. 算法框：为配对选择器补 Algorithm 伪代码框。
4. 图注：结论句压缩到样本中位长度，Alt text 行保留。
5. 标题与术语：certified 与 guaranteed 的取舍由作者决定，改动需全文同步。
