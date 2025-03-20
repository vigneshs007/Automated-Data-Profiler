# Automated Data Profiler & Visualization

## 📌 Project Overview
This project is an **Automated Data Profiler & Visualization Tool** that analyzes any given dataset, performs Exploratory Data Analysis (EDA), and generates a report with key insights.

## 📊 Features
✅ Reads CSV datasets automatically
✅ Detects missing values & handles them
✅ Generates key statistical summaries
✅ Visualizes data distributions using histograms
✅ Detects correlations using heatmaps
✅ Identifies outliers using boxplots
✅ Generates an **HTML or PDF report** with findings

## 🔧 Technologies Used
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Pandas Profiling
- ReportLab (for PDF generation)

## 📂 Dataset Used
**Dataset Name:** Superstore Sales Data  
**Download Link:** [Kaggle - Superstore Sales](https://www.kaggle.com/datasets/rohitsahoo/sales-forecasting)

## 🛠 Installation & Usage
1. **Clone the repository**
```bash
git clone https://github.com/yourusername/Automated-Data-Profiler.git
cd Automated-Data-Profiler
```
2. **Install required dependencies**
```bash
pip install pandas numpy matplotlib seaborn pandas-profiling reportlab
```
3. **Run the Jupyter Notebook**
```bash
jupyter notebook
```
4. **Load and analyze your dataset**
```python
import pandas as pd
df = pd.read_csv("your_dataset.csv")
```
5. **Generate an automated report**
```python
from pandas_profiling import ProfileReport
profile = ProfileReport(df, explorative=True)
profile.to_file("data_profile_report.html")
```

## 📜 Report Generation
- **HTML Report:** Automatically created using Pandas Profiling
- **PDF Report:** Uses ReportLab to save key insights

## 🚀 Future Improvements