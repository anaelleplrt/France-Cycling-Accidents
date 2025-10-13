"""
Data loading utilities for the cycling accidents dashboard.
"""

import streamlit as st
import pandas as pd
from pathlib import Path


@st.cache_data(show_spinner=False)
def load_data():
    """
    Load the cycling accidents dataset.
    
    Returns:
        pd.DataFrame: Raw dataset with all columns
    """
    # Path to the CSV file
    data_path = Path(__file__).parents[1] / "data" / "accidentsVelofull.csv"
    
    # Load the CSV
    df = pd.read_csv(data_path, low_memory=False)
    
    return df


def get_data_info():
    """
    Returns metadata about the dataset.
    
    Returns:
        dict: Dataset metadata
    """
    return {
        "source": "data.gouv.fr",
        "dataset_name": "Accidents de vélo en France",
        "original_source": "BAAC - Observatoire National Interministériel de la Sécurité Routière (ONISR)",
        "period": "2005-2023",
        "license": "Open License (Licence Ouverte)",
        "url": "https://www.data.gouv.fr/datasets/accidents-de-velo/",
        "description": "Cycling accidents involving at least one injured person requiring medical care, recorded by law enforcement."
    }


def get_license_text():
    """
    Returns the license information for display.
    
    Returns:
        str: License text
    """
    return """
    **Data License**: Open License (Licence Ouverte)
    
    This dataset is provided by the French government and is freely reusable 
    for academic and non-commercial purposes with proper attribution.
    
    **Source**: BAAC - ONISR (Observatoire National Interministériel de la Sécurité Routière)
    """