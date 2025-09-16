import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import streamlit as st

class BudgetVisualizations:
    def __init__(self):
        # Premium dark theme colors
        self.colors = {
            'primary': '#00FFFF',      # Cyan
            'secondary': '#FF1493',    # Deep Pink
            'accent': '#FFD700',       # Gold
            'success': '#00FF7F',      # Spring Green
            'danger': '#FF4500',       # Orange Red
            'background': '#0a0a0a',   # Deep Black
            'surface': '#1a1a2e',      # Dark Blue
            'text': '#ffffff',         # White
            'text_secondary': '#b0b0b0' # Light Gray
        }
        
        # Custom color palette for charts
        self.chart_colors = [
            '#00FFFF', '#FF1493', '#FFD700', '#00FF7F', '#FF4500',
            '#9370DB', '#00CED1', '#FF69B4', '#32CD32', '#FF6347'
        ]
    
    def create_revenue_breakdown_chart(self, revenue_data: List[Dict], year: int) -> go.Figure:
        """Create an animated donut chart for revenue breakdown"""
        if not revenue_data:
            return self._create_empty_chart("No revenue data available")
        
        labels = [item['source'] for item in revenue_data]
        values = [item['amount'] for item in revenue_data]
        
        fig = go.Figure(data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker=dict(
                    colors=self.chart_colors[:len(labels)],
                    line=dict(color='#ffffff', width=2)
                ),
                textinfo='label+percent',
                textposition='outside',
                textfont=dict(size=12, color='white'),
                hovertemplate='<b>%{label}</b><br>' +
                            'Amount: ₹%{value:,.0f} crores<br>' +
                            'Percentage: %{percent}<br>' +
                            '<extra></extra>'
            )
        ])
        
        # Add center text
        fig.add_annotation(
            text=f"<b>Revenue {year}</b><br>₹{sum(values):,.0f} Cr",
            x=0.5, y=0.5,
            font_size=16,
            font_color='white',
            showarrow=False
        )
        
        fig.update_layout(
            title=dict(
                text=f"<b>Revenue Breakdown - {year}</b>",
                x=0.5,
                font=dict(size=20, color='white')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(color='white')
            ),
            margin=dict(l=50, r=150, t=80, b=50)
        )
        
        return fig
    
    def create_ministry_allocation_chart(self, ministry_data: List[Dict], year: int) -> go.Figure:
        """Create a horizontal bar chart for top ministry allocations"""
        if not ministry_data:
            return self._create_empty_chart("No ministry data available")
        
        # Take top 10 ministries
        top_ministries = ministry_data[:10]
        
        ministries = [m['ministry'] for m in top_ministries]
        amounts = [m['amount'] for m in top_ministries]
        
        # Truncate long ministry names
        ministries_short = [name[:30] + '...' if len(name) > 30 else name for name in ministries]
        
        fig = go.Figure(data=[
            go.Bar(
                x=amounts,
                y=ministries_short,
                orientation='h',
                marker=dict(
                    color=amounts,
                    colorscale=[[0, self.colors['primary']], [1, self.colors['secondary']]],
                    line=dict(color='white', width=1)
                ),
                text=[f"₹{amt:,.0f}" for amt in amounts],
                textposition='auto',
                textfont=dict(color='white', size=11),
                hovertemplate='<b>%{y}</b><br>' +
                            'Allocation: ₹%{x:,.0f} crores<br>' +
                            '<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title=dict(
                text=f"<b>Top Ministry Allocations - {year}</b>",
                x=0.5,
                font=dict(size=20, color='white')
            ),
            xaxis=dict(
                title="Allocation (₹ Crores)",
                gridcolor='rgba(255,255,255,0.1)',
                color='white'
            ),
            yaxis=dict(
                title="Ministries",
                color='white'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=200, r=50, t=80, b=50)
        )
        
        return fig
    
    def create_fiscal_health_chart(self, fiscal_data: Dict) -> go.Figure:
        """Create a gauge chart for fiscal health indicators"""
        if not fiscal_data or fiscal_data.get('error'):
            return self._create_empty_chart("No fiscal data available")
        
        deficit_ratio = fiscal_data.get('fiscal_deficit_ratio', 0)
        
        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=deficit_ratio,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "<b>Fiscal Deficit (% of GDP)</b>", 'font': {'color': 'white', 'size': 18}},
            delta={'reference': 3.0},  # Target fiscal deficit
            gauge={
                'axis': {'range': [0, 10], 'tickcolor': 'white'},
                'bar': {'color': self.colors['primary']},
                'steps': [
                    {'range': [0, 3], 'color': self.colors['success']},
                    {'range': [3, 6], 'color': self.colors['accent']},
                    {'range': [6, 10], 'color': self.colors['danger']}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 6
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(l=50, r=50, t=100, b=50)
        )
        
        return fig
    
    def create_trend_analysis_chart(self, comparison_data: Dict) -> go.Figure:
        """Create multi-line chart for budget trends"""
        if not comparison_data or comparison_data.get('error'):
            return self._create_empty_chart("No comparison data available")
        
        budget_summary = comparison_data.get('budget_summary', [])
        if not budget_summary:
            return self._create_empty_chart("No budget summary data available")
        
        years = [item['year'] for item in budget_summary]
        expenditures = [item['total_expenditure'] for item in budget_summary]
        receipts = [item['total_receipts'] for item in budget_summary]
        deficits = [item['fiscal_deficit_as_gdp_pct'] for item in budget_summary]
        
        # Create subplot with secondary y-axis
        fig = make_subplots(
            specs=[[{"secondary_y": True}]],
            subplot_titles=["Budget Trends Analysis"]
        )
        
        # Add expenditure and receipts
        fig.add_trace(
            go.Scatter(
                x=years,
                y=expenditures,
                mode='lines+markers',
                name='Total Expenditure',
                line=dict(color=self.colors['primary'], width=3),
                marker=dict(size=8),
                hovertemplate='<b>Expenditure</b><br>Year: %{x}<br>Amount: ₹%{y:,.0f} crores<extra></extra>'
            ),
            secondary_y=False
        )
        
        fig.add_trace(
            go.Scatter(
                x=years,
                y=receipts,
                mode='lines+markers',
                name='Total Receipts',
                line=dict(color=self.colors['success'], width=3),
                marker=dict(size=8),
                hovertemplate='<b>Receipts</b><br>Year: %{x}<br>Amount: ₹%{y:,.0f} crores<extra></extra>'
            ),
            secondary_y=False
        )
        
        # Add fiscal deficit ratio on secondary y-axis
        fig.add_trace(
            go.Scatter(
                x=years,
                y=deficits,
                mode='lines+markers',
                name='Fiscal Deficit (% GDP)',
                line=dict(color=self.colors['secondary'], width=3, dash='dash'),
                marker=dict(size=8),
                hovertemplate='<b>Fiscal Deficit</b><br>Year: %{x}<br>Ratio: %{y:.1f}% of GDP<extra></extra>'
            ),
            secondary_y=True
        )
        
        # Update axes
        fig.update_xaxes(
            title_text="Year",
            gridcolor='rgba(255,255,255,0.1)',
            color='white'
        )
        
        fig.update_yaxes(
            title_text="Amount (₹ Crores)",
            secondary_y=False,
            gridcolor='rgba(255,255,255,0.1)',
            color='white'
        )
        
        fig.update_yaxes(
            title_text="Fiscal Deficit (% of GDP)",
            secondary_y=True,
            color='white'
        )
        
        fig.update_layout(
            title=dict(
                text="<b>Budget Trends Over Time</b>",
                x=0.5,
                font=dict(size=20, color='white')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(26,26,46,0.8)',
                font=dict(color='white')
            ),
            hovermode='x unified'
        )
        
        return fig
    
    def create_ministry_comparison_chart(self, ministry_trends: Dict, selected_ministries: List[str] = None) -> go.Figure:
        """Create comparison chart for selected ministries"""
        if not ministry_trends:
            return self._create_empty_chart("No ministry trend data available")
        
        # Use top 5 ministries if none selected
        if not selected_ministries:
            selected_ministries = list(ministry_trends.keys())[:5]
        
        fig = go.Figure()
        
        for i, ministry in enumerate(selected_ministries):
            if ministry in ministry_trends:
                data = ministry_trends[ministry]
                years = [item['year'] for item in data]
                amounts = [item['amount'] for item in data]
                
                ministry_short = ministry[:20] + '...' if len(ministry) > 20 else ministry
                
                fig.add_trace(
                    go.Scatter(
                        x=years,
                        y=amounts,
                        mode='lines+markers',
                        name=ministry_short,
                        line=dict(color=self.chart_colors[i % len(self.chart_colors)], width=3),
                        marker=dict(size=8),
                        hovertemplate=f'<b>{ministry_short}</b><br>Year: %{{x}}<br>Allocation: ₹%{{y:,.0f}} crores<extra></extra>'
                    )
                )
        
        fig.update_layout(
            title=dict(
                text="<b>Ministry Allocation Trends</b>",
                x=0.5,
                font=dict(size=20, color='white')
            ),
            xaxis=dict(
                title="Year",
                gridcolor='rgba(255,255,255,0.1)',
                color='white'
            ),
            yaxis=dict(
                title="Allocation (₹ Crores)",
                gridcolor='rgba(255,255,255,0.1)',
                color='white'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(26,26,46,0.8)',
                font=dict(color='white')
            ),
            hovermode='x unified'
        )
        
        return fig
    
    def create_revenue_vs_expenditure_chart(self, budget_summary: List[Dict]) -> go.Figure:
        """Create waterfall chart showing revenue vs expenditure"""
        if not budget_summary:
            return self._create_empty_chart("No budget summary available")
        
        # Use latest year data
        latest_data = budget_summary[-1] if budget_summary else {}
        
        receipts = latest_data.get('total_receipts', 0)
        expenditure = latest_data.get('total_expenditure', 0)
        deficit = expenditure - receipts
        year = latest_data.get('year', 'N/A')
        
        fig = go.Figure(go.Waterfall(
            name="",
            orientation="v",
            measure=["absolute", "absolute", "relative"],
            x=["Total Receipts", "Total Expenditure", "Fiscal Deficit"],
            y=[receipts, expenditure, -deficit],
            text=[f"₹{receipts:,.0f}", f"₹{expenditure:,.0f}", f"₹{deficit:,.0f}"],
            textposition="outside",
            textfont=dict(color='white', size=14),
            connector={"line": {"color": "rgba(255,255,255,0.3)"}},
            increasing={"marker": {"color": self.colors['success']}},
            decreasing={"marker": {"color": self.colors['danger']}},
            totals={"marker": {"color": self.colors['primary']}},
            hovertemplate='<b>%{x}</b><br>Amount: ₹%{y:,.0f} crores<extra></extra>'
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>Budget Balance - {year}</b>",
                x=0.5,
                font=dict(size=20, color='white')
            ),
            xaxis=dict(color='white'),
            yaxis=dict(
                title="Amount (₹ Crores)",
                gridcolor='rgba(255,255,255,0.1)',
                color='white'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        return fig
    
    def create_scheme_performance_chart(self, schemes_data: List[Dict]) -> go.Figure:
        """Create bubble chart for scheme performance"""
        if not schemes_data:
            return self._create_empty_chart("No scheme data available")
        
        # Prepare data
        scheme_names = [scheme['scheme'][:30] + '...' if len(scheme['scheme']) > 30 else scheme['scheme'] 
                      for scheme in schemes_data[:10]]
        amounts = [scheme['amount'] for scheme in schemes_data[:10]]
        types = [scheme['type'] for scheme in schemes_data[:10]]
        
        # Create color mapping for types
        unique_types = list(set(types))
        type_colors = {t: self.chart_colors[i % len(self.chart_colors)] for i, t in enumerate(unique_types)}
        colors = [type_colors[t] for t in types]
        
        fig = go.Figure(data=go.Scatter(
            x=list(range(len(scheme_names))),
            y=amounts,
            mode='markers',
            marker=dict(
                size=[min(60, max(20, amt/1000)) for amt in amounts],  # Size based on amount
                color=colors,
                opacity=0.8,
                line=dict(width=2, color='white')
            ),
            text=scheme_names,
            textposition="middle center",
            textfont=dict(color='white', size=10),
            hovertemplate='<b>%{text}</b><br>Amount: ₹%{y:,.0f} crores<br>Type: %{customdata}<extra></extra>',
            customdata=types
        ))
        
        fig.update_layout(
            title=dict(
                text="<b>Major Schemes by Allocation</b>",
                x=0.5,
                font=dict(size=20, color='white')
            ),
            xaxis=dict(
                showticklabels=False,
                showgrid=False,
                color='white'
            ),
            yaxis=dict(
                title="Allocation (₹ Crores)",
                gridcolor='rgba(255,255,255,0.1)',
                color='white'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        return fig
    
    def _create_empty_chart(self, message: str) -> go.Figure:
        """Create an empty chart with a message"""
        fig = go.Figure()
        
        fig.add_annotation(
            text=message,
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=16, color='white')
        )
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False, color='white'),
            yaxis=dict(showgrid=False, showticklabels=False, color='white'),
            font=dict(color='white')
        )
        
        return fig
    
    def create_kpi_cards_data(self, year_overview: Dict) -> Dict:
        """Prepare data for KPI cards display"""
        if not year_overview or year_overview.get('error'):
            return {}
        
        budget_summary = year_overview.get('budget_summary', {})
        fiscal_health = year_overview.get('fiscal_health', {})
        
        return {
            'total_expenditure': {
                'value': budget_summary.get('total_expenditure', 0),
                'format': 'crores',
                'trend': fiscal_health.get('deficit_trend', 'Unknown'),
                'color': 'primary'
            },
            'total_receipts': {
                'value': budget_summary.get('total_receipts', 0),
                'format': 'crores',
                'trend': 'Stable',
                'color': 'success'
            },
            'fiscal_deficit': {
                'value': budget_summary.get('fiscal_deficit_as_gdp_pct', 0),
                'format': 'percentage',
                'trend': fiscal_health.get('deficit_trend', 'Unknown'),
                'color': 'danger' if budget_summary.get('fiscal_deficit_as_gdp_pct', 0) > 6 else 'accent'
            },
            'gdp_ratio': {
                'value': fiscal_health.get('expenditure_to_gdp', 0),
                'format': 'percentage',
                'trend': 'Stable',
                'color': 'secondary'
            }
        }
