# Cycling Safety in France (2005-2023)

Interactive Streamlit dashboard analyzing 18 years of bicycle accident data from the French National Road Accident Database (BAAC).

**Course**: Data Vizualisation #EFREIDataStories2025  
**Author**: Anaëlle Pollart  
**Professor**: Mano Joseph Mathew  
**Institution**: EFREI Paris

---

## About This Project

This dashboard analyzes **79,965 cycling accidents** (2005-2023) to identify patterns, risk factors, and provide evidence-based safety recommendations for policymakers and urban planners.

**Research Questions:**
- When and where do cycling accidents occur?
- What conditions (weather, lighting, infrastructure) affect severity?
- Who are the most vulnerable cyclists?
- How effective is cycling infrastructure?

---
## Demo Video
A 5 minutes walkthrough demonstrating the dashboard's narrative and interactive features.
**Video link**: https://youtu.be/FNrXl76EINc

---

## Quick Start

### Option 1: Use the deployed app (Recommended)
The dashboard is already deployed and ready to use:  
**Deployed URL**: https://france-cycling-accidents.streamlit.app/

No installation required! Just click and explore.


### Option 2: Run Locally :
**Prerequisites :**
- Python 3.8+
- pip

**Setup Instructions :**

**1. Extract the ZIP file**
**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the app**
```bash
streamlit run app.py (or, if needed : python -m streamlit run app.py)
```

The app will open at `http://localhost:8501`

---

### Project Structure
```text
├── app.py                    # Main application
├── download_data.py          # Script to download dataset from data.gouv.fr
├── sections/                 # Dashboard pages
│   ├── intro.py
│   ├── data_quality.py
│   ├── overview.py
│   ├── deep_dives.py
│   └── conclusions.py
├── utils/                    # Helper functions
│   ├── io.py                 # Data loading
│   ├── prep.py               # Data cleaning
│   └── viz.py                # Visualizations
├── data/
│   └── accidentsVelofull.csv # Our Dataset in csv
├── requirements.txt
└── README.md
```

---

## Dependencies
streamlit>=1.33.0  
pandas>=2.0.0  
numpy>=1.24.0  
plotly>=5.14.0  
matplotlib>=3.7.0  
requests>=2.31.0
All required libraries are listed in `requirements.txt`.

---

## Data Source

**Dataset**: Base BAAC (French National Road Accident Database)  
**Provider**: ONISR (Observatoire National Interministériel de la Sécurité Routière)  
**Source**: [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/accidents-de-velo/)  
**Direct download**: [CSV file](https://www.data.gouv.fr/api/1/datasets/r/4c75d6c0-c927-48ca-92db-5bcce9f17ae7)  
**License**: Open License (Licence Ouverte) - Free for academic use  
**Period**: 2005-2023 (18 years)  
**Size**: 79,965 records

Each record represents one person involved in a cycling accident requiring medical attention.

---

## Data Availability

**Dataset included**: The CSV file `data/accidentsVelofull.csv` is directly included in the repository for immediate use.

**Download script provided**: Although the dataset is manageable in size (~80 MB), we follow data science best practices by including a `download_data.py` file, which :

- Enables downloading the latest version from [data.gouv.fr](https://www.data.gouv.fr/api/1/datasets/r/4c75d6c0-c927-48ca-92db-5bcce9f17ae7)
- Implements caching (only downloads if file doesn't exist)
- Demonstrates scalable approach for larger datasets

This dual strategy ensures both immediate reproducibility and adherence to best practices.

---

## Features

- **Interactive filters**: Year range, departments, severity, location type
- **5 dashboard sections**: Introduction, Data Quality, Overview, Deep Dive Analysis, Conclusions
- **10+ interactive visualizations**: Plotly charts, matplotlib waffle charts
- **Interactive map**: Department-level heatmap
- **Performance optimized**: `@st.cache_data` on all data operations
- **Responsive design**: Works on desktop and tablet

---

## Limitations

- Only includes reported accidents (minor unreported incidents not captured)
- Some missing values in optional fields
- Analysis shows correlation, not causation

Full data quality documentation available in the dashboard's **Data Quality** section.

---

## 🎓 Academic Context

**Course**: Data Visualization  
**Hashtag**: #EFREIDataStories2025  
**Professor**: Mano Joseph Mathew  
**Institution**: EFREI Paris  
**Year**: 2025

---

## License

**Data**: Open License (Licence Ouverte) - ONISR/data.gouv.fr  
**Code**: Academic project for EFREI course

---

**Built with Python, Streamlit, and Open Data**
