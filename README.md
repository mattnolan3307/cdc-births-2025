# Provisional 2025 CDC U.S. Birth Counts Dashboard

A Streamlit analytics application designed for **undergraduate business analytics students** to explore provisional 2025 CDC live birth count data across U.S. geographies, calendar months, and infant sexes.

---

## 📌 Project Overview & Objectives

* **Target Audience**: Business Analytics undergraduate students & data auditing practitioners.
* **Domain Context**: Provisional 2025 Centers for Disease Control and Prevention (CDC) National Center for Health Statistics (NCHS) Natality Data.
* **Analytical Focus**: Evaluating exploratory data analysis (EDA), data quality auditing, geographic scale variance, seasonal birth trends, and demographic sex proportions.

---

## 🛠️ Technology Stack

* **Framework**: Streamlit 1.64+
* **Data Processing**: pandas, openpyxl
* **Data Visualizations**: Plotly Express & Plotly Graph Objects
* **Language**: Python 3.11+ / 3.13+

---

## 🚀 Running the Dashboard Locally

1. **Install Dependencies**:
   ```bash
   py -m pip install streamlit pandas plotly openpyxl
   ```

2. **Launch Application**:
   ```bash
   py -m streamlit run app.py
   ```

3. **Open Browser**:
   Navigate to `http://localhost:8501` in your browser.

---

## 📊 Pedagogical Principles & Rule Compliance

1. **Birth Counts vs. Birth Rates**: All figures represent raw **live birth counts**, not birth rates per capita. The dataset contains no population denominator figures, so rate calculations cannot be derived.
2. **Data Integrity**: 1,224 exact observations (51 states/DC × 12 months × 2 sexes), 0 missing values, and 3,604,640 total live births.
3. **Chronological Sorting**: Months strictly follow calendar sequence (Jan–Dec / Month Codes 1–12).
4. **Accessible Visuals**: Custom high-contrast palettes (Teal for Female, Indigo for Male), zero-baseline axes (`rangemode='tozero'`), formatted thousands separators, and responsive tabs.
