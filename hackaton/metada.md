# Dataset Features Metadata

## Overview
- **Total Features:** 16 (9 numerical + 7 categorical)
- **Training Samples:** 38,000

---

## Numerical Features (num_1 to num_9)

### num_1 - Umur
- **Type:** Integer

### num_2 - pendapatan
- **Type:** Integer


### num_3 - pinjaman
- **Type:** Integer

### num_4 - Skor kredit
- **Type:** Integer


### num_5 - bulan bekerja
- **Type:** Integer


### num_6 - jumlah akun kredit yang aktif
- **Type:** Integer
- **Notes:** jumlah akun kredit yang aktif

### num_7 - interest
- **Type:** Float
-

### num_8 - bulan pinjaman
- **Type:** Integer


### num_9 - Ratio debt to income
- **Type:** Float

---

## Categorical Features (cat_1 to cat_7)

### cat_1 - level edukasi
- **Type:** Categorical


### cat_2 - jenis pekerjaan
- **Type:** Categorical


### cat_3 - status menikah
- **Type:** Categorical


### cat_4 - ada mortgage
- **Type:** Categorical (Binary)


### cat_5 - punya tanggungan
- **Type:** Categorical (Binary)


### cat_6 - Tujuan loan
- **Type:** Categorical


### cat_7 - Ada Co-Signer
- **Type:** Categorical (Binary)

---

## Target Variable

### target - Loan Default Status
- **Type:** Binary Integer
- **Values:** 0 or 1
- **Distribution:**
  - Class 0 (No Default)
  - Class 1 (Default)


---

## Submission Requirements

### File Format
- **Format:** CSV with headers
- **Filename:** `nama_team_predictions.csv`
- **Encoding:** UTF-8

### Columns Required
1. `id` - Row identifier (0-1499)
2. `prediction` - Predicted class (0 or 1)
3. `probability` - Predicted probability of class 1 (0.0 to 1.0)

---

## Evaluation Metrics

- **Primary Metric:** AUC-ROC (Area Under Receiver Operating Characteristic)
- **Secondary Metric:** F1-Score (harmonic mean of precision and recall)
- **Other Metrics:** Accuracy, Precision, Recall, Sensitivity, Specificity
- **Ranking:** Primary by AUC-ROC (descending), secondary by F1-Score (descending)

---
