"""
Styling Components Module — Google-Inspired Clean Theme
Minimal CSS for a clean, modern web audit interface
"""

import streamlit as st


class AppStyling:
    """Clean, Google-inspired styling for the web audit application"""

    @staticmethod
    def apply_complete_theme():
        """Apply the complete Google-inspired theme"""
        st.markdown("""
        <style>
        /* ── Import Google Font ─────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* ── Global Reset ───────────────────────────────── */
        *, *::before, *::after { box-sizing: border-box; }

        html, body, [data-testid="stAppViewContainer"],
        [data-testid="stApp"], .main, .block-container {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
            background-color: #ffffff !important;
            color: #202124 !important;
        }

        .block-container {
            max-width: 960px !important;
            padding: 1rem 2rem 4rem 2rem !important;
        }

        /* ── Headings ───────────────────────────────────── */
        h1, h2, h3, h4, h5, h6,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            font-family: 'Inter', sans-serif !important;
            color: #202124 !important;
            font-weight: 600 !important;
        }

        /* ── Search Input (Google-style pill) ────────────── */
        [data-testid="stTextInput"] input {
            border: 1px solid #dfe1e5 !important;
            background-color: #fff !important;
            color: #202124 !important;
            border-radius: 24px !important;
            padding: 12px 20px !important;
            font-size: 16px !important;
            font-family: 'Inter', sans-serif !important;
            transition: box-shadow 0.2s, border-color 0.2s !important;
            box-shadow: none !important;
        }
        [data-testid="stTextInput"] input:hover {
            box-shadow: 0 1px 6px rgba(32,33,36,.18) !important;
            border-color: #dfe1e5 !important;
        }
        [data-testid="stTextInput"] input:focus {
            box-shadow: 0 1px 6px rgba(32,33,36,.28) !important;
            border-color: #4285f4 !important;
            outline: none !important;
        }
        [data-testid="stTextInput"] label {
            display: none !important;
        }

        /* ── Primary Button ──────────────────────────────── */
        .stButton > button[kind="primary"],
        button[data-testid="stBaseButton-primary"] {
            background-color: #4285f4 !important;
            color: #fff !important;
            border: none !important;
            border-radius: 24px !important;
            padding: 10px 24px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            font-family: 'Inter', sans-serif !important;
            letter-spacing: 0.02em;
            transition: background-color 0.15s, box-shadow 0.15s !important;
            box-shadow: none !important;
        }
        .stButton > button[kind="primary"]:hover,
        button[data-testid="stBaseButton-primary"]:hover {
            background-color: #3367d6 !important;
            box-shadow: 0 1px 3px rgba(66, 133, 244, 0.3) !important;
        }

        /* ── Secondary / other buttons ───────────────────── */
        .stButton > button:not([kind="primary"]),
        button[data-testid="stBaseButton-secondary"] {
            background-color: #f8f9fa !important;
            color: #3c4043 !important;
            border: 1px solid #dadce0 !important;
            border-radius: 20px !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            font-family: 'Inter', sans-serif !important;
            padding: 8px 16px !important;
        }
        .stButton > button:not([kind="primary"]):hover,
        button[data-testid="stBaseButton-secondary"]:hover {
            background-color: #f1f3f4 !important;
            border-color: #d2d5d9 !important;
        }

        /* ── Tabs ────────────────────────────────────────── */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0px !important;
            border-bottom: 1px solid #e8eaed !important;
            background-color: transparent !important;
        }
        .stTabs [data-baseweb="tab"] {
            font-family: 'Inter', sans-serif !important;
            color: #5f6368 !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            padding: 10px 16px !important;
            border-bottom: 3px solid transparent !important;
            background-color: transparent !important;
        }
        .stTabs [data-baseweb="tab"]:hover {
            color: #202124 !important;
            background-color: #f8f9fa !important;
        }
        .stTabs [aria-selected="true"] {
            color: #4285f4 !important;
            border-bottom: 3px solid #4285f4 !important;
            background-color: transparent !important;
        }

        /* ── Metrics ─────────────────────────────────────── */
        [data-testid="stMetric"] {
            background: #f8f9fa;
            border: 1px solid #e8eaed;
            border-radius: 12px;
            padding: 16px;
        }
        [data-testid="stMetricLabel"] {
            font-size: 12px !important;
            color: #5f6368 !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }
        [data-testid="stMetricValue"] {
            font-size: 24px !important;
            font-weight: 600 !important;
            color: #202124 !important;
        }

        /* ── Cards (custom HTML) ─────────────────────────── */
        .audit-card {
            background: #ffffff;
            border: 1px solid #e8eaed;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 12px;
            transition: box-shadow 0.2s;
        }
        .audit-card:hover {
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .card-title {
            font-size: 14px;
            font-weight: 600;
            color: #202124;
            margin-bottom: 8px;
        }
        .card-value {
            font-size: 28px;
            font-weight: 700;
            color: #4285f4;
        }
        .card-subtitle {
            font-size: 12px;
            color: #5f6368;
            margin-top: 4px;
        }

        /* ── Status Badges ───────────────────────────────── */
        .badge-pass {
            display: inline-block;
            background: #e6f4ea;
            color: #137333;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        .badge-fail {
            display: inline-block;
            background: #fce8e6;
            color: #c5221f;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        .badge-warn {
            display: inline-block;
            background: #fef7e0;
            color: #b05a00;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        .badge-info {
            display: inline-block;
            background: #e8f0fe;
            color: #1a73e8;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        .badge-clean {
            display: inline-block;
            background: #e6f4ea;
            color: #137333;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }
        .badge-listed {
            display: inline-block;
            background: #fce8e6;
            color: #c5221f;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 500;
        }

        /* ── Tool Link Grid ──────────────────────────────── */
        .tool-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 12px;
            margin-top: 12px;
        }
        .tool-card {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            background: #fff;
            border: 1px solid #e8eaed;
            border-radius: 12px;
            padding: 16px;
            text-decoration: none;
            color: #202124;
            transition: box-shadow 0.15s, border-color 0.15s;
        }
        .tool-card:hover {
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-color: #4285f4;
        }
        .tool-icon {
            font-size: 28px;
            line-height: 1;
            flex-shrink: 0;
        }
        .tool-name {
            font-size: 14px;
            font-weight: 600;
            color: #1a73e8;
            margin-bottom: 4px;
        }
        .tool-desc {
            font-size: 12px;
            color: #5f6368;
        }
        .tool-category {
            font-size: 10px;
            color: #9aa0a6;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-top: 4px;
        }

        /* ── Expanders ───────────────────────────────────── */
        [data-testid="stExpander"] {
            border: 1px solid #e8eaed !important;
            border-radius: 12px !important;
            overflow: hidden;
        }
        [data-testid="stExpander"] summary {
            font-weight: 500 !important;
            color: #202124 !important;
        }

        /* ── Sidebar ─────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background-color: #f8f9fa !important;
            border-right: 1px solid #e8eaed !important;
        }
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #202124 !important;
        }
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
            color: #3c4043 !important;
        }

        /* ── Dividers ────────────────────────────────────── */
        hr {
            border: none !important;
            border-top: 1px solid #e8eaed !important;
            margin: 16px 0 !important;
        }

        /* ── Info / Warning / Error boxes ─────────────────── */
        .stAlert {
            border-radius: 8px !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* ── Progress bar ────────────────────────────────── */
        .stProgress > div > div {
            background-color: #4285f4 !important;
        }

        /* ── Spinner ─────────────────────────────────────── */
        .stSpinner > div {
            border-top-color: #4285f4 !important;
        }

        /* ── Data tables ─────────────────────────────────── */
        .stDataFrame, [data-testid="stDataFrame"] {
            border-radius: 8px !important;
            overflow: hidden;
        }

        /* ── Header area ─────────────────────────────────── */
        .app-header {
            text-align: center;
            padding: 3rem 0 1.5rem 0;
        }
        .app-header h1 {
            font-size: 2.5rem !important;
            font-weight: 300 !important;
            color: #202124 !important;
            margin: 0 !important;
            letter-spacing: -0.02em;
        }
        .app-header .subtitle {
            font-size: 14px;
            color: #5f6368;
            margin-top: 4px;
        }

        /* ── Quick-tool buttons row ──────────────────────── */
        .quick-tools {
            display: flex;
            justify-content: center;
            gap: 8px;
            margin-top: 16px;
            flex-wrap: wrap;
        }
        .quick-tool-btn {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #f8f9fa;
            border: 1px solid #e8eaed;
            border-radius: 20px;
            padding: 8px 16px;
            font-size: 13px;
            font-weight: 500;
            color: #3c4043;
            text-decoration: none;
            cursor: default;
            transition: background 0.15s;
        }
        .quick-tool-btn:hover {
            background: #f1f3f4;
        }

        /* ── Record table ────────────────────────────────── */
        .record-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        .record-table th {
            text-align: left;
            padding: 8px 12px;
            background: #f8f9fa;
            color: #5f6368;
            font-weight: 600;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 2px solid #e8eaed;
        }
        .record-table td {
            padding: 8px 12px;
            border-bottom: 1px solid #f1f3f4;
            color: #202124;
        }
        .record-table tr:last-child td {
            border-bottom: none;
        }

        /* ── Hide Streamlit branding ─────────────────────── */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
        """, unsafe_allow_html=True)
