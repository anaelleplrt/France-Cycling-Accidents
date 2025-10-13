"""
Introduction section for the cycling safety dashboard.
Presents the context, objectives, and research questions.
"""

import streamlit as st


def render(metadata):
    """
    Render the introduction section.
    
    Args:
        metadata (dict): Dataset metadata from get_data_info()
    """
    
    # ========================================================================
    # HOOK
    # ========================================================================
    
    st.markdown("## 🚴 Why Cycling Safety Matters ?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class='kpi-container'>
            <h3 style='color: #e74c3c; margin: 0;'>80,000+</h3>
            <p style='margin: 0;'>Cyclists injured</p>
            <p style='font-size: 0.9rem; color: #777;'>2005-2023</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='kpi-container'>
            <h3 style='color: #f39c12; margin: 0;'>18 years</h3>
            <p style='margin: 0;'>of data analyzed</p>
            <p style='font-size: 0.9rem; color: #777;'>Comprehensive study</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='kpi-container'>
            <h3 style='color: #27ae60; margin: 0;'>100%</h3>
            <p style='margin: 0;'>Open data</p>
            <p style='font-size: 0.9rem; color: #777;'>Transparent & reusable</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ========================================================================
    # CONTEXT
    # ========================================================================
    
    st.markdown("### 📖 Context")
    
    st.markdown("""
    Cycling has experienced a **significant boom in France** over the past two decades, 
    driven by environmental concerns, urban congestion, and health awareness. 
    
    However, this increase in cycling activity raises critical questions about **cyclist safety**. 
    Understanding accident patterns, risk factors, and vulnerable populations is essential 
    for policymakers, urban planners, and cyclists themselves.
    
    This dashboard analyzes **nearly two decades of bicycle accident data** from the 
    French national road accident database (BAAC), maintained by the National Interministerial 
    Road Safety Observatory (ONISR).
    """)
    
    # ========================================================================
    # RESEARCH QUESTIONS
    # ========================================================================
    
    st.markdown("### ❓ Key Research Questions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Temporal patterns:**
        - How have cycling accidents evolved over 18 years?
        - What is the impact of COVID-19 on accident rates?
        - When (time of day, season) are accidents most frequent?
        
        **Geographic patterns:**
        - Which departments are most dangerous for cyclists?
        - Are accidents more severe in urban or rural areas?
        """)
    
    with col2:
        st.markdown("""
        **Risk factors:**
        - What role do lighting conditions play in accident severity?
        - How does weather affect cycling safety?
        - Do bike lanes and infrastructure actually protect cyclists?
        
        **Victim profiles:**
        - Which age groups are most affected by cycling accidents?
        - Which age groups face the highest fatality rates?
        - Are there gender differences in accident severity and volume?
        """)
    
    # ========================================================================
    # OBJECTIVES
    # ========================================================================
    
    st.markdown("### 🎯 Dashboard Objectives")
    
    st.info("""
    **This interactive dashboard aims to:**
    
    1. **Identify high-risk conditions** that lead to severe cycling accidents
    2. **Reveal geographic disparities** in cycling safety across France
    3. **Understand temporal trends** and the impact of major events (e.g., COVID-19)
    4. **Profile vulnerable populations** requiring targeted safety measures
    5. **Provide actionable insights** for policymakers and urban planners
    6. **Raise awareness** among cyclists about risk factors they can control
    """)
    
    # ========================================================================
    # TARGET AUDIENCE
    # ========================================================================
    
    st.markdown("### 👥 Who Is This For?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🏛️ Policymakers**
        - Urban planners
        - Transport authorities
        - Safety regulators
        """)
    
    with col2:
        st.markdown("""
        **🚴 Cycling Advocates**
        - ONGs & associations
        - Community groups
        - Safety campaigners
        """)
    
    with col3:
        st.markdown("""
        **📊 Researchers**
        - Transport researchers
        - Data analysts
        - Students
        """)
    
    # ========================================================================
    # DATA SOURCE
    # ========================================================================
    
    st.markdown("### 📂 About the Data")
    
    st.markdown(f"""
    **Source:** {metadata['original_source']}
    
    **Dataset:** {metadata['dataset_name']}
    
    **Period covered:** {metadata['period']} (18 years)
    
    **Description:** {metadata['description']}
    
    **License:** {metadata['license']} - This data is freely reusable for academic 
    and non-commercial purposes with proper attribution.
    
    **URL:** [{metadata['url']}]({metadata['url']})
    """)
    
    st.warning("""
    ⚠️ **Important note:** Each row in the dataset represents **one person involved** 
    in a cycling accident. A single accident may involve multiple people (e.g., child 
    seat, group cycling), resulting in multiple rows. This is accounted for in our analysis.
    """)
    
    # ========================================================================
    # HOW TO USE THIS DASHBOARD
    # ========================================================================
    
    st.markdown("### 🧭 How to Navigate This Dashboard")
    
    st.markdown("""
    Use the **sidebar** on the left to:
    - 📖 Navigate between sections
    - 🎛️ Apply filters (year range, departments, severity, location type)
    - ℹ️ View dataset information
                """)
    
    st.info("""
    For the filter 'location type' : 
    - “In built-up area” → Analyzes only accidents in cities (urban)
    - “Outside built-up area” → Analyzes only accidents outside city (in rural areas)
            """)
                
    st.markdown("""
    **Recommended flow between sections :**
    1. **Data Quality** → Understand how the data was cleaned and its limitations
    2. **Overview** → Get high-level trends, key metrics, and geographic distribution map
    3. **Deep Dive Analysis** → Explore specific patterns in detail
    4. **Conclusions** → Review key insights and recommendations
    
    💡 **Tip:** Filters apply to all sections except Introduction and Data Quality.
    """)
    
    # ========================================================================
    # CALL TO ACTION
    # ========================================================================
    
    st.success("""
    **Ready to explore?** 
    
    Start by reviewing the **Data Quality** section to understand how the data 
    was processed, then dive into the **Overview** to see the big picture!
    """)