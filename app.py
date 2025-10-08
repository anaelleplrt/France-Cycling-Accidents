"""
Cycling Safety in France (2005-2023)
Interactive dashboard analyzing bicycle accidents data from BAAC/ONISR.

Author: Anaëlle Pollart
Course: #EFREIDataStories2025
Professor: Mano Joseph Mathew
"""

import streamlit as st
import pandas as pd

# Import utilities
from utils.io import load_data, get_data_info
from utils.prep import clean_data, create_aggregated_tables

# Import sections
from sections import intro, data_quality, overview, deep_dives, conclusions


# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Cycling Safety in France",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown("""
    <style>
    /* Main title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1.2rem;
        color: #555;
        margin-top: 0;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    
    /* KPI styling */
    .kpi-container {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


# ============================================================================
# LOAD AND CACHE DATA
# ============================================================================

@st.cache_data(show_spinner=False)
def get_data():
    """Load and preprocess data with caching."""
    with st.spinner("Loading data..."):
        # Load raw data
        df_raw = load_data()
        
        # Clean and preprocess
        df_clean = clean_data(df_raw)
        
        # Create aggregated tables for visualizations
        tables = create_aggregated_tables(df_clean)
        
    return df_raw, df_clean, tables


# Load data
df_raw, df, tables = get_data()
metadata = get_data_info()


# ============================================================================
# SIDEBAR - NAVIGATION & FILTERS
# ============================================================================

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Flag_of_France.svg/1280px-Flag_of_France.svg.png", 
                 width=100)

st.sidebar.title("🚴 Navigation")

# Section selection
section = st.sidebar.radio(
    "Go to section:",
    [
        "📖 Introduction",
        "🔍 Data Quality",
        "📊 Overview",
        "🔬 Deep Dive Analysis",
        "💡 Conclusions"
    ],
    index=0
)

st.sidebar.markdown("---")

# ============================================================================
# GLOBAL FILTERS (Applied to all sections except intro and data quality)
# ============================================================================

st.sidebar.title("🎛️ Filters")

# Year range filter
year_min, year_max = int(df['year'].min()), int(df['year'].max())
year_range = st.sidebar.slider(
    "Year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)

# Department filter (multiselect)
all_departments = ['All'] + sorted(df['dep'].dropna().unique().tolist())
selected_departments = st.sidebar.multiselect(
    "Departments",
    options=all_departments,
    default=['All']
)

# Gravity filter
gravity_options = ['All'] + df['gravity'].dropna().unique().tolist()
selected_gravity = st.sidebar.multiselect(
    "Accident severity",
    options=gravity_options,
    default=['All']
)

# Agglomeration filter
agglomeration_options = ['All'] + df['agglomeration'].dropna().unique().tolist()
selected_agglomeration = st.sidebar.selectbox(
    "Location type",
    options=agglomeration_options,
    index=0
)

st.sidebar.markdown("---")

# Dataset info in sidebar
with st.sidebar.expander("ℹ️ About the data"):
    st.write(f"**Source:** {metadata['original_source']}")
    st.write(f"**Period:** {metadata['period']}")
    st.write(f"**Total records:** {len(df):,}")
    st.write(f"**License:** {metadata['license']}")


# ============================================================================
# APPLY FILTERS TO DATAFRAME
# ============================================================================

def apply_filters(dataframe):
    """Apply global filters to the dataframe."""
    filtered = dataframe.copy()
    
    # Year filter
    filtered = filtered[
        (filtered['year'] >= year_range[0]) & 
        (filtered['year'] <= year_range[1])
    ]
    
    # Department filter
    if 'All' not in selected_departments and len(selected_departments) > 0:
        filtered = filtered[filtered['dep'].isin(selected_departments)]
    
    # Gravity filter
    if 'All' not in selected_gravity and len(selected_gravity) > 0:
        filtered = filtered[filtered['gravity'].isin(selected_gravity)]
    
    # Agglomeration filter
    if selected_agglomeration != 'All':
        filtered = filtered[filtered['agglomeration'] == selected_agglomeration]
    
    return filtered


# Apply filters (except for intro and data quality sections)
if section not in ["📖 Introduction", "🔍 Data Quality"]:
    df_filtered = apply_filters(df)
else:
    df_filtered = df


# ============================================================================
# MAIN CONTENT - RENDER SELECTED SECTION
# ============================================================================

# Header with title and subtitle
st.markdown("""
    <h1 style='font-size: 3.5rem; color: #1f77b4; margin-bottom: 0;'>
        🚴 Cycling Safety in France (2005-2023)
    </h1>
    <p style='font-size: 1.5rem; color: #555; margin-top: 0.5rem; margin-bottom: 2rem;'>
        Understanding bicycle accident patterns to improve cyclist safety
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

# Render the selected section
if section == "📖 Introduction":
    intro.render(metadata)

elif section == "🔍 Data Quality":
    data_quality.render(df_raw, df)

elif section == "📊 Overview":
    overview.render(df_filtered, tables)

elif section == "🔬 Deep Dive Analysis":
    deep_dives.render(df_filtered, tables)

elif section == "💡 Conclusions":
    conclusions.render(df_filtered)


# ============================================================================
# FOOTER
# ============================================================================

st.markdown("""
    <div style='text-align: center; color: #777; font-size: 0.9rem;'>
        <p>
            📊 Data Storytelling Dashboard | #EFREIDataStories2025<br>
            👨‍🎓 Anaëlle Pollart<br>
            📅 2025 | Built with Streamlit & Python
        </p>
        <p style='font-size: 0.8rem;'>
            <strong>Data Source:</strong> BAAC - ONISR (data.gouv.fr) | 
            <strong>License:</strong> Open License (Licence Ouverte)
        </p>
    </div>
""", unsafe_allow_html=True)