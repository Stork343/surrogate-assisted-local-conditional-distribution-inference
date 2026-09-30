# JRSSB 写作风格模型（从 20 篇语料提炼）

日期：2026-09-30。本文件是语料的定性提炼：每个写作场景给出句式模板、语料原句（方括号为 `corpus_manifest.csv` 的编号）与使用要点。量化画像见 `JRSSB_STYLE_PROFILE.md`；本文件回答"怎么写"，画像回答"写多少"。

## 一、开场句式（摘要与引言第一句）

模板：`In many <领域> <applications/settings/studies>, <关键量> is <difficult/expensive/costly> to <observe/collect/verify>, <后果从句>`，随后一句给出本文动作。

语料原句：
- [01] "In many experimental and observational studies, the outcome of interest is often difficult or expensive to observe, reducing effective sample sizes for estimating average treatment effects."
- [02] "In many modern machine learning applications, the outcome is expensive or time-consuming to collect while the predictor information is easy to obtain."
- [06] "In this work, we consider the problem of building distribution-free prediction intervals with finite-sample conditional coverage guarantees."
- [11] "This paper develops novel conformal prediction methods for classification tasks that can automatically adapt to random label contamination."
- [14] "This article addresses the problem of testing the conditional independence..."

要点：情境句给普遍困难，动作句给本文对象；两种顺序都出现，以情境先行更常见。首句不放结论、不放 but 转折。

## 二、贡献句

模板：`In this paper, we <propose/develop/introduce/consider> <对象> for <目的> under <条件>`，或 `We <study/establish/derive> <结果>`，随后一句说明与既有工作的差异。

语料原句：
- [01] "We study how incorporating data on units for which only surrogate outcomes not of primary interest are observed can increase the precision of ATE estimation."
- [01] "We develop robust ATE estimation and inference methods that realize these efficiency gains."
- [03] "In this paper, we propose a two-step SSL procedure for evaluating a prediction rule derived from a working binary regression model based on the Brier score and overall misclassification rate under stratified sampling."
- [04] "We introduce two-phase rejective sampling (TPRS) and explore its asymptotic design properties with commonly-used estimators, namely weighted expansion and regression estimators."
- [04] "We present the first derivation of the asymptotic distribution result under TPRS."
- [20] "We propose statistically optimal adaptive procedures that effectively balance this trade-off between privacy and accuracy."

要点：动词直接给动作（propose、develop、introduce、consider、study、present、establish、derive、quantify）；差异句用 "the first"、"complementing"、"in contrast to" 表达；不写 "we believe"。

## 三、定理的引入与解释

引入模板：
- `<量> 的 <性质> is given in the following theorem.`（[04]）
- `Before stating our main theorem, we define <对象>, which plays an important role in <用途>.`（[19]）
- `With the above preparation, we state our main results concerning <对象>.`（[19]）
- `Our main result, captured in Theorem X, quantifies <量>.`（[20]）
- `Our main result (Theorem X in Section Y) specialises the general setting ... to give <更明确的结果>.`（[05]）

解释模板：
- `Theorem X provides <上界/下界/刻画> for <量> as a function of <变量>.`（[19]）
- `Proposition X guarantees that <性质>.`（[05]）

要点：先备好记号再宣布定理；解释句用 provides、guarantees、characterises、quantifies 一类的实义动词，把定理翻译成一句话的量词化陈述；解释段可放入编号 Remark。

## 四、结果报告句（模拟与应用）

模板：`<Table/Figure> N <verb> <对象> <限定从句>`，动词按用途选择：

- summarize/summarise：整表汇总。[01] "Table 2 summarizes the results of ... from 1000 replications of the experiments, where ..."
- report：单一指标。[01] "Table 2 reports the average length and the coverage frequency of the confidence intervals."
- illustrate：机制或示例。[05] "Figure 3 illustrates the predictive value of our learned embeddings ..."
- show：直接比较。[19] "Fig.3 shows the empirical predictive risk of the target-only estimator, distTL, and angleTL."
- compare：方法间对照。[18] "Figure 2 compares the bounds provided by Theorems 1 and 2 as a function of τ."
- present：陈列性内容。[05] "Figure 6 presents the first 16 images from the MNIST dataset ..."

要点：动词与图形职能对应；报告句之后立刻给一句解读，数字本身由图表承载；不写 "It can be seen that"。

## 五、过渡与引导句

模板与语料原句：
- `In this section, we <review/discuss/state/present> <对象>.` [04] "In this section, we review the existing methods for using auxiliary variables in two-phase sampling to enhance estimation efficiency and identify areas needing new strategies."；[17] "In this section, we discuss the computation for solving the penalized estimating function (6)."
- `In this paper/article, we address this gap in <领域> through <手段>.` [02]
- `We now turn to <下一主题>.` / `The remainder of this paper is organized as follows.`
- 回引：`Recall that <已定义对象>.` / `Note that <需要提醒的性质>.`

要点：每节开头一句，节内小转换用 "We now"；回引只用于定义与关键交叉引用。

## 六、动词与语气词汇表

高频实义动词（20 篇正文合计次数，按频次排序）：
- consider 236、guarantee 158、show 141、construct 131、propose 84、observe 80、compare 67、demonstrate 62、introduce 50、evaluate 46、establish 39、develop 37、derive 33、prove 29、illustrate 29、extend 26、report 21、indicate 19、quantify 18、imply 14、suggest 14、summarize 13、explain 13、characterize 10。
- 方法层用 propose、develop、introduce、construct、consider；理论层用 derive、establish、prove、characterize、quantify、guarantee；证据层用 show、demonstrate、illustrate、observe、report、summarize、compare、evaluate；解释层用 suggest、indicate、imply、explain。
- `guarantee` 在语料中出现 158 次，是这套论文的本土动词；`certify/certificate` 出现零次。

连接与转折：in contrast、however、in fact、note that、recall that、specifically、in particular、together with。

语气参数（画像中位）：`we` 12.9 每千词；情态词 may/might/could/suggest 2.3；论证动词 show/establish/prove 3.3；含否定句 7.1%。解释句用情态，数值结论不用。

## 七、句法节奏与段落构造

- 平均句长中位 31.5 词；典型节奏是长句铺垫加短句收束，句长在 10--40 词间起伏。
- 段落中位 113 词：主题句、支撑（数据、比较、因果）、一句含义或转折；删去只复述本段的收尾句。
- 一段一个任务；新任务换段，配一句引导句。

## 八、可直接套用的句式清单

1. `In many <settings>, <quantity> is <difficult> to <obtain>, <consequence>.`
2. `In this paper, we <propose/develop> <method> for <target> under <conditions>.`
3. `We <study/establish> <result>, and we <develop> <procedure> that <realizes> <gain>.`
4. `Before stating our main theorem, we define <object>, which plays an important role in <role>.`
5. `Our main result, captured in Theorem <N>, quantifies <quantity>.`
6. `Theorem <N> provides <bounds/characterisation> for <quantity> as a function of <variables>.`
7. `Table <N> summarizes <results> from <replications> of the experiments, where <design>.`
8. `Figure <N> illustrates/shows/compares <object>, <qualifier>.`
9. `In this section, we <review/discuss/state> <object>.`
10. `We now turn to <next topic>.`
11. `Recall that <defined object>; <consequence>.`
12. `This <theorem/result> suggests that <interpretation>, which <implication>.`

## 九、语料中未见的形式

以下写法在 20 篇语料中未出现，写作时避免：
- "delve into"、"it is worth noting that"、"needless to say"。
- 摘要以结论或 but 转折开场。
- 定理后立刻接证明而不给一句解释。
- "It can be seen that"、"as we all know"。
- 标题使用 certified/certificate 一类词（语料用 guarantees）。

