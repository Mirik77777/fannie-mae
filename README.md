# Fannie Mae Loan Performance — Big Data Analysis on AWS

Uses AWS (S3, Athena, Glue, EMR) and PySpark / SparkSQL to analyse the **Fannie Mae Single-Family Loan Performance Dataset (2020–2025)** — approximately **569 million records**.

## Project at a glance

| | |
|---|---|
| **Dataset** | Fannie Mae Single-Family Loan Performance 2020–2025 |
| **Volume** | ~569 million records, ~110 columns per record |
| **Storage** | Amazon S3 (raw CSV, curated Parquet) |
| **Query engine** | Amazon Athena (for ETL), PySpark on EMR (for analysis) |
| **Cluster** | EMR m5.xlarge, Spark 3.5.6 |
| **Notebook** | JupyterHub on EMR master node |

## Research questions

1. **Does high DTI (>43%) combined with high CLTV (>80%) amplify 90+ day delinquency non-linearly, and how does it vary by state?**
2. **Which loan servicers resolve delinquencies fastest ("cure"), and which let them escalate into serious delinquency ("roll")?**

## ETL pipeline

```
Raw CSV (S3)  ->  Glue Crawler  ->  Athena (CSV table)
                                         |
                                         v
                                    CTAS query
                                         |
                                         v
                               Parquet on S3 (39 cols, Snappy)
                                         |
                                         v
                                    EMR + Spark
                                         |
                                         v
                                    SparkSQL views
                                         |
                                         v
                             PySpark analysis + visualisations
```

The CSV to Parquet step reduced Athena scan cost by ~80-90% on subsequent queries, and dropped the column count from ~110 to 39 based on the Fannie Mae data dictionary.

## Repository structure

```
.
├── README.md
├── .gitignore
├── fannie_mae_project_Individual.docx   # Individual report (full write-up)
├── Group_Report.docx                    # Group report (see credits)
├── Group_Presentation.pptx              # Group presentation (see credits)
├── sql/                                 # All SQL scripts (Athena + SparkSQL)
└── pyspark/                             # PySpark notebooks / visualisation scripts
```

Code is organised in the order it runs in the pipeline. File prefixes (01–20) follow execution order; the appendix label (SQL1.x, SparkSQL1.x, PySpark1.x) is preserved in the filename so you can cross-reference with the report.

## Key findings

### Question 1 — Risk layering (DTI x CLTV)

- **Baseline** (Low DTI & Low CLTV): 0.208% delinquency rate
- **Dual risk** (High DTI & High CLTV): 0.968% delinquency — **4.67x baseline**
- Effect is **non-linear**: risk layering multiplies rather than adds
- State variance: Delaware hits **7.11x** multiplier, Wisconsin 6.72x, South Dakota 6.50x — local economic conditions matter
- Washington D.C. and New York have the highest absolute dual-risk rates (1.80% and 1.38%)
- Largest financial exposure sits with California, Florida, Texas due to sheer loan volume

### Question 2 — Servicer performance (cure vs. roll)

Based on 548 million month-over-month transition records:

- **Best cure rates:** RoundPoint (88.3%), Nexus Nova (86.6%), NewRez (86.5%)
- **Worst cure rates:** Guaranteed Rate (73.2%), Rocket Mortgage (73.4%) — despite handling the largest volumes
- **Lowest roll rate** (least escalation to serious delinquency): PHH Asset Services (2.1%)
- **Highest roll rates:** Guaranteed Rate (9.8%), PennyMac Corp. (9.3%)
- **Cure speed:** RoundPoint resolves in 1.02 months average with max severity 1.16 — intervenes before escalation. Arvest Central Mortgage reaches max severity 5.96, suggesting reactive rather than proactive handling.

**Takeaway:** volume does not equal quality. Smaller specialised servicers consistently outperform the largest ones on both metrics.

## Group work — credits

The **group report** (`Group_Report.docx`) and **group presentation** (`Group_Presentation.pptx`) were completed collaboratively with three teammates. All four contributors did their own share of the work; different sections of both deliverables were led by different team members. The individual report (`fannie_mae_project_Individual.docx`) plus the code in `sql/` and `pyspark/` is my own work and extends the group foundation with the independent risk-layering and servicer-performance analyses described above.

Teammate identifiers were anonymised before publication. If you are one of my teammates and would like your name credited or the group documents removed, please contact me.

## Tech stack

AWS S3 · AWS Glue · Amazon Athena · Amazon EMR · PySpark 3.5.6 · SparkSQL · Python 3 · pandas · matplotlib · JupyterHub

## Reproducibility notes

- Raw data is public and free: [Fannie Mae Single-Family Loan Performance Data](https://capitalmarkets.fanniemae.com/credit-risk-transfer/single-family-credit-risk-transfer/fannie-mae-single-family-loan-performance-data)
- Total raw size: ~57 GB compressed / ~847 GB uncompressed
- EMR cluster config: m5.xlarge for master + core nodes
- JupyterHub access requires opening TCP port 9443 on the master node's security group
- Parquet conversion is the single most valuable optimisation — do it first
- All code was originally written and run in a JupyterHub notebook on EMR; the `.sql` and `.py` files here are extracted verbatim

## Author

**Mirfayzbek Sharipov** · [LinkedIn](https://linkedin.com/in/mirfayzbek-sharipov/)
