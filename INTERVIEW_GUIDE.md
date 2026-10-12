# Interview Guide

## 60-second explanation

I built this project to predict article popularity from pre-publication metadata using a real historical dataset of 39,644 Mashable articles. I used chronological train/validation/test partitions rather than a random split so the evaluation better reflects forward-looking prediction. I excluded URL, observation age, and share-history fields to reduce leakage risk. Ridge regression was selected over histogram gradient boosting using validation log-MAE, then evaluated once on the final test period. The improvement over the median baseline is modest, about 2.52% in log-MAE, so I present it as a real but limited signal rather than a production-ready predictor.

## Questions I should be able to answer

- Why use chronological rather than random splitting?
- Why predict log1p(shares)?
- What leakage risks exist in this dataset?
- Why did Ridge beat the more complex model?
- What is the difference between log-scale MAE and original-share MAE?
- How would I detect temporal drift?
- How does the exported model reach the browser/API?

## Strong limitation statement

The data comes from one historical publisher and exposure windows vary. This is reproducible historical evidence, not a claim about current media performance or causal impact.

## 20-second recruiter version

Real-data regression project with 39,644 articles, chronological evaluation, leakage controls, baseline comparison, model export, API inference, temporal robustness tests, Docker, experiment tracking, and CI.
