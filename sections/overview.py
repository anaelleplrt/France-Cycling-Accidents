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
            help="Number and percentage of fatal accidents"
        )
    
    with col3:
        st.metric(
            label="🏥 Severe Accidents",
            value=f"{total_severe:,}",
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
    # URBAN VS RURAL COMPARISON
    # ========================================================================
    
    st.markdown("---")
    st.markdown("### Urban vs Rural: Accident Volume & Severity")
    
    st.markdown("""
    Comparing accident patterns and severity distribution between built-up areas (urban) and open roads (rural).
    """)
    
    st.info("""
    💡 **Interactive chart tips:**
    - 🖱️ **Hover** over the bars to see detailed numbers
    - 👆 **Click** on severity levels in the legend to show/hide them
    """)
    
    # Filter only valid French department codes (needed for urban/rural analysis)
    valid_dept_pattern = r'^(0[1-9]|[1-8][0-9]|9[0-5]|2[AB])$'
    df_valid_depts = df_filtered[df_filtered['dep'].str.match(valid_dept_pattern, na=False)]
    
    # Calculate urban vs rural by gravity
    urban_rural_gravity = df_valid_depts.groupby(['agglomeration', 'gravity']).size().reset_index(name='count')
    
    # Calculate totals for each location type
    urban_rural_totals = df_valid_depts.groupby('agglomeration').size().reset_index(name='total')
    
    # Merge to get percentages
    urban_rural_gravity = urban_rural_gravity.merge(urban_rural_totals, on='agglomeration')
    urban_rural_gravity['percentage'] = (urban_rural_gravity['count'] / urban_rural_gravity['total'] * 100).round(1)
    
    if len(urban_rural_totals) >= 2:
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown("##### 🏙️ Urban (Built-up Area)")
            urban_total = urban_rural_totals[urban_rural_totals['agglomeration'] == 'In built-up area']['total'].values[0] if len(urban_rural_totals[urban_rural_totals['agglomeration'] == 'In built-up area']) > 0 else 0
            urban_data = urban_rural_gravity[urban_rural_gravity['agglomeration'] == 'In built-up area']
            
            st.metric("Total Accidents", f"{urban_total:,}")
            st.markdown("**Distribution:**")
            
            for _, row in urban_data.iterrows():
                st.write(f"• **{row['gravity']}**: {row['count']:,} ({row['percentage']:.1f}%)")
        
        with col2:
            # Stacked bar chart comparing gravity distribution
            fig_comparison = px.bar(
                urban_rural_gravity,
                x='agglomeration',
                y='count',
                color='gravity',
                title='Accident Severity Distribution: Urban vs Rural',
                labels={'count': 'Number of Accidents', 'agglomeration': 'Location Type'},
                color_discrete_map={
                    'Unharmed': '#2ecc71',
                    'Minor injury': '#f1c40f',
                    'Hospitalized': '#e67e22',
                    'Killed': '#e74c3c'
                },
                barmode='stack',
                text='count'
            )
            
            fig_comparison.update_traces(
                texttemplate='%{text:,}', 
                textposition='inside',
                textfont=dict(size=18, color='black')  # ← AJOUTÉ
            )
            fig_comparison.update_layout(height=400)
            
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Calculate key metrics
            urban_killed_pct = urban_rural_gravity[(urban_rural_gravity['agglomeration'] == 'In built-up area') & (urban_rural_gravity['gravity'] == 'Killed')]['percentage'].values[0] if len(urban_rural_gravity[(urban_rural_gravity['agglomeration'] == 'In built-up area') & (urban_rural_gravity['gravity'] == 'Killed')]) > 0 else 0
            
            rural_killed_pct = urban_rural_gravity[(urban_rural_gravity['agglomeration'] == 'Outside built-up area') & (urban_rural_gravity['gravity'] == 'Killed')]['percentage'].values[0] if len(urban_rural_gravity[(urban_rural_gravity['agglomeration'] == 'Outside built-up area') & (urban_rural_gravity['gravity'] == 'Killed')]) > 0 else 0
            
            if urban_killed_pct > 0:
                risk_ratio = rural_killed_pct / urban_killed_pct
                
        with col3:
            st.markdown("##### 🌾 Rural (Outside Built-up)")
            rural_total = urban_rural_totals[urban_rural_totals['agglomeration'] == 'Outside built-up area']['total'].values[0] if len(urban_rural_totals[urban_rural_totals['agglomeration'] == 'Outside built-up area']) > 0 else 0
            rural_data = urban_rural_gravity[urban_rural_gravity['agglomeration'] == 'Outside built-up area']
            
            st.metric("Total Accidents", f"{rural_total:,}")
            st.markdown("**Distribution:**")
            
            for _, row in rural_data.iterrows():
                st.write(f"• **{row['gravity']}**: {row['count']:,} ({row['percentage']:.1f}%)")
        
                
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🏙️ Urban Areas (High Volume, Lower Severity)")
            st.info("""
            **Characteristics:**
            - 🚴 More cyclists = more accidents overall
            - 🐌 Lower speeds (30-50 km/h zones)
            - 🛣️ Better infrastructure (bike lanes)
            - 🏥 Faster emergency response
            
            **Result**: Many accidents but proportionally fewer deaths
            """)
        
        with col2:
            st.markdown("##### 🌾 Rural Areas (Low Volume, Higher Severity)")
            st.warning("""
            **Characteristics:**
            - 🚗💨 Higher speeds (80-90 km/h)
            - 🛣️ No dedicated bike infrastructure
            - 🌑 Poor lighting at night
            - 🏥 Delayed emergency care
            
            **Result**: Fewer accidents but proportionally more deadly
            """)
        
        st.success(f"""
        💡 **The Urban-Rural Paradox:**
        
        Urban areas have {(urban_total/urban_rural_totals['total'].sum()*100):.0f}% of accidents but only {urban_killed_pct:.1f}% are fatal.
        Rural areas have {(rural_total/urban_rural_totals['total'].sum()*100):.0f}% of accidents but {rural_killed_pct:.1f}% are fatal ({risk_ratio:.1f}x higher!).
        
        **Policy implication**: Cities need **volume management** (more bike lanes), rural areas need **speed reduction** and **infrastructure**.
        """)
    else:
        st.warning("Insufficient data for urban/rural comparison.")
    

    # ========================================================================
    # DEMOGRAPHICS ANALYSIS
    # ========================================================================
    
    st.markdown("---")
    st.markdown("### 👥 Demographics: Who Are the Victims?")
    
    st.markdown("""
    Understanding the profile of cycling accident victims helps identify vulnerable groups 
    and tailor prevention campaigns.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 Age Distribution")
        
        # Age distribution by gravity
        age_data = df_filtered.groupby(['age_group', 'gravity']).size().reset_index(name='count')

        # # Pivot data for heatmap
        age_pivot = age_data.pivot(index='gravity', columns='age_group', values='count').fillna(0)
        # 
        # # Reorder gravity for better visualization
        gravity_order = ['Killed', 'Hospitalized', 'Minor injury', 'Unharmed']
        age_pivot = age_pivot.reindex(gravity_order)
        # 
        fig_age = px.imshow(
        age_pivot,
        labels=dict(x="Age Group", y="Severity", color="Accidents"),
        title='Accident Heatmap: Age vs Severity',
        color_continuous_scale='OrRd',
        text_auto=True,
        aspect='auto'
         )
        # 
        fig_age.update_layout(
            height=500,
        )
        st.plotly_chart(fig_age, use_container_width=True)
        
        
        # Calculate age statistics
        total_by_age = df_filtered.groupby('age_group').agg({
            'date': 'count',
            'is_fatal': 'sum'
        }).reset_index()
        total_by_age.columns = ['age_group', 'total', 'fatal']
        total_by_age['fatal_rate'] = (total_by_age['fatal'] / total_by_age['total'] * 100).round(1)
        
        most_affected = total_by_age.sort_values('total', ascending=False).iloc[0]
        most_at_risk = total_by_age.sort_values('fatal_rate', ascending=False).iloc[0]
        
        st.info(f"""
        **📊 Age Insights:**
        - Most affected group: **{most_affected['age_group']}** ({most_affected['total']:,} accidents)
        - Highest fatal rate: **{most_at_risk['age_group']}** ({most_at_risk['fatal_rate']:.1f}%)
        - Average victim age: **{df_filtered['age'].mean():.0f} years**
        """)
    
    with col2:
        st.markdown("#### 👫 Gender Distribution")
        
        # Gender distribution by gravity
        gender_data = df_filtered.groupby(['gender', 'gravity']).size().reset_index(name='count')
        
        fig_gender = px.bar(
            gender_data,
            x='gravity',
            y='count',
            color='gravity',
            facet_col='gender',
            title='Accidents by Gender and Severity',
            labels={'count': 'Number of Victims', 'gravity': 'Severity'},
            color_discrete_map={
                'Unharmed': '#2ecc71',
                'Minor injury': '#f1c40f',
                'Hospitalized': '#e67e22',
                'Killed': '#e74c3c'
            },
            text='count'
        )
        
        fig_gender.update_traces(
            texttemplate='%{text:,}',
            textposition='outside'
        )
        
        fig_gender.update_layout(height=500, showlegend=False)
        fig_gender.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        
        st.plotly_chart(fig_gender, use_container_width=True)
        
        

        
        # Calculate gender statistics
        gender_stats = df_filtered.groupby('gender').agg({
            'date': 'count',
            'is_fatal': 'sum'
        }).reset_index()
        gender_stats.columns = ['gender', 'total', 'fatal']
        gender_stats['fatal_rate'] = (gender_stats['fatal'] / gender_stats['total'] * 100).round(1)
        
        if len(gender_stats) >= 2:
            male_stats = gender_stats[gender_stats['gender'] == 'Male'].iloc[0] if len(gender_stats[gender_stats['gender'] == 'Male']) > 0 else None
            female_stats = gender_stats[gender_stats['gender'] == 'Female'].iloc[0] if len(gender_stats[gender_stats['gender'] == 'Female']) > 0 else None
            
            if male_stats is not None and female_stats is not None:
                male_pct = (male_stats['total'] / gender_stats['total'].sum() * 100)
                
                st.warning(f"""
                **👫 Gender Insights:**
                - Male victims: **{male_pct:.0f}%** of total ({male_stats['total']:,} accidents)
                - Female victims: **{100-male_pct:.0f}%** of total ({female_stats['total']:,} accidents)
                - Male fatal rate: **{male_stats['fatal_rate']:.1f}%**
                - Female fatal rate: **{female_stats['fatal_rate']:.1f}%**
                
                Men are over-represented in cycling accidents, possibly due to higher cycling rates 
                and more risk-taking behaviors.
                """)


   

    # ========================================================================
    # TEMPORAL EVOLUTION
    # ========================================================================
    
    st.markdown("---")
    st.markdown("### 📈 Temporal Evolution (2005-2022)")
    
    st.markdown("""
    This chart shows how cycling accidents evolved over 18 years, broken down by severity level.
    """)
    
    # Aggregate by year and gravity
    yearly_data = df_filtered.groupby(['year', 'gravity']).size().reset_index(name='count')
    
    # Ensure proper ordering of gravity levels for visual display
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
    
    # Add annotations for key events
    # COVID-19 annotation
    if 2020 in yearly_data['year'].values:
        covid_y = yearly_data[yearly_data['year'] == 2020]['count'].sum()
        fig_evolution.add_annotation(
            x=2020,
            y=covid_y,
            text="COVID-19<br>Lockdowns",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#e74c3c",
            ax=-50,
            ay=-60,
            font=dict(size=10, color="#e74c3c", weight="bold"),
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="#e74c3c",
            borderwidth=2
        )
    
    # 2017 laws annotation
    if 2017 in yearly_data['year'].values:
        laws_y = yearly_data[yearly_data['year'] == 2017]['count'].sum()
        fig_evolution.add_annotation(
            x=2017,
            y=laws_y,
            text="2017 Laws<br>(Helmet + E-bike)",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#3498db",
            ax=50,
            ay=-50,
            font=dict(size=10, color="#3498db"),
            bgcolor="rgba(255,255,255,0.7)"
        )
    
    st.plotly_chart(fig_evolution, use_container_width=True)
    
    # Key insight box - calculate trends
    yearly_detail = df_filtered.groupby('year').size().reset_index(name='total')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Calculate long-term trend
        if len(yearly_detail) > 0:
            early_years = yearly_detail[yearly_detail['year'].isin([2005, 2006, 2007])]['total'].sum()
            pre_covid = yearly_detail[yearly_detail['year'].isin([2017, 2018, 2019])]['total'].sum()
            
            if early_years > 0:
                change_pct = ((pre_covid - early_years) / early_years) * 100
                trend = "decreased" if change_pct < 0 else "increased"
                
                st.info(f"""
                📊 **Long-term Trend (2005-2019):**  
                Accidents have **{trend} by {abs(change_pct):.0f}%** comparing 2005-2007 vs 2017-2019 
                (before COVID impact).
                
                This decline is primarily due to 2017 legislation (helmet law + e-bike subsidy).
                """)
    
    with col2:
        # COVID impact
        if all(year in yearly_detail['year'].values for year in [2019, 2020, 2021]):
            accidents_2019 = yearly_detail[yearly_detail['year'] == 2019]['total'].values[0]
            accidents_2020 = yearly_detail[yearly_detail['year'] == 2020]['total'].values[0]
            accidents_2021 = yearly_detail[yearly_detail['year'] == 2021]['total'].values[0]
            
            if accidents_2019 > 0:
                covid_drop_2020 = ((accidents_2020 - accidents_2019) / accidents_2019) * 100
                covid_drop_2021 = ((accidents_2021 - accidents_2019) / accidents_2019) * 100
                
                st.warning(f"""
                🦠 **COVID-19 Impact:**  
                - **2020**: {abs(covid_drop_2020):.0f}% drop from 2019 (lockdowns)
                - **2021**: {abs(covid_drop_2021):.0f}% below 2019 level
                - **2022**: Partial recovery
                
                Cycling decreased during lockdowns but is gradually recovering.
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
        
        Accidents showed a **gradual decline** from 2005 to 2022, with major drops in 2017 (new laws) 
        and 2020 (COVID-19 pandemic).
        """)
    
    with insight2:
        st.markdown("""
        **🗺️ Geographic Concentration**
        
        Urban departments (especially Paris region) account for the **majority of accidents**, 
        reflecting higher cycling activity in cities.
        """)
    
    with insight3:
        st.markdown("""
        **⚠️ Urban-Rural Paradox**
        
        Cities have **more accidents but lower fatality rates** due to lower speeds and better infrastructure. 
        Rural areas are far more deadly.
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