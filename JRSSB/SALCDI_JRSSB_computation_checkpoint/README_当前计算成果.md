# JRSSB 修改：当前计算成果

本包是已经运行的计算成果检查点，不是最终投稿包。

已完成：6,000 次主模拟（12 个设定，每个 500 次）、400 次三路轮换验证、60 次数值精度检查、梯度及中心化导数单元测试、未核验结局泄漏测试、离散分布置信带扩展测试，以及二元子模型的精确计算。

主模拟没有程序报错。数值精度检查的 60 次比较中有 2 次选择权重改变；该检查是数值收敛评估，不是严格的一致积分误差认证。

尚未完成：JRSSB 正文与完整补充证明整合、新的 EPA 超阈概率差实证分析、最终投稿材料与全链条核验。因此 submission_ready=false。

## 文件

- code/：本轮实际运行的程序。
- results/main/replicates.csv：主模拟逐次完整结果。
- results/main/summary.csv：汇总与 Monte Carlo 标准误。
- results/main/manifest.json：设定、种子及程序哈希。
- results/：样本轮换、精确二元模型和数值检查结果。
- prior_core/jrssb_core_v1/：上一轮核心技术稿及其复核程序；保留原版本标识，不表示本轮重新完成了全部证明。
- audit/completion_status.json：机器可读的真实完成状态。

## 重现

Python 依赖：numpy、scipy、pandas。

```bash
OPENBLAS_NUM_THREADS=1 python code/test_core.py
OPENBLAS_NUM_THREADS=1 python code/simulation.py --reps 500 --workers 4 --output rerun
```

EPA 行级配对数据未包含于本包，不以旧稿汇总表或模拟数据替代新的真实分析。
