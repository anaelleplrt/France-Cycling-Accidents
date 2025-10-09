"""
Visualization functions for the cycling accidents dashboard.
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import folium
from folium import plugins
import streamlit as st


# ============================================================================
# 1. TEMPORAL PATTERNS
# ============================================================================

def plot_hourly_distribution(df):
    """
    Grouped bar chart showing hourly accident distribution by severity.
    """
    # Extract hour from hour column
    df_copy = df.copy()
    
    # Group by hour and gravity
    hourly = df_copy.groupby(['hour', 'gravity']).size().reset_index(name='count')
    
    # Create grouped bar chart
    fig = px.bar(
        hourly,
        x='hour',
        y='count',
        color='gravity',
        color_discrete_map={
            'Unharmed': '#2ecc71',
            'Minor injury': '#f1c40f',
            'Hospitalized': '#e67e22',
            'Killed': '#e74c3c'
        },
        title='Accident distribution by hour of day',
        labels={'hour': 'Hour', 'count': 'Number of accidents', 'gravity': 'Severity'},
        barmode='group'
    )
    
    fig.update_layout(
        xaxis=dict(tickmode='linear', tick0=0, dtick=2),
        hovermode='x unified',
        height=450
    )
    
    return fig


def plot_day_season_heatmap(df):
    """
    Heatmap showing accidents by day of week and season.
    """
    # Use existing season column from cleaned data
    df_copy = df.copy()
    
    # Create mapping for day_of_week if needed
    if 'day_of_week' in df_copy.columns:
        day_col = 'day_of_week'
    else:
        day_col = 'day_name'  # Assuming day_name exists
    
    # Create pivot table
    heatmap_data = df_copy.groupby([day_col, 'season']).size().reset_index(name='count')
    pivot = heatmap_data.pivot(index=day_col, columns='season', values='count')
    
    # Day order (adjust based on your data format)
    if 'Monday' in pivot.index.tolist():
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    else:
        day_order = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']
    
    # Season order (adjust based on your data)
    if 'Spring' in pivot.columns.tolist():
        season_order = ['Spring', 'Summer', 'Autumn', 'Winter']
    else:
        season_order = ['Printemps', 'Été', 'Automne', 'Hiver']
    
    # Reindex days (fill missing days with 0)
    pivot = pivot.reindex(day_order, fill_value=0)
    
    # Reindex seasons (only keep existing ones, fill missing with 0)
    existing_seasons = [s for s in season_order if s in pivot.columns]
    missing_seasons = [s for s in season_order if s not in pivot.columns]
    
    # Add missing seasons with 0 values
    for season in missing_seasons:
        pivot[season] = 0
    
    # Reorder columns
    pivot = pivot[season_order]
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='YlOrRd',
        text=pivot.values,
        texttemplate='%{text}',
        textfont={"size": 12},
        colorbar=dict(title="Accidents")
    ))
    
    fig.update_layout(
        title='Accident distribution by day of week and season',
        xaxis_title='Season',
        yaxis_title='Day of week',
        height=400
    )
    
    return fig


# ============================================================================
# 2. WEATHER & LIGHTING CONDITIONS
# ============================================================================

def plot_weather_lighting_conditions(df):
    """
    Grouped horizontal bar chart showing weather and lighting impact on fatal rate.
    """
    # Calculate stats by lighting (using 'lighting' column)
    lighting_stats = df.groupby('lighting').agg(
        total=('lighting', 'size'),
        fatal=('is_fatal', 'sum')
    ).reset_index()
    lighting_stats['fatal_rate'] = (lighting_stats['fatal'] / lighting_stats['total'] * 100).round(2)
    lighting_stats['type'] = 'Luminosité'
    lighting_stats.columns = ['condition', 'total', 'fatal', 'fatal_rate', 'type']
    
    # Calculate stats by weather (using 'weather' column)
    weather_stats = df.groupby('weather').agg(
        total=('weather', 'size'),
        fatal=('is_fatal', 'sum')
    ).reset_index()
    weather_stats['fatal_rate'] = (weather_stats['fatal'] / weather_stats['total'] * 100).round(2)
    weather_stats['type'] = 'Météo'
    weather_stats.columns = ['condition', 'total', 'fatal', 'fatal_rate', 'type']
    
    # Combine
    combined = pd.concat([lighting_stats, weather_stats], ignore_index=True)
    
    # Sort by fatal rate
    combined = combined.sort_values('fatal_rate', ascending=True)
    
    # Create grouped bar chart
    fig = go.Figure()
    
    for condition_type in ['Luminosité', 'Météo']:
        subset = combined[combined['type'] == condition_type]
        # Translate type for legend
        type_label = 'Lighting' if condition_type == 'Luminosité' else 'Weather'
        fig.add_trace(go.Bar(
            y=subset['condition'],
            x=subset['fatal_rate'],
            name=type_label,
            orientation='h',
            text=subset['fatal_rate'].apply(lambda x: f'{x:.1f}%'),
            textposition='outside'
        ))
    
    fig.update_layout(
        title='Fatal accident rate by weather and lighting conditions',
        xaxis_title='Fatality rate (%)',
        yaxis_title='',
        barmode='group',
        height=500,
        showlegend=True
    )
    
    return fig


# ============================================================================
# 3. INFRASTRUCTURE ANALYSIS
# ============================================================================

def plot_waffle_situation(df):
    """
    Waffle chart showing accident distribution by road situation with severity.
    Creates a grid of squares where each square represents a proportion of accidents.
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib import colors as mcolors
    
    # Use situation column to show where cyclists were when accident occurred
    situation_col = 'situation'
    
    # Group by situation and gravity
    situation_gravity = df.groupby([situation_col, 'gravity']).size().reset_index(name='count')
    
    # Color mapping for severity
    color_map = {
        'Unharmed': '#2ecc71',
        'Minor injury': '#f1c40f',
        'Hospitalized': '#e67e22',
        'Killed': '#e74c3c'
    }
    
    # Get unique situations (keep all of them)
    situations = situation_gravity[situation_col].unique()
    n_situations = len(situations)
    
    # Calculate grid layout
    n_cols = 4  # 4 columns instead of 5 for better readability
    n_rows = (n_situations + n_cols - 1) // n_cols  # Calculate needed rows
    
    # Create figure with subplots - larger size
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
    if n_rows == 1:
        axes = axes.reshape(1, -1)
    axes = axes.flatten()
    
    # Waffle chart parameters
    rows, cols = 10, 10  # 10x10 grid = 100 squares
    
    for idx, situation in enumerate(situations):
        ax = axes[idx]
        
        # Get data for this situation
        subset = situation_gravity[situation_gravity[situation_col] == situation]
        total = subset['count'].sum()
        
        if total == 0:
            ax.axis('off')
            continue
        
        # Calculate proportions (out of 100 squares)
        proportions = {}
        for _, row in subset.iterrows():
            gravity = row['gravity']
            count = row['count']
            proportion = int(round((count / total) * 100))
            proportions[gravity] = proportion
        
        # Ensure total is exactly 100
        total_prop = sum(proportions.values())
        if total_prop < 100:
            max_key = max(proportions, key=proportions.get)
            proportions[max_key] += (100 - total_prop)
        elif total_prop > 100:
            max_key = max(proportions, key=proportions.get)
            proportions[max_key] -= (total_prop - 100)
        
        # Create cumulative sums for coloring
        cumsum = {'Killed': 0, 'Hospitalized': 0, 'Minor injury': 0, 'Unharmed': 0}
        for gravity in ['Killed', 'Hospitalized', 'Minor injury', 'Unharmed']:
            if gravity in proportions:
                cumsum[gravity] = sum(proportions.get(g, 0) for g in ['Killed', 'Hospitalized', 'Minor injury', 'Unharmed'][:list(['Killed', 'Hospitalized', 'Minor injury', 'Unharmed']).index(gravity) + 1])
        
        # Create waffle chart
        current_square = 0
        for i in range(rows):
            for j in range(cols):
                square_color = '#cccccc'
                
                if current_square < cumsum['Killed']:
                    square_color = color_map['Killed']
                elif current_square < cumsum['Hospitalized']:
                    square_color = color_map['Hospitalized']
                elif current_square < cumsum['Minor injury']:
                    square_color = color_map['Minor injury']
                elif current_square < cumsum['Unharmed']:
                    square_color = color_map['Unharmed']
                
                square = mpatches.Rectangle((j, rows - i - 1), 1, 1, 
                                            facecolor=square_color, 
                                            edgecolor='white', linewidth=1.5)
                ax.add_patch(square)
                current_square += 1
        
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_aspect('equal')
        ax.axis('off')
        
        # Better titles - don't shorten too much
        situation_short = situation.replace('On ', '')
        if len(situation_short) > 20:
            situation_short = situation_short[:20] + '...'
        ax.set_title(situation_short, fontsize=11, fontweight='bold', pad=8)
    
    # Hide unused subplots
    for idx in range(n_situations, len(axes)):
        axes[idx].axis('off')
    
    # Add legend at the top - LARGER
    legend_elements = [
        mpatches.Patch(facecolor=color_map['Unharmed'], label='Unharmed'),
        mpatches.Patch(facecolor=color_map['Minor injury'], label='Minor injury'),
        mpatches.Patch(facecolor=color_map['Hospitalized'], label='Hospitalized'),
        mpatches.Patch(facecolor=color_map['Killed'], label='Killed')
    ]
    fig.legend(handles=legend_elements, loc='upper center', ncol=4, 
              fontsize=13, frameon=False, bbox_to_anchor=(0.5, 0.97),
              markerscale=1.5)  # Larger legend markers
    
    plt.suptitle('Accident distribution by road situation', 
                fontsize=15, fontweight='bold', y=0.95)
    plt.tight_layout(rect=[0, 0, 1, 0.92])
    
    return fig


def plot_bike_infrastructure_effectiveness(df):
    """
    Grouped bar chart comparing accidents WITH vs WITHOUT bike infrastructure.
    """
    # Use has_bike_infrastructure column if it exists
    df_copy = df.copy()
    
    if 'has_bike_infrastructure' in df_copy.columns:
        df_copy['infra_type'] = df_copy['has_bike_infrastructure'].map({
            True: 'With cycling infrastructure',
            False: 'Without cycling infrastructure'
        })
    else:
        # Fallback: check infrastructure column
        bike_infra_keywords = ['Bike lane', 'Piste cyclable', 'Bande cyclable', 'separated', 'painted']
        df_copy['has_bike_infra'] = df_copy['infrastructure'].str.contains('|'.join(bike_infra_keywords), case=False, na=False)
        df_copy['infra_type'] = df_copy['has_bike_infra'].map({
            True: 'With cycling infrastructure',
            False: 'Without cycling infrastructure'
        })
    
    # Group by infrastructure type and gravity
    infra_gravity = df_copy.groupby(['infra_type', 'gravity']).size().reset_index(name='count')
    
    fig = px.bar(
        infra_gravity,
        x='infra_type',
        y='count',
        color='gravity',
        color_discrete_map={
            'Unharmed': '#2ecc71',
            'Minor injury': '#f1c40f',
            'Hospitalized': '#e67e22',
            'Killed': '#e74c3c'
        },
        title='Cycling infrastructure effectiveness on accident severity',
        labels={'infra_type': 'Infrastructure type', 'count': 'Number of accidents', 'gravity': 'Severity'},
        barmode='group',
        text='count'
    )
    
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(
        height=550,
        xaxis_title='Infrastructure type',
        yaxis_title='Number of accidents'
    )
    
    return fig


