"""
Data preprocessing and cleaning utilities.
This module handles all data transformations, encoding, and feature engineering.
"""

import pandas as pd
import numpy as np
from datetime import datetime


# ============================================================================
# DICTIONARIES FOR DECODING CATEGORICAL VARIABLES
# ============================================================================

GRAVITY_DICT = {
    1: 'Unharmed',
    2: 'Killed',          
    3: 'Hospitalized',
    4: 'Minor injury'     
}

LIGHTING_DICT = {
    1: 'Daylight',
    2: 'Twilight or dawn',
    3: 'Night without street lighting',
    4: 'Night with street lighting off',
    5: 'Night with street lighting on'
}

WEATHER_DICT = {
    1: 'Normal',
    2: 'Light rain',
    3: 'Heavy rain',
    4: 'Snow - hail',
    5: 'Fog - smoke',
    6: 'Strong wind - storm',
    7: 'Dazzling weather',
    8: 'Overcast',
    9: 'Other'
}

AGGLOMERATION_DICT = {
    1: 'Outside built-up area',
    2: 'In built-up area'
}

INTERSECTION_DICT = {
    1: 'Outside intersection',
    2: 'X intersection',
    3: 'T intersection',
    4: 'Y intersection',
    5: 'Intersection with more than 4 branches',
    6: 'Roundabout',
    7: 'Square',
    8: 'Level crossing',
    9: 'Other intersection'
}

ROAD_CATEGORY_DICT = {
    1: 'Highway',
    2: 'National road',
    3: 'Departmental road',
    4: 'Municipal road',
    5: 'Off public network',
    6: 'Parking lot',
    9: 'Other'
}

SURFACE_DICT = {
    1: 'Normal',
    2: 'Wet',
    3: 'Puddles',
    4: 'Flooded',
    5: 'Snowy',
    6: 'Mud',
    7: 'Icy',
    8: 'Oil - grease',
    9: 'Other'
}

INFRASTRUCTURE_DICT = {
    0: 'Without infrastructure',
    1: 'Bike lane (physically separated)',
    2: 'Bike lane (painted)',
    3: 'Reserved lane',
    4: 'Other infrastructure'
}

# NEW: Situation dictionary
SITUATION_DICT = {
    -1: 'Not specified',
    0: 'None',
    1: 'On roadway',
    2: 'On emergency lane',
    3: 'On shoulder',
    4: 'On sidewalk',
    5: 'On bike path',
    6: 'On other special lane',
    8: 'Other'
}

GENDER_DICT = {
    1: 'Male',
    2: 'Female'
}

TRIP_PURPOSE_DICT = {
    0: 'Not specified',
    1: 'Home - work',
    2: 'Home - school',
    3: 'Shopping',
    4: 'Professional use',
    5: 'Leisure',
    9: 'Other'
}

COLLISION_TYPE_DICT = {
    1: 'Two vehicles - front',
    2: 'Two vehicles - from rear',
    3: 'Two vehicles - from side',
    4: 'Three or more vehicles - chain',
    5: 'Three or more vehicles - multiple',
    6: 'Other collision',
    7: 'Without collision'
}


# ============================================================================
# DATA CLEANING AND PREPROCESSING
# ============================================================================

def clean_data(df_raw):
    """
    Clean and preprocess the raw dataset.
    
    Steps performed:
    1. Remove unnecessary columns
    2. Normalize department codes
    3. Remove invalid rows
    4. Handle missing values
    5. Decode categorical variables
    6. Convert date/time formats
    7. Create calculated features
    
    Args:
        df_raw (pd.DataFrame): Raw dataset
        
    Returns:
        pd.DataFrame: Cleaned dataset
    """
    df = df_raw.copy()
    
    # ========================================================================
    # 1. REMOVE UNNECESSARY COLUMNS
    # ========================================================================
    columns_to_drop = [
        'Num_Acc',           # Technical ID
        'vehiculeid',        # Technical ID
        'lartpc',            # TPC width (too specific, many missing)
        'larrout',           # Road width (many missing)
        'nbv',               # Number of lanes (string format, inconsistent)
        '_infos_commune.code_epci'  # EPCI code (incomplete)
    ]
    
    df = df.drop(columns=columns_to_drop, errors='ignore')
    
    # ========================================================================
    # 2. NORMALIZE DEPARTMENT CODES
    # ========================================================================
    # Ensure all department codes have leading zeros (01, 02, ... 09)
    df['dep'] = df['dep'].astype(str).str.zfill(2)
    
    # ========================================================================
    # 3. REMOVE INVALID ROWS
    # ========================================================================
    initial_rows = len(df)
    
    # Remove rows with invalid/missing critical data
    # 1. Remove rows without year
    df = df[df['an'].notna()]
    
    # 2. Remove rows without gravity information (critical variable)
    df = df[df['grav'].notna()]
    
    # 3. Remove rows with invalid years (outside expected range)
    df = df[(df['an'] >= 2005) & (df['an'] <= 2023)]
    
    # 4. Remove rows without valid dates
    df = df[df['date'].notna()]
    
    # 5. Remove rows with invalid age (negative or extremely high)
    df = df[(df['age'].isna()) | ((df['age'] >= 0) & (df['age'] <= 120))]
    
    rows_removed = initial_rows - len(df)
    
    # ========================================================================
    # 4. HANDLE MISSING VALUES
    # ========================================================================
    # For numeric columns with codes, -1 or 0 often means "not specified"
    # We'll keep them as is and document in data quality section
    
    # ========================================================================
    # 5. DECODE CATEGORICAL VARIABLES
    # ========================================================================
    df['gravity'] = df['grav'].map(GRAVITY_DICT)
    df['lighting'] = df['lum'].map(LIGHTING_DICT)
    df['weather'] = df['atm'].map(WEATHER_DICT)
    df['agglomeration'] = df['agg'].map(AGGLOMERATION_DICT)
    df['intersection_type'] = df['int'].map(INTERSECTION_DICT)
    df['road_category'] = df['catr'].map(ROAD_CATEGORY_DICT)
    df['surface_condition'] = df['surf'].map(SURFACE_DICT)
    df['infrastructure'] = df['infra'].map(INFRASTRUCTURE_DICT)
    df['situation'] = df['situ'].map(SITUATION_DICT)  # NEW: Decode situation
    df['gender'] = df['sexe'].map(GENDER_DICT)
    df['trip_purpose'] = df['trajet'].map(TRIP_PURPOSE_DICT)
    df['collision_type'] = df['col'].map(COLLISION_TYPE_DICT)
    
    # ========================================================================
    # 6. CONVERT DATE/TIME FORMATS
    # ========================================================================
    # Create a proper datetime column
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['hrmn'], errors='coerce')
    
    # Extract useful time components
    df['year'] = df['an']
    df['month_num'] = pd.to_datetime(df['date'], errors='coerce').dt.month
    df['month_name'] = pd.to_datetime(df['date'], errors='coerce').dt.month_name()
    df['day_of_week'] = pd.to_datetime(df['date'], errors='coerce').dt.day_name()
    
    # Extract hour from hrmn (format: "HH:MM")
    df['hour'] = pd.to_datetime(df['hrmn'], format='%H:%M', errors='coerce').dt.hour
    
    # Create time period categories
    df['time_period'] = pd.cut(
        df['hour'], 
        bins=[0, 6, 12, 18, 24],
        labels=['Night (0-6h)', 'Morning (6-12h)', 'Afternoon (12-18h)', 'Evening (18-24h)'],
        include_lowest=True
    )
    
    # ========================================================================
    # 7. CREATE CALCULATED FEATURES
    # ========================================================================
    
    # Age groups
    df['age_group'] = pd.cut(
        df['age'],
        bins=[0, 12, 17, 25, 35, 50, 65, 100],
        labels=['0-12', '13-17', '18-25', '26-35', '36-50', '51-65', '65+']
    )
    
    # Binary flags for severity
    df['is_severe'] = df['grav'].isin([2, 3])  # Hospitalized or killed
    df['is_fatal'] = df['grav'] == 2  # Killed
    
    # Dangerous conditions flag (night OR bad weather OR slippery surface)
    df['dangerous_conditions'] = (
        (df['lum'] >= 3) |  # Night
        (df['atm'].isin([2, 3, 4, 5])) |  # Bad weather
        (df['surf'].isin([2, 3, 5, 7]))  # Slippery surface
    )
    
    # Infrastructure safety flag
    df['has_bike_infrastructure'] = df['infra'].isin([1, 2])  # Bike lane or path
    
    # Weekend flag
    df['is_weekend'] = df['day_of_week'].isin(['Saturday', 'Sunday'])
    
    # Season
    df['season'] = df['month_num'].map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Autumn', 10: 'Autumn', 11: 'Autumn'
    })
    
    # ========================================================================
    # 8. REMOVE ORIGINAL ENCODED COLUMNS (Keep only decoded versions)
    # ========================================================================
    # Remove original encoded columns as decoded versions are more user-friendly
    columns_to_remove_after_decoding = [
        'grav', 'lum', 'atm', 'agg', 'int', 'catr', 
        'surf', 'infra', 'situ', 'sexe', 'trajet', 'col',  # Added 'situ' here
        'an'  # duplicate of 'year'
    ]
    df = df.drop(columns=columns_to_remove_after_decoding, errors='ignore')
    
    return df


def get_cleaning_summary(df_raw, df_clean):
    """
    Generate a summary of cleaning operations performed.
    
    Args:
        df_raw (pd.DataFrame): Original raw dataset
        df_clean (pd.DataFrame): Cleaned dataset
        
    Returns:
        dict: Summary statistics
    """
    summary = {
        'original_rows': len(df_raw),
        'original_cols': len(df_raw.columns),
        'cleaned_rows': len(df_clean),
        'cleaned_cols': len(df_clean.columns),
        'rows_removed': len(df_raw) - len(df_clean),
        'cols_removed': len(df_raw.columns) - len(df_clean.columns),
        'missing_values_original': df_raw.isnull().sum().sum(),
        'missing_values_cleaned': df_clean.isnull().sum().sum(),
    }
    
    return summary


def get_missing_values_report(df):
    """
    Generate a detailed report of missing values.
    
    Args:
        df (pd.DataFrame): Dataset
        
    Returns:
        pd.DataFrame: Missing values report
    """
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    
    report = pd.DataFrame({
        'Column': missing.index,
        'Missing Count': missing.values,
        'Missing Percentage': missing_pct.values
    })
    
    # Only show columns with missing values
    report = report[report['Missing Count'] > 0].sort_values('Missing Percentage', ascending=False)
    
    return report


# ============================================================================
# DATA AGGREGATION FOR VISUALIZATIONS
# ============================================================================

def create_aggregated_tables(df):
    """
    Create pre-aggregated tables for efficient visualizations.
    
    Args:
        df (pd.DataFrame): Cleaned dataset
        
    Returns:
        dict: Dictionary of aggregated DataFrames
    """
    tables = {}
    
    # By year
    tables['by_year'] = df.groupby(['year', 'gravity']).size().reset_index(name='count')
    
    # By department
    tables['by_department'] = df.groupby('dep').agg({
        'date': 'count',
        'is_fatal': 'sum',
        'is_severe': 'sum',
        'lat': 'first',
        'long': 'first'
    }).reset_index()
    tables['by_department'].columns = ['department', 'total_accidents', 'fatal', 'severe', 'lat', 'long']
    
    # By lighting
    tables['by_lighting'] = df.groupby(['lighting', 'gravity']).size().reset_index(name='count')
    
    # By infrastructure
    tables['by_infrastructure'] = df.groupby(['infrastructure', 'gravity']).size().reset_index(name='count')
    
    # By hour
    tables['by_hour'] = df.groupby(['hour', 'gravity']).size().reset_index(name='count')
    
    # By month and trip purpose (for seasonality)
    tables['by_month_purpose'] = df.groupby(['month_num', 'month_name', 'trip_purpose']).size().reset_index(name='count')
    
    # By age group
    tables['by_age'] = df.groupby(['age_group', 'gravity']).size().reset_index(name='count')
    
    return tables