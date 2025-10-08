"""
Overview section for the cycling safety dashboard.
Presents high-level trends, KPIs, and key patterns.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def render(df_filtered, tables):
    """
    Render the overview section.
    
    Args:
        df_filtered (pd.DataFrame): Filtered dataset based on sidebar selections
        tables (dict): Pre-aggregated tables from create_aggregated_tables()
    """
    
    st.markdown("## 📊 Overview: Cycling Accidents in France")
    
    st.markdown("""
    This section provides a **high-level view** of cycling accident patterns across France 
    from 2005 to 2022. Use the sidebar filters to explore specific time periods, departments, 
    or severity levels.
    """)
    
    # ========================================================================
    # KEY METRICS (KPIs)
    # ========================================================================
    
    st.markdown("---")
    st.markdown("### 🎯 Key Metrics")
    
    # Calculate KPIs
    total_accidents = len(df_filtered)
    total_fatal = df_filtered['is_fatal'].sum()
    total_severe = df_filtered['is_severe'].sum()
    fatal_rate = (total_fatal / total_accidents * 100) if total_accidents > 0 else 0
    severe_rate = (total_severe / total_accidents * 100) if total_accidents > 0 else 0
    
    # Average age
    avg_age = df_filtered['age'].mean()
    
    # Most common time period
    if 'time_period' in df_filtered.columns:
        most_common_period = df_filtered['time_period'].mode()[0] if len(df_filtered) > 0 else "N/A"
    else:
        most_common_period = "N/A"
    
    # Display KPIs in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            label="🚴 Total Victims",
            value=f"{total_accidents:,}",
            help="Number of people involved in cycling accidents (filtered)"
        )
    
    with col2:
        st.metric(
            label="💀 Fatal Accidents",
            value=f"{total_fatal:,}",
            delta=f"{fatal_rate:.1f}%",
            help="Number and percentage of fatal accidents"
        )
    
    with col3:
        st.metric(
            label="🏥 Severe Accidents",
            value=f"{total_severe:,}",
            delta=f"{severe_rate:.1f}%",
            help="Hospitalized or killed (severe injuries)"
        )
    
    with col4:
        st.metric(
            label="👤 Average Age",
            value=f"{avg_age:.0f} years",
            help="Average age of victims"
        )
    
    with col5:
        st.metric(
            label="🕐 Peak Period",
            value=most_common_period,
            help="Most common time period for accidents"
        )
    
    # ========================================================================
    # TEMPORAL EVOLUTION
    # ========================================================================
    
    st.markdown("---")
    st.markdown("### 📈 Temporal Evolution (2005-2022)")
    
    st.markdown("""
    This chart shows how cycling accidents evolved over 18 years, broken down by severity level.
    Notice the significant drop in 2020-2021 due to COVID-19 lockdowns.
    """)
    
    # Aggregate by year and gravity
    yearly_data = df_filtered.groupby(['year', 'gravity']).size().reset_index(name='count')
    
    # Ensure proper ordering of gravity levels
    gravity_order = ['Unharmed', 'Minor injury', 'Hospitalized', 'Killed']
    yearly_data['gravity'] = pd.Categorical(yearly_data['gravity'], categories=gravity_order, ordered=True)
    yearly_data = yearly_data.sort_values(['year', 'gravity'])
    
    # Create stacked area chart
    fig_evolution = px.area(
        yearly_data,
        x='year',
        y='count',
        color='gravity',
        title='Number of Cycling Accident Victims by Year and Severity',
        labels={'count': 'Number of Victims', 'year': 'Year', 'gravity': 'Severity'},
        color_discrete_map={
            'Unharmed': '#2ecc71',
            'Minor injury': '#f1c40f',
            'Hospitalized': '#e67e22',
            'Killed': '#e74c3c'
        }
    )
    
    fig_evolution.update_layout(
        height=450,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Add annotation for COVID-19
    fig_evolution.add_annotation(
        x=2020,
        y=yearly_data[yearly_data['year'] == 2020]['count'].sum(),
        text="COVID-19<br>Impact",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#95a5a6",
        ax=-50,
        ay=-50,
        font=dict(size=10, color="#7f8c8d")
    )
    
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Key insight box
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate trend
        if len(yearly_data) > 0:
            early_years = yearly_data[yearly_data['year'] <= 2007]['count'].sum()
            recent_years = yearly_data[yearly_data['year'] >= 2019]['count'].sum()
            
            if early_years > 0:
                change_pct = ((recent_years - early_years) / early_years) * 100
                trend = "increased" if change_pct > 0 else "decreased"
                
                st.info(f"""
                **📊 Long-term Trend:**  
                Accidents have **{trend} by {abs(change_pct):.0f}%** comparing 2005-2007 vs 2019-2022.
                """)
    
    with col2:
        # COVID impact
        if 2019 in yearly_data['year'].values and 2020 in yearly_data['year'].values:
            accidents_2019 = yearly_data[yearly_data['year'] == 2019]['count'].sum()
            accidents_2020 = yearly_data[yearly_data['year'] == 2020]['count'].sum()
            
            if accidents_2019 > 0:
                covid_drop = ((accidents_2020 - accidents_2019) / accidents_2019) * 100
                
                st.warning(f"""
                **🦠 COVID-19 Impact:**  
                Accidents dropped by **{abs(covid_drop):.0f}%** from 2019 to 2020 due to lockdowns.
                """)
    
# ========================================================================
    # GEOGRAPHIC DISTRIBUTION
    # ========================================================================
    
    st.markdown("---")
    st.markdown("### 🗺️ Geographic Distribution by Department")
    
    st.markdown("""
    This treemap shows the relative concentration of cycling accidents across French departments. 
    **Box size** = total accident count | **Color intensity** = fatal rate (%)
    """)
    
    # Aggregate by department
    # Filter only valid French department codes (01-95, 2A, 2B)
    valid_dept_pattern = r'^(0[1-9]|[1-8][0-9]|9[0-5]|2[AB])$'
    df_valid_depts = df_filtered[df_filtered['dep'].str.match(valid_dept_pattern, na=False)]
    
    dept_data = df_valid_depts.groupby('dep').agg({
        'date': 'count',
        'is_fatal': 'sum',
        'is_severe': 'sum'
    }).reset_index()
    dept_data.columns = ['department', 'total_accidents', 'fatal', 'severe']
    
    # Calculate rates
    dept_data['fatal_rate'] = (dept_data['fatal'] / dept_data['total_accidents'] * 100).round(1)
    dept_data['severe_rate'] = (dept_data['severe'] / dept_data['total_accidents'] * 100).round(1)
    
    # Create treemap
    fig_dept = px.treemap(
        dept_data,
        path=['department'],
        values='total_accidents',
        color='fatal_rate',
        hover_data={'total_accidents': ':,', 'fatal': True, 'fatal_rate': ':.1f', 'severe_rate': ':.1f'},
        color_continuous_scale='Reds',
        title='Cycling Accidents by Department',
        range_color=[0, dept_data['fatal_rate'].quantile(0.95)]  # Cap at 95th percentile for better color distribution
    )
    
    fig_dept.update_traces(
        textposition='middle center',
        textfont=dict(size=12, color='white', family='Arial Black'),
        hovertemplate='<b>Dept %{label}</b><br>' +
                      'Total: %{value:,} accidents<br>' +
                      'Fatal: %{customdata[0]:.0f} (%{color:.1f}%)<br>' +
                      'Severe: %{customdata[2]:.1f}%<br>' +
                      '<extra></extra>'
    )
    
    fig_dept.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    st.plotly_chart(fig_dept, use_container_width=True)
    
    # ========================================================================
    # DETAILED ANALYSIS
    # ========================================================================
    
    st.markdown("---")
    st.markdown("#### 📊 Geographic Analysis: Key Findings")
    
    # Calculate comprehensive statistics
    total_depts = len(dept_data)
    total_accidents_filtered = dept_data['total_accidents'].sum()
    dept_data_sorted = dept_data.sort_values('total_accidents', ascending=False)
    
    # Top department
    top_1 = dept_data_sorted.iloc[0]
    
    # Concentration metrics
    top_3_count = dept_data_sorted.head(3)['total_accidents'].sum()
    top_3_pct = (top_3_count / total_accidents_filtered * 100)
    top_5_count = dept_data_sorted.head(5)['total_accidents'].sum()
    top_5_pct = (top_5_count / total_accidents_filtered * 100)
    top_10_count = dept_data_sorted.head(10)['total_accidents'].sum()
    top_10_pct = (top_10_count / total_accidents_filtered * 100)
    
    # Risk analysis (departments with at least 500 accidents for statistical significance)
    significant_depts = dept_data[dept_data['total_accidents'] >= 500]
    
    if len(significant_depts) > 0:
        safest_dept = significant_depts.sort_values('fatal_rate').iloc[0]
        most_dangerous = significant_depts.sort_values('fatal_rate', ascending=False).iloc[0]
    else:
        safest_dept = None
        most_dangerous = None
    
    # Regional patterns (Paris region vs rest)
    paris_region_codes = ['75', '77', '78', '91', '92', '93', '94', '95']
    paris_region = dept_data[dept_data['department'].isin(paris_region_codes)]
    other_depts = dept_data[~dept_data['department'].isin(paris_region_codes)]
    
    paris_accidents = paris_region['total_accidents'].sum()
    paris_pct = (paris_accidents / total_accidents_filtered * 100)
    
    # Display analysis in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("##### 🏙️ Urban Dominance")
        st.markdown(f"""
        **Paris (75)** is overwhelmingly dominant with **{top_1['total_accidents']:,} accidents** 
        ({(top_1['total_accidents']/total_accidents_filtered*100):.1f}% of national total).
        
        **Île-de-France region** (8 departments):
        - Total: **{paris_accidents:,} accidents**
        - Share: **{paris_pct:.1f}%** of all accidents
        - Average per dept: **{(paris_accidents/len(paris_region)):.0f}**
        
        **Rest of France** ({len(other_depts)} departments):
        - Average per dept: **{(other_depts['total_accidents'].sum()/len(other_depts)):.0f}**
        
        ➡️ **Ile de France region has {(paris_accidents/len(paris_region))/(other_depts['total_accidents'].sum()/len(other_depts)):.1f}x** more accidents per department than the rest of France.
        """)
    
    with col2:
        st.markdown("##### 📈 Extreme Concentration")
        st.markdown(f"""
        A tiny fraction of departments accounts for most accidents:
        
        - **Top 3 depts**: {top_3_pct:.0f}% of accidents
        - **Top 5 depts**: {top_5_pct:.0f}% of accidents  
        - **Top 10 depts**: {top_10_pct:.0f}% of accidents
        
        **Coverage**: {total_depts} departments out of 101
        
        **Bottom 50%** of departments combined have fewer accidents than Paris alone.
        
        ➡️ This extreme concentration suggests **cycling activity is heavily urban-centric**.
        """)
    
    with col3:
        st.markdown("##### ⚠️ Risk vs Volume")
        if most_dangerous is not None and safest_dept is not None:
            risk_ratio = most_dangerous['fatal_rate'] / safest_dept['fatal_rate'] if safest_dept['fatal_rate'] > 0 else 0
            
            st.markdown(f"""
            **Highest fatal rate** (min. 500 accidents):
            - Dept **{most_dangerous['department']}**: {most_dangerous['fatal_rate']:.1f}%
            - {most_dangerous['total_accidents']:,} accidents, {most_dangerous['fatal']:.0f} deaths
            
            **Lowest fatal rate** (min. 500 accidents):
            - Dept **{safest_dept['department']}**: {safest_dept['fatal_rate']:.1f}%
            - {safest_dept['total_accidents']:,} accidents, {safest_dept['fatal']:.0f} deaths
            
            ➡️ **{risk_ratio:.1f}x** difference in fatal rates between most and least dangerous departments.
            
            **Key insight**: High volume ≠ high danger. Some busy urban areas have lower fatal rates (better infrastructure, lower speeds).
            """)
        else:
            st.info("Insufficient data (fewer than 500 accidents per department) to perform risk comparison.")

    
    
    # Deeper insights section
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("""
        ⚠️ **Why such concentration in Paris?**
        
        1. **Population density**: 20% of French population in Île-de-France
        2. **Cycling infrastructure**: Extensive bike lane network encourages cycling
        3. **Modal shift policies**: Active promotion of cycling vs cars
        4. **Commuting patterns**: High daily cycling for work/school
        5. **Reporting quality**: Better accident documentation in urban areas
        
        **Note**: High numbers reflect both risk AND exposure (more cyclists = more potential accidents).
        """)
    
    with col2:
        st.success("""
        ✅ **Policy Implications**
        
        **For high-volume departments (Paris, Lyon, Marseille):**
        - Focus on **intersection safety** (most common accident sites)
        - Separate bike lanes from traffic
        - Reduce vehicle speeds in mixed zones
        
        **For high-risk rural departments:**
        - Improve **road surface maintenance**
        - Better **signage and lighting**
        - Targeted campaigns for motorist awareness
        
        **One-size-fits-all approaches won't work** - urban and rural areas need different interventions.
        """)

    # ========================================================================
    # URBAN VS RURAL COMPARISON
    # ========================================================================
    
    st.markdown("---")
    st.markdown("#### 🏙️ vs 🌾 Urban vs Rural Comparison")
    
    st.markdown("""
    The dataset includes an `agglomeration` field indicating whether accidents occurred 
    **inside built-up areas** (urban) or **outside built-up areas** (rural).
    """)
    
    # Calculate urban vs rural statistics
    urban_rural = df_valid_depts.groupby('agglomeration').agg({
        'date': 'count',
        'is_fatal': 'sum',
        'is_severe': 'sum'
    }).reset_index()
    urban_rural.columns = ['location_type', 'total_accidents', 'fatal', 'severe']
    
    # Calculate rates
    urban_rural['fatal_rate'] = (urban_rural['fatal'] / urban_rural['total_accidents'] * 100).round(1)
    urban_rural['severe_rate'] = (urban_rural['severe'] / urban_rural['total_accidents'] * 100).round(1)
    
    # Split urban and rural
    if len(urban_rural) >= 2:
        urban = urban_rural[urban_rural['location_type'] == 'In built-up area'].iloc[0] if len(urban_rural[urban_rural['location_type'] == 'In built-up area']) > 0 else None
        rural = urban_rural[urban_rural['location_type'] == 'Outside built-up area'].iloc[0] if len(urban_rural[urban_rural['location_type'] == 'Outside built-up area']) > 0 else None
        
        if urban is not None and rural is not None:
            # Create comparison visualization
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                st.markdown("##### 🏙️ Urban Areas")
                st.metric("Total Accidents", f"{urban['total_accidents']:,}")
                st.metric("Fatal Rate", f"{urban['fatal_rate']:.1f}%")
                st.metric("Severe Rate", f"{urban['severe_rate']:.1f}%")
                st.metric("Share of Total", f"{(urban['total_accidents']/urban_rural['total_accidents'].sum()*100):.0f}%")
            
            with col2:
                # Create comparative bar chart
                comparison_data = pd.DataFrame({
                    'Location': ['Urban', 'Rural', 'Urban', 'Rural'],
                    'Metric': ['Fatal Rate', 'Fatal Rate', 'Severe Rate', 'Severe Rate'],
                    'Value': [urban['fatal_rate'], rural['fatal_rate'], 
                             urban['severe_rate'], rural['severe_rate']]
                })
                
                fig_comparison = px.bar(
                    comparison_data,
                    x='Metric',
                    y='Value',
                    color='Location',
                    barmode='group',
                    title='Urban vs Rural: Severity Comparison',
                    labels={'Value': 'Rate (%)', 'Metric': ''},
                    color_discrete_map={'Urban': '#3498db', 'Rural': '#e67e22'}
                )
                
                fig_comparison.update_layout(height=300)
                st.plotly_chart(fig_comparison, use_container_width=True)
                
                # Statistical comparison
                fatal_diff = rural['fatal_rate'] / urban['fatal_rate'] if urban['fatal_rate'] > 0 else 0
                severe_diff = rural['severe_rate'] / urban['severe_rate'] if urban['severe_rate'] > 0 else 0
                
                if fatal_diff > 1:
                    st.error(f"""
                    ⚠️ **Rural areas are {fatal_diff:.1f}x more deadly** than urban areas.
                    
                    Despite having fewer accidents overall, rural accidents are significantly more severe.
                    """)
                else:
                    st.success(f"""
                    ✅ **Urban areas are {1/fatal_diff:.1f}x more deadly** than rural areas.
                    """)
            
            with col3:
                st.markdown("##### 🌾 Rural Areas")
                st.metric("Total Accidents", f"{rural['total_accidents']:,}")
                st.metric("Fatal Rate", f"{rural['fatal_rate']:.1f}%")
                st.metric("Severe Rate", f"{rural['severe_rate']:.1f}%")
                st.metric("Share of Total", f"{(rural['total_accidents']/urban_rural['total_accidents'].sum()*100):.0f}%")
            
            # Detailed analysis
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 🏙️ Why Urban Areas Have More Accidents")
                st.info("""
                **Volume factors:**
                - 🚴 **Higher cycling density**: More cyclists per km²
                - 🚦 **More intersections**: Complex traffic situations
                - 🚗 **Mixed traffic**: Cars, buses, bikes, pedestrians
                - 📊 **Better reporting**: All accidents more likely to be recorded
                
                **Protective factors:**
                - 🐌 **Lower speeds**: 30-50 km/h zones common
                - 🛣️ **Better infrastructure**: Bike lanes, traffic lights
                - 👮 **More enforcement**: Police presence
                - 🏥 **Faster emergency response**: Hospitals nearby
                
                ➡️ **Many accidents, but less severe outcomes**
                """)
            
            with col2:
                st.markdown("##### 🌾 Why Rural Areas Are More Dangerous")
                st.warning("""
                **Risk factors:**
                - 🚗💨 **Higher speeds**: 80-90 km/h on rural roads
                - 🛣️ **No bike infrastructure**: Cyclists share road with fast traffic
                - 🌑 **Poor lighting**: Many accidents at night
                - 🚧 **Road conditions**: Narrower roads, worse maintenance
                
                **Severity factors:**
                - ⚡ **High-speed impacts**: Kinetic energy = speed²
                - 🏥 **Delayed emergency care**: Longer ambulance times
                - 👥 **Isolation**: Less witnesses, delayed help
                - 🚜 **Heavy vehicles**: Trucks, agricultural machinery
                
                ➡️ **Fewer accidents, but much more deadly**
                """)
            
           
    
    # Final key takeaways
    st.info("""
    💡 **Critical Takeaways:**
    
    1. **Geographic inequality is extreme**: Top 10 departments = {top_10_pct:.0f}% of accidents, but they also have the most cyclists
    
    2. **Volume ≠ Danger**: High accident counts often reflect high cycling volume, not necessarily dangerous conditions. 
       Paris has many accidents but relatively moderate fatal rates due to infrastructure and lower speeds.
    
    3. **Urban-rural divide**: Urban areas need intersection safety and traffic calming; rural areas need better road conditions and motorist awareness.
    
    4. **Data context matters**: Absolute numbers don't tell the full story. We need cycling volume data to calculate true risk rates 
       (accidents per 1000 cyclists, not just total accidents).
    
    5. **Targeted interventions**: The top 10 departments should be priority zones for infrastructure investment, 
       but don't neglect high-risk rural areas with smaller absolute numbers.
    """.format(top_10_pct=top_10_pct))
    
    # ========================================================================
    # SEVERITY BREAKDOWN
    # ========================================================================
    
    st.markdown("---")
    st.markdown("### ⚠️ Accident Severity Distribution")
    
    # Calculate severity distribution
    severity_dist = df_filtered['gravity'].value_counts().reset_index()
    severity_dist.columns = ['Severity', 'Count']
    severity_dist['Percentage'] = (severity_dist['Count'] / severity_dist['Count'].sum() * 100).round(1)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Pie chart
        fig_severity = px.pie(
            severity_dist,
            values='Count',
            names='Severity',
            title='Distribution of Accident Severity',
            color='Severity',
            color_discrete_map={
                'Unharmed': '#2ecc71',
                'Minor injury': '#f1c40f',
                'Hospitalized': '#e67e22',
                'Killed': '#e74c3c'
            },
            hole=0.4
        )
        
        fig_severity.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Count: %{value:,}<br>Percentage: %{percent}<extra></extra>'
        )
        
        fig_severity.update_layout(height=400)
        
        st.plotly_chart(fig_severity, use_container_width=True)
    
    with col2:
        st.markdown("#### 📊 Breakdown")
        
        for idx, row in severity_dist.iterrows():
            # Color based on severity
            if row['Severity'] == 'Killed':
                emoji = "💀"
                color = "#e74c3c"
            elif row['Severity'] == 'Hospitalized':
                emoji = "🏥"
                color = "#e67e22"
            elif row['Severity'] == 'Minor injury':
                emoji = "🤕"
                color = "#f1c40f"
            else:
                emoji = "✅"
                color = "#2ecc71"
            
            st.markdown(f"""
            <div style='background-color: {color}20; padding: 10px; border-radius: 5px; margin-bottom: 10px; border-left: 4px solid {color};'>
                <h4 style='margin: 0; color: {color};'>{emoji} {row['Severity']}</h4>
                <p style='margin: 5px 0 0 0; font-size: 1.2rem;'><strong>{row['Count']:,}</strong> ({row['Percentage']:.1f}%)</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.info("""
        💡 **Key Insight:**  
        While most accidents result in minor injuries, the proportion of severe/fatal 
        accidents requires attention for safety improvements.
        """)
    
    # ========================================================================
    # QUICK INSIGHTS SUMMARY
    # ========================================================================
    
    st.markdown("---")
    st.markdown("### 💡 Quick Insights")
    
    insight1, insight2, insight3 = st.columns(3)
    
    with insight1:
        st.markdown("""
        **🕐 Temporal Pattern**
        
        Accidents show a **declining trend** from 2005-2010, followed by relative stability. 
        The COVID-19 pandemic caused a sharp but temporary drop in 2020-2021.
        """)
    
    with insight2:
        st.markdown("""
        **🗺️ Geographic Concentration**
        
        Urban departments (especially Paris region) account for the **majority of accidents**, 
        reflecting higher cycling activity in cities.
        """)
    
    with insight3:
        st.markdown("""
        **⚠️ Severity Levels**
        
        Most accidents result in **minor injuries**, but severe and fatal accidents 
        represent a significant public health concern requiring targeted interventions.
        """)
    
    # ========================================================================
    # CALL TO ACTION
    # ========================================================================
    
    st.success("""
    **👉 Want to dig deeper?**  
    Head to the **Deep Dive Analysis** section to explore:
    - Hourly and daily patterns
    - Weather and lighting conditions
    - Infrastructure effectiveness
    - Victim profiles by age and gender
    """)