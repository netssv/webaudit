"""
Web Audit Tool - Streamlit Application
Modular, comprehensive website analysis tool
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import sys
import os
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our web auditor
from web_auditor import WebAuditor

# Page configuration
st.set_page_config(
    page_title="Web Audit Tool",
    page_icon="�",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for consistent dark Web 4.0 interface
st.markdown("""
<style>
    /* Base styles - consistent dark theme */
    .stApp {
        background-color: #ffffff;
        color: #1a1a1a;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* All text elements - dark gray on white */
    .stMarkdown, .stText, .stCaption, .stSubheader, .stHeader {
        color: #1a1a1a;
    }
    
    /* Input styling - dark theme */
    .stSelectbox label, .stTextInput label, .stRadio label, .stCheckbox label {
        color: #1a1a1a;
        font-weight: 400;
    }
    
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background-color: transparent;
        color: #1a1a1a;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0;
        position: relative;
    }
    
    .search-container {
        max-width: 600px;
        margin: 2rem auto;
        text-align: center;
    }
    
    /* Buttons - consistent with header dark theme */
    .stButton > button {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        color: #ffffff !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 4px rgba(26, 26, 26, 0.1) !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%) !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(26, 26, 26, 0.15) !important;
    }
    
    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        color: #ffffff !important;
        border: 2px solid #2d2d2d !important;
        font-weight: 600 !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%) !important;
        border: 2px solid #404040 !important;
        color: #ffffff !important;
    }
    
    /* Progress bar - matching dark theme */
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
    }
    
    .stProgress > div > div > div {
        background-color: #f5f5f5;
    }
    
    /* Metric cards - dark theme */
    .metric-card {
        background: #ffffff;
        padding: 1rem;
        border: 1px solid #e5e5e5;
        margin: 0.5rem 0;
        color: #1a1a1a;
        box-shadow: 0 2px 4px rgba(26, 26, 26, 0.05);
    }
    
    /* Status indicators - dark theme */
    .status-good { border-left: 3px solid #2d2d2d; }
    .status-warning { border-left: 3px solid #666666; }
    .status-error { border-left: 3px solid #1a1a1a; }
    
    .example-domains {
        text-align: center;
        margin: 1rem 0;
        font-size: 0.9rem;
        color: #666666;
    }
    
    .example-domains a {
        color: #1a1a1a;
        text-decoration: underline;
        margin: 0 10px;
    }
    
    .example-domains a:hover {
        color: #2d2d2d;
    }
    
    /* Sidebar - dark theme */
    .stSidebar {
        background-color: #ffffff;
        color: #1a1a1a;
        border-right: 1px solid #e5e5e5;
    }
    
    /* Download button styling */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%) !important;
        color: #ffffff !important;
        border: 1px solid #2d2d2d !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%) !important;
        color: #ffffff !important;
        border: 1px solid #404040 !important;
    }
    
    /* Spinner/Loading - dark theme */
    .stSpinner > div {
        border-top-color: #2d2d2d !important;
    }
    
    /* Input fields - dark theme with proper contrast */
    .stTextInput > div > div > input {
        border: 1px solid #e5e5e5 !important;
        border-radius: 4px !important;
        color: #1a1a1a !important;
        background-color: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2d2d2d !important;
        box-shadow: 0 0 0 2px rgba(45, 45, 45, 0.1) !important;
        color: #1a1a1a !important;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        color: #1a1a1a !important;
        background-color: #ffffff !important;
        border: 1px solid #e5e5e5 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #2d2d2d !important;
        color: #1a1a1a !important;
    }
    
    /* Error and warning messages */
    .stAlert {
        border-radius: 4px !important;
    }
    
    .stAlert > div {
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }
    
    /* Metric containers and labels */
    .metric-container {
        color: #1a1a1a !important;
    }
    
    .metric-container [data-testid="metric-container"] {
        color: #1a1a1a !important;
    }
    
    .metric-container [data-testid="metric-container"] > div {
        color: #1a1a1a !important;
    }
    
    /* All metric labels and values */
    [data-testid="metric-container"] label {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-delta"] {
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }
    
    /* Success/Info/Warning/Error text */
    .stSuccess, .stInfo, .stWarning, .stError {
        color: #1a1a1a !important;
        font-weight: 500 !important;
    }
    
    /* DataFrame and table styling */
    .dataframe {
        color: #1a1a1a !important;
    }
    
    .dataframe th {
        background-color: #f8f9fa !important;
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    .dataframe td {
        color: #1a1a1a !important;
    }
    
    /* Chart containers */
    .stPlotlyChart {
        color: #1a1a1a !important;
    }
    
    /* Expander headers */
    .streamlit-expanderHeader {
        color: #1a1a1a !important;
        font-weight: 600 !important;
    }
    
    /* Code blocks */
    .stCode {
        background-color: #f8f9fa !important;
        color: #1a1a1a !important;
        border: 1px solid #e5e5e5 !important;
    }
    
    /* Checkbox styling - dark theme */
    .stCheckbox > label > div:first-child {
        border: 1px solid #e5e5e5;
    }
    
    .stCheckbox > label > div:first-child[aria-checked="true"] {
        background-color: #2d2d2d;
        border-color: #2d2d2d;
    }
    
    /* Tabs styling - dark theme with proper contrast */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 20px;
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 1px solid #e5e5e5;
        border-radius: 4px;
        color: #1a1a1a !important;
        font-weight: 500 !important;
        font-size: 14px !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: #ffffff !important;
        border-color: #2d2d2d;
        font-weight: 600 !important;
    }
    
    /* Tab content text contrast */
    .stTabs [data-baseweb="tab-panel"] {
        color: #1a1a1a;
    }
    
    /* Sidebar text contrast */
    .stSidebar .stCheckbox label {
        color: #1a1a1a !important;
    }
    
    .stSidebar .stSubheader {
        color: #1a1a1a !important;
    }
    
    .stSidebar .stMarkdown {
        color: #1a1a1a !important;
    }
    
    /* Popover styling - dark theme */
    .stPopover > div > div {
        border: 1px solid #e5e5e5;
        box-shadow: 0 4px 12px rgba(26, 26, 26, 0.1);
    }
    
    /* Global text contrast - catch all */
    p, h1, h2, h3, h4, h5, h6, span, label, div {
        color: #1a1a1a !important;
    }
    
    /* Specific overrides for dark background elements */
    .stButton > button, 
    .stDownloadButton > button,
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    .sidebar-header,
    header[data-testid="stHeader"] {
        color: #ffffff !important;
    }
    
    /* Header section - force white text on dark background */
    .header-container,
    .header-container *,
    .header-container h1,
    .header-container p {
        color: #ffffff !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
    }
    
    /* Ensure proper inheritance for nested elements */
    .stTabs [data-baseweb="tab"][aria-selected="true"] * {
        color: #ffffff !important;
    }
    
    .stButton > button *, 
    .stDownloadButton > button * {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'audit_results' not in st.session_state:
        st.session_state.audit_results = None
    if 'auditor' not in st.session_state:
        st.session_state.auditor = WebAuditor()
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False
    
    # API Integration settings (for future use)
    if 'api_settings' not in st.session_state:
        st.session_state.api_settings = {
            'google_pagespeed': {'enabled': False, 'api_key': ''},
            'hubspot': {'enabled': False, 'token': ''},
            'openai_gpt': {'enabled': False, 'api_key': ''},
            'semrush': {'enabled': False, 'api_key': ''},
            'ahrefs': {'enabled': False, 'api_key': ''}
        }
    
    # ChatGPT prompt management
    if 'show_chatgpt_prompt' not in st.session_state:
        st.session_state.show_chatgpt_prompt = False
    if 'chatgpt_prompt' not in st.session_state:
        st.session_state.chatgpt_prompt = ""
    
def display_header():
    """Display the main header with Web 4.0 minimal design"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: #ffffff;
        padding: 4rem 2rem;
        margin: -1rem -1rem 3rem -1rem;
        text-align: center;
        border-radius: 0;
        position: relative;
    ">
        <div class="header-container" style="
            max-width: 800px;
            margin: 0 auto;
            position: relative;
        ">
            <h1 style="
                font-size: 3.5rem;
                font-weight: 300;
                letter-spacing: -2px;
                margin: 0 0 1rem 0;
                color: #ffffff !important;
                line-height: 1.1;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            ">Web Audit Tool</h1>
            <p style="
                font-size: 1.25rem;
                font-weight: 300;
                color: #ffffff !important;
                margin: 0;
                opacity: 0.9;
                line-height: 1.4;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            ">Comprehensive website analysis for SEO, performance, and security</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_search_interface():
    """Display the search interface"""
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # URL input with proper label
    url_input = st.text_input(
        label="Website URL",
        placeholder="Enter website URL (e.g., example.com)",
        label_visibility="hidden",
        key="url_input"
    )
    
    # Example domains
    st.markdown("""
    <div class="example-domains">
        Try these examples: 
        <a href="#" onclick="document.querySelector('[data-testid=\"stTextInput\"] input').value='github.com'">github.com</a>
        <a href="#" onclick="document.querySelector('[data-testid=\"stTextInput\"] input').value='stackoverflow.com'">stackoverflow.com</a>
        <a href="#" onclick="document.querySelector('[data-testid=\"stTextInput\"] input').value='google.com'">google.com</a>
    </div>
    """, unsafe_allow_html=True)
    
    # Audit button
    audit_button = st.button(
        "Start Audit",
        key="audit_button",
        use_container_width=True,
        type="primary"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return url_input, st.session_state.selected_modules, audit_button

def display_loading_progress():
    """Display loading progress for audit"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        "Validating URL...",
        "Analyzing DNS...",
        "Checking SSL/TLS...",
        "Testing Performance...",
        "Analyzing SEO...",
        "Detecting Marketing Tools...",
        "Gathering Ranking Data...",
        "Generating Report..."
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(steps))
        time.sleep(0.5)
    
    progress_bar.empty()
    status_text.empty()

def display_audit_results(results):
    """Display comprehensive audit results"""
    if 'error' in results:
        st.error(f"{results['error']}")
        return
    
    # Results header
    st.success(f"Audit completed for **{results['domain']}**")
    
    # Export buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Download JSON Report"):
            filename = st.session_state.auditor.export_to_json(results)
            if filename:
                with open(filename, 'r') as f:
                    st.download_button(
                        label="📄 Download JSON",
                        data=f.read(),
                        file_name=filename,
                        mime="application/json"
                    )
            else:
                st.error("Failed to generate JSON report")
    
    with col2:
        if st.button("📋 Generate Summary"):
            summary = st.session_state.auditor.generate_summary_report(results)
            st.text_area(
                label="Summary Report",
                value=summary, 
                height=200,
                label_visibility="visible"
            )
    
    # Create tabs based on selected modules
    selected_modules = st.session_state.get('selected_modules', {
        'dns': True, 'ssl': True, 'seo_marketing': True, 
        'performance': True, 'ranking': True
    })
    
    # Build tab list and display functions based on selected modules
    tab_list = []
    tab_functions = []
    
    if selected_modules.get('performance', False):
        tab_list.append("Performance")
        tab_functions.append(('performance', display_performance_analysis))
    
    if selected_modules.get('seo_marketing', False):
        tab_list.append("SEO & Marketing")
        tab_functions.append(('seo_marketing', display_seo_marketing_analysis))
    
    if selected_modules.get('ssl', False):
        tab_list.append("Security")
        tab_functions.append(('ssl', display_security_analysis))
    
    if selected_modules.get('dns', False):
        tab_list.append("DNS")
        tab_functions.append(('dns', display_dns_analysis))
    
    if selected_modules.get('ranking', False):
        tab_list.append("Ranking")
        tab_functions.append(('ranking', display_ranking_analysis))
    
    # Always add metrics, AI analysis, and raw data if we have any modules selected
    if tab_list:
        tab_list.extend(["Metrics", "AI Analysis", "Raw Data"])
        tab_functions.extend([
            ('metrics', lambda data: display_metrics_dashboard(data)),
            ('ai_analysis', lambda data: display_ai_analysis(results)),
            ('raw', lambda data: display_raw_data_only(results))
        ])
    
    # Create tabs only if we have modules selected
    if not tab_list:
        st.warning("Please select at least one module to display results.")
        return
    
    tabs = st.tabs(tab_list)
    audit_data = results.get('results', {})
    
    # Display each tab with its corresponding function
    for i, (data_key, display_func) in enumerate(tab_functions):
        with tabs[i]:
            if data_key in ['metrics', 'raw', 'ai_analysis']:
                display_func(audit_data)
            else:
                display_func(audit_data.get(data_key, {}))

def display_performance_analysis(performance_data):
    """Display performance analysis"""
    if not performance_data or 'error' in performance_data:
        st.warning("! Performance data not available")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        response_time = performance_data.get('response_time', 0)
        color = "normal" if response_time < 1000 else "inverse"
        st.metric("Response Time", f"{response_time}ms", delta=None)
    
    with col2:
        status_code = performance_data.get('status_code', 0)
        st.metric("Status Code", status_code)
    
    with col3:
        page_size = performance_data.get('page_size', 0)
        size_kb = round(page_size / 1024, 1) if page_size else 0
        st.metric("Page Size", f"{size_kb} KB")
    
    with col4:
        redirects = performance_data.get('redirect_count', 0)
        st.metric("Redirects", redirects)
    
    # Server information
    if 'server_info' in performance_data:
        st.subheader("◇ Server Information")
        server_info = performance_data['server_info']
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Server:** {server_info.get('server', 'Unknown')}")
            st.write(f"**Powered By:** {server_info.get('powered_by', 'Unknown')}")
        with col2:
            st.write(f"**Content Type:** {server_info.get('content_type', 'Unknown')}")
            st.write(f"**Compression:** {performance_data.get('compression', 'none')}")

def display_seo_marketing_analysis(seo_data):
    """Display comprehensive SEO and marketing analysis"""
    if not seo_data or 'error' in seo_data:
        st.warning("! SEO data not available")
        return
    
    # Check if we have the new comprehensive analysis format
    if 'categories' in seo_data and 'overall_score' in seo_data:
        display_comprehensive_seo_analysis(seo_data)
    else:
        display_basic_seo_analysis(seo_data)

def display_comprehensive_seo_analysis(seo_data):
    """Display the new comprehensive SEO analysis"""
    
    # Overall Score and Issues Summary
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        overall_score = seo_data.get('overall_score', 0)
        st.metric("Overall SEO Score", f"{overall_score}%")
        
    with col2:
        issues = seo_data.get('issues', {})
        critical_count = issues.get('critical', 0)
        error_count = issues.get('errors', 0)
        total_issues = critical_count + error_count
        st.metric("Critical Issues", total_issues, delta=f"{critical_count} critical")
        
    with col3:
        warnings = issues.get('warnings', 0)
        st.metric("Warnings", warnings, delta="⚠️" if warnings > 0 else "✅")
        
    with col4:
        # Page info
        page_info = seo_data.get('page_info', {})
        lang = page_info.get('language', 'Unknown')
        st.metric("Language", lang.upper() if lang != 'unknown' else 'Not Set')
    
    # Category Scores
    st.subheader("📊 SEO Categories Breakdown")
    categories = seo_data.get('categories', {})
    
    category_names = {
        'meta_data': 'Meta Data',
        'page_quality': 'Page Quality', 
        'page_structure': 'Page Structure',
        'links': 'Links',
        'server': 'Server Config',
        'external_factors': 'External Factors'
    }
    
    # Display category scores in a grid
    cols = st.columns(3)
    for i, (key, category) in enumerate(categories.items()):
        with cols[i % 3]:
            score = category.get('score', 0)
            name = category_names.get(key, key.replace('_', ' ').title())
            
            # Color coding
            if score >= 80:
                color = "🟢"
            elif score >= 60:
                color = "🟡"
            else:
                color = "🔴"
            
            st.metric(f"{color} {name}", f"{score}%")
            
            # Progress bar
            st.progress(score / 100)
    
    # To-Do List
    todo_list = seo_data.get('todo_list', [])
    if todo_list:
        st.subheader("📋 Priority To-Do List")
        
        # Group by importance
        errors = [item for item in todo_list if item.get('importance') == 'error']
        warnings = [item for item in todo_list if item.get('importance') == 'warning']
        
        if errors:
            st.error("🔴 **Critical Issues** (Fix Immediately)")
            for i, item in enumerate(errors[:5], 1):  # Show top 5
                st.write(f"{i}. {item.get('action', 'Unknown action')}")
                
        if warnings:
            st.warning("🟡 **Warnings** (Recommended Improvements)")
            for i, item in enumerate(warnings[:5], 1):  # Show top 5
                st.write(f"{i}. {item.get('action', 'Unknown action')}")
    
    # Detailed Category Analysis
    st.subheader("🔍 Detailed Analysis")
    
    # Create tabs for each category
    tab_names = [category_names.get(key, key.replace('_', ' ').title()) for key in categories.keys()]
    tab_names = [name for name in tab_names if name is not None]  # Filter out None values
    if tab_names:
        tabs = st.tabs(tab_names)
        
        for i, (key, category) in enumerate(categories.items()):
            if i < len(tabs):  # Ensure we don't exceed tab count
                with tabs[i]:
                    display_category_details(key, category, category_names.get(key, key.replace('_', ' ').title()))
    
    # Page Information Summary
    st.subheader("📄 Page Information")
    page_info = seo_data.get('page_info', {})
    
    info_cols = st.columns(4)
    with info_cols[0]:
        st.write(f"**Language:** {page_info.get('language', 'Unknown')}")
        st.write(f"**Charset:** {page_info.get('charset', 'Unknown')}")
        
    with info_cols[1]:
        st.write(f"**Word Count:** {seo_data.get('word_count', 'Unknown')}")
        st.write(f"**File Size:** {seo_data.get('file_size', 'Unknown')} bytes" if seo_data.get('file_size') else "**File Size:** Unknown")
        
    with info_cols[2]:
        viewport = page_info.get('viewport')
        st.write(f"**Viewport:** {'✅ Mobile Ready' if viewport else '❌ Not Set'}")
        favicon = page_info.get('favicon')
        st.write(f"**Favicon:** {'✅ Present' if favicon else '❌ Missing'}")
        
    with info_cols[3]:
        st.write(f"**Status Code:** {seo_data.get('status_code', 'Unknown')}")
        response_time = seo_data.get('response_time')
        if response_time:
            rt_seconds = response_time.total_seconds() if hasattr(response_time, 'total_seconds') else response_time
            st.write(f"**Response Time:** {rt_seconds:.2f}s")
        else:
            st.write("**Response Time:** Unknown")

    # Social Media Links
    social_links = seo_data.get('social_media_links', {})
    if social_links:
        st.subheader("📱 Social Media Presence")
        social_cols = st.columns(min(len(social_links), 4))
        for i, (platform, link) in enumerate(social_links.items()):
            with social_cols[i % 4]:
                # Get platform icon
                platform_icons = {
                    'Facebook': '📘', 'X (Twitter)': '❌', 'LinkedIn': '💼', 
                    'Instagram': '📷', 'YouTube': '🎥', 'TikTok': '🎵',
                    'Pinterest': '📌', 'Snapchat': '👻', 'WhatsApp': '💬',
                    'Telegram': '✈️', 'Discord': '🎮', 'Reddit': '🤖',
                    'Tumblr': '🎨', 'Twitch': '🎯', 'Vimeo': '🎬',
                    'GitHub': '👨‍💻', 'GitLab': '🦊', 'Behance': '🎨',
                    'Dribbble': '🏀', 'Medium': '📝', 'Mastodon': '🐘',
                    'Threads': '🧵', 'Gmail': '📧', 'Email': '✉️'
                }
                icon = platform_icons.get(platform, '🔗')
                st.write(f"{icon} **{platform}**")
                
                # For email, display email address
                if platform in ['Gmail', 'Email']:
                    st.write(f"📧 {link}")
                else:
                    st.write(f"[Visit Profile]({link})")
    
    # Marketing Tools
    marketing_tools = seo_data.get('marketing_tools', [])
    if marketing_tools:
        st.subheader("🎯 Marketing Tools Detected")
        marketing_cols = st.columns(min(len(marketing_tools), 4))
        for i, tool in enumerate(marketing_tools):
            with marketing_cols[i % 4]:
                st.success(f"✅ {tool}")

def display_category_details(category_key, category_data, category_name):
    """Display detailed information for a specific SEO category"""
    checks = category_data.get('checks', [])
    score = category_data.get('score', 0)
    
    # Category score
    st.metric(f"{category_name} Score", f"{score}/100")
    
    if not checks:
        st.info("No detailed checks available for this category.")
        return
    
    # Group checks by status
    passed_checks = [check for check in checks if check.get('status') == 'pass']
    warning_checks = [check for check in checks if check.get('status') == 'warning']
    error_checks = [check for check in checks if check.get('status') == 'error']
    
    # Display errors first (most important)
    if error_checks:
        st.error("🔴 **Issues Found**")
        for check in error_checks:
            with st.expander(f"❌ {check.get('name', 'Unknown Check')}", expanded=True):
                st.write(f"**Importance:** {check.get('importance', 'Unknown').replace('_', ' ').title()}")
                st.write(f"**Issue:** {check.get('message', 'No message')}")
                if check.get('details'):
                    st.write(f"**Details:** {check.get('details')}")
    
    # Display warnings
    if warning_checks:
        st.warning("🟡 **Recommendations**")
        for check in warning_checks:
            with st.expander(f"⚠️ {check.get('name', 'Unknown Check')}"):
                st.write(f"**Importance:** {check.get('importance', 'Unknown').replace('_', ' ').title()}")
                st.write(f"**Recommendation:** {check.get('message', 'No message')}")
                if check.get('details'):
                    st.write(f"**Details:** {check.get('details')}")
    
    # Display passed checks
    if passed_checks:
        st.success("✅ **Passed Checks**")
        for check in passed_checks:
            with st.expander(f"✅ {check.get('name', 'Unknown Check')}"):
                st.write(f"**Status:** {check.get('message', 'No message')}")
                if check.get('details'):
                    st.write(f"**Details:** {check.get('details')}")

def display_basic_seo_analysis(seo_data):
    """Display basic SEO analysis (fallback for old format)"""
    # SEO Score
    seo_score = seo_data.get('seo_score', 0)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.metric("SEO Score", f"{seo_score}/100")
        
        # Progress bar for SEO score
        progress_color = "🟢" if seo_score >= 80 else "🟡" if seo_score >= 60 else "🔴"
        st.progress(seo_score / 100)
        st.write(f"{progress_color} Score: {seo_score}/100")
    
    # Basic SEO Elements
    st.subheader("◇ Basic SEO Elements")
    col1, col2 = st.columns(2)
    
    with col1:
        title = seo_data.get('title')
        if title:
            st.write(f"**Title:** {title}")
            st.write(f"**Length:** {len(title)} characters")
        else:
            st.warning("! No title tag found")
    
    with col2:
        description = seo_data.get('meta_description')
        if description:
            st.write(f"**Meta Description:** {description[:100]}...")
            st.write(f"**Length:** {len(description)} characters")
        else:
            st.warning("! No meta description found")
    
    # Marketing Tools
    marketing_tools = seo_data.get('marketing_tools', [])
    if marketing_tools:
        st.subheader("🎯 Marketing Tools Detected")
        cols = st.columns(min(len(marketing_tools), 4))
        for i, tool in enumerate(marketing_tools):
            with cols[i % 4]:
                st.info(f"✅ {tool}")
    
    # Social Media Links
    social_links = seo_data.get('social_media_links', {})
    if social_links:
        st.subheader("📱 Social Media Presence")
        social_cols = st.columns(min(len(social_links), 4))
        for i, (platform, link) in enumerate(social_links.items()):
            with social_cols[i % 4]:
                # Get platform icon
                platform_icons = {
                    'Facebook': '📘', 'X (Twitter)': '❌', 'LinkedIn': '💼', 
                    'Instagram': '📷', 'YouTube': '🎥', 'TikTok': '🎵',
                    'Pinterest': '📌', 'Snapchat': '👻', 'WhatsApp': '💬',
                    'Telegram': '✈️', 'Discord': '🎮', 'Reddit': '🤖',
                    'Tumblr': '🎨', 'Twitch': '🎯', 'Vimeo': '🎬',
                    'GitHub': '👨‍💻', 'GitLab': '🦊', 'Behance': '🎨',
                    'Dribbble': '🏀', 'Medium': '📝', 'Mastodon': '🐘',
                    'Threads': '🧵', 'Gmail': '📧', 'Email': '✉️'
                }
                icon = platform_icons.get(platform, '🔗')
                st.write(f"{icon} **{platform}**")
                
                # For email, display email address
                if platform in ['Gmail', 'Email']:
                    st.write(f"📧 {link}")
                else:
                    st.write(f"[Visit Profile]({link})")

def display_security_analysis(ssl_data):
    """Display security analysis"""
    if not ssl_data:
        st.warning("! SSL data not available")
        return
    
    has_ssl = ssl_data.get('has_ssl', False)
    
    if has_ssl:
        st.success("✓ SSL/TLS Enabled")
        
        col1, col2 = st.columns(2)
        with col1:
            protocol = ssl_data.get('protocol_version')
            if protocol:
                st.write(f"**Protocol:** {protocol}")
            
            expiry_days = ssl_data.get('days_until_expiry')
            if expiry_days is not None:
                if expiry_days > 30:
                    st.success(f"**Certificate Valid:** {expiry_days} days remaining")
                elif expiry_days > 0:
                    st.warning(f"**Certificate Expires Soon:** {expiry_days} days")
                else:
                    st.error("**Certificate Expired**")
        
        with col2:
            issuer = ssl_data.get('issuer')
            if issuer:
                st.write(f"**Issuer:** {issuer.get('organizationName', 'Unknown')}")
            
            subject = ssl_data.get('subject')
            if subject:
                st.write(f"**Subject:** {subject.get('commonName', 'Unknown')}")
    else:
        st.error("X No SSL/TLS detected")

def display_dns_analysis(dns_data):
    """Display DNS analysis"""
    if not dns_data or 'error' in dns_data:
        st.warning("! DNS data not available")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 IP Information")
        ip_address = dns_data.get('ip_address')
        if ip_address:
            st.write(f"**IP Address:** {ip_address}")
        
        response_time = dns_data.get('dns_response_time')
        if response_time:
            st.write(f"**DNS Response Time:** {response_time:.2f}ms")
    
    with col2:
        st.subheader("🌐 DNS Records")
        a_records = dns_data.get('a_records', [])
        if a_records:
            st.write("**A Records:**")
            for record in a_records[:3]:
                st.write(f"  • {record}")

def display_ranking_analysis(ranking_data):
    """Display ranking analysis"""
    if not ranking_data or 'error' in ranking_data:
        st.warning("! Ranking data not available")
        return
    
    # Authority Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        da = ranking_data.get('domain_authority', 0)
        st.metric("Domain Authority", da)
    
    with col2:
        pa = ranking_data.get('page_authority', 0)
        st.metric("Page Authority", pa)
    
    with col3:
        tf = ranking_data.get('trust_flow', 0)
        st.metric("Trust Flow", tf)
    
    with col4:
        visibility = ranking_data.get('seo_visibility', 0)
        st.metric("SEO Visibility", f"{visibility}%")
    
    # Traffic and Backlinks
    st.subheader("📊 Traffic & Backlinks")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        traffic = ranking_data.get('organic_traffic_estimate', 0)
        st.metric("Organic Traffic Est.", f"{traffic:,}")
    
    with col2:
        backlinks = ranking_data.get('backlink_estimate', 0)
        st.metric("Backlinks Est.", f"{backlinks:,}")
    
    with col3:
        domains = ranking_data.get('referring_domains', 0)
        st.metric("Referring Domains", f"{domains:,}")

def display_technical_analysis(audit_data):
    """Display technical analysis"""
    st.subheader("🔧 Technical Details")
    
    # Headers information
    perf_data = audit_data.get('performance', {})
    if 'cache_headers' in perf_data:
        st.write("**Cache Headers:**")
        cache_headers = perf_data['cache_headers']
        for header, value in cache_headers.items():
            if value:
                st.write(f"  • {header}: {value}")

def display_metrics_dashboard(audit_data):
    """Display metrics dashboard with charts"""
    st.subheader("📈 Metrics Dashboard")
    
    # Performance Chart
    perf_data = audit_data.get('performance', {})
    if perf_data:
        fig = go.Figure()
        
        response_time = perf_data.get('response_time', 0)
        page_size = perf_data.get('page_size', 0) / 1024  # Convert to KB
        
        fig.add_trace(go.Bar(
            name='Performance Metrics',
            x=['Response Time (ms)', 'Page Size (KB)'],
            y=[response_time, page_size]
        ))
        
        fig.update_layout(title="Performance Metrics")
        st.plotly_chart(fig, use_container_width=True)
    
    # SEO Score Chart
    seo_data = audit_data.get('seo_marketing', {})
    if seo_data and 'seo_score' in seo_data:
        score = seo_data['seo_score']
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = score,
            title = {'text': "SEO Score"},
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)

def json_serializer(obj):
    """JSON serializer for objects not serializable by default json code"""
    from datetime import datetime, date, timedelta
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, timedelta):
        return obj.total_seconds()  # Convert timedelta to seconds (float)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def display_raw_data(results):
    """Display raw data with better styling and ChatGPT analysis option"""
    st.subheader("Raw Audit Data")
    
    # Create a responsive layout for ChatGPT analysis
    st.markdown("### AI Analysis Assistant")
    
    # Generate the ChatGPT prompt
    domain = results.get('domain', 'Unknown')
    selected_modules = results.get('selected_modules', {})
    active_modules = [module.replace('_', ' ').title() for module, enabled in selected_modules.items() if enabled]
    
    prompt = f"""Please analyze this website audit data for {domain}:

**Analyzed Modules:** {', '.join(active_modules) if active_modules else 'None'}
**Audit Date:** {results.get('timestamp', 'N/A')}

**Raw Data:**
```json
{json.dumps(results, indent=2, default=json_serializer)}
```

Please provide:
1. **Summary** of the website's overall health
2. **Key Issues** that need immediate attention  
3. **Performance Insights** and optimization recommendations
4. **SEO Recommendations** for better search rankings
5. **Security Assessment** and any concerns
6. **Action Plan** with prioritized next steps

Focus on actionable insights and specific recommendations."""

    # Display raw JSON with better styling
    json_container = st.container()
    with json_container:
        if st.session_state.dark_mode:
            # Dark mode JSON styling
            st.markdown("""
            <style>
                .stJson {
                    background-color: #374151 !important;
                    color: #ffffff !important;
                    border: 1px solid #4b5563 !important;
                    border-radius: 0.5rem !important;
                    padding: 1rem !important;
                }
            </style>
            """, unsafe_allow_html=True)
        else:
            # Light mode JSON styling
            st.markdown("""
            <style>
                .stJson {
                    background-color: #f9fafb !important;
                    color: #1f2937 !important;
                    border: 1px solid #d1d5db !important;
                    border-radius: 0.5rem !important;
                    padding: 1rem !important;
                }
            </style>
            """, unsafe_allow_html=True)
        
        st.json(results)

def display_ai_analysis(results):
    """Display AI Analysis in its own dedicated tab"""
    st.markdown("### 🤖 AI Analysis Assistant")
    
    # Generate the ChatGPT prompt
    domain = results.get('domain', 'Unknown')
    selected_modules = results.get('selected_modules', {})
    active_modules = [module.replace('_', ' ').title() for module, enabled in selected_modules.items() if enabled]
    
    prompt = f"""Please analyze this website audit data for {domain}:

**Analyzed Modules:** {', '.join(active_modules) if active_modules else 'None'}
**Audit Date:** {results.get('timestamp', 'N/A')}

**Raw Data:**
```json
{json.dumps(results, indent=2, default=json_serializer)}
```

Please provide:
1. **Summary** of the website's overall health
2. **Key Issues** that need immediate attention  
3. **Performance Insights** and optimization recommendations
4. **SEO Recommendations** for better search rankings
5. **Security Assessment** and any concerns
6. **Action Plan** with prioritized next steps

Focus on actionable insights and specific recommendations."""

    # Store the prompt in session state
    st.session_state.chatgpt_prompt = prompt
    
    # Improved ChatGPT link functionality
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.info(f"🎯 **Ready to analyze: {domain}**\n\nClick the button to open ChatGPT with your audit data pre-loaded for AI analysis.")
    
    with col2:
        # URL-safe encoding for ChatGPT
        import urllib.parse
        encoded_prompt = urllib.parse.quote(prompt, safe='')
        chatgpt_url = f"https://chat.openai.com/?q={encoded_prompt}"
        
        # Truncate if URL is too long (browsers have limits around 8000 characters)
        if len(chatgpt_url) > 7000:
            # Create a shorter prompt for very long data
            short_prompt = f"""Please analyze this website audit for {domain}. Modules analyzed: {', '.join(active_modules) if active_modules else 'None'}. 

Key findings from audit:
- Domain: {domain}
- Analysis date: {results.get('timestamp', 'N/A')}
- Selected modules: {len(active_modules)} modules

Please provide actionable insights for website optimization, SEO improvements, and security recommendations."""
            
            encoded_prompt = urllib.parse.quote(short_prompt, safe='')
            chatgpt_url = f"https://chat.openai.com/?q={encoded_prompt}"
        
        st.markdown(f"""
        <a href="{chatgpt_url}" target="_blank" style="text-decoration: none;">
            <button style="
                background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
                color: #ffffff;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
                width: 100%;
                transition: all 0.3s ease;
                font-size: 14px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            ">
                🚀 Analyze with ChatGPT
            </button>
        </a>
        """, unsafe_allow_html=True)
    
    # Show/Hide prompt option
    with st.expander("📋 View Generated Prompt", expanded=False):
        st.markdown("**This prompt will be sent to ChatGPT:**")
        st.code(prompt, language="text")
        
        # Copy to clipboard button
        st.markdown("""
        <script>
        function copyToClipboard() {
            navigator.clipboard.writeText(`""" + prompt.replace('`', '\\`') + """`);
        }
        </script>
        <button onclick="copyToClipboard()" style="
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: #ffffff;
            border: none;
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 10px;
        ">📋 Copy Prompt</button>
        """, unsafe_allow_html=True)

def display_raw_data_only(results):
    """Display only the raw JSON data without AI analysis"""
    st.subheader("📊 Raw Audit Data")
    
    # Display raw JSON with better styling
    json_container = st.container()
    with json_container:
        if st.session_state.dark_mode:
            # Dark mode JSON styling
            st.markdown("""
            <style>
                .stJson {
                    background-color: #374151 !important;
                    color: #ffffff !important;
                    border: 1px solid #4b5563 !important;
                    border-radius: 0.5rem !important;
                    padding: 1rem !important;
                }
            </style>
            """, unsafe_allow_html=True)
        else:
            # Light mode JSON styling
            st.markdown("""
            <style>
                .stJson {
                    background-color: #f9fafb !important;
                    color: #1f2937 !important;
                    border: 1px solid #d1d5db !important;
                    border-radius: 0.5rem !important;
                    padding: 1rem !important;
                }
            </style>
            """, unsafe_allow_html=True)
        
        st.json(results)

def handle_example_domain(domain):
    """Handle example domain clicks"""
    st.session_state.url_input = domain
    st.rerun()

def main():
    """Main application"""
    initialize_session_state()
    
    # Apply comprehensive theme CSS
    if st.session_state.dark_mode:
        # DARK MODE - Complete styling
        st.markdown("""
        <style>
            /* Main app background and text */
            .stApp {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
            }
            
            /* Main content area */
            .main > div {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
            }
            
            /* Headers */
            .main-header {
                background: linear-gradient(90deg, #4a5568 0%, #2d3748 100%) !important;
                color: #ffffff !important;
            }
            
            /* Sidebar */
            .stSidebar {
                background-color: #2d3748 !important;
            }
            
            .stSidebar > div {
                background-color: #2d3748 !important;
            }
            
            /* All text elements */
            .stMarkdown, .stText, .stCaption, .stSubheader, .stHeader {
                color: #ffffff !important;
            }
            
            /* Selectboxes */
            .stSelectbox > div > div {
                background-color: #374151 !important;
                color: #ffffff !important;
                border: 1px solid #4b5563 !important;
            }
            
            .stSelectbox label {
                color: #ffffff !important;
            }
            
            /* Text inputs */
            .stTextInput > div > div > input {
                background-color: #374151 !important;
                color: #ffffff !important;
                border: 1px solid #4b5563 !important;
            }
            
            .stTextInput label {
                color: #ffffff !important;
            }
            
            /* Text areas */
            .stTextArea > div > div > textarea {
                background-color: #374151 !important;
                color: #ffffff !important;
                border: 1px solid #4b5563 !important;
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
                font-size: 13px !important;
            }
            
            .stTextArea label {
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            
            /* Buttons */
            .stButton > button {
                background-color: #374151 !important;
                color: #ffffff !important;
                border: 1px solid #4b5563 !important;
            }
            
            .stButton > button:hover {
                background-color: #4b5563 !important;
                color: #ffffff !important;
            }
            
            /* Radio buttons */
            .stRadio > div {
                color: #ffffff !important;
            }
            
            .stRadio label {
                color: #ffffff !important;
            }
            
            /* Checkboxes */
            .stCheckbox > div {
                color: #ffffff !important;
            }
            
            .stCheckbox label {
                color: #ffffff !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #374151 !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #374151 !important;
                color: #ffffff !important;
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #4b5563 !important;
                color: #ffffff !important;
            }
            
            /* Metrics */
            .stMetric {
                background-color: #374151 !important;
                color: #ffffff !important;
                padding: 1rem !important;
                border-radius: 0.5rem !important;
            }
            
            .stMetric label {
                color: #ffffff !important;
            }
            
            .stMetric .metric-value {
                color: #ffffff !important;
            }
            
            /* Success/Error/Warning messages */
            .stSuccess {
                background-color: #065f46 !important;
                color: #ffffff !important;
            }
            
            .stError {
                background-color: #7f1d1d !important;
                color: #ffffff !important;
            }
            
            .stWarning {
                background-color: #92400e !important;
                color: #ffffff !important;
            }
            
            .stInfo {
                background-color: #1e3a8a !important;
                color: #ffffff !important;
            }
            
            /* Metric cards */
            .metric-card {
                background: #374151 !important;
                color: #ffffff !important;
                border-left-color: #60a5fa !important;
            }
            
            /* Example domains */
            .example-domains {
                color: #d1d5db !important;
            }
            
            .example-domains a {
                color: #60a5fa !important;
            }
            
            /* Data display elements */
            .stDataFrame {
                background-color: #374151 !important;
                color: #ffffff !important;
            }
            
            /* JSON display */
            .stJson {
                background-color: #374151 !important;
                color: #ffffff !important;
                border: 1px solid #4b5563 !important;
                border-radius: 0.5rem !important;
                padding: 1rem !important;
            }
            
            /* Spinner */
            .stSpinner {
                color: #ffffff !important;
            }
            
            /* Sidebar toggle button - Dark mode */
            button[data-testid="collapsedControl"] {
                background-color: #374151 !important;
                color: #ffffff !important;
                border: 1px solid #4b5563 !important;
            }
            
            button[data-testid="collapsedControl"]:hover {
                background-color: #4b5563 !important;
                color: #ffffff !important;
            }
        </style>
        """, unsafe_allow_html=True)
    else:
        # LIGHT MODE - Complete styling 
        st.markdown("""
        <style>
            /* Main app background and text */
            .stApp {
                background-color: #ffffff !important;
                color: #1f2937 !important;
            }
            
            /* Main content area */
            .main > div {
                background-color: #ffffff !important;
                color: #1f2937 !important;
            }
            
            /* Headers */
            .main-header {
                background: linear-gradient(90deg, #667eea 0%, #764ba2 100%) !important;
                color: #ffffff !important;
            }
            
            /* Sidebar */
            .stSidebar {
                background-color: #f9fafb !important;
            }
            
            .stSidebar > div {
                background-color: #f9fafb !important;
            }
            
            /* All text elements */
            .stMarkdown, .stText, .stCaption, .stSubheader, .stHeader {
                color: #1f2937 !important;
            }
            
            /* Selectboxes */
            .stSelectbox > div > div {
                background-color: #ffffff !important;
                color: #1f2937 !important;
                border: 1px solid #d1d5db !important;
            }
            
            .stSelectbox label {
                color: #1f2937 !important;
            }
            
            /* Text inputs */
            .stTextInput > div > div > input {
                background-color: #ffffff !important;
                color: #1f2937 !important;
                border: 1px solid #d1d5db !important;
            }
            
            .stTextInput label {
                color: #1f2937 !important;
            }
            
            /* Text areas */
            .stTextArea > div > div > textarea {
                background-color: #f9fafb !important;
                color: #1f2937 !important;
                border: 1px solid #d1d5db !important;
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace !important;
                font-size: 13px !important;
            }
            
            .stTextArea label {
                color: #1f2937 !important;
                font-weight: 600 !important;
            }
            
            /* Buttons */
            .stButton > button {
                background-color: #3b82f6 !important;
                color: #ffffff !important;
                border: 1px solid #3b82f6 !important;
                font-weight: 500 !important;
            }
            
            .stButton > button:hover {
                background-color: #2563eb !important;
                color: #ffffff !important;
                border: 1px solid #2563eb !important;
            }
            
            /* Secondary buttons (if any) */
            .stButton[data-testid="stButton"] button[kind="secondary"] {
                background-color: #ffffff !important;
                color: #1f2937 !important;
                border: 1px solid #d1d5db !important;
            }
            
            .stButton[data-testid="stButton"] button[kind="secondary"]:hover {
                background-color: #f3f4f6 !important;
                color: #1f2937 !important;
            }
            
            /* Radio buttons */
            .stRadio > div {
                color: #1f2937 !important;
            }
            
            .stRadio label {
                color: #1f2937 !important;
            }
            
            /* Checkboxes */
            .stCheckbox > div {
                color: #1f2937 !important;
            }
            
            .stCheckbox label {
                color: #1f2937 !important;
            }
            
            /* Tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #f3f4f6 !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                background-color: #f3f4f6 !important;
                color: #1f2937 !important;
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #ffffff !important;
                color: #1f2937 !important;
            }
            
            /* Metrics */
            .stMetric {
                background-color: #ffffff !important;
                color: #1f2937 !important;
                padding: 1rem !important;
                border-radius: 0.5rem !important;
                border: 1px solid #e5e7eb !important;
            }
            
            .stMetric label {
                color: #1f2937 !important;
            }
            
            .stMetric .metric-value {
                color: #1f2937 !important;
            }
            
            /* Success/Error/Warning messages */
            .stSuccess {
                background-color: #dcfce7 !important;
                color: #166534 !important;
                border: 1px solid #bbf7d0 !important;
            }
            
            .stError {
                background-color: #fef2f2 !important;
                color: #991b1b !important;
                border: 1px solid #fecaca !important;
            }
            
            .stWarning {
                background-color: #fffbeb !important;
                color: #92400e !important;
                border: 1px solid #fed7aa !important;
            }
            
            .stInfo {
                background-color: #eff6ff !important;
                color: #1e40af !important;
                border: 1px solid #bfdbfe !important;
            }
            
            /* Metric cards */
            .metric-card {
                background: #ffffff !important;
                color: #1f2937 !important;
                border-left-color: #3b82f6 !important;
                box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1) !important;
            }
            
            /* Example domains */
            .example-domains {
                color: #6b7280 !important;
            }
            
            .example-domains a {
                color: #3b82f6 !important;
            }
            
            /* Data display elements */
            .stDataFrame {
                background-color: #ffffff !important;
                color: #1f2937 !important;
            }
            
            /* JSON display */
            .stJson {
                background-color: #f9fafb !important;
                color: #1f2937 !important;
                border: 1px solid #d1d5db !important;
                border-radius: 0.5rem !important;
                padding: 1rem !important;
            }
            
            /* Spinner */
            .stSpinner {
                color: #1f2937 !important;
            }
            
            /* Sidebar toggle button - Light mode */
            .stSidebar .css-1d391kg {
                background-color: #374151 !important;
                color: #ffffff !important;
            }
            
            button[data-testid="collapsedControl"] {
                background-color: #f3f4f6 !important;
                color: #1f2937 !important;
                border: 1px solid #d1d5db !important;
            }
            
            button[data-testid="collapsedControl"]:hover {
                background-color: #e5e7eb !important;
                color: #1f2937 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    display_header()
    
    # Initialize session state for modules if not exists
    if 'selected_modules' not in st.session_state:
        st.session_state.selected_modules = {
            'dns': True,
            'ssl': True,
            'seo_marketing': True,
            'performance': True,
            'ranking': True
        }
    
    # Search interface
    url_input, selected_modules, audit_button = display_search_interface()
    
    # Process audit request - trigger on button click or Enter key
    url_changed = url_input and url_input != st.session_state.get('previous_url', '')
    if (audit_button and url_input) or url_changed:
        # Store the current URL to track changes
        st.session_state.previous_url = url_input
        with st.spinner("Performing audit..."):
            display_loading_progress()
            results = st.session_state.auditor.comprehensive_audit(url_input, selected_modules)
            st.session_state.audit_results = results
    
    # Display results
    if st.session_state.audit_results:
        display_audit_results(st.session_state.audit_results)
    
    # Sidebar with additional options
    with st.sidebar:
        st.header("Settings")
        
        # Module Selection
        st.subheader("Analysis Modules")
        
        st.session_state.selected_modules['performance'] = st.checkbox(
            "Performance Analysis", 
            value=st.session_state.selected_modules['performance'],
            key="sidebar_module_performance"
        )
        
        st.session_state.selected_modules['seo_marketing'] = st.checkbox(
            "SEO & Marketing", 
            value=st.session_state.selected_modules['seo_marketing'],
            key="sidebar_module_seo"
        )
        
        st.session_state.selected_modules['ssl'] = st.checkbox(
            "Security (SSL/TLS)", 
            value=st.session_state.selected_modules['ssl'],
            key="sidebar_module_ssl"
        )
        
        st.session_state.selected_modules['dns'] = st.checkbox(
            "DNS Analysis", 
            value=st.session_state.selected_modules['dns'],
            key="sidebar_module_dns"
        )
        
        st.session_state.selected_modules['ranking'] = st.checkbox(
            "Ranking Analysis", 
            value=st.session_state.selected_modules['ranking'],
            key="sidebar_module_ranking"
        )
        
        # Small clear button
        if st.button("🗑️ Clear All", key="clear_modules", help="Uncheck all modules"):
            for key in st.session_state.selected_modules:
                st.session_state.selected_modules[key] = False
            st.rerun()
        
        st.divider()
        
        # Theme Settings
        st.subheader("Appearance")
        theme_option = st.radio(
            "Theme Mode",
            ["Light Mode", "Dark Mode"],
            index=1 if st.session_state.dark_mode else 0,
            key="theme_radio"
        )
        
        # Update theme if changed
        new_dark_mode = theme_option == "Dark Mode"
        if new_dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = new_dark_mode
            st.rerun()
        
        st.divider()
        
        # API Integrations (Future)
        st.subheader("API Integrations")
        st.write("*Coming Soon:*")
        
        # Google PageSpeed API
        google_api = st.checkbox("Google PageSpeed Insights", disabled=True)
        if google_api:
            st.text_input("API Key", placeholder="Enter Google API Key", disabled=True)
        
        # HubSpot API
        hubspot_api = st.checkbox("HubSpot Marketing Hub", disabled=True)
        if hubspot_api:
            st.text_input("HubSpot Token", placeholder="Enter HubSpot Token", disabled=True)
        
        # OpenAI GPT API
        gpt_api = st.checkbox("GPT Analysis & Insights", disabled=True)
        if gpt_api:
            st.text_input("OpenAI API Key", placeholder="Enter OpenAI API Key", disabled=True)
        
        # SEMrush API
        semrush_api = st.checkbox("SEMrush Data", disabled=True)
        if semrush_api:
            st.text_input("SEMrush API Key", placeholder="Enter SEMrush API Key", disabled=True)
        
        # Ahrefs API
        ahrefs_api = st.checkbox("Ahrefs Backlink Data", disabled=True)
        if ahrefs_api:
            st.text_input("Ahrefs API Key", placeholder="Enter Ahrefs API Key", disabled=True)
        
        st.caption("These integrations will provide enhanced data and AI-powered insights")
        
        st.divider()
        
        # About Section
        st.subheader("About")
        st.write("This tool performs comprehensive website audits including performance, SEO, security, and marketing analysis.")
        
        # Creator Information
        st.markdown("---")
        st.markdown("**Created by:**")
        st.markdown("**Rodrigo Martel**")
        st.markdown("[GitHub: @netssv](https://github.com/netssv)")
        
        # Version and Tech Stack
        st.markdown("---")
        st.markdown("**Built with:**")
        st.markdown("• Streamlit")
        st.markdown("• Python 3.12")
        st.markdown("• Plotly for visualizations")
        st.markdown("• Modular architecture")
        
        st.caption("Open source web audit tool for comprehensive website analysis")
        
        # Clear Results
        if st.button("Clear Results"):
            st.session_state.audit_results = None
            st.session_state.audit_results = None
            st.rerun()

if __name__ == "__main__":
    main()
