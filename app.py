import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from typing import Dict, List, Any
import time
import os
from datetime import datetime

# Import custom modules
from data_processor import DataProcessor
from chatbot import BudgetChatbot
from visualizations import BudgetVisualizations
from styles import apply_custom_styles, create_kpi_card, create_section_header, create_loading_indicator, format_currency

# Page configuration
st.set_page_config(
    page_title="Government Budget Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
apply_custom_styles()

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = DataProcessor()
    
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = BudgetChatbot(st.session_state.data_processor)
    
if 'visualizations' not in st.session_state:
    st.session_state.visualizations = BudgetVisualizations()
    
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = 2025
    
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    
if 'comparison_years' not in st.session_state:
    st.session_state.comparison_years = [2023, 2024, 2025]

def main():
    """Main application function"""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 class="main-title">Government Budget Dashboard</h1>
        <p class="main-subtitle">Ultra-Premium Interactive Financial Analysis Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar()
    
    # Main content
    render_main_content()

def render_sidebar():
    """Render the sidebar with controls and chat"""
    
    with st.sidebar:
        st.markdown(create_section_header("🎯 Controls", "Navigate through budget data"), unsafe_allow_html=True)
        
        # Year selector
        st.markdown('<div class="year-selector">', unsafe_allow_html=True)
        selected_year = st.selectbox(
            "Select Budget Year",
            options=list(range(2016, 2026)),
            index=list(range(2016, 2026)).index(st.session_state.selected_year),
            help="Choose a year to explore budget data"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        if selected_year != st.session_state.selected_year:
            st.session_state.selected_year = selected_year
            st.rerun()
        
        st.divider()
        
        # Quick stats
        with st.spinner("Loading overview..."):
            year_overview = st.session_state.data_processor.get_year_overview(selected_year)
            
        if not year_overview.get('error'):
            st.markdown(create_section_header("📊 Quick Stats", f"Year {selected_year}"), unsafe_allow_html=True)
            
            budget_data = year_overview.get('budget_summary', {})
            
            # Mini KPI cards
            col1, col2 = st.columns(2)
            
            with col1:
                expenditure = budget_data.get('total_expenditure', 0)
                st.metric(
                    "Total Expenditure",
                    f"₹{expenditure:,.0f} Cr",
                    help="Total government expenditure for the year"
                )
                
                deficit_pct = budget_data.get('fiscal_deficit_as_gdp_pct', 0)
                st.metric(
                    "Fiscal Deficit",
                    f"{deficit_pct:.1f}% of GDP",
                    help="Fiscal deficit as percentage of GDP"
                )
            
            with col2:
                receipts = budget_data.get('total_receipts', 0)
                st.metric(
                    "Total Receipts",
                    f"₹{receipts:,.0f} Cr",
                    help="Total government receipts for the year"
                )
                
                gdp = budget_data.get('gdp_nominal_in_crores', 0)
                st.metric(
                    "GDP (Nominal)",
                    f"₹{gdp:,.0f} Cr",
                    help="Nominal GDP for the year"
                )
        
        st.divider()
        
        # AI Chat Interface
        render_chat_interface()

def render_chat_interface():
    """Render the AI chatbot interface"""
    
    st.markdown(create_section_header("🤖 AI Budget Assistant", "Ask questions about budget data"), unsafe_allow_html=True)
    
    # Suggested questions
    with st.expander("💡 Suggested Questions", expanded=False):
        suggested = st.session_state.chatbot.get_suggested_questions(st.session_state.selected_year)
        
        for i, question in enumerate(suggested[:5]):
            if st.button(question, key=f"suggested_{i}", help="Click to ask this question"):
                response = st.session_state.chatbot.get_response(question, st.session_state.selected_year)
                st.session_state.chat_history.append({"user": question, "assistant": response})
                st.rerun()
    
    # Chat input
    user_query = st.text_input(
        "Ask me about budget data:",
        placeholder="e.g., What is the defense budget allocation?",
        help="Type your question about government budget and finances"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("Send", disabled=not user_query):
            if user_query.strip():
                with st.spinner("AI is analyzing..."):
                    response = st.session_state.chatbot.get_response(user_query, st.session_state.selected_year)
                    st.session_state.chat_history.append({"user": user_query, "assistant": response})
                st.rerun()
    
    with col2:
        if st.button("Clear"):
            st.session_state.chat_history = []
            st.session_state.chatbot.clear_conversation()
            st.rerun()
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # Show last 3 exchanges
        for chat in st.session_state.chat_history[-3:]:
            st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {chat["user"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-message assistant-message"><strong>AI:</strong> {chat["assistant"]}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        if len(st.session_state.chat_history) > 3:
            if st.button("Show Full Conversation"):
                for chat in st.session_state.chat_history:
                    st.text_area("You:", chat["user"], disabled=True)
                    st.text_area("AI:", chat["assistant"], disabled=True)

def render_main_content():
    """Render the main dashboard content"""
    
    # Tab interface
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Overview",
        "🏛️ Ministries", 
        "💰 Revenue vs Expenditure",
        "📈 Insights",
        "⚖️ Comparison"
    ])
    
    with tab1:
        render_overview_tab()
    
    with tab2:
        render_ministries_tab()
    
    with tab3:
        render_revenue_expenditure_tab()
    
    with tab4:
        render_insights_tab()
    
    with tab5:
        render_comparison_tab()

def render_overview_tab():
    """Render the overview tab"""
    
    st.markdown(create_section_header(
        f"Budget Overview {st.session_state.selected_year}", 
        "Comprehensive snapshot of government finances"
    ), unsafe_allow_html=True)
    
    with st.spinner("Loading overview data..."):
        year_overview = st.session_state.data_processor.get_year_overview(st.session_state.selected_year)
    
    if year_overview.get('error'):
        st.error(f"Error loading data: {year_overview['error']}")
        return
    
    budget_data = year_overview.get('budget_summary', {})
    fiscal_health = year_overview.get('fiscal_health', {})
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        expenditure = budget_data.get('total_expenditure', 0)
        trend = fiscal_health.get('deficit_trend', 'Unknown')
        st.markdown(create_kpi_card(
            "Total Expenditure", 
            expenditure, 
            trend, 
            "crores", 
            "primary"
        ), unsafe_allow_html=True)
    
    with col2:
        receipts = budget_data.get('total_receipts', 0)
        st.markdown(create_kpi_card(
            "Total Receipts", 
            receipts, 
            "Stable", 
            "crores", 
            "success"
        ), unsafe_allow_html=True)
    
    with col3:
        deficit_pct = budget_data.get('fiscal_deficit_as_gdp_pct', 0)
        color = "danger" if deficit_pct > 6 else "warning" if deficit_pct > 4 else "success"
        st.markdown(create_kpi_card(
            "Fiscal Deficit", 
            deficit_pct, 
            fiscal_health.get('deficit_trend', 'Unknown'), 
            "percentage", 
            color
        ), unsafe_allow_html=True)
    
    with col4:
        exp_to_gdp = fiscal_health.get('expenditure_to_gdp', 0)
        st.markdown(create_kpi_card(
            "Expenditure to GDP", 
            exp_to_gdp, 
            "Stable", 
            "percentage", 
            "secondary"
        ), unsafe_allow_html=True)
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        revenue_data = year_overview.get('revenue_breakdown', [])
        revenue_chart = st.session_state.visualizations.create_revenue_breakdown_chart(
            revenue_data, st.session_state.selected_year
        )
        st.plotly_chart(revenue_chart, width='stretch', key="overview_revenue_chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        ministry_data = year_overview.get('top_ministries', [])
        ministry_chart = st.session_state.visualizations.create_ministry_allocation_chart(
            ministry_data, st.session_state.selected_year
        )
        st.plotly_chart(ministry_chart, width='stretch', key="overview_ministry_chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Fiscal health gauge
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    fiscal_chart = st.session_state.visualizations.create_fiscal_health_chart(fiscal_health)
    st.plotly_chart(fiscal_chart, width='stretch', key="overview_fiscal_chart")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Key schemes
    schemes = year_overview.get('key_schemes', [])
    if schemes:
        st.markdown(create_section_header("Major Schemes & Allocations", f"Key government initiatives in {st.session_state.selected_year}"), unsafe_allow_html=True)
        
        scheme_df = pd.DataFrame(schemes[:10])
        if not scheme_df.empty:
            scheme_df['amount_formatted'] = scheme_df['amount'].apply(lambda x: f"₹{x:,.0f} Cr")
            st.dataframe(
                scheme_df[['ministry', 'scheme', 'amount_formatted', 'type']].rename(columns={
                    'ministry': 'Ministry',
                    'scheme': 'Scheme/Grant',
                    'amount_formatted': 'Allocation',
                    'type': 'Type'
                }),
                use_container_width=True
            )
    
    # Budget speech summary
    speech_summary = year_overview.get('speech_summary', '')
    if speech_summary and speech_summary != "No speech data available":
        st.markdown(create_section_header("Budget Speech Highlights", f"Key themes from {st.session_state.selected_year} budget speech"), unsafe_allow_html=True)
        st.info(speech_summary)

def render_ministries_tab():
    """Render the ministries tab"""
    
    st.markdown(create_section_header(
        f"Ministry-wise Analysis {st.session_state.selected_year}", 
        "Detailed breakdown of ministry allocations"
    ), unsafe_allow_html=True)
    
    with st.spinner("Loading ministry data..."):
        year_overview = st.session_state.data_processor.get_year_overview(st.session_state.selected_year)
    
    if year_overview.get('error'):
        st.error(f"Error loading data: {year_overview['error']}")
        return
    
    top_ministries = year_overview.get('top_ministries', [])
    
    if not top_ministries:
        st.warning("No ministry data available for this year.")
        return
    
    # Ministry selector
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ministry_names = [m['ministry'] for m in top_ministries]
        selected_ministry = st.selectbox(
            "Select Ministry for Detailed Analysis",
            options=ministry_names,
            help="Choose a ministry to see detailed allocation breakdown"
        )
    
    with col2:
        if st.button("Analyze with AI", help="Get AI insights about this ministry"):
            query = f"Analyze the budget allocation and trends for {selected_ministry}"
            with st.spinner("AI is analyzing ministry data..."):
                response = st.session_state.chatbot.get_response(query, st.session_state.selected_year)
                st.info(response)
    
    # Ministry details
    if selected_ministry:
        with st.spinner("Loading ministry details..."):
            ministry_details = st.session_state.data_processor.get_ministry_details(
                st.session_state.selected_year, selected_ministry
            )
        
        if not ministry_details.get('error'):
            # Ministry overview
            col1, col2, col3 = st.columns(3)
            
            with col1:
                current_allocation = ministry_details.get('current_allocation', 0)
                st.metric(
                    "Current Allocation",
                    f"₹{current_allocation:,.0f} Cr",
                    help=f"Budget allocation for {st.session_state.selected_year}"
                )
            
            with col2:
                rank = ministry_details.get('rank', 0)
                st.metric(
                    "Ranking",
                    f"#{rank}",
                    help="Rank by total allocation amount"
                )
            
            with col3:
                total_10_year = ministry_details.get('total_10_year', 'N/A')
                if total_10_year != 'N/A':
                    # Extract numeric value from string like "₹ 67,15,019"
                    try:
                        total_clean = total_10_year.replace('₹ ', '').replace(',', '')
                        total_numeric = float(total_clean)
                        st.metric(
                            "10-Year Total",
                            f"₹{total_numeric:,.0f} Cr",
                            help="Total allocation over 10 years (2016-2025)"
                        )
                    except:
                        st.metric("10-Year Total", total_10_year)
                else:
                    st.metric("10-Year Total", "N/A")
            
            # Historical trend chart
            historical_data = ministry_details.get('historical_trend', [])
            if historical_data:
                st.markdown(create_section_header("Allocation Trend", "Historical budget allocation over years"), unsafe_allow_html=True)
                
                years = [item['year'] for item in historical_data]
                amounts = [item['amount'] for item in historical_data]
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=years,
                    y=amounts,
                    mode='lines+markers',
                    name=selected_ministry[:30] + '...' if len(selected_ministry) > 30 else selected_ministry,
                    line=dict(color='#00FFFF', width=3),
                    marker=dict(size=8, color='#00FFFF'),
                    hovertemplate='<b>Year:</b> %{x}<br><b>Allocation:</b> ₹%{y:,.0f} Cr<extra></extra>'
                ))
                
                fig.update_layout(
                    title=f"<b>{selected_ministry} - Budget Trend</b>",
                    xaxis_title="Year",
                    yaxis_title="Allocation (₹ Crores)",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white')
                )
                
                st.plotly_chart(fig, width='stretch', key="ministry_trend_chart")
            
            # Major schemes
            major_schemes = ministry_details.get('major_schemes', [])
            if major_schemes:
                st.markdown(create_section_header("Major Schemes", f"Key initiatives under {selected_ministry}"), unsafe_allow_html=True)
                
                scheme_df = pd.DataFrame(major_schemes)
                if not scheme_df.empty:
                    scheme_df['amount_formatted'] = scheme_df['amount'].apply(lambda x: f"₹{x:,.0f} Cr")
                    st.dataframe(
                        scheme_df[['scheme', 'amount_formatted', 'type']].rename(columns={
                            'scheme': 'Scheme/Grant Name',
                            'amount_formatted': 'Allocation',
                            'type': 'Type'
                        }),
                        use_container_width=True
                    )
    
    # Overall ministry ranking
    st.markdown(create_section_header("Ministry Rankings", f"All ministries ranked by allocation in {st.session_state.selected_year}"), unsafe_allow_html=True)
    
    ministry_df = pd.DataFrame(top_ministries)
    if not ministry_df.empty:
        ministry_df['amount_formatted'] = ministry_df['amount'].apply(lambda x: f"₹{x:,.0f} Cr")
        st.dataframe(
            ministry_df[['rank', 'ministry', 'amount_formatted']].rename(columns={
                'rank': 'Rank',
                'ministry': 'Ministry',
                'amount_formatted': 'Allocation'
            }),
            use_container_width=True
        )

def render_revenue_expenditure_tab():
    """Render the revenue vs expenditure tab"""
    
    st.markdown(create_section_header(
        f"Revenue vs Expenditure Analysis {st.session_state.selected_year}", 
        "Balance sheet style financial breakdown"
    ), unsafe_allow_html=True)
    
    with st.spinner("Loading financial data..."):
        year_overview = st.session_state.data_processor.get_year_overview(st.session_state.selected_year)
    
    if year_overview.get('error'):
        st.error(f"Error loading data: {year_overview['error']}")
        return
    
    budget_data = year_overview.get('budget_summary', {})
    revenue_breakdown = year_overview.get('revenue_breakdown', [])
    
    # Financial summary
    col1, col2, col3 = st.columns(3)
    
    total_receipts = budget_data.get('total_receipts', 0)
    total_expenditure = budget_data.get('total_expenditure', 0)
    fiscal_deficit = budget_data.get('fiscal_deficit_in_crores', 0)
    
    with col1:
        st.markdown(create_kpi_card(
            "Total Receipts", 
            total_receipts, 
            "Revenue Side", 
            "crores", 
            "success"
        ), unsafe_allow_html=True)
    
    with col2:
        st.markdown(create_kpi_card(
            "Total Expenditure", 
            total_expenditure, 
            "Expense Side", 
            "crores", 
            "primary"
        ), unsafe_allow_html=True)
    
    with col3:
        balance = total_receipts - total_expenditure
        color = "success" if balance >= 0 else "danger"
        trend = "Surplus" if balance >= 0 else "Deficit"
        st.markdown(create_kpi_card(
            "Budget Balance", 
            abs(balance), 
            trend, 
            "crores", 
            color
        ), unsafe_allow_html=True)
    
    # Waterfall chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    waterfall_chart = st.session_state.visualizations.create_revenue_vs_expenditure_chart([budget_data])
    st.plotly_chart(waterfall_chart, width='stretch', key="revenue_expenditure_waterfall")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Revenue and Expenditure side by side
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(create_section_header("💰 Revenue Sources", "Breakdown of government receipts"), unsafe_allow_html=True)
        
        if revenue_breakdown:
            # Revenue pie chart
            revenue_chart = st.session_state.visualizations.create_revenue_breakdown_chart(
                revenue_breakdown, st.session_state.selected_year
            )
            st.plotly_chart(revenue_chart, width='stretch', key="revenue_breakdown_chart")
            
            # Revenue table
            revenue_df = pd.DataFrame(revenue_breakdown)
            revenue_df['amount_formatted'] = revenue_df['amount'].apply(lambda x: f"₹{x:,.0f} Cr")
            revenue_df['percentage_formatted'] = revenue_df['percentage'].apply(lambda x: f"{x:.1f}%")
            
            st.dataframe(
                revenue_df[['source', 'amount_formatted', 'percentage_formatted']].rename(columns={
                    'source': 'Revenue Source',
                    'amount_formatted': 'Amount',
                    'percentage_formatted': 'Share'
                }),
                use_container_width=True
            )
        else:
            st.warning("No revenue data available for this year.")
    
    with col2:
        st.markdown(create_section_header("💸 Expenditure by Ministries", "Top spending ministries"), unsafe_allow_html=True)
        
        top_ministries = year_overview.get('top_ministries', [])
        if top_ministries:
            # Ministry expenditure chart
            ministry_chart = st.session_state.visualizations.create_ministry_allocation_chart(
                top_ministries[:8], st.session_state.selected_year
            )
            st.plotly_chart(ministry_chart, width='stretch', key="expenditure_ministry_chart")
            
            # Expenditure table
            ministry_df = pd.DataFrame(top_ministries[:10])
            ministry_df['amount_formatted'] = ministry_df['amount'].apply(lambda x: f"₹{x:,.0f} Cr")
            
            st.dataframe(
                ministry_df[['ministry', 'amount_formatted', 'rank']].rename(columns={
                    'ministry': 'Ministry',
                    'amount_formatted': 'Allocation',
                    'rank': 'Rank'
                }),
                use_container_width=True
            )
        else:
            st.warning("No expenditure data available for this year.")
    
    # Fiscal indicators
    st.divider()
    st.markdown(create_section_header("📊 Fiscal Health Indicators", "Key financial ratios and metrics"), unsafe_allow_html=True)
    
    fiscal_health = year_overview.get('fiscal_health', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        deficit_ratio = budget_data.get('fiscal_deficit_as_gdp_pct', 0)
        st.metric(
            "Fiscal Deficit (% of GDP)",
            f"{deficit_ratio:.1f}%",
            help="Fiscal deficit as percentage of GDP"
        )
    
    with col2:
        exp_to_gdp = fiscal_health.get('expenditure_to_gdp', 0)
        st.metric(
            "Expenditure to GDP",
            f"{exp_to_gdp:.1f}%",
            help="Total expenditure as percentage of GDP"
        )
    
    with col3:
        rev_to_gdp = fiscal_health.get('revenue_to_gdp', 0)
        st.metric(
            "Revenue to GDP",
            f"{rev_to_gdp:.1f}%",
            help="Total revenue as percentage of GDP"
        )
    
    with col4:
        gdp = budget_data.get('gdp_nominal_in_crores', 0)
        st.metric(
            "Nominal GDP",
            f"₹{gdp:,.0f} Cr",
            help="Gross Domestic Product (Nominal)"
        )

def render_insights_tab():
    """Render the insights tab with AI-powered analysis"""
    
    st.markdown(create_section_header(
        "AI-Powered Budget Insights", 
        "Comprehensive analysis of trends, patterns, and key findings"
    ), unsafe_allow_html=True)
    
    with st.spinner("Generating insights..."):
        insights_data = st.session_state.data_processor.get_insights_data()
    
    if insights_data.get('error'):
        st.error(f"Error generating insights: {insights_data['error']}")
        return
    
    # Key Findings
    key_findings = insights_data.get('key_findings', [])
    if key_findings:
        st.markdown(create_section_header("🔍 Key Findings", "Major insights from budget analysis"), unsafe_allow_html=True)
        
        for i, finding in enumerate(key_findings, 1):
            st.success(f"**Finding #{i}:** {finding}")
    
    # Revenue Trends Analysis
    revenue_trends = insights_data.get('revenue_trends', {})
    if revenue_trends:
        st.markdown(create_section_header("📈 Revenue Trends", "Growth analysis of major revenue sources"), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        for i, (source, data) in enumerate(revenue_trends.items()):
            if i < 3:  # Show top 3 sources
                with [col1, col2, col3][i]:
                    avg_growth = data.get('avg_growth', 0)
                    growth_color = "success" if avg_growth > 0 else "danger" if avg_growth < -5 else "warning"
                    
                    st.markdown(create_kpi_card(
                        source.replace(' (GST)', ''),
                        avg_growth,
                        "Average Growth",
                        "percentage",
                        growth_color
                    ), unsafe_allow_html=True)
        
        # Revenue trend chart
        if revenue_trends:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            fig = go.Figure()
            colors = ['#00FFFF', '#FF1493', '#FFD700']
            
            for i, (source, data) in enumerate(revenue_trends.items()):
                growth_data = data.get('growth_rates', [])
                if growth_data:
                    years = [item['year'] for item in growth_data]
                    rates = [item['growth_rate'] for item in growth_data]
                    
                    fig.add_trace(go.Scatter(
                        x=years,
                        y=rates,
                        mode='lines+markers',
                        name=source,
                        line=dict(color=colors[i % len(colors)], width=3),
                        marker=dict(size=8)
                    ))
            
            fig.update_layout(
                title="<b>Revenue Growth Trends</b>",
                xaxis_title="Year",
                yaxis_title="Growth Rate (%)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, width='stretch', key="revenue_growth_chart")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Expenditure Patterns
    expenditure_patterns = insights_data.get('expenditure_patterns', {})
    if expenditure_patterns:
        st.markdown(create_section_header("💸 Expenditure Patterns", "Analysis of spending trends and ministry performance"), unsafe_allow_html=True)
        
        # Top growing and declining ministries
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🚀 Top Growing Ministries")
            top_growing = expenditure_patterns.get('top_growing_ministries', [])
            
            for ministry, growth in top_growing[:5]:
                color = "success" if growth > 50 else "warning" if growth > 20 else "primary"
                st.markdown(f"""
                <div style="padding: 0.5rem; margin: 0.25rem 0; background: rgba(26,26,46,0.6); border-radius: 8px; border-left: 3px solid {'#00FF7F' if color == 'success' else '#FFD700' if color == 'warning' else '#00FFFF'};">
                    <strong>{ministry[:40]}...</strong><br>
                    <span style="color: {'#00FF7F' if color == 'success' else '#FFD700' if color == 'warning' else '#00FFFF'};">+{growth:.1f}% growth</span>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("📉 Declining Ministries")
            declining = expenditure_patterns.get('declining_ministries', [])
            
            for ministry, growth in declining:
                st.markdown(f"""
                <div style="padding: 0.5rem; margin: 0.25rem 0; background: rgba(26,26,46,0.6); border-radius: 8px; border-left: 3px solid #FF4500;">
                    <strong>{ministry[:40]}...</strong><br>
                    <span style="color: #FF4500;">{growth:.1f}% decline</span>
                </div>
                """, unsafe_allow_html=True)
    
    # Fiscal Analysis
    fiscal_analysis = insights_data.get('fiscal_analysis', {})
    if fiscal_analysis:
        st.markdown(create_section_header("⚖️ Fiscal Health Analysis", "Long-term fiscal sustainability metrics"), unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            avg_deficit = fiscal_analysis.get('average_deficit_ratio', 0)
            color = "success" if avg_deficit < 3 else "warning" if avg_deficit < 6 else "danger"
            st.markdown(create_kpi_card(
                "Avg Deficit Ratio",
                avg_deficit,
                "10-Year Average",
                "percentage",
                color
            ), unsafe_allow_html=True)
        
        with col2:
            avg_exp_gdp = fiscal_analysis.get('average_expenditure_to_gdp', 0)
            st.markdown(create_kpi_card(
                "Avg Exp/GDP Ratio",
                avg_exp_gdp,
                "10-Year Average",
                "percentage",
                "primary"
            ), unsafe_allow_html=True)
        
        with col3:
            trend_analysis = fiscal_analysis.get('trend_analysis', 'Unknown')
            color = "success" if "improving" in trend_analysis.lower() else "danger" if "deteriorating" in trend_analysis.lower() else "warning"
            st.info(f"**Fiscal Trend:** {trend_analysis}")
        
        # Fiscal trend chart
        yearly_data = fiscal_analysis.get('yearly_data', [])
        if yearly_data:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            years = [item['year'] for item in yearly_data]
            deficit_ratios = [item['fiscal_deficit_ratio'] for item in yearly_data]
            exp_to_gdp = [item['expenditure_to_gdp'] for item in yearly_data]
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=years,
                y=deficit_ratios,
                mode='lines+markers',
                name='Fiscal Deficit (% of GDP)',
                line=dict(color='#FF4500', width=3),
                marker=dict(size=8)
            ))
            
            fig.add_trace(go.Scatter(
                x=years,
                y=exp_to_gdp,
                mode='lines+markers',
                name='Expenditure (% of GDP)',
                line=dict(color='#00FFFF', width=3),
                marker=dict(size=8)
            ))
            
            fig.update_layout(
                title="<b>Fiscal Health Trends</b>",
                xaxis_title="Year",
                yaxis_title="Percentage of GDP",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, width='stretch', key="fiscal_health_chart")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # AI-Generated Analysis
    st.divider()
    st.markdown(create_section_header("🤖 AI Analysis", f"Comprehensive budget analysis for {st.session_state.selected_year}"), unsafe_allow_html=True)
    
    # Generate AI analysis for current year
    if st.button("Generate AI Analysis for Current Year", help="Get comprehensive AI analysis"):
        with st.spinner("AI is analyzing budget data..."):
            analysis_query = f"Provide a comprehensive analysis of the {st.session_state.selected_year} budget including key highlights, policy priorities, fiscal health, and recommendations."
            ai_analysis = st.session_state.chatbot.get_response(analysis_query, st.session_state.selected_year)
            st.info(ai_analysis)
    
    # Budget speech analysis
    if st.button("Analyze Budget Speech", help="Get AI analysis of budget speech"):
        with st.spinner("Analyzing budget speech..."):
            speech_analysis = st.session_state.chatbot.analyze_budget_speech(st.session_state.selected_year)
            st.success(speech_analysis)

def render_comparison_tab():
    """Render the comparison tab"""
    
    st.markdown(create_section_header(
        "Multi-Year Budget Comparison", 
        "Compare budget data across multiple years"
    ), unsafe_allow_html=True)
    
    # Year selection for comparison
    st.subheader("Select Years for Comparison")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        available_years = list(range(2016, 2026))
        selected_years = st.multiselect(
            "Choose up to 5 years to compare:",
            options=available_years,
            default=st.session_state.comparison_years,
            max_selections=5,
            help="Select multiple years to see comparative analysis"
        )
    
    with col2:
        if st.button("Reset to Defaults"):
            selected_years = [2023, 2024, 2025]
            st.session_state.comparison_years = selected_years
            st.rerun()
    
    if selected_years != st.session_state.comparison_years:
        st.session_state.comparison_years = selected_years
        st.rerun()
    
    if not selected_years:
        st.warning("Please select at least one year for comparison.")
        return
    
    if len(selected_years) < 2:
        st.info("Select at least 2 years to see meaningful comparisons.")
        return
    
    with st.spinner("Loading comparison data..."):
        comparison_data = st.session_state.data_processor.get_comparison_data(selected_years)
    
    if comparison_data.get('error'):
        st.error(f"Error loading comparison data: {comparison_data['error']}")
        return
    
    # Budget summary comparison
    budget_summaries = comparison_data.get('budget_summary', [])
    if budget_summaries:
        st.markdown(create_section_header("📊 Budget Overview Comparison", "Key metrics across selected years"), unsafe_allow_html=True)
        
        # Create comparison metrics
        years = [item['year'] for item in budget_summaries]
        expenditures = [item['total_expenditure'] for item in budget_summaries]
        receipts = [item['total_receipts'] for item in budget_summaries]
        deficits = [item['fiscal_deficit_as_gdp_pct'] for item in budget_summaries]
        
        # Metrics table
        comparison_df = pd.DataFrame({
            'Year': years,
            'Total Expenditure (₹ Cr)': [f"{exp:,.0f}" for exp in expenditures],
            'Total Receipts (₹ Cr)': [f"{rec:,.0f}" for rec in receipts],
            'Fiscal Deficit (% GDP)': [f"{def_:.1f}%" for def_ in deficits],
            'Budget Balance (₹ Cr)': [f"{rec-exp:+,.0f}" for exp, rec in zip(expenditures, receipts)]
        })
        
        st.dataframe(comparison_df, use_container_width=True)
        
        # Trend chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        trend_chart = st.session_state.visualizations.create_trend_analysis_chart(comparison_data)
        st.plotly_chart(trend_chart, width='stretch', key="comparison_trend_chart")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Ministry comparison
    ministry_trends = comparison_data.get('ministry_trends', {})
    if ministry_trends:
        st.markdown(create_section_header("🏛️ Ministry Allocation Trends", "Compare spending across ministries"), unsafe_allow_html=True)
        
        # Ministry selector for comparison
        available_ministries = list(ministry_trends.keys())
        selected_ministries = st.multiselect(
            "Select ministries to compare:",
            options=available_ministries,
            default=available_ministries[:5] if len(available_ministries) >= 5 else available_ministries,
            max_selections=8,
            help="Choose ministries to see their allocation trends"
        )
        
        if selected_ministries:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            ministry_comparison_chart = st.session_state.visualizations.create_ministry_comparison_chart(
                ministry_trends, selected_ministries
            )
            st.plotly_chart(ministry_comparison_chart, width='stretch', key="comparison_ministry_chart")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Ministry comparison table
            ministry_comparison_data = []
            for ministry in selected_ministries:
                if ministry in ministry_trends:
                    data = ministry_trends[ministry]
                    for item in data:
                        ministry_comparison_data.append({
                            'Ministry': ministry,
                            'Year': item['year'],
                            'Allocation': item['amount']
                        })
            
            if ministry_comparison_data:
                comp_df = pd.DataFrame(ministry_comparison_data)
                pivot_df = comp_df.pivot(index='Ministry', columns='Year', values='Allocation')
                
                # Format as currency
                for col in pivot_df.columns:
                    pivot_df[col] = pivot_df[col].apply(lambda x: f"₹{x:,.0f}" if pd.notna(x) else "N/A")
                
                st.dataframe(pivot_df, use_container_width=True)
    
    # Revenue comparison
    revenue_comparison = comparison_data.get('revenue_comparison', {})
    if revenue_comparison:
        st.markdown(create_section_header("💰 Revenue Source Trends", "Track revenue sources over time"), unsafe_allow_html=True)
        
        # Revenue selector
        available_sources = list(revenue_comparison.keys())
        selected_sources = st.multiselect(
            "Select revenue sources to compare:",
            options=available_sources,
            default=available_sources[:4] if len(available_sources) >= 4 else available_sources,
            max_selections=6,
            help="Choose revenue sources to see their trends"
        )
        
        if selected_sources:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            fig = go.Figure()
            colors = ['#00FFFF', '#FF1493', '#FFD700', '#00FF7F', '#FF4500', '#9370DB']
            
            for i, source in enumerate(selected_sources):
                if source in revenue_comparison:
                    data = revenue_comparison[source]
                    years = [item['year'] for item in data]
                    amounts = [item['amount'] for item in data]
                    
                    source_short = source[:20] + '...' if len(source) > 20 else source
                    
                    fig.add_trace(go.Scatter(
                        x=years,
                        y=amounts,
                        mode='lines+markers',
                        name=source_short,
                        line=dict(color=colors[i % len(colors)], width=3),
                        marker=dict(size=8),
                        hovertemplate=f'<b>{source_short}</b><br>Year: %{{x}}<br>Amount: ₹%{{y:,.0f}} Cr<extra></extra>'
                    ))
            
            fig.update_layout(
                title="<b>Revenue Source Trends</b>",
                xaxis_title="Year",
                yaxis_title="Amount (₹ Crores)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, width='stretch', key="revenue_sources_chart")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Year-over-year analysis
    if len(selected_years) >= 2:
        st.markdown(create_section_header("📈 Growth Analysis", "Year-over-year changes and growth rates"), unsafe_allow_html=True)
        
        # Calculate growth rates
        growth_data = []
        for i in range(1, len(budget_summaries)):
            current = budget_summaries[i]
            previous = budget_summaries[i-1]
            
            exp_growth = ((current['total_expenditure'] - previous['total_expenditure']) / previous['total_expenditure']) * 100
            rec_growth = ((current['total_receipts'] - previous['total_receipts']) / previous['total_receipts']) * 100
            gdp_growth = ((current['gdp_nominal_in_crores'] - previous['gdp_nominal_in_crores']) / previous['gdp_nominal_in_crores']) * 100
            
            growth_data.append({
                'Year': f"{previous['year']}-{current['year']}",
                'Expenditure Growth (%)': f"{exp_growth:+.1f}%",
                'Revenue Growth (%)': f"{rec_growth:+.1f}%",
                'GDP Growth (%)': f"{gdp_growth:+.1f}%",
                'Deficit Change (pp)': f"{current['fiscal_deficit_as_gdp_pct'] - previous['fiscal_deficit_as_gdp_pct']:+.1f}"
            })
        
        if growth_data:
            growth_df = pd.DataFrame(growth_data)
            st.dataframe(growth_df, use_container_width=True)
    
    # AI Comparison Analysis
    st.divider()
    if st.button("Generate AI Comparison Analysis", help="Get AI insights about the comparison"):
        with st.spinner("AI is analyzing comparison data..."):
            comparison_query = f"Compare and analyze the budget data for years {', '.join(map(str, selected_years))}. Highlight key trends, changes, and insights."
            ai_comparison = st.session_state.chatbot.get_response(comparison_query)
            st.info(ai_comparison)

if __name__ == "__main__":
    main()
