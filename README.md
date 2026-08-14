# Responsible AI for Public Health: Respiratory Hospitalization Forecasting Case Study

This repository contains the code, documentation, evaluation artifacts, and Responsible AI governance materials associated with a public health forecasting case study developed at the **National Health AI Innovation Center (NIAR-Saúde/UFMG)**.

The case study investigates the prediction of monthly hospitalizations due to respiratory diseases using aggregated data from the Brazilian Unified Health System (SUS). Beyond predictive performance, the project examines how Responsible AI practices can be incorporated into the development and governance lifecycle through temporal validation, fairness assessment, explainability, documentation, and institutional oversight.

The repository supports two complementary research studies:

1. **Responsible AI for Public Health: A Methodological Illustration with a Forecasting Model applied to Respiratory Hospitalizations on SUS Data**
   This study focuses on the methodological integration of Responsible AI practices into the forecasting pipeline, including leakage-controlled temporal validation, fairness auditing, explainability, reproducibility, and structured documentation.

2. **From Principles to Longitudinal AI Governance: An Evidence-Based Framework for Continuous Oversight**
   This study uses the same forecasting system as a case study for the **Framework for Institutional AI Responsibility (FIAR)**, examining how technical and governance artifacts can support auditable oversight, institutional decision-making, and future longitudinal governance assessment.

## Case Study

The task consists of predicting the monthly number of hospitalizations associated with respiratory diseases (ICD-10 Chapter J) at the hospital level.

The study uses aggregated public data from the Brazilian Hospital Information System (SIH/SUS), available through DataSUS. The modeling pipeline was designed to preserve temporal integrity and to support evaluation beyond aggregate predictive accuracy.

The case includes:

* temporal train–validation–test separation;
* baseline and LightGBM forecasting models;
* an intentionally leaked configuration used to illustrate the impact of temporal leakage;
* subgroup-based performance and fairness analysis;
* fairness mitigation through resampling;
* global and local explainability using SHAP;
* reproducibility controls;
* Data Card and Model Card documentation;
* Responsible AI assessment and audit artifacts; and
* governance records supporting institutional review and decision-making.

## Repository Structure

```text
.
├── SIH_Data/
│   └── Data and preprocessing resources used in the case study
│
├── docs/
│   ├── Data_Card/
│   ├── Model_Card/
│   ├── Fairness/
│   ├── Explicability/
│   ├── metric_Images/
│   ├── metrics_report.md
│   └── project_doc.md
│
├── audits/
│   ├── 01_initial_form/
│   ├── 02_audit_reports/
│   └── README.md
│
├── Map/
│
├── v1.ipynb
├── v2.ipynb
└── README.md
```

### `docs/`

Contains the main technical and Responsible AI documentation generated for the case study, including Data Card, Model Card, fairness evaluation, explainability materials, metrics, and project documentation.

### `audits/`

Contains governance and Responsible AI assessment materials used to document and evaluate the project. These artifacts provide part of the evidence base used in the FIAR case study.

### Notebooks

The notebooks contain the experimental pipeline used to develop and evaluate the forecasting models and the associated Responsible AI analyses.

## Responsible AI Evaluation

Responsible AI was operationalized through technical and documentation safeguards integrated into the modeling workflow.

### Temporal integrity

The experimental design uses a temporal train–validation–test split. Features are constructed only from historically available information in the valid configurations, preventing future information from entering model development.

An intentionally leaked LightGBM configuration is also included as a stress test to illustrate how inappropriate temporal design can artificially improve predictive performance.

### Fairness

Model performance is evaluated both globally and across relevant subgroups, including demographic, geographic, and hospital-level characteristics.

The analysis identified relatively low disparities across sex, age, and race/ethnicity groups, while substantially larger disparities were observed across geographic regions and hospital sizes. A resampling-based mitigation strategy was evaluated to reduce regional disparities, although residual disparities remained after mitigation.

The analysis should therefore be interpreted as an assessment of performance parity across predefined groups rather than as a complete operationalization of the broader concept of fairness.

### Explainability

SHAP is used to examine both global and local model behavior. The analysis provides information about the features contributing to predictions but should not be interpreted as establishing causal relationships or definitive explanations for model outputs.

### Auditability and reproducibility

The repository includes structured documentation artifacts intended to improve traceability and reproducibility, including:

* Data Card;
* Model Card;
* fairness analysis;
* explainability analysis;
* Responsible AI evaluation materials; and
* governance and audit records.

Experimental reproducibility is further supported through predefined temporal partitions, documented model configurations, evaluation metrics, and repeated model runs.

## FIAR Governance Case Study

This repository also provides the technical and governance evidence used in the case-study application of the **Framework for Institutional AI Responsibility (FIAR)**.

In the FIAR study, the forecasting project was evaluated not only in terms of model performance but also in terms of the availability and traceability of evidence required for institutional oversight.

The initial governance assessment identified gaps in standardized documentation, structured fairness evaluation, formal technical decision records, explainability documentation, and experimental traceability.

Following an adequacy phase, the project produced a structured evidence package including:

* Data Card;
* Model Card;
* Fairness Report;
* Explainability Report;
* Technical Decision Record; and
* Consolidated Responsible AI Report.

These artifacts were used to connect technical findings to governance decisions. In particular, persistent regional performance disparities led to continued monitoring requirements and restrictions on the role of the system as secondary decision support.

The case represents the **first formal governance cycle** of the project. It therefore provides evidence of an emerging structured governance process, but does not by itself demonstrate longitudinal recurrence across multiple governance cycles. Future reassessments are required to evaluate whether governance practices remain recurrent, continuous, and traceable across successive system versions.

## Data

The case study uses aggregated data from the Brazilian Unified Health System (SUS), primarily from the Hospital Information System (SIH/SUS).

The prediction task is defined at the hospital-by-month level and considers historical hospitalization activity and other aggregated hospital characteristics.

Please refer to the Data Card and project documentation in this repository for detailed information about data provenance, temporal coverage, preprocessing, inclusion and exclusion criteria, and known limitations.

## Research Use

This repository is intended to support transparency and reproducibility of the methodological and governance case study. It should not be interpreted as a production-ready clinical system or as a tool for autonomous healthcare decision-making.

The forecasting system is studied as a decision-support application for public health planning and governance research.

## Related Publications

### Responsible AI for Public Health

**Responsible AI for Public Health: A Methodological Illustration with a Forecasting Model applied to Respiratory Hospitalizations on SUS Data**

This work presents the technical and methodological Responsible AI pipeline illustrated by the respiratory hospitalization forecasting case.

### FIAR — Longitudinal AI Governance

**From Principles to Longitudinal AI Governance: An Evidence-Based Framework for Continuous Oversight**

This work uses the respiratory hospitalization forecasting project as a case study to illustrate how FIAR connects lifecycle evidence, governance assessment, and institutional action, while establishing the basis for future longitudinal governance evaluation.

## Acknowledgments

This work was developed in the context of NIAR-Saúde/UFMG and related Responsible AI research initiatives.

## Citation

Citation information for the associated publications will be added as their final bibliographic records become available.

