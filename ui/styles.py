"""
UI Styles Module
Contains all CSS styling for the Web Audit Tool
"""

import streamlit as st

def apply_light_mode_styles():
    """Apply light mode CSS styles"""
    st.markdown("""
    <style>
        /* Base styles - improved contrast */
        .stApp {
            background-color: #ffffff;
            color: #1a1a1a;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        }
        
        /* All text elements - high contrast dark text on white */
        .stMarkdown, .stText, .stCaption, .stSubheader, .stHeader {
            color: #1a1a1a !important;
        }
        
        /* Headers with better contrast */
        h1, h2, h3, h4, h5, h6 {
            color: #0d1117 !important;
            font-weight: 600 !important;
        }
        
        /* Input styling - better contrast */
        .stSelectbox label, .stTextInput label, .stRadio label, .stCheckbox label {
            color: #0d1117 !important;
            font-weight: 500 !important;
        }
        
        /* Input fields with better borders */
        .stTextInput > div > div > input {
            border: 2px solid #d0d7de !important;
            background-color: #ffffff !important;
            color: #1a1a1a !important;
        }
        
        /* Sidebar improvements */
        .css-1d391kg {
            background-color: #f6f8fa !important;
            border-right: 1px solid #d0d7de !important;
        }
        
        /* Button improvements */
        .stButton > button {
            background-color: #0969da !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 6px !important;
            font-weight: 500 !important;
            padding: 0.5rem 1rem !important;
        }
        
        .stButton > button:hover {
            background-color: #0860ca !important;
            color: #ffffff !important;
        }
        
        /* Alert boxes with better contrast */
        .stAlert {
            background-color: #f6f8fa !important;
            border: 1px solid #d0d7de !important;
            color: #1a1a1a !important;
        }
        
        .stSuccess {
            background-color: #dcfce7 !important;
            border: 1px solid #16a34a !important;
            color: #166534 !important;
        }
        
        .stError {
            background-color: #fef2f2 !important;
            border: 1px solid #dc2626 !important;
            color: #991b1b !important;
        }
        
        .stWarning {
            background-color: #fef3c7 !important;
            border: 1px solid #d97706 !important;
            color: #92400e !important;
        }
        
        .stInfo {
            background-color: #dbeafe !important;
            border: 1px solid #2563eb !important;
            color: #1d4ed8 !important;
        }
        
        /* Code block styling */
        .stCodeBlock {
            background-color: #f6f8fa !important;
            border: 1px solid #d0d7de !important;
            border-radius: 8px !important;
        }
        
        /* Metric styling */
        .metric-container {
            background-color: #ffffff !important;
            border: 1px solid #e1e4e8 !important;
            border-radius: 8px !important;
            padding: 16px !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        }
        
        /* Progress bar styling */
        .stProgress > div > div {
            background-color: #0969da !important;
        }
        
        /* Tabs styling */
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
        
        /* Checkbox styling - Enhanced contrast */
        .stSidebar .stCheckbox > label > div:first-child {
            border: 2px solid #6c757d !important;
            background-color: #ffffff !important;
        }
        
        .stSidebar .stCheckbox > label > div:first-child[aria-checked="true"] {
            background-color: #1a1a1a !important;
            border-color: #1a1a1a !important;
        }
        
        .stSidebar .stCheckbox > label > div:first-child[aria-checked="true"]::after {
            color: #ffffff !important;
        }
        
        /* Regular checkbox styling */
        .stCheckbox > label > div:first-child {
            border: 1px solid #e5e5e5;
        }
        
        .stCheckbox > label > div:first-child[aria-checked="true"] {
            background-color: #2d2d2d;
            border-color: #2d2d2d;
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
        
        /* Popover styling */
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

def apply_dark_mode_styles():
    """Apply dark mode CSS styles"""
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
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #4f46e5 !important;
            color: #ffffff !important;
            border: none !important;
        }
        
        .stButton > button:hover {
            background-color: #4338ca !important;
        }
        
        /* Tabs */
        .stTabs [data-baseweb="tab"] {
            background-color: #374151 !important;
            color: #ffffff !important;
            border: 1px solid #4b5563 !important;
        }
        
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #4f46e5 !important;
            color: #ffffff !important;
        }
        
        /* Charts and plots */
        .stPlotlyChart {
            background-color: #1a1a1a !important;
        }
        
        /* DataFrames */
        .dataframe {
            background-color: #374151 !important;
            color: #ffffff !important;
        }
        
        .dataframe th {
            background-color: #4b5563 !important;
            color: #ffffff !important;
        }
        
        /* Metrics */
        .metric-container {
            background-color: #374151 !important;
            border: 1px solid #4b5563 !important;
        }
        
        /* Code blocks */
        .stCode {
            background-color: #374151 !important;
            color: #ffffff !important;
            border: 1px solid #4b5563 !important;
        }
        
        /* Alerts */
        .stSuccess {
            background-color: #065f46 !important;
            color: #ffffff !important;
        }
        
        .stError {
            background-color: #7f1d1d !important;
            color: #ffffff !important;
        }
        
        .stWarning {
            background-color: #78350f !important;
            color: #ffffff !important;
        }
        
        .stInfo {
            background-color: #1e3a8a !important;
            color: #ffffff !important;
        }
        
        /* Progress bar */
        .stProgress > div > div {
            background-color: #4f46e5 !important;
        }
        
        /* Override text colors for dark mode */
        h1, h2, h3, h4, h5, h6, p, span, label, div {
            color: #ffffff !important;
        }
        
        /* Sidebar specific styling */
        .stSidebar .stCheckbox label {
            color: #ffffff !important;
        }
        
        .stSidebar .stSubheader {
            color: #ffffff !important;
        }
        
        .stSidebar .stMarkdown {
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)

def apply_theme_styles(dark_mode=False):
    """Apply theme-specific styles based on mode"""
    if dark_mode:
        apply_dark_mode_styles()
    else:
        apply_light_mode_styles()
