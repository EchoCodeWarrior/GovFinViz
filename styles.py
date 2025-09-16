import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles for premium dark mode"""
    
    custom_css = """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Roboto:wght@300;400;500;700&family=Fira+Code:wght@400;500&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
        color: #ffffff;
    }
    
    /* Custom Background with Subtle Animation */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(0, 255, 255, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(255, 20, 147, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(255, 215, 0, 0.05) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
        animation: subtleFloat 20s ease-in-out infinite;
    }
    
    @keyframes subtleFloat {
        0%, 100% { transform: translateY(0px) scale(1); }
        50% { transform: translateY(-10px) scale(1.02); }
    }
    
    /* Header Styles */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(255, 20, 147, 0.1));
        border-radius: 20px;
        border: 1px solid rgba(0, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .main-title {
        font-family: 'Orbitron', monospace;
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(45deg, #00FFFF, #FF1493, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
        margin-bottom: 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { filter: brightness(1) drop-shadow(0 0 10px rgba(0, 255, 255, 0.5)); }
        to { filter: brightness(1.2) drop-shadow(0 0 20px rgba(0, 255, 255, 0.8)); }
    }
    
    .main-subtitle {
        font-family: 'Roboto', sans-serif;
        font-size: 1.2rem;
        color: #b0b0b0;
        font-weight: 300;
    }
    
    /* Year Selector Styles */
    .year-selector {
        background: rgba(26, 26, 46, 0.8);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .year-selector .stSelectbox > div > div {
        background-color: rgba(26, 26, 46, 0.9);
        border: 2px solid rgba(0, 255, 255, 0.5);
        border-radius: 10px;
        color: white;
    }
    
    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(22, 33, 62, 0.8));
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.5rem;
        border: 1px solid rgba(0, 255, 255, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #00FFFF, #FF1493, #FFD700);
        animation: shimmer 2s linear infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 255, 255, 0.2);
        border-color: rgba(0, 255, 255, 0.6);
    }
    
    .kpi-title {
        font-family: 'Roboto', sans-serif;
        font-size: 0.9rem;
        color: #b0b0b0;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-family: 'Fira Code', monospace;
        font-size: 2rem;
        font-weight: 700;
        color: #00FFFF;
        margin-bottom: 0.25rem;
    }
    
    .kpi-value.success { color: #00FF7F; }
    .kpi-value.danger { color: #FF4500; }
    .kpi-value.warning { color: #FFD700; }
    .kpi-value.secondary { color: #FF1493; }
    
    .kpi-trend {
        font-family: 'Roboto', sans-serif;
        font-size: 0.8rem;
        color: #b0b0b0;
    }
    
    /* Tab Styles */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(26, 26, 46, 0.8);
        border-radius: 15px;
        padding: 0.5rem;
        gap: 0.5rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 255, 255, 0.3);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 10px;
        color: #b0b0b0;
        padding: 0.75rem 1.5rem;
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        border: 1px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(0, 255, 255, 0.1);
        color: #00FFFF;
        border-color: rgba(0, 255, 255, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(255, 20, 147, 0.2));
        color: #ffffff !important;
        border-color: #00FFFF !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(26, 26, 46, 0.6);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    
    /* Chat Interface */
    .chat-container {
        background: rgba(26, 26, 46, 0.8);
        border-radius: 15px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid rgba(0, 255, 255, 0.3);
        backdrop-filter: blur(10px);
        max-height: 500px;
        overflow-y: auto;
    }
    
    .chat-message {
        margin: 1rem 0;
        padding: 1rem;
        border-radius: 10px;
        animation: fadeInUp 0.3s ease;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 255, 255, 0.05));
        border-left: 3px solid #00FFFF;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: linear-gradient(135deg, rgba(255, 20, 147, 0.1), rgba(255, 20, 147, 0.05));
        border-left: 3px solid #FF1493;
        margin-right: 2rem;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background: rgba(26, 26, 46, 0.8);
        border: 2px solid rgba(0, 255, 255, 0.3);
        border-radius: 10px;
        color: white;
        font-family: 'Roboto', sans-serif;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #00FFFF;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #00FFFF, #FF1493);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-family: 'Roboto', sans-serif;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(0, 255, 255, 0.4);
        filter: brightness(1.1);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(26, 26, 46, 0.9), rgba(22, 33, 62, 0.9));
        backdrop-filter: blur(10px);
    }
    
    /* Metrics */
    .metric-container {
        background: rgba(26, 26, 46, 0.6);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(0, 255, 255, 0.2);
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(0, 255, 255, 0.3);
        border-radius: 50%;
        border-top-color: #00FFFF;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 26, 46, 0.5);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00FFFF, #FF1493);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FF1493, #FFD700);
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .kpi-value {
            font-size: 1.5rem;
        }
        
        .kpi-card {
            margin: 0.25rem;
            padding: 1rem;
        }
    }
    
    /* Special Effects */
    .glow-effect {
        animation: pulseGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes pulseGlow {
        from {
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
        }
        to {
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.6);
        }
    }
    
    /* Data Table Styles */
    .dataframe {
        background: rgba(26, 26, 46, 0.8) !important;
        border-radius: 10px;
        border: 1px solid rgba(0, 255, 255, 0.3);
    }
    
    .dataframe th {
        background: rgba(0, 255, 255, 0.2) !important;
        color: white !important;
        font-family: 'Roboto', sans-serif;
        font-weight: 600;
    }
    
    .dataframe td {
        color: white !important;
        font-family: 'Fira Code', monospace;
    }
    
    /* Success/Error Messages */
    .stAlert {
        background: rgba(26, 26, 46, 0.8);
        border-radius: 10px;
        border-left: 4px solid #00FFFF;
        backdrop-filter: blur(10px);
    }
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)

def create_kpi_card(title: str, value: any, trend: str = "", format_type: str = "number", color_class: str = "primary"):
    """Create a styled KPI card"""
    
    # Format the value based on type
    if format_type == "crores":
        formatted_value = f"₹{value:,.0f}"
        unit = "Cr"
    elif format_type == "percentage":
        formatted_value = f"{value:.1f}"
        unit = "%"
    elif format_type == "number":
        formatted_value = f"{value:,.0f}"
        unit = ""
    else:
        formatted_value = str(value)
        unit = ""
    
    # Trend arrow
    trend_arrow = ""
    if trend.lower() in ["improving", "up", "increasing"]:
        trend_arrow = "↗️"
    elif trend.lower() in ["deteriorating", "down", "decreasing"]:
        trend_arrow = "↘️"
    elif trend.lower() in ["stable", "unchanged"]:
        trend_arrow = "→"
    
    card_html = f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value {color_class}">
            {formatted_value}<span style="font-size: 0.7em; color: #b0b0b0;">{unit}</span>
        </div>
        <div class="kpi-trend">{trend_arrow} {trend}</div>
    </div>
    """
    
    return card_html

def create_section_header(title: str, subtitle: str = ""):
    """Create a styled section header"""
    header_html = f"""
    <div style="margin: 2rem 0 1rem 0; text-align: center;">
        <h2 style="
            font-family: 'Orbitron', monospace;
            font-size: 2rem;
            font-weight: 700;
            color: #00FFFF;
            margin-bottom: 0.5rem;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
        ">{title}</h2>
        {f'<p style="color: #b0b0b0; font-size: 1rem; margin: 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """
    return header_html

def create_loading_indicator(text: str = "Loading..."):
    """Create a loading indicator"""
    loading_html = f"""
    <div style="text-align: center; padding: 2rem;">
        <div class="loading-spinner"></div>
        <p style="color: #b0b0b0; margin-top: 1rem; font-family: 'Roboto', sans-serif;">{text}</p>
    </div>
    """
    return loading_html

def format_currency(amount: float, format_type: str = "crores") -> str:
    """Format currency amounts consistently"""
    if format_type == "crores":
        return f"₹{amount:,.0f} Cr"
    elif format_type == "lakhs":
        return f"₹{amount/100:,.0f} L"
    else:
        return f"₹{amount:,.0f}"

def create_metric_comparison(current: float, previous: float, title: str, format_type: str = "crores"):
    """Create a metric with comparison"""
    change = current - previous
    change_pct = (change / previous * 100) if previous != 0 else 0
    
    color = "success" if change >= 0 else "danger"
    arrow = "↗️" if change >= 0 else "↘️"
    
    return {
        "title": title,
        "current": format_currency(current, format_type),
        "change": f"{arrow} {change_pct:+.1f}%",
        "color": color
    }
