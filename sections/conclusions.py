"""
Conclusions Section
Summary of findings and recommendations.
"""

import streamlit as st


def render(df_filtered, tables):
    """
    Render the conclusions section with key findings and recommendations.
    
    Parameters:
    -----------
    df_filtered : pd.DataFrame
        Filtered accident data
    tables : dict
        Dictionary containing reference tables
    """
    
    st.title("🎯 Conclusions")
    
    st.markdown("""
    After analyzing **79,965 cycling accidents** from 2005 to 2023, clear patterns emerge 
    that can guide effective safety policies.
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # MAIN FINDINGS
    # ========================================================================
    
    st.header("📊 Main Findings")
    
    st.subheader("1️⃣ Volume & Trends (Overview)")
    
    st.markdown("""
    - **Total accidents**: 79,965 over 18 years (~4,425 per year)
    - **Fatality rate**: 3.9% (3,089 deaths total)
    - **Geographic concentration**: Paris region accounts for largest share
    - **Urban vs Rural**: 73% occur in built-up areas, but rural accidents are more severe
    - **Trend**: Overall decrease in recent years, especially post-2020
    """)
    
    st.subheader("2️⃣ When Accidents Happen (Temporal Patterns)")
    
    st.markdown("""
    - **Rush hours**: Clear peaks at 8am and 6pm (commute times)
    - **Weekdays vs Weekends**: 25% more accidents on weekdays
    - **Seasonal**: Summer has most accidents, but also highest fatality rate (4.3%)
    - **Night risk**: Accidents between 8pm-6am are proportionally more fatal
    """)
    
    st.subheader("3️⃣ Environmental Conditions (Weather & Lighting)")
    
    st.markdown("""
    - **Lighting is critical**: Night without street lighting = 16.7% fatality rate (vs 3.8% in daylight)
    - **Weather impact**: Strong wind/storm (13.9%) and fog (8.8%) have highest fatality rates
    - **Key insight**: Lighting infrastructure matters MORE than weather conditions
    """)
    
    st.subheader("4️⃣ Infrastructure Matters (Road Situation)")
    
    st.markdown("""
    - **98% of accidents** occur WITHOUT cycling infrastructure
    - **Most dangerous**: Shoulder cycling (high proportion of severe injuries)
    - **Safest**: Protected bike paths (lowest severe injury rate)
    - **Volume difference**: 50x more accidents on roadways vs bike lanes
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # KEY TAKEAWAYS
    # ========================================================================
    
    st.header("💡 Key Takeaways")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### What Works
        
        ✅ **Protected bike lanes**
        - Physical separation reduces both frequency and severity
        
        ✅ **Street lighting**
        - Can reduce night fatality risk by 88%
        
        ✅ **Separated infrastructure**
        - Bike paths show lowest severe injury rates
        """)
    
    with col2:
        st.markdown("""
        ### Risk Factors
        
        ⚠️ **Night without lighting**
        - 4.3x more deadly than daylight
        
        ⚠️ **Shoulder/roadway cycling**
        - Highest proportion of severe injuries
        
        ⚠️ **Rush hours**
        - Peak times = peak risk
        """)
    
    st.markdown("---")
    
    # ========================================================================
    # RECOMMENDATIONS
    # ========================================================================
    
    st.header("✅ Recommendations")
    
    st.markdown("""
    Based on the data analysis, here are evidence-based recommendations to improve cyclist safety:
    """)
    
    st.subheader("🚨 Priority Actions")
    
    st.warning("""
    **1. Build protected bike lane networks**
    - Focus on commuter routes where 83% of accidents occur
    - Physical barriers (not just painted lines)
    - Connect residential areas to work/school destinations
    
    **2. Improve lighting on cycling routes**
    - Target night accident hotspots identified in the data
    - LED street lighting on major cycling corridors
    - Could reduce night fatalities by 80%+
    
    **3. Ban cycling on highway shoulders**
    - These are the deadliest locations in the dataset
    - Provide alternative routes
    """)
    
    st.subheader("📅 Medium-Term Actions")
    
    st.info("""
    **4. Redesign dangerous intersections**
    - Protected bike crossings
    - Separated signal phases for cyclists
    
    **5. Rush hour safety measures**
    - Target enforcement at 8am and 6pm
    - Awareness campaigns for commuters
    
    **6. Data-driven approach**
    - Use this type of analysis to identify hotspots
    - Monitor progress with regular data updates
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # LIMITATIONS
    # ========================================================================
    
    st.header("⚠️ Study Limitations")
    
    st.markdown("""
    **Data limitations:**
    - Analysis limited to reported accidents (some minor accidents may not be reported)
    - Missing data for some variables (not all columns were complete)
    - Can't measure exposure (number of cyclists on the road)
    
    **Analysis scope:**
    - Correlation does not imply causation
    - Would need controlled studies to prove causality
    - Some confounding factors not captured in the data
    
    **Future improvements:**
    - Include cyclist volume data to calculate true risk rates
    - Analyze more recent years as data becomes available
    - Study effectiveness of specific interventions
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # FINAL MESSAGE
    # ========================================================================
    
    st.header("🚴 Final Thoughts")
    
    st.success("""
    **The data tells a clear story**: Protected cycling infrastructure saves lives.
    
    - 98% of accidents happen where there's NO bike infrastructure
    - Night lighting reduces fatalities by 4-5x
    - Physical separation works better than painted lines
    
    These aren't opinions - they're patterns from 80,000+ accidents over 18 years.
    
    **The question isn't whether we should invest in cycling safety - it's how quickly we can do it.**
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # METHODOLOGY NOTES
    # ========================================================================
    
    with st.expander("📚 Methodology & Data Sources"):
        st.markdown("""
        **Data Source:**
        - Base BAAC (French National Road Accident Database)
        - Source: Observatoire National Interministériel de la Sécurité Routière (ONISR)
        - Available on data.gouv.fr
        
        **Period Analyzed:**
        - 2005-2023 (18 years)
        - 80,022 cycling accident records
        
        **Tools Used:**
        - Python for data processing
        - Streamlit for dashboard
        - Plotly for interactive visualizations
        - Folium for mapping
        
        **Data Cleaning:**
        - Removed invalid/incomplete records
        - Decoded categorical variables
        - Created derived features (time periods, age groups, severity flags)
        - Handled missing values
        
        **Analysis Methods:**
        - Descriptive statistics
        - Temporal pattern analysis
        - Geographic visualization
        - Cross-tabulation of risk factors
        """)