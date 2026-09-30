# Corpus Quality Report

日期：2026-09-30。对象：`JRSSB/writing_samples/` 下的 20 篇 JRSSB 论文。

## 语料规模与来源

- 20 篇，全部为 JRSSB Series B 正式刊出论文（或在线优先版）。
- 每篇经 Crossref 核对期刊、卷期、页码与 DOI，经 arXiv 接口核对编号与题名，下载文件首页题名与刊出题名一致。
- 01--12 于 2026-09-29 取得，13--20 于 2026-09-30 取得。
- 来源为 arXiv 作者自存版，非排版后的期刊版。词条见 `corpus_manifest.csv`。

## 纳入与剔除

- 剔除数：0。20 篇全部纳入。
- 纳入标准：JRSSB 刊出；方向与目标手稿相邻（替代变量与结果稀缺、半监督、两阶段抽样、预测集与校准、协变量迁移、双样本合并、选择性误差控制、迁移理论）；arXiv 全文可得；Crossref 与 arXiv 双核对通过。
- 首选但未纳入：Lei & Wasserman (2014) "Distribution-free Prediction Bands for Non-parametric Regression"（JRSSB 76(1) 71--96），未找到可合法获取的全文，以 Zhang, Huang & Yang (2026) 替补。

## 已知度量失效

自动抽取在个别论文上失效，失效项不进入中位数，论文本身保留：

- 摘要抽取失败：09、12、13、17、20（5 篇）。
- 引言抽取失败或不完整：09、10、13、20（4 篇）。
- 讨论抽取失败：04、07、08、09、17、18（6 篇）。
- 参考文献块定位失败：03、08、12（3 篇）。

## 版本差异的口径说明

- arXiv 版含附录与补充材料，页数远长于刊出版（例如 01 为 87 页对 30 页，11 为 127 页对 20 页）。正文统计一律截到 References 之前。
- arXiv 版的排版、行距与字号与期刊版不同，词数与页数不可直接换算；本报告只用词数、句数、公式数、图表数与字母种类等与排版无关的量。
- 图形的配色、线型与字号未做视觉检查，图注关键词计数对图形类型信号太弱，该维度不进入结论。
- 参考文献条数按 References 块内含年份的行数近似，含少量噪声。

## 可复现性

- 度量脚本（作者本地）：`_build_check/measure_samples.ps1`、`measure_deep.ps1`、`measure_extra.ps1`、`measure_symbols.ps1`。
- 指标明细：`corpus_database/corpus_metrics.csv`（21 行，20 篇样本加目标稿）。
- 样本题录：`corpus_manifest.csv`。
