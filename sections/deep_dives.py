"""
Deep Dive Analysis Section
Detailed temporal, weather, and infrastructure analysis.
"""

import streamlit as st
from streamlit_folium import st_folium
from utils import viz


def render(df_filtered, tables):
    """
    Render the deep dive analysis section with detailed visualizations.
    
    Parameters:
    -----------
    df_filtered : pd.DataFrame
        Filtered accident data based on sidebar selections
    tables : dict
        Dictionary containing reference tables (not used here, but kept for consistency)
    """
    
    st.title("🔬 Deep Dive Analysis")
    
    st.markdown("""
    This section explores in detail the temporal, weather, and infrastructure factors 
    that influence the severity of cycling accidents.
    """)
    
    # ========================================================================
    # 1. TEMPORAL PATTERNS
    # ========================================================================
    
    st.header("⏰ Temporal Patterns")
    
    st.markdown("""
    **Key Question**: When are cyclists most at risk?
    """)
    
    # Hourly distribution
    with st.container():
        fig_hourly = viz.plot_hourly_distribution(df_filtered)
        st.plotly_chart(fig_hourly, use_container_width=True)
        
        st.info("""
        **💡 Insights**:
        - **Accident peaks**: 8am (commute to work) and 5pm (return home)
        - **Low activity hours**: 2am-5am (very few cyclists)
        - **Severity**: Night accidents (8pm-6am) are proportionally more fatal
        """)
    
    # Day and season heatmap
    with st.container():
        fig_heatmap = viz.plot_day_season_heatmap(df_filtered)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        st.info("""
        **💡 Insights**:
        - **Weekdays**: Much more accidents (commuting trips)
        - **Weekends**: Fewer accidents but more leisure cycling
        - **Seasons**: Spring/Summer > Autumn/Winter (more cyclists on the road)
        """)
    
    st.markdown("---")
    
    # ========================================================================
    # 2. WEATHER & LIGHTING CONDITIONS
    # ========================================================================
    
    st.header("🌦️ Weather & Lighting Conditions")
    
    st.markdown("""
    **Key Question**: Under what conditions are accidents most severe?
    """)
    
    with st.container():
        fig_weather = viz.plot_weather_lighting_conditions(df_filtered)
        st.plotly_chart(fig_weather, use_container_width=True)
        
        st.warning("""
        **⚠️ Major risk factors**:
        - **Night without street lighting**: Fatality rate 2-3x higher
        - **Rain + Night**: Particularly dangerous combination
        - **Twilight**: Reduced visibility, drivers not adapted
        
        **Recommendation**: Reflective equipment and lighting are mandatory!
        """)
    
    st.markdown("---")
    
    # ========================================================================
    # 3. INFRASTRUCTURE ANALYSIS
    # ========================================================================
    
    st.header("🛣️ Infrastructure Analysis")
    
    st.markdown("""
    **Key Question**: Does cycling infrastructure truly protect cyclists?
    """)
    
    # Two columns for the infrastructure analysis
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        # Waffle chart - Road situation
        st.subheader("Road Situation Distribution")
        fig_waffle = viz.plot_waffle_situation(df_filtered)
        st.pyplot(fig_waffle)
        
        st.caption("""
        💡 Each square represents 1% of accidents in that situation.
        """)
    
    with col2:
        # Bar chart - Infrastructure effectiveness
        st.subheader("Cycling Infrastructure Effectiveness")
        fig_infra = viz.plot_bike_infrastructure_effectiveness(df_filtered)
        st.plotly_chart(fig_infra, use_container_width=True)
        
        st.caption("""
        💡 Global comparison: presence vs absence of cycling infrastructure.
        """)
    
    st.info("""
    **Key observations**:
    - **On roadway**: Most common but dangerous situation
    - **On bike path**: Significantly safer (more green squares)
    - **On shoulder**: Very dangerous (more red/orange squares)
    - **With infrastructure**: Dramatically reduces severe accidents
    """)
    
    st.success("""
    **✅ Infrastructure Analysis Conclusions**:
    1. **Separated bike lanes**: Significant reduction in severe accidents
    2. **On roadway**: Most frequent situation but much more dangerous
    3. **Shoulder cycling**: Highest risk situation (fast-moving vehicles)
    4. **Required investment**: Physical separation between bikes and cars is essential
    
    💡 **Policy recommendation**: Prioritize construction of physically separated bike lanes 
    on high-traffic routes to dramatically reduce cyclist fatalities.
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # 4. INTERACTIVE MAP
    # ========================================================================
    
    st.header("🗺️ Interactive Accident Map")
    
    st.markdown("""
    **Explore the geographic distribution** of accidents with this interactive map.  
    *Note: For performance reasons, a sample of 5,000 accidents is displayed.*
    """)
    
    # Display info about filters
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Accidents displayed", f"{min(len(df_filtered), 5000):,}")
    with col2:
        st.metric("Total dataset", f"{len(df_filtered):,}")
    with col3:
        sample_pct = (min(len(df_filtered), 5000) / len(df_filtered) * 100) if len(df_filtered) > 0 else 0
        st.metric("Sample %", f"{sample_pct:.1f}%")
    
    # Create and display map
    with st.spinner("Generating interactive map..."):
        folium_map = viz.create_interactive_map(df_filtered, sample_size=5000)
        st_folium(folium_map, width=None, height=600)
    
    st.info("""
    **💡 Map usage**:
    - **Zoom**: Double-click or use +/- buttons
    - **Clusters**: Click on circle groups to zoom in
    - **Details**: Click on a point to see accident information
    - **Colors**: Green (unharmed) → Yellow (minor) → Orange (hospitalized) → Red (killed)
    
    **Observations**:
    - High concentration in **major metropolitan areas** (Paris, Lyon, Marseille)
    - Severe accidents more frequent on **main road axes**
    - Rural areas: Fewer accidents but often more severe
    """)
    
    st.markdown("---")
    
    # ========================================================================
    # SUMMARY & KEY TAKEAWAYS
    # ========================================================================
    
    st.header("📊 Deep Dive Analysis Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Identified Risk Factors
        
        **Temporal**:
        - Rush hours (8am, 6pm)
        - Weekdays > weekends
        - Spring/Summer > Winter
        
        **Environmental**:
        - Night without street lighting
        - Rain + reduced visibility
        - Twilight (dangerous transition)
        
        **Infrastructure**:
        - Riding on roadway without protection
        - Shoulders (fast-moving vehicles)
        - Absence of separated bike lanes
        """)
    
    with col2:
        st.markdown("""
        ### ✅ Priority Recommendations
        
        **Short term**:
        1. Awareness campaigns for equipment (lights, vests)
        2. Improved street lighting on cycling routes
        3. 30 km/h zones in dense urban areas
        
        **Medium/Long term**:
        1. Construction of **physically separated** bike lanes
        2. Intersection improvements (high-risk zones)
        3. Continuous cycling route networks (avoid roadway)
        4. Traffic-calmed zones around schools/city centers
        """)
    
    st.success("""
    **🚴 Key message**: Cycling infrastructure that is physically separated 
    from motor vehicle traffic is the best way to **drastically reduce 
    the severity of accidents**. Investment in these facilities is cost-effective 
    both in human and economic terms (avoided healthcare costs).
    """)