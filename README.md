# 项目目录说明

本目录按投稿轨道分成两部分，`JASA/` 与 `JRSSB/`。

## V5 已交付稿件

[`JRSSB/submission_v5/`](JRSSB/submission_v5/) 保存本次交付的 V5 润色稿：正文 29 页、补充材料 53 页、投稿信、完整 LaTeX 源码、矢量图和编译后的下载包。GitHub Actions 已核对 45 个源码文件并完成编译；不重新运行统计分析。`writing_v4/` 的后续编辑与其他历史目录均保留，不被 V5 快照覆盖。

- [正文 PDF](JRSSB/submission_v5/01_Manuscript/manuscript.pdf)
- [补充材料 PDF](JRSSB/submission_v5/02_Supplementary_Material/supplement.pdf)
- [稿件材料 ZIP](JRSSB/submission_v5/downloads/JRSSB_V5_editorial_submission.zip)
- [完整 LaTeX 源码](JRSSB/submission_v5/04_LaTeX_Source/)

本次上传不含 `Frozen_V3_reproduction.zip`，该冻结计算归档仍在作者已下载的 V5 完整包内。上面的稿件材料 ZIP 不等同于包含逐次计算结果的完整复现包；已有早期计算检查点也不替代该冻结归档。

## JASA

- `JASA-active/`：2026-08-25 提交 JASA 的完整包，含正文、投稿信、补充材料、数据与代码、LaTeX 源码与图表。
- `JASA_Initial_Submission_2026-08-25.zip`：当时的投稿包压缩文件。

## JRSSB

- `JRSSB_revision_v3/`：JRSSB V3 投稿包（2026-09-29），含正文、补充材料、投稿信、代码、逐次结果、图表与审计记录。
- `JRSSB_V3_完整源码数据与复现包_20260929.zip`：与上一条对应的复现包压缩文件。
- `SALCDI_JRSSB_computation_checkpoint/`：JRSSB 计算检查点与早期技术说明。
- `EPA_handoff_20260928_110006/` 与同名 zip：从 JASA 匿名代码包导出的 EPA 配对数据快照，用于 JRSSB 的 EPA 分析。
- `EPA_date_recovery_20260928/`：EPA 日期恢复的映射表与审查记录。
- `date_recovery_work/`：日期恢复的中间脚本，已被 `.gitignore` 忽略。
- `writing_samples/`：12 篇相邻方向 JRSSB 论文的 arXiv 版本，用于写作与结构对照，已被 `.gitignore` 忽略。
- `writing_v4/`：正文凝练工作稿，含 `paper` 与 `figures` 的副本及 `handoff.md` 交接说明，供外部协作改写使用。

`_build_check/` 存放本机 LaTeX 复核用的副本与日志，已被 `.gitignore` 忽略。
