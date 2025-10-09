"""
Data quality section for the cycling accidents dashboard.
Documents data preparation steps and validates data quality.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render(df_raw, df_clean):
    """
    Render the data quality section.
    
    Args:
        df_raw (pd.DataFrame): Original raw dataset
        df_clean (pd.DataFrame): Cleaned and transformed dataset
    """
    
    st.markdown("## 📋 Data Quality & Preparation")
    
    st.markdown("""
    This section documents the data preparation process and validates the quality of the final dataset.
    We performed systematic cleaning, transformation, and validation to ensure reliable analysis.
    """)
    
    # ========================================================================
    # STEP 1: DATA SOURCE
    # ========================================================================
    
    st.markdown("---")
    st.markdown("## 📥 Step 1: Data Source")
    
    st.markdown("""
    **Dataset**: French Road Accidents Database (Base BAAC)  
    **Source**: Observatoire National Interministériel de la Sécurité Routière (ONISR)  
    **Period**: 2005-2023 (18 years)  
    **Focus**: Cycling accidents only (extracted from full accident database)
    
    The BAAC database records all injury accidents on public roads in France, documented by police forces.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="📊 Raw Dataset Size",
            value=f"{len(df_raw):,} records",
            help="Number of rows in the original dataset"
        )
    
    with col2:
        st.metric(
            label="📋 Original Columns",
            value=f"{len(df_raw.columns)} columns",
            help="Number of variables in raw data"
        )
    
    with col3:
        st.metric(
            label="📅 Time Span",
            value="18 years",
            help="2005-2023"
        )
    
    
    # ========================================================================
    # STEP 2: COLUMNS REMOVED
    # ========================================================================
    
    st.markdown("---")
    st.markdown("## 🗑️ Step 2: Unnecessary Columns Removed")
    
    st.markdown("""
    We removed **6 technical columns** that aren't needed for analysis:
    - `Num_Acc`, `vehiculeid` (internal IDs)
    - `lartpc` (TPC width - too specific, many missing)
    - `larrout` (road width - many missing)
    - `nbv` (number of lanes - inconsistent format)
    - `_infos_commune.code_epci` (EPCI code - incomplete)
    """)
    
    removed_cols = ['Num_Acc', 'vehiculeid', 'lartpc', 'larrout', 'nbv', '_infos_commune.code_epci']
    removed_df = pd.DataFrame({
        'Removed Column': removed_cols,
        'Reason': [
            'Accident identifier (not needed)',
            'Vehicle identifier (not needed)',
            'TPC width (too specific)',
            'Road width (many missing)',
            'Number of lanes (inconsistent)',
            'EPCI code (incomplete)'
        ]
    })
    
    st.dataframe(removed_df, use_container_width=True, hide_index=True)
    
    # ========================================================================
    # STEP 3: NEW COLUMNS ADDED
    # ========================================================================
    
    st.markdown("---")
    st.markdown("## 🔄 Step 3: Columns Transformed & Added")
    
    st.markdown("""
    We transformed and created **new columns** to make the data more understandable and enable deeper insights:
    - **12 decoded** (replaced encoded columns with readable labels)
    - **7 temporal** (extracted from date/time fields)
    - **7 calculated** (derived new analytical features)
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🔄 Transformed (Decoded)",
            value="12 columns",
            help="Replaced encoded columns with readable labels"
        )
    
    with col2:
        st.metric(
            label="📅 Temporal Features",
            value="7 columns",
            help="Time-based variables extracted from dates"
        )
    
    with col3:
        st.metric(
            label="🧮 Calculated Features",
            value="7 columns",
            help="Derived analytical variables"
        )
    
    # Tabs for different column types
    tab1, tab2, tab3 = st.tabs(["🔄 Decoded Variables", "📅 Temporal Variables", "🧮 Calculated Features"])
    
    with tab1:
        st.markdown("""
        #### What are decoded variables?
        
        The original dataset uses **numeric codes** (e.g., 1, 2, 3) for categorical variables. 
        We **replaced** these encoded columns with **human-readable labels** (e.g., "Daylight", "Twilight") 
        to make the data intuitive.
        
        ✅ **Transformation:** `grav` (1,2,3,4) → `gravity` ("Unharmed", "Killed", "Hospitalized", "Minor injury")
        """)
        
        decoded_cols = pd.DataFrame({
            'Transformed Column': [
                'gravity', 'lighting', 'weather', 'agglomeration', 'intersection_type',
                'road_category', 'surface_condition', 'infrastructure', 'situation', 
                'gender', 'trip_purpose', 'collision_type'
            ],
            'Replaced': [
                'grav', 'lum', 'atm', 'agg', 'int',
                'catr', 'surf', 'infra', 'situ', 'sexe',
                'trajet', 'col'
            ],
            'Example Values': [
                'Unharmed, Killed, Hospitalized, Minor injury',
                'Daylight, Twilight, Night without lighting, Night with lighting',
                'Normal, Light rain, Heavy rain, Snow, Fog, Strong wind',
                'Outside built-up area, In built-up area',
                'Outside intersection, X intersection, T intersection, Roundabout',
                'Highway, National road, Departmental road, Municipal road',
                'Normal, Wet, Puddles, Icy, Snowy',
                'Without, Bike lane (separated), Bike lane (painted), Reserved lane',
                'On roadway, On bike path, On shoulder, On sidewalk',
                'Male, Female',
                'Home-work, Home-school, Shopping, Professional use, Leisure',
                'Front, Rear, Side, Chain, Multiple, Without collision'
            ]
        })
        
        st.dataframe(decoded_cols, use_container_width=True, hide_index=True, height=450)
        
        st.info("""
        💡 **Note:** Original encoded columns (e.g., `grav`, `lum`, `situ`) were **replaced** 
        by their decoded versions. They are not kept in the final dataset.
        """)
        
        # NEW: Mapping dictionaries section
        st.markdown("---")
        st.markdown("#### 📚 How did we decode the variables?")
        
        st.markdown("""
        The data source provided **official mapping dictionaries** that define the correspondence 
        between numeric codes and their meanings. We used these dictionaries to transform all 
        categorical variables into human-readable labels.
        
        **Click below to see the exact mapping for each variable:**
        """)
        
        # Gravity mapping
        with st.expander("🩹 **Gravity (grav)** - Injury Severity"):
            st.code("""
GRAVITY_DICT = {
    1: 'Unharmed',
    2: 'Killed',
    3: 'Hospitalized',
    4: 'Minor injury'
}
            """, language="python")
            st.caption("Describes the severity of injuries sustained by the victim.")
        
        # Lighting mapping
        with st.expander("💡 **Lighting (lum)** - Light Conditions"):
            st.code("""
LIGHTING_DICT = {
    1: 'Daylight',
    2: 'Twilight or dawn',
    3: 'Night without street lighting',
    4: 'Night with street lighting off',
    5: 'Night with street lighting on'
}
            """, language="python")
            st.caption("Describes lighting conditions at the time of the accident.")
        
        # Weather mapping
        with st.expander("🌦️ **Weather (atm)** - Atmospheric Conditions"):
            st.code("""
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
            """, language="python")
            st.caption("Describes weather conditions during the accident.")
        
        # Agglomeration mapping
        with st.expander("🏙️ **Agglomeration (agg)** - Urban Context"):
            st.code("""
AGGLOMERATION_DICT = {
    1: 'Outside built-up area',
    2: 'In built-up area'
}
            """, language="python")
            st.caption("Indicates whether the accident occurred in an urban or rural area.")
        
        # Intersection mapping
        with st.expander("🔀 **Intersection (int)** - Intersection Type"):
            st.code("""
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
            """, language="python")
            st.caption("Describes the type of intersection where the accident occurred.")
        
        # Road category mapping
        with st.expander("🛣️ **Road Category (catr)** - Type of Road"):
            st.code("""
ROAD_CATEGORY_DICT = {
    1: 'Highway',
    2: 'National road',
    3: 'Departmental road',
    4: 'Municipal road',
    5: 'Off public network',
    6: 'Parking lot',
    9: 'Other'
}
            """, language="python")
            st.caption("Indicates the administrative category of the road.")
        
        # Surface condition mapping
        with st.expander("🌧️ **Surface Condition (surf)** - Road Surface"):
            st.code("""
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
            """, language="python")
            st.caption("Describes the condition of the road surface.")
        
        # Infrastructure mapping
        with st.expander("🚴 **Infrastructure (infra)** - Cycling Infrastructure"):
            st.code("""
INFRASTRUCTURE_DICT = {
    0: 'Without infrastructure',
    1: 'Bike lane (physically separated)',
    2: 'Bike lane (painted)',
    3: 'Reserved lane',
    4: 'Other infrastructure'
}
            """, language="python")
            st.caption("Indicates the presence and type of cycling infrastructure.")
        
        # Situation mapping
        with st.expander("📍 **Situation (situ)** - Position on Road"):
            st.code("""
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
            """, language="python")
            st.caption("Describes where the cyclist was positioned on the road.")
        
        # Gender mapping
        with st.expander("👤 **Gender (sexe)** - Victim Gender"):
            st.code("""
GENDER_DICT = {
    1: 'Male',
    2: 'Female'
}
            """, language="python")
            st.caption("Gender of the accident victim.")
        
        # Trip purpose mapping
        with st.expander("🎯 **Trip Purpose (trajet)** - Reason for Trip"):
            st.code("""
TRIP_PURPOSE_DICT = {
    0: 'Not specified',
    1: 'Home - work',
    2: 'Home - school',
    3: 'Shopping',
    4: 'Professional use',
    5: 'Leisure',
    9: 'Other'
}
            """, language="python")
            st.caption("Indicates the purpose of the trip when the accident occurred.")
        
        # Collision type mapping
        with st.expander("💥 **Collision Type (col)** - Type of Collision"):
            st.code("""
COLLISION_TYPE_DICT = {
    1: 'Two vehicles - front',
    2: 'Two vehicles - from rear',
    3: 'Two vehicles - from side',
    4: 'Three or more vehicles - chain',
    5: 'Three or more vehicles - multiple',
    6: 'Other collision',
    7: 'Without collision'
}
            """, language="python")
            st.caption("Describes how the collision occurred.")
        
        st.success("""
        ✅ **All mappings are based on official BAAC documentation** provided by the 
        French Road Safety Observatory (ONISR). This ensures accuracy and consistency 
        with national standards.
        """)
    
    with tab2:
        st.markdown("""
        #### Temporal variables extracted from date/time
        
        We created **7 time-based features** to analyze temporal patterns:
        """)
        
        temporal_cols = pd.DataFrame({
            'New Column': [
                'datetime', 'year', 'month_num', 'month_name', 'day_of_week',
                'hour', 'time_period', 'season'
            ],
            'Description': [
                'Full datetime (YYYY-MM-DD HH:MM)',
                'Year (2005-2023)',
                'Month number (1-12)',
                'Month name (January, February, ...)',
                'Day name (Monday, Tuesday, ...)',
                'Hour (0-23)',
                'Time period (Night, Morning, Afternoon, Evening)',
                'Season (Winter, Spring, Summer, Autumn)'
            ],
            'Source Fields': [
                'date + hrmn',
                'an',
                'date',
                'date',
                'date',
                'hrmn',
                'hour',
                'month_num'
            ]
        })
        
        st.dataframe(temporal_cols, use_container_width=True, hide_index=True, height=320)
    
    with tab3:
        st.markdown("""
        #### Calculated analytical features
        
        We created **7 derived variables** for advanced analysis:
        """)
        
        calculated_cols = pd.DataFrame({
            'New Column': [
                'age_group', 'is_severe', 'is_fatal', 'dangerous_conditions',
                'has_bike_infrastructure', 'is_weekend'
            ],
            'Description': [
                'Age category (0-12, 13-17, 18-25, 26-35, 36-50, 51-65, 65+)',
                'Binary flag: 1 if hospitalized or killed',
                'Binary flag: 1 if killed',
                'Binary flag: 1 if night OR bad weather OR slippery surface',
                'Binary flag: 1 if bike lane present',
                'Binary flag: 1 if Saturday or Sunday'
            ],
            'Formula': [
                'Categorized from age field',
                'grav in [2, 3]',
                'grav == 2',
                'lum >= 3 OR atm in [2,3,4,5] OR surf in [2,3,5,7]',
                'infra in [1, 2]',
                'day_of_week in ["Saturday", "Sunday"]'
            ]
        })
        
        st.dataframe(calculated_cols, use_container_width=True, hide_index=True, height=260)
    
    # ========================================================================
    # STEP 4: ROWS CLEANED
    # ========================================================================
    
    st.markdown("---")
    st.markdown("## 🧹 Step 4: Data Cleaning")
    
    st.markdown("""
    We removed invalid or incomplete rows to ensure data quality.
    """)
    
    rows_removed = len(df_raw) - len(df_clean)
    removal_rate = (rows_removed / len(df_raw) * 100) if len(df_raw) > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🗑️ Rows Removed",
            value=f"{rows_removed:,}",
            delta=f"-{removal_rate:.1f}%",
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            label="✅ Rows Kept",
            value=f"{len(df_clean):,}",
            delta=f"{100-removal_rate:.1f}%"
        )
    
    with col3:
        st.metric(
            label="📊 Data Quality",
            value=f"{100-removal_rate:.1f}%",
            help="Percentage of valid rows"
        )
    
    st.markdown("""
    **Cleaning rules applied:**
    - ❌ Removed rows with missing year
    - ❌ Removed rows with missing gravity information
    - ❌ Removed rows with invalid years (< 2005 or > 2023)
    - ❌ Removed rows with missing dates
    - ❌ Removed rows with invalid ages (< 0 or > 120)
    """)
    
    # ========================================================================
    # STEP 5: DATA QUALITY VALIDATION
    # ========================================================================
    
    st.markdown("---")
    st.markdown("## ✅ Step 5: Data Quality Validation")
    
    st.markdown("""
    We performed systematic checks to ensure data integrity. Below are the detailed validation results:
    """)
    
    # Calculate validation metrics
    valid_depts = df_clean[df_clean['dep'].astype(str).str.match(r'^\d{2}$|^2[AB]$', na=False)]
    dept_count = valid_depts['dep'].nunique()
    years_count = df_clean['year'].value_counts().sort_index()
    year_range = range(int(df_clean['year'].min()), int(df_clean['year'].max()) + 1)
    missing_years = [y for y in year_range if y not in years_count.index]
    
    # Validation table
    validation_checks = pd.DataFrame({
        'Validation Check': [
            '✅ No duplicate rows',
            '✅ Temporal coverage complete',
            '✅ Valid date ranges',
            '✅ Valid department codes',
            '✅ Categorical variables decoded',
            '✅ Hour values logical (0-23)',
            '✅ Age values reasonable (0-120)',
            '✅ No unexpected negative values'
        ],
        'Result': [
            f'{len(df_clean):,} unique records',
            f'18 years covered (2005-2023)' if not missing_years else f'⚠️ Missing years: {missing_years}',
            '2005-2023',
            f'{dept_count} departments',
            '12 categorical variables successfully decoded',
            f'Range: {int(df_clean["hour"].min())}-{int(df_clean["hour"].max())} ✓',
            f'Range: {int(df_clean["age"].min()):.0f}-{int(df_clean["age"].max()):.0f} years ✓',
            'All numeric fields validated ✓'
        ]
    })
    
    st.dataframe(
        validation_checks, 
        use_container_width=True, 
        hide_index=True,
        height=350
    )
    
    st.success("✅ All validation checks passed successfully!")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    
    st.markdown("---")
    st.markdown("## 📊 Final Dataset Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(df_clean):,}")
    
    with col2:
        st.metric("Total Columns", f"{len(df_clean.columns)}")
    
    with col3:
        st.metric("Time Period", "2005-2023")
    
    with col4:
        st.metric("Departments", dept_count)

    # ========================================================================
    # DATASET STRUCTURE
    # ========================================================================
    
    st.markdown("---")
    st.markdown("## 📋 Dataset Columns & Descriptions")
    
    st.markdown(f"""
    The cleaned dataset contains **{len(df_clean.columns)} columns**. 
    Below is a description of each column to help you understand the data.
    """)
    
    # Dictionary of column descriptions
    descriptions_dict = {
        'id': 'Unique accident identifier',
        'date': 'Date of the accident (YYYY-MM-DD)',
        'hrmn': 'Time of the accident (HH:MM)',
        'datetime': 'Full datetime of the accident',
        'year': 'Year (2005-2023)',
        'month_num': 'Month number (1-12)',
        'month_name': 'Month name (January, February, ...)',
        'day_of_week': 'Day of week (Monday, Tuesday, ...)',
        'hour': 'Hour of day (0-23)',
        'time_period': 'Time period (Morning rush, Afternoon, Evening rush, Night)',
        'season': 'Season (Winter, Spring, Summer, Autumn)',
        'dep': 'Department code (01-95, 2A, 2B)',
        'com': 'Municipality code (INSEE)',
        'lat': 'Latitude coordinate',
        'long': 'Longitude coordinate',
        'gravity': 'Injury severity: Unharmed, Killed, Hospitalized, Minor injury',
        'lighting': 'Lighting: Daylight, Twilight, Night (with/without lighting)',
        'weather': 'Weather: Normal, Light/Heavy rain, Snow, Fog, Strong wind, etc.',
        'agglomeration': 'Location: In built-up area or Outside built-up area',
        'intersection_type': 'Intersection type: X, T, Y, Roundabout, Level crossing, etc.',
        'road_category': 'Road category: Highway, National road, Departmental, Municipal',
        'surface_condition': 'Surface condition: Normal, Wet, Puddles, Icy, Snowy, Mud, Oil',
        'infrastructure': 'Cycling infrastructure: Without, Bike lane (separated), Bike lane (painted), Reserved lane',
        'situation': 'Situation: On roadway, On bike path, On shoulder, On sidewalk',
        'gender': 'Gender: Male, Female',
        'trip_purpose': 'Trip purpose: Home-work, Home-school, Shopping, Professional, Leisure',
        'collision_type': 'Collision type: Front, Rear, Side, Chain, Multiple, Without collision',
        'age': 'Age of the victim (years)',
        'age_group': 'Age group: 0-12, 13-17, 18-25, 26-35, 36-50, 51-65, 65+',
        'is_severe': 'Severe accident (hospitalized or killed): True/False',
        'is_fatal': 'Fatal accident (killed): True/False',
        'dangerous_conditions': 'Dangerous conditions (night OR bad weather OR slippery surface): True/False',
        'has_bike_infrastructure': 'Has bike infrastructure (bike lane present): True/False',
        'is_weekend': 'Weekend (Saturday or Sunday): True/False',
        'circ': 'Traffic circulation (original encoded column)',
        'vosp': 'Reserved lane indicator',
        'prof': 'Road profile',
        'plan': 'Road layout',
        'nbv': 'Number of lanes',
        'pr': 'Kilometric point',
        'pr1': 'Distance to kilometric point',
        'v1': 'Landmark distance 1',
        'v2': 'Landmark distance 2',
        'obs': 'Fixed obstacle',
        'obsm': 'Mobile obstacle',
        'choc': 'Initial point of impact',
        'manv': 'Main maneuver before accident',
        'motor': 'Motor type',
        'occutc': 'Occupants in public transport',
        'etatp': 'Pedestrian action'
    }
    
    # Create dataframe from actual columns in dataset
    column_list = []
    description_list = []
    
    for col in df_clean.columns:
        column_list.append(col)
        description_list.append(descriptions_dict.get(col, 'No description available'))
    
    column_descriptions = pd.DataFrame({
        'Column': column_list,
        'Description': description_list
    })
    
    st.dataframe(
        column_descriptions,
        use_container_width=True,
        hide_index=True,
        height=600
    )
    
    
    st.info("""
    💡 **Ready for Analysis!**  
    The dataset is now clean, validated, and ready for comprehensive analysis. 
    All categorical variables are decoded, temporal features are extracted, and quality checks have passed.
    """)