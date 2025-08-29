"""
Styling Components Module
Contains all CSS styling and theme management for the web audit application
"""

import streamlit as st

class AppStyling:
    """Comprehensive styling and CSS management for the web audit application"""
    
    @staticmethod
    def apply_main_theme():
        """Apply Web 4.0 theme with maximum readability and modern design"""
        st.markdown("""
        <style>
            /* Web 4.0 Base styles - Clean, modern, accessible */
            .stApp {
                background-color: #ffffff;
                color: #1a1a1a;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                line-height: 1.6;
                letter-spacing: 0.01em;
            }
            
            /* Ultra-aggressive top spacing elimination */
            .stApp {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            
            .stApp > header {
                display: none !important;
                height: 0 !important;
            }
            
            .stApp > .main {
                padding-top: 0 !important;
                margin-top: 0 !important;
            }
            
            .main .block-container {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                margin-top: 0 !important;
                max-width: 100% !important;
            }
            
            /* Force zero top spacing on ALL elements */
            .main .block-container > div:first-child,
            .main .block-container > div:first-child > div,
            .main .block-container > div:first-child > div > div,
            .element-container:first-child,
            .stMarkdown:first-child,
            .stTitle:first-child {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
            /* Override Streamlit's default spacing */
            .block-container > div:first-child {
                margin-top: 0 !important;
            }
            
            /* Remove ALL top margins from headers */
            h1:first-child, h2:first-child, h3:first-child,
            .stMarkdown h1:first-child, .stMarkdown h2:first-child, .stMarkdown h3:first-child {
                margin-top: 0 !important;
                padding-top: 0 !important;
            }
            
            /* Typography - Web 4.0 standards */
            .stMarkdown, .stText, .stCaption, .stSubheader, .stHeader {
                color: #1a1a1a !important;
                font-weight: 400 !important;
            }
            
            /* Headers - Clean hierarchy without backgrounds */
            h1, h2, h3, h4, h5, h6 {
                color: #1a1a1a !important;
                font-weight: 300 !important;
                background: none !important;
                background-color: transparent !important;
                padding: 0 !important;
                margin: 1.2rem 0 0.8rem 0 !important;
                letter-spacing: -0.02em !important;
            }
            
            h1 { font-size: 3.2rem !important; font-weight: 200 !important; }
            h2 { font-size: 1.2rem !important; font-weight: 300 !important; }
            h3 { font-size: 1.0rem !important; font-weight: 400 !important; }
            
            /* Input styling - Modern minimal design */
            .stSelectbox label, .stTextInput label, .stRadio label, .stCheckbox label {
                color: #1a1a1a !important;
                font-weight: 500 !important;
                font-size: 0.9rem !important;
            }
            
            /* Input fields - Clean borders, good spacing */
            .stTextInput > div > div > input {
                border: 1px solid #f8f9fa !important;
                background-color: #ffffff !important;
                color: #1a1a1a !important;
                border-radius: 24px !important;
                padding: 0.75rem 1rem !important;
                font-size: 1rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 1px 6px rgba(32,33,36,.28) !important;
            }
            
            .stTextInput > div > div > input:focus {
                border: 1px solid #f8f9fa !important;
                box-shadow: 0 1px 6px rgba(32,33,36,.28) !important;
                outline: none !important;
            }
            
            /* Sidebar - Modern card-like design */
            .stSidebar {
                background-color: #fafbfc !important;
                border-right: 1px solid #e1e5e9 !important;
            }
            
            .stSidebar > div {
                background-color: #fafbfc !important;
                color: #1a1a1a !important;
                padding: 1rem !important;
            }
            
            /* Modern Web 4.0 Button System - Simplified and Clean */
            .stButton > button {
                background-color: #ffffff !important;
                color: #1976d2 !important;
                border: 2px solid #1976d2 !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
                padding: 0.6rem 1.2rem !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
                letter-spacing: 0.01em !important;
                text-transform: none !important;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
                box-shadow: none !important;
            }
            
            .stButton > button:hover {
                background-color: #1976d2 !important;
                color: #ffffff !important;
                border-color: #1976d2 !important;
                box-shadow: 0 2px 8px rgba(25, 118, 210, 0.2) !important;
            }
            
            .stButton > button:active {
                transform: translateY(1px) !important;
            }
            
            /* Primary action buttons - Enhanced specificity */
            .stButton > button[kind="primary"],
            button[kind="primary"] {
                background-color: #1976d2 !important;
                color: #ffffff !important;
                border: 2px solid #1976d2 !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
                padding: 0.6rem 1.2rem !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
                letter-spacing: 0.01em !important;
                box-shadow: 0 2px 4px rgba(25, 118, 210, 0.2) !important;
            }

            .stButton > button[kind="primary"]:hover,
            button[kind="primary"]:hover {
                background-color: #1565c0 !important;
                border-color: #1565c0 !important;
                box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3) !important;
                transform: translateY(-1px) !important;
            }
            
            /* Download and action buttons - Enhanced styling */
            .stDownloadButton > button {
                background-color: #4caf50 !important;
                color: #ffffff !important;
                border: 2px solid #4caf50 !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
                padding: 0.6rem 1.2rem !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
                letter-spacing: 0.01em !important;
                box-shadow: none !important;
                width: 100% !important;
            }
            
            .stDownloadButton > button:hover {
                background-color: #45a049 !important;
                border-color: #45a049 !important;
                box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3) !important;
                transform: translateY(-1px) !important;
            }
            
            /* Alert boxes - Subtle, modern design */
            .stAlert {
                background-color: #f8f9fa !important;
                border: 1px solid #e1e5e9 !important;
                color: #1a1a1a !important;
                border-radius: 8px !important;
                font-weight: 400 !important;
            }
            
            .stSuccess {
                background-color: #f0f9f4 !important;
                border: 1px solid #22c55e !important;
                color: #166534 !important;
            }
            
            .stError {
                background-color: #fef2f2 !important;
                border: 1px solid #ef4444 !important;
                color: #dc2626 !important;
            }
            
            .stWarning {
                background-color: #fffbeb !important;
                border: 1px solid #f59e0b !important;
                color: #92400e !important;
            }
            
            .stInfo {
                background-color: #eff6ff !important;
                border: 1px solid #3b82f6 !important;
                color: #1e40af !important;
            }
            
            /* Modern spacing and layouts */
            .element-container {
                margin-bottom: 1rem !important;
            }
            
            /* Ultra-compact padding for maximum space utilization */
            .block-container {
                padding-top: 0 !important;
                padding-bottom: 0 !important;
                margin-top: 0 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_dark_mode_overrides():
        """Apply dark mode with Web 4.0 standards and excellent readability"""
        st.markdown("""
        <style>
            /* Dark mode - Modern Web 4.0 standards with aggressive text color overrides */
            .stApp {
                background-color: #0f0f0f !important;
                color: #f5f5f5 !important;
            }
            
            /* Override ALL text elements - Ultra-aggressive approach */
            .stApp *, 
            .stApp *:not(.stButton):not(.stSelectbox):not(.stTextInput),
            .stMarkdown, .stMarkdown *,
            .stText, .stText *,
            .stCaption, .stCaption *,
            .stSubheader, .stSubheader *,
            .stHeader, .stHeader *,
            .stWrite, .stWrite *,
            p, span, div:not(.stButton):not(.stSelectbox):not(.stTextInput),
            .main .block-container *:not(.stButton):not(.stSelectbox):not(.stTextInput) {
                color: #f5f5f5 !important;
            }
            
            /* Headers - Clean typography in dark mode */
            h1, h2, h3, h4, h5, h6,
            .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, 
            .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
                color: #ffffff !important;
                font-weight: 300 !important;
                background: none !important;
                background-color: transparent !important;
                letter-spacing: -0.02em !important;
            }
            
            h1 { font-size: 3.2rem !important; font-weight: 200 !important; }
            h2 { font-size: 1.2rem !important; font-weight: 300 !important; }
            h3 { font-size: 1.0rem !important; font-weight: 400 !important; }
            
            /* Main title and subtitle overrides for dark mode */
            .main-title {
                color: #ffffff !important;
                font-size: 3.2rem !important;
                font-weight: 400 !important;
                margin: 0 !important;
                letter-spacing: -0.02em !important;
            }
            
            .main-subtitle {
                color: #cccccc !important;
                font-size: 0.85rem !important;
                font-weight: 300 !important;
                margin: 0 !important;
                letter-spacing: 0.01em !important;
                padding-bottom: 0.5rem !important;
            }
            
            /* Header container styling for dark mode */
            .header-container {
                border-bottom: 1px solid #404040 !important;
            }
            
            /* Dark mode inputs - Google-style for consistency */
            .stTextInput > div > div > input {
                border: 1px solid #4a4a4a !important;
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                border-radius: 24px !important;
                padding: 0.75rem 1rem !important;
                font-size: 1rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 1px 6px rgba(255,255,255,.1) !important;
            }
            
            .stTextInput > div > div > input:focus {
                border: 1px solid #1976d2 !important;
                box-shadow: 0 1px 6px rgba(25, 118, 210, 0.3) !important;
                outline: none !important;
            }
            
            /* Input labels in dark mode */
            .stSelectbox label, .stTextInput label, .stRadio label, .stCheckbox label {
                color: #f5f5f5 !important;
                font-weight: 500 !important;
                font-size: 0.9rem !important;
            }
            
            /* Radio button labels */
            .stRadio > div > label > div > span {
                color: #f5f5f5 !important;
            }
            
            /* Checkbox labels */
            .stCheckbox > div > label > div > span {
                color: #f5f5f5 !important;
            }
            
            /* Metric labels and values */
            .metric-container {
                color: #f5f5f5 !important;
            }
            
            .metric-container * {
                color: #f5f5f5 !important;
            }
            
            /* Dark mode sidebar - Modern design */
            .stSidebar {
                background-color: #1a1a1a !important;
                border-right: 1px solid #404040 !important;
            }
            
            .stSidebar > div {
                background-color: #1a1a1a !important;
                color: #f5f5f5 !important;
                padding: 1.5rem 1rem !important;
            }
            
            /* Sidebar text elements */
            .stSidebar .stMarkdown, 
            .stSidebar .stText, 
            .stSidebar .stCaption, 
            .stSidebar .stSubheader, 
            .stSidebar .stHeader {
                color: #f5f5f5 !important;
                font-weight: 400 !important;
                line-height: 1.5 !important;
            }
            
            .stSidebar .stCheckbox label {
                color: #f5f5f5 !important;
                font-weight: 400 !important;
                font-size: 0.85rem !important;
                line-height: 1.4 !important;
            }
            
            /* Sidebar headers */
            .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
                color: #ffffff !important;
                font-weight: 300 !important;
                background: none !important;
                background-color: transparent !important;
                margin: 0.8rem 0 0.4rem 0 !important;
                letter-spacing: -0.01em !important;
                font-size: 0.95rem !important;
            }
            
            /* Dark mode buttons - Clean and consistent */
            .stButton > button {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                border: 2px solid #4a4a4a !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
                padding: 0.6rem 1.2rem !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
                letter-spacing: 0.01em !important;
                box-shadow: none !important;
            }
            
            .stButton > button:hover {
                background-color: #4a4a4a !important;
                color: #ffffff !important;
                border-color: #666666 !important;
                box-shadow: 0 2px 8px rgba(255, 255, 255, 0.1) !important;
            }
            
            /* Primary buttons in dark mode - Enhanced specificity */
            .stButton > button[kind="primary"],
            button[kind="primary"] {
                background-color: #1976d2 !important;
                color: #ffffff !important;
                border: 2px solid #1976d2 !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
                padding: 0.6rem 1.2rem !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
                letter-spacing: 0.01em !important;
                box-shadow: 0 2px 4px rgba(25, 118, 210, 0.2) !important;
            }

            .stButton > button[kind="primary"]:hover,
            button[kind="primary"]:hover {
                background-color: #1565c0 !important;
                border-color: #1565c0 !important;
                box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3) !important;
            }
            
            /* Download buttons in dark mode */
            .stDownloadButton > button {
                background-color: #4caf50 !important;
                color: #ffffff !important;
                border: 2px solid #4caf50 !important;
                border-radius: 8px !important;
                font-weight: 500 !important;
                padding: 0.6rem 1.2rem !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
                letter-spacing: 0.01em !important;
                box-shadow: none !important;
                width: 100% !important;
            }
            
            .stDownloadButton > button:hover {
                background-color: #45a049 !important;
                border-color: #45a049 !important;
                box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3) !important;
                transform: translateY(-1px) !important;
            }
            
            /* Sidebar buttons in dark mode */
            .stSidebar .stButton > button {
                background-color: #2d2d2d !important;
                color: #f5f5f5 !important;
                border: 1px solid #404040 !important;
                border-radius: 6px !important;
                font-weight: 400 !important;
                font-size: 0.85rem !important;
                padding: 0.5rem 1rem !important;
                transition: all 0.2s ease !important;
            }
            
            .stSidebar .stButton > button:hover {
                background-color: #404040 !important;
                color: #f5f5f5 !important;
                border-color: #666666 !important;
            }
            
            .stSidebar .stButton > button[kind="primary"] {
                background-color: #f5f5f5 !important;
                color: #0f0f0f !important;
                border-color: #f5f5f5 !important;
            }
            
            .stSidebar .stButton > button[kind="primary"]:hover {
                background-color: #e0e0e0 !important;
                border-color: #e0e0e0 !important;
            }
            
            /* Dark mode checkboxes */
            .stSidebar .stCheckbox > label > div:first-child {
                border: 2px solid #666666 !important;
                background-color: #1a1a1a !important;
                border-radius: 4px !important;
            }
            
            /* Dark mode tabs */
            .stTabs [data-baseweb="tab-list"] {
                background-color: #1a1a1a !important;
                border-bottom: 1px solid #404040 !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                color: #cccccc !important;
                background-color: transparent !important;
                border: none !important;
                padding: 0.75rem 1.5rem !important;
                font-weight: 400 !important;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                color: #ffffff !important;
                background-color: #2d2d2d !important;
            }
            
            .stTabs [aria-selected="true"] {
                color: #ffffff !important;
                background-color: #1976d2 !important;
                border-bottom: 2px solid #1976d2 !important;
            }
            
            /* Dark mode metrics */
            .stMetric {
                background-color: #1a1a1a !important;
                border: 1px solid #404040 !important;
                border-radius: 8px !important;
                padding: 1rem !important;
            }
            
            .stMetric > div {
                color: #f5f5f5 !important;
            }
            
            .stMetric label {
                color: #cccccc !important;
                font-size: 0.85rem !important;
            }
            
            .stMetric [data-testid="metric-value"] {
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            
            /* Dark mode alerts and messages */
            .stAlert, .stSuccess, .stInfo, .stWarning, .stError {
                background-color: #2d2d2d !important;
                border: 1px solid #404040 !important;
                color: #f5f5f5 !important;
            }
            
            /* Dark mode expander */
            .streamlit-expanderHeader {
                background-color: #2d2d2d !important;
                color: #f5f5f5 !important;
                border: 1px solid #404040 !important;
            }
            
            .streamlit-expanderContent {
                background-color: #1a1a1a !important;
                border: 1px solid #404040 !important;
                color: #f5f5f5 !important;
            }
            
            .stSidebar .stCheckbox > label > div:first-child[aria-checked="true"] {
                background-color: #f5f5f5 !important;
                border-color: #f5f5f5 !important;
            }
            
            .stSidebar .stCheckbox > label > div:first-child[aria-checked="true"]::after {
                color: #0f0f0f !important;
                font-weight: 600 !important;
            }
            
            /* Dark mode tabs - Modern underline style */
            .stTabs [data-baseweb="tab-list"] {
                border-bottom: 1px solid #404040 !important;
            }
            
            .stTabs [data-baseweb="tab"] {
                background: transparent !important;
                border: none !important;
                border-bottom: 2px solid transparent !important;
                color: #999999 !important;
                font-weight: 400 !important;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                color: #f5f5f5 !important;
                border-bottom-color: #666666 !important;
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background: transparent !important;
                color: #ffffff !important;
                border-bottom-color: #ffffff !important;
                font-weight: 500 !important;
            }
            
            /* Dark mode progress bar */
            .stProgress > div > div > div > div {
                background: linear-gradient(90deg, #f5f5f5 0%, #e0e0e0 100%) !important;
                border-radius: 4px !important;
            }
            
            .stProgress > div > div > div {
                background-color: #2d2d2d !important;
                border: 1px solid #404040 !important;
                border-radius: 4px !important;
            }
            
            /* Dark mode alerts */
            .stAlert {
                background-color: #1a1a1a !important;
                border: 1px solid #404040 !important;
                color: #f5f5f5 !important;
                border-radius: 8px !important;
            }
            
            .stSuccess {
                background-color: #0d2818 !important;
                border: 1px solid #22c55e !important;
                color: #84cc16 !important;
            }
            
            .stError {
                background-color: #2d1515 !important;
                border: 1px solid #ef4444 !important;
                color: #f87171 !important;
            }
            
            .stWarning {
                background-color: #2d2209 !important;
                border: 1px solid #f59e0b !important;
                color: #fbbf24 !important;
            }
            
            .stInfo {
                background-color: #0f1729 !important;
                border: 1px solid #3b82f6 !important;
                color: #60a5fa !important;
            }
            
            /* Dark mode dividers */
            .stSidebar hr {
                border-color: #404040 !important;
                margin: 1.5rem 0 !important;
            }
            
            /* Dark mode table and data elements */
            .dataframe {
                color: #f5f5f5 !important;
                border: 1px solid #404040 !important;
            }
            
            .dataframe th {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                font-weight: 600 !important;
                border: 1px solid #404040 !important;
            }
            
            .dataframe td {
                color: #f5f5f5 !important;
                border: 1px solid #404040 !important;
                background-color: #1a1a1a !important;
            }
            
            /* Dark mode code blocks */
            .stCode {
                background-color: #1a1a1a !important;
                color: #f5f5f5 !important;
                border: 1px solid #404040 !important;
                font-weight: 400 !important;
            }
            
            /* Dark mode JSON display */
            .stJson {
                background-color: #1a1a1a !important;
                border: 1px solid #404040 !important;
                color: #f5f5f5 !important;
            }
            
            /* Dark mode text elements */
            div[data-testid="stText"] {
                color: #f5f5f5 !important;
                font-weight: 400 !important;
            }
            
            /* Dark mode metrics */
            [data-testid="metric-container"] {
                background-color: #1a1a1a !important;
                border: 1px solid #404040 !important;
                border-radius: 8px !important;
                padding: 1rem !important;
            }
            
            [data-testid="metric-container"] label {
                color: #f5f5f5 !important;
                font-weight: 500 !important;
            }
            
            [data-testid="metric-container"] [data-testid="metric-value"] {
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            
            [data-testid="metric-container"] [data-testid="metric-delta"] {
                color: #f5f5f5 !important;
                font-weight: 500 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_button_styling():
        """Apply enhanced button styling with black theme and minimal design"""
        st.markdown("""
        <style>
            /* Advanced button styling - Black minimal theme */
            .stButton > button {
                background: #000000 !important;
                color: #ffffff !important;
                border: 2px solid #000000 !important;
                border-radius: 4px !important;
                font-weight: 600 !important;
                padding: 0.75rem 1.5rem !important;
                transition: all 0.2s ease !important;
                box-shadow: none !important;
            }
            
            .stButton > button:hover {
                background: #333333 !important;
                color: #ffffff !important;
                border: 2px solid #333333 !important;
                transform: none !important;
                box-shadow: none !important;
            }
            
            /* Primary button styling - Enhanced specificity */
            .stButton > button[kind="primary"],
            button[kind="primary"] {
                background-color: #1976d2 !important;
                color: #ffffff !important;
                border: 2px solid #1976d2 !important;
                font-weight: 600 !important;
                border-radius: 8px !important;
                padding: 0.6rem 1.2rem !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
                letter-spacing: 0.01em !important;
                box-shadow: 0 2px 4px rgba(25, 118, 210, 0.2) !important;
            }

            .stButton > button[kind="primary"]:hover,
            button[kind="primary"]:hover {
                background-color: #1565c0 !important;
                border-color: #1565c0 !important;
                box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3) !important;
                transform: translateY(-1px) !important;
            }
            }
            
            /* Download button styling */
            .stDownloadButton > button {
                background: #000000 !important;
                color: #ffffff !important;
                border: 2px solid #000000 !important;
                border-radius: 4px !important;
                font-weight: 600 !important;
            }
            
            .stDownloadButton > button:hover {
                background: #333333 !important;
                color: #ffffff !important;
                border: 2px solid #333333 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_sidebar_styling():
        """Apply Web 4.0 sidebar styling with excellent readability"""
        st.markdown("""
        <style>
            /* Sidebar - Modern card design */
            .stSidebar {
                background-color: #fafbfc !important;
                color: #1a1a1a !important;
                border-right: 1px solid #e1e5e9 !important;
            }
            
            .stSidebar > div {
                background-color: #fafbfc !important;
                color: #1a1a1a !important;
                padding: 1.5rem 1rem !important;
            }
            
            /* All sidebar text elements - Excellent readability */
            .stSidebar .stMarkdown, 
            .stSidebar .stText, 
            .stSidebar .stCaption, 
            .stSidebar .stSubheader, 
            .stSidebar .stHeader {
                color: #1a1a1a !important;
                font-weight: 400 !important;
                line-height: 1.5 !important;
            }
            
            .stSidebar .stCheckbox label {
                color: #1a1a1a !important;
                font-weight: 400 !important;
                font-size: 0.85rem !important;
                line-height: 1.4 !important;
            }
            
            /* Sidebar toggle button - Modern design */
            button[data-testid="collapsedControl"] {
                background-color: #1a1a1a !important;
                color: #ffffff !important;
                border: none !important;
                border-radius: 8px !important;
                padding: 0.75rem !important;
                box-shadow: 0 2px 8px rgba(26, 26, 26, 0.1) !important;
                min-width: 44px !important;
                min-height: 44px !important;
                font-weight: 500 !important;
                transition: all 0.2s ease !important;
            }
            
            button[data-testid="collapsedControl"]:hover {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                transform: translateY(-1px) !important;
                box-shadow: 0 4px 12px rgba(26, 26, 26, 0.15) !important;
            }
            
            /* Checkbox styling - Modern, accessible */
            .stSidebar .stCheckbox > label > div:first-child {
                border: 2px solid #d1d5db !important;
                background-color: #ffffff !important;
                border-radius: 4px !important;
                width: 20px !important;
                height: 20px !important;
            }
            
            .stSidebar .stCheckbox > label > div:first-child[aria-checked="true"] {
                background-color: #1a1a1a !important;
                border-color: #1a1a1a !important;
            }
            
            .stSidebar .stCheckbox > label > div:first-child[aria-checked="true"]::after {
                color: #ffffff !important;
                font-weight: 600 !important;
            }
            
            /* Sidebar headers - Clean typography */
            .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
                color: #1a1a1a !important;
                font-weight: 300 !important;
                background: none !important;
                background-color: transparent !important;
                margin: 1rem 0 0.5rem 0 !important;
                letter-spacing: -0.01em !important;
                font-size: 0.95rem !important;
            }
            
            /* Sidebar dividers - Subtle */
            .stSidebar hr {
                border-color: #e1e5e9 !important;
                margin: 1.5rem 0 !important;
            }
            
            /* Sidebar buttons - Consistent with main theme */
            .stSidebar .stButton > button {
                background-color: #f3f4f6 !important;
                color: #1a1a1a !important;
                border: 1px solid #d1d5db !important;
                border-radius: 6px !important;
                font-weight: 400 !important;
                font-size: 0.85rem !important;
                padding: 0.5rem 1rem !important;
                transition: all 0.2s ease !important;
            }
            
            .stSidebar .stButton > button:hover {
                background-color: #e5e7eb !important;
                color: #1a1a1a !important;
                border-color: #9ca3af !important;
            }
            
            .stSidebar .stButton > button[kind="primary"] {
                background-color: #1976d2 !important;
                color: #ffffff !important;
                border: 2px solid #1976d2 !important;
                font-weight: 600 !important;
                border-radius: 6px !important;
                padding: 0.5rem 1rem !important;
                font-size: 0.85rem !important;
                transition: all 0.2s ease !important;
                letter-spacing: 0.01em !important;
                box-shadow: 0 2px 4px rgba(25, 118, 210, 0.2) !important;
            }

            .stSidebar .stButton > button[kind="primary"]:hover {
                background-color: #1565c0 !important;
                border-color: #1565c0 !important;
                box-shadow: 0 4px 12px rgba(25, 118, 210, 0.3) !important;
                transform: translateY(-1px) !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_tabs_styling():
        """Apply Web 4.0 tabs styling with excellent readability"""
        st.markdown("""
        <style>
            /* Tabs styling - Modern card-based design */
            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                background-color: transparent;
                border-bottom: 1px solid #e1e5e9;
                padding-bottom: 0;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 48px;
                padding: 0 1.5rem;
                background: transparent !important;
                border: none !important;
                border-bottom: 2px solid transparent !important;
                border-radius: 0 !important;
                color: #6b7280 !important;
                font-weight: 400 !important;
                font-size: 0.9rem !important;
                transition: all 0.2s ease !important;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                color: #1a1a1a !important;
                border-bottom-color: #d1d5db !important;
            }
            
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background: transparent !important;
                color: #1a1a1a !important;
                border-bottom-color: #1a1a1a !important;
                font-weight: 500 !important;
            }
            
            /* Tab content - Compact spacing */
            .stTabs [data-baseweb="tab-panel"] {
                color: #1a1a1a !important;
                padding-top: 0.5rem !important;
            }
            
            /* Tab content headers */
            .stTabs [data-baseweb="tab-panel"] h1,
            .stTabs [data-baseweb="tab-panel"] h2,
            .stTabs [data-baseweb="tab-panel"] h3 {
                color: #1a1a1a !important;
                font-weight: 300 !important;
                background: none !important;
                margin-top: 0 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_input_styling():
        """Apply enhanced input field styling with maximum contrast"""
        st.markdown("""
        <style>
            /* Input fields - Maximum contrast design */
            .stTextInput > div > div > input {
                border: 1px solid #f8f9fa !important;
                background-color: #ffffff !important;
                color: #1a1a1a !important;
                border-radius: 24px !important;
                padding: 0.75rem 1rem !important;
                font-size: 1rem !important;
                transition: all 0.2s ease !important;
                box-shadow: 0 1px 6px rgba(32,33,36,.28) !important;
            }
            
            .stTextInput > div > div > input:focus {
                border: 1px solid #f8f9fa !important;
                box-shadow: 0 1px 6px rgba(32,33,36,.28) !important;
                outline: none !important;
            }
            
            /* Text area styling - Maximum contrast */
            .stTextArea textarea {
                color: #000000 !important;
                background-color: #ffffff !important;
                border: 2px solid #000000 !important;
                font-weight: 500 !important;
            }
            
            .stTextArea textarea:focus {
                border-color: #000000 !important;
                color: #000000 !important;
                box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.1) !important;
            }
            
            /* Select box styling */
            .stSelectbox > div > div {
                border: 2px solid #000000 !important;
                background-color: #ffffff !important;
            }
            
            .stSelectbox > div > div > div {
                color: #000000 !important;
                font-weight: 500 !important;
            }
            
            /* Input labels with maximum contrast */
            .stTextInput label, .stTextArea label, .stSelectbox label {
                color: #000000 !important;
                font-weight: 700 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_metric_styling():
        """Apply enhanced metric and dashboard styling with maximum contrast"""
        st.markdown("""
        <style>
            /* Metric containers and labels - Maximum contrast */
            .metric-container {
                color: #000000 !important;
            }
            
            .metric-container [data-testid="metric-container"] {
                color: #000000 !important;
                background-color: #ffffff !important;
                border: 1px solid #cccccc !important;
            }
            
            .metric-container [data-testid="metric-container"] > div {
                color: #000000 !important;
            }
            
            /* All metric labels and values */
            [data-testid="metric-container"] label {
                color: #000000 !important;
                font-weight: 700 !important;
            }
            
            [data-testid="metric-container"] [data-testid="metric-value"] {
                color: #000000 !important;
                font-weight: 800 !important;
            }
            
            [data-testid="metric-container"] [data-testid="metric-delta"] {
                color: #000000 !important;
                font-weight: 600 !important;
            }
            
            /* Metric cards - Maximum contrast design */
            .metric-card {
                background: #ffffff;
                padding: 1rem;
                border: 2px solid #000000;
                margin: 0.5rem 0;
                color: #000000;
                box-shadow: none;
                border-radius: 4px;
            }
            
            /* Status indicators - High contrast */
            .status-good { border-left: 4px solid #000000; }
            .status-warning { border-left: 4px solid #666666; }
            .status-error { border-left: 4px solid #333333; }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_table_and_chart_styling():
        """Apply styling for tables, charts and data displays with maximum contrast"""
        st.markdown("""
        <style>
            /* DataFrame and table styling - Maximum contrast */
            .dataframe {
                color: #000000 !important;
                border: 2px solid #000000 !important;
            }
            
            .dataframe th {
                background-color: #000000 !important;
                color: #ffffff !important;
                font-weight: 700 !important;
                border: 1px solid #000000 !important;
            }
            
            .dataframe td {
                color: #000000 !important;
                border: 1px solid #cccccc !important;
                background-color: #ffffff !important;
            }
            
            /* Chart containers */
            .stPlotlyChart {
                color: #000000 !important;
            }
            
            /* Code blocks - Maximum contrast */
            .stCode {
                background-color: #ffffff !important;
                color: #000000 !important;
                border: 2px solid #000000 !important;
                font-weight: 600 !important;
            }
            
            /* Expander headers - Maximum contrast */
            .streamlit-expanderHeader {
                color: #000000 !important;
                font-weight: 700 !important;
                background-color: #ffffff !important;
                border: 1px solid #cccccc !important;
            }
            
            /* JSON display and code elements */
            .stJson {
                background-color: #ffffff !important;
                border: 2px solid #000000 !important;
                color: #000000 !important;
            }
            
            /* Text elements in content areas */
            .element-container div {
                color: #000000 !important;
            }
            
            /* Ensure all text is highly contrasted */
            div[data-testid="stText"] {
                color: #000000 !important;
                font-weight: 500 !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_progress_and_loading_styling():
        """Apply Web 4.0 styling for progress bars and loading elements"""
        st.markdown("""
        <style>
            /* Progress bar - Modern design */
            .stProgress > div > div > div > div {
                background: linear-gradient(90deg, #1a1a1a 0%, #2d2d2d 100%) !important;
                border-radius: 4px !important;
            }
            
            .stProgress > div > div > div {
                background-color: #f3f4f6 !important;
                border: 1px solid #e1e5e9 !important;
                border-radius: 4px !important;
                height: 8px !important;
            }
            
            /* Spinner/Loading - Modern theme */
            .stSpinner > div {
                border-top-color: #1a1a1a !important;
                border-left-color: #1a1a1a !important;
                border-width: 3px !important;
            }
            
            /* Loading text with excellent readability */
            .stSpinner + div {
                color: #1a1a1a !important;
                font-weight: 400 !important;
                font-size: 0.9rem !important;
                margin-top: 0.5rem !important;
            }
            
            /* Status indicators */
            .status-text {
                color: #6b7280 !important;
                font-size: 0.85rem !important;
                font-style: italic !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_example_domains_styling():
        """Apply styling for example domains section with maximum contrast"""
        st.markdown("""
        <style>
            .example-domains {
                text-align: center;
                margin: 1rem 0;
                font-size: 0.9rem;
                color: #666666;
                font-weight: 500;
            }
            
            .example-domains a {
                color: #000000;
                text-decoration: underline;
                margin: 0 10px;
                font-weight: 600;
            }
            
            .example-domains a:hover {
                color: #333333;
                text-decoration: none;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def apply_complete_theme(dark_mode=False):
        """Apply the complete theme with all styling components"""
        # Apply base theme
        AppStyling.apply_main_theme()
        
        # Apply component-specific styling
        AppStyling.apply_button_styling()
        AppStyling.apply_sidebar_styling()
        AppStyling.apply_tabs_styling()
        AppStyling.apply_input_styling()
        AppStyling.apply_metric_styling()
        AppStyling.apply_table_and_chart_styling()
        AppStyling.apply_progress_and_loading_styling()
        AppStyling.apply_example_domains_styling()
        
        # Apply dark mode overrides if enabled
        if dark_mode:
            AppStyling.apply_dark_mode_overrides()
