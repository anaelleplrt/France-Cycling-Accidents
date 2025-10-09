"""
Deep Dive Analysis Section
Detailed temporal, weather, and infrastructure analysis.
"""

import streamlit as st
from streamlit_folium import st_folium
from utils import viz


def render(df_filtered, tables, year_range=None, selected_departments=None, selected_gravity=None, selected_agglomeration=None):
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

    # Check if any filter is active
    filters_active = (
        (year_range is not None and year_range != (df_filtered['year'].min(), df_filtered['year'].max())) or
        (selected_departments is not None and selected_departments != ['All']) or
        (selected_gravity is not None and selected_gravity != ['All']) or
        (selected_agglomeration is not None and selected_agglomeration != 'All')
    )
    
    # Hourly distribution
    with st.container():
        fig_hourly = viz.plot_hourly_distribution(df_filtered)
        st.plotly_chart(fig_hourly, use_container_width=True)
        
        # Calculate hourly stats
        hourly_stats = df_filtered.groupby('hour').agg(
            total=('hour', 'size'),
            fatal=('is_fatal', 'sum')
        )
        hourly_stats['fatal_rate'] = (hourly_stats['fatal'] / hourly_stats['total'] * 100).round(1)
        
        peak_hour = hourly_stats['total'].idxmax()
        peak_count = hourly_stats['total'].max()
        lowest_hour = hourly_stats['total'].idxmin()
        most_dangerous_hour = hourly_stats['fatal_rate'].idxmax()
        most_dangerous_rate = hourly_stats['fatal_rate'].max()
        
        if filters_active:
            # DYNAMIC ANALYSIS
            st.info(f"""
            **💡 Insights** ({len(df_filtered):,} accidents in selection):
            - **Peak hour**: {peak_hour}h ({peak_count:,} accidents)
            - **Lowest activity**: {lowest_hour}h (fewest cyclists)
            - **Most dangerous hour**: {most_dangerous_hour}h ({most_dangerous_rate:.1f}% fatality rate)
            
            💡 Blue line shows volume, red dashed line shows fatality rate.
            """)
        else:
            # GLOBAL ANALYSIS
            st.info("""
            **💡 Insights**:
            - **Accident peaks**: 8am (commute to work) and 6pm (return home)
            - **Low activity hours**: 2am-5am (very few cyclists)
            - **Severity**: Night accidents (8pm-6am) are proportionally more fatal
            
            **Rush hour risk**: Morning and evening commutes concentrate both volume AND risk.
            """)
    
    # Weekly and seasonal patterns (two separate charts)
    col1, col2 = st.columns(2)
    
    with col1:
        fig_weekly = viz.plot_weekly_pattern(df_filtered)
        st.plotly_chart(fig_weekly, use_container_width=True)
        
    
    with col2:
        fig_seasonal = viz.plot_seasonal_pattern(df_filtered)
        st.plotly_chart(fig_seasonal, use_container_width=True)
        st.caption("""
        💡 **Interactive features**: 
        - **Hover** over bars to see exact numbers for each severity level
        - **Click on legend items** (Hospitalized, Killed, etc.) to show/hide categories
        - **Double-click legend** to isolate a single severity level
        """)
    
    # Calculate actual seasonal totals AND severity rates
    seasonal_stats = df_filtered.groupby('season').agg(
        total=('season', 'size'),
        fatal=('is_fatal', 'sum'),
        severe=('is_severe', 'sum')
    )
    seasonal_stats['fatal_rate'] = (seasonal_stats['fatal'] / seasonal_stats['total'] * 100).round(1)
    seasonal_stats['severe_rate'] = (seasonal_stats['severe'] / seasonal_stats['total'] * 100).round(1)
    
    seasonal_totals = seasonal_stats.sort_values('total', ascending=False)
    highest_season = seasonal_totals.index[0]
    highest_count = seasonal_totals.loc[highest_season, 'total']
    lowest_season = seasonal_totals.index[-1]
    lowest_count = seasonal_totals.loc[lowest_season, 'total']
    
    # Find most/least dangerous seasons by severity
    most_dangerous_season = seasonal_stats['fatal_rate'].idxmax()
    most_dangerous_rate = seasonal_stats['fatal_rate'].max()
    safest_season = seasonal_stats['fatal_rate'].idxmin()
    safest_rate = seasonal_stats['fatal_rate'].min()
    
    # Weekly stats
    weekly_stats = df_filtered.groupby('day_of_week').size()
    peak_day = weekly_stats.idxmax()
    peak_count = weekly_stats.max()
    
    # Check if filters are active
    if filters_active:
        # DYNAMIC ANALYSIS (with filters)
        st.info(f"""
        **📊 Temporal Analysis** ({len(df_filtered):,} accidents in selection):
        
        **Weekly pattern**:
        - Peak day: **{peak_day}** ({peak_count:,} accidents)
        - Weekday vs weekend distribution visible in the chart
        
        **Seasonal pattern**:
        - Most accidents: **{highest_season}** ({highest_count:,} accidents)
        - Least accidents: **{lowest_season}** ({lowest_count:,} accidents)
        - Fatality rates: {most_dangerous_season} is deadliest ({most_dangerous_rate:.1f}%)
        
        💡 Adjust filters (year, department, severity) to explore specific temporal patterns.
        """)
    else:
        # GLOBAL DETAILED ANALYSIS (no filters)
        st.info(f"""
        **💡 Temporal Insights** ({len(df_filtered):,} accidents analyzed):
        
        **Weekly patterns**:
        - **Weekdays (Mon-Fri)**: Higher accident volume - commuting traffic dominates
        - **Peak risk**: Mid-week days (Tue-Thu) show highest accident counts
        - **Weekend (Sat-Sun)**: ~25% drop - more leisure cycling, less commuter traffic
        
        **Seasonal patterns - Volume**:
        - **{highest_season}**: Highest volume ({highest_count:,} accidents) - peak cycling season
        - **{lowest_season}**: Lowest volume ({lowest_count:,} accidents) - weather deterrent
        
        **Seasonal patterns - Severity**:
        - **Most dangerous**: {most_dangerous_season} ({most_dangerous_rate:.1f}% fatality rate). Possible factors: faster speeds in good weather, more inexperienced cyclists (tourists), or sun glare reducing visibility.
        - **Safest**: {safest_season} ({safest_rate:.1f}% fatality rate)
        """)
    

    st.markdown("---")
    
    # ========================================================================
    # 2. WEATHER & LIGHTING CONDITIONS
    # ========================================================================
    
    st.header("🌦️ Weather & Lighting Conditions")
    
    st.markdown("""
    **Key Question**: Under what conditions are accidents most fatale?
    """)
    
    with st.container():
        fig_weather = viz.plot_weather_lighting_conditions(df_filtered)
        st.plotly_chart(fig_weather, use_container_width=True)
        
    # Check if any filter is active
        filters_active = (
            (year_range is not None and year_range != (df_filtered['year'].min(), df_filtered['year'].max())) or
            (selected_departments is not None and selected_departments != ['All']) or
            (selected_gravity is not None and selected_gravity != ['All']) or
            (selected_agglomeration is not None and selected_agglomeration != 'All')
        )
        
        if filters_active:
            # ANALYSE DYNAMIQUE (quand filtres actifs)
            lighting_stats = df_filtered.groupby('lighting').agg(
                total=('lighting', 'size'),
                fatal=('is_fatal', 'sum')
            )
            lighting_stats['fatal_rate'] = (lighting_stats['fatal'] / lighting_stats['total'] * 100).round(1)
            
            weather_stats = df_filtered.groupby('weather').agg(
                total=('weather', 'size'),
                fatal=('is_fatal', 'sum')
            )
            weather_stats['fatal_rate'] = (weather_stats['fatal'] / weather_stats['total'] * 100).round(1)
            
            worst_lighting = lighting_stats['fatal_rate'].idxmax()
            worst_lighting_rate = lighting_stats['fatal_rate'].max()
            worst_weather = weather_stats['fatal_rate'].idxmax()
            worst_weather_rate = weather_stats['fatal_rate'].max()
            
            st.info(f"""
            **📊 Analysis for filtered selection** ({len(df_filtered):,} accidents):
            
            **Lighting conditions**:
            - Most dangerous: **{worst_lighting}** ({worst_lighting_rate:.1f}% fatality rate)
            - Total accidents in worst lighting: {lighting_stats.loc[worst_lighting, 'total']:,}
            
            **Weather conditions**:
            - Most dangerous: **{worst_weather}** ({worst_weather_rate:.1f}% fatality rate)
            - Total accidents in worst weather: {weather_stats.loc[worst_weather, 'total']:,}
            
            💡 Use filters to explore specific conditions (year, department, etc.)
            """)
        else:
            # ANALYSE GLOBALE (par défaut, sans filtres)
            st.info("""
            **💡Weather & Lighting Conditions Insights**:
            
            **Lighting is the dominant risk factor**:
            - **Night without street lighting**: 16.7% fatality rate - **4.3x higher** than daylight (3.8%)
            - **Night with lighting off**: 6.0% fatality rate - still dangerous
            - **Twilight/Dawn**: 3.8% - transition period creates visibility issues
            - **Night with lighting on**: Only 1.9% - infrastructure makes a difference
            
            **Weather amplifies the risk**:
            - **Strong wind/storm**: 13.9% fatality rate - destabilizes cyclists
            - **Fog/smoke**: 8.8% - severely reduced visibility
            - **Dazzling weather**: 8.4% - sun glare impairs vision
            - **Heavy rain**: 4.7% - wet surfaces + reduced visibility
            - **Normal weather**: 3.8% baseline - but still represents most accidents

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
    **💡 How to read the waffle chart**: Each 10×10 grid represents 100% of accidents for that road situation. Each square represents 1% of accidents in that situation.
    
    Colors show severity distribution: 🟢 Green (unharmed) → 🟡 Yellow (minor) → 🟠 Orange (hospitalized) → 🔴 Red (killed).
    
    **Key insight**: Compare the color patterns - more green = safer infrastructure.
    """)
    
    with col2:
        # Bar chart - Infrastructure effectiveness
        st.subheader("Cycling Infrastructure Effectiveness")
        fig_infra = viz.plot_bike_infrastructure_effectiveness(df_filtered)
        st.plotly_chart(fig_infra, use_container_width=True)
        
        st.caption("""
        💡 Global comparison: presence vs absence of cycling infrastructure.
        """)
    
# Detailed analysis below the charts
    st.markdown("---")

    
    # Check if filters are active
    filters_active = (
        (year_range is not None and year_range != (df_filtered['year'].min(), df_filtered['year'].max())) or
        (selected_departments is not None and selected_departments != ['All']) or
        (selected_gravity is not None and selected_gravity != ['All']) or
        (selected_agglomeration is not None and selected_agglomeration != 'All')
    )
    
    if filters_active:
        # DYNAMIC ANALYSIS (when filters active)
        # Calculate severity distribution by situation
        situation_severity = df_filtered.groupby(['situation', 'gravity']).size().unstack(fill_value=0)
        situation_totals = situation_severity.sum(axis=1)
        situation_pct = situation_severity.div(situation_totals, axis=0) * 100
        
        # Calculate "danger score" (killed + hospitalized %)
        if 'Killed' in situation_pct.columns and 'Hospitalized' in situation_pct.columns:
            situation_pct['danger_score'] = situation_pct['Killed'] + situation_pct['Hospitalized']
        elif 'Killed' in situation_pct.columns:
            situation_pct['danger_score'] = situation_pct['Killed']
        else:
            situation_pct['danger_score'] = 0
            
        # Calculate "safety score" (unharmed %)
        if 'Unharmed' in situation_pct.columns:
            situation_pct['safety_score'] = situation_pct['Unharmed']
        else:
            situation_pct['safety_score'] = 0
        
        most_dangerous = situation_pct['danger_score'].idxmax()
        danger_score = situation_pct['danger_score'].max()
        safest = situation_pct['safety_score'].idxmax()
        safety_score = situation_pct['safety_score'].max()
        
        # Infrastructure comparison
        infra_stats = df_filtered.groupby('has_bike_infrastructure').agg(
            total=('has_bike_infrastructure', 'size')
        )
        with_infra = infra_stats.loc[True, 'total'] if True in infra_stats.index else 0
        without_infra = infra_stats.loc[False, 'total'] if False in infra_stats.index else 0
        
        st.info(f"""
        **💡 Infrastructure Insight** ({len(df_filtered):,} accidents in selection):
        
        **Waffle chart severity patterns**:
        - **Most red/orange (most dangerous)**: **{most_dangerous}**
          - {danger_score:.1f}% killed or hospitalized
          - Highest proportion of severe accidents
        
        - **Most green (safest)**: **{safest}**
          - {safety_score:.1f}% unharmed
          - Best protection for cyclists
        
        **Infrastructure volume**:
        - With cycling infrastructure: {with_infra:,} accidents
        - Without cycling infrastructure: {without_infra:,} accidents
        - **Risk multiplier**: {(without_infra/with_infra if with_infra > 0 else 0):.1f}x more accidents occur without infrastructure
        
        💡 **Critical insight**: Areas without infrastructure for bike have **{(without_infra/with_infra if with_infra > 0 else 0):.0f} times more accidents**.
        This proves the urgent need for protected cycling infrastructure.""")
        
    else:
        st.info("""
        **💡 Infrastructure Insights**:
""")
        # GLOBAL DETAILED ANALYSIS (no filters)
        col1, col2 = st.columns(2)

        with col1:
            st.info("""                    
            **Road situation severity comparison**:
            - **On shoulder**: Deadliest pattern  
                - ~15-20% red/dark orange squares at top = high killed/hospitalized rate  
                - Narrow space + fast vehicles = severe impacts  

            - **On roadway**: High severity  
                - ~10-15% red/orange at top = significant severe accidents  
                - Most common situation (83% of all accidents)  
                - Mixing with car traffic = dangerous  

            - **On bike path**: Safest pattern  
                - ~15-20% green squares at bottom = high unharmed rate  
                - Only ~5-8% red/orange = low severe accident rate  
                - Physical separation protects cyclists  
                    
            - **On sidewalk**: Moderate severity  
                - ~10-15% green squares = some protection  
                - ~8-10% red/orange = moderate severe accidents  
                - Better than roadway, worse than bike path  

            """)

        with col2:
            st.info("""
            **Infrastructure effectiveness** (from bar chart):  
            
            - **Volume comparison**:  
                - WITHOUT infrastructure: 78,436 accidents (98.0%)  
                - WITH infrastructure: 1,586 accidents (2.0%)  
            
            - **Severity distribution**:  
                - WITH: Lower hospitalization rate (24.5% vs 32.7%)  
                - WITHOUT: More severe outcomes overall  

            **Key takeaway**: 
            - Protected bike lanes don't just reduce accident volume – they also reduce severity.  
            - A cyclist on a bike path has **50x less chance** of being in an accident than on the roadway.
           
            
            Cycling infrastructure that is physically separated from motor vehicle traffic is the best way to **drastically reduce the severity of accidents**. Investment in these facilities is cost-effective both in human and economic terms (avoided healthcare costs).

            """)


        st.success("""
        **✅ Evidence-Based Policy Recommendations**:
                
        **Why shoulder cycling is deadly** (highest red proportion in waffle):
        - Vehicles traveling 70-130 km/h on highways
        - No physical barrier between cyclist and traffic
        - Emergency lane = false sense of security
        
        **Why bike paths and sidewalk work** (most green squares):
        - Physical separation eliminates car-bike collisions
        - Lower speeds (typically 20-30 km/h)
        - Dedicated space reduces stress and sudden movements
        
        **Immediate actions**:
        1. **Ban cyclists from highway shoulders** - build alternative routes
        2. **Convert painted bike lanes to protected lanes** - add physical barriers
        3. **Prioritize bike infrastructure on commuter routes** - where 83% of accidents occur
        """)
    

    # ========================================================================
    # QUICK INSIGHTS SUMMARY
    # ========================================================================
    
    st.markdown("---")
    st.header("⚡ Quick Insights Summary")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **⏰ When?**
        - Rush hours: 8am & 6pm
        - Weekdays > weekends
        - Summer >> Winter
        """)
    
    with col2:
        st.markdown("""
        **🌦️ Conditions?**
        - Night w/o lights: 4x deadlier
        - Strong wind: 13.9% fatality
        - Lighting > weather impact
        """)
    
    with col3:
        st.markdown("""
        **🛣️ Where?**
        - Shoulder = deadliest
        - Bike lanes = 50x safer
        - 98% accidents w/o infrastructure
        """)
    
    st.info("""
    **🎯**: The data is clear - **protected bike lanes save lives**. 
    Night lighting, separated infrastructure, and rush hour safety measures are the three pillars 
    for reducing cyclist fatalities. See the Conclusions section for detailed policy recommendations.
    """)