"""Theme configuration and management"""

class ThemeConfig:
    """Theme configuration and styling management"""
    
    WEB_4_CSS = """
    <style>
    /* Web 4.0 Pure Black/White Minimal Theme */
    
    /* Global Reset */
    .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: #000000 !important;
        border-right: 2px solid #000000 !important;
    }
    
    .css-1d391kg .stMarkdown, 
    .css-1d391kg .stSelectbox label,
    .css-1d391kg .stButton button {
        color: #FFFFFF !important;
    }
    
    /* Header and Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
        font-weight: 700 !important;
        letter-spacing: -0.5px !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        transform: translateY(-2px) !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        font-weight: 500 !important;
    }
    
    .stTextInput > div > div > input:focus {
        box-shadow: 0 0 0 2px #000000 !important;
        border-color: #000000 !important;
    }
    
    /* Select Boxes */
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
    }
    
    /* Metrics */
    .metric-container {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        padding: 20px !important;
        margin: 10px 0 !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }
    
    [data-testid="metric-container"] {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        padding: 15px !important;
        box-shadow: 2px 2px 0px #000000 !important;
    }
    
    [data-testid="metric-container"] > div {
        color: #000000 !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border-radius: 0px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        border-top: none !important;
    }
    
    /* Progress Bars */
    .stProgress > div > div > div {
        background-color: #000000 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px !important;
        background-color: #FFFFFF !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    /* Success/Error Messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 0px !important;
        border: 2px solid #000000 !important;
        font-weight: 500 !important;
    }
    
    .stSuccess {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    /* ChatGPT Integration Styling */
    .chatgpt-container {
        background-color: #FFFFFF !important;
        border: 2px solid #000000 !important;
        border-radius: 0px !important;
        padding: 20px !important;
        margin: 20px 0 !important;
        box-shadow: 4px 4px 0px #000000 !important;
    }
    
    .chatgpt-response {
        background-color: #F8F8F8 !important;
        border: 1px solid #000000 !important;
        border-radius: 0px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        font-family: 'Courier New', monospace !important;
    }
    
    /* Custom Animations */
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .audit-result {
        animation: slideIn 0.5s ease-out !important;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px !important;
        background-color: #FFFFFF !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background-color: #000000 !important;
        border-radius: 0px !important;
    }
    
    /* Remove default Streamlit styling */
    .css-1rs6os, .css-17ziqus {
        visibility: hidden !important;
    }
    
    /* Hide hamburger menu */
    #MainMenu {
        visibility: hidden !important;
    }
    
    /* Hide footer */
    footer {
        visibility: hidden !important;
    }
    
    /* Header styling */
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    </style>
    """
    
    DARK_THEME_CSS = """
    <style>
    /* Dark Theme Override */
    .stApp {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 2px solid #FFFFFF !important;
    }
    
    .stButton > button:hover {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 4px 4px 0px #FFFFFF !important;
    }
    
    .stTextInput > div > div > input {
        background-color: #000000 !important;
        color: #FFFFFF !important;
        border: 2px solid #FFFFFF !important;
    }
    
    .metric-container,
    [data-testid="metric-container"] {
        background-color: #000000 !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 4px 4px 0px #FFFFFF !important;
    }
    
    [data-testid="metric-container"] > div {
        color: #FFFFFF !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }
    
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    
    .streamlit-expanderContent {
        background-color: #000000 !important;
        border: 2px solid #FFFFFF !important;
    }
    
    .chatgpt-container {
        background-color: #000000 !important;
        border: 2px solid #FFFFFF !important;
        box-shadow: 4px 4px 0px #FFFFFF !important;
    }
    
    .chatgpt-response {
        background-color: #1A1A1A !important;
        border: 1px solid #FFFFFF !important;
        color: #FFFFFF !important;
    }
    
    ::-webkit-scrollbar {
        background-color: #000000 !important;
    }
    
    ::-webkit-scrollbar-thumb {
        background-color: #FFFFFF !important;
    }
    </style>
    """
    
    @classmethod
    def get_theme_css(cls, is_dark_theme=False):
        """Get theme CSS based on current theme mode"""
        if is_dark_theme:
            return cls.WEB_4_CSS + cls.DARK_THEME_CSS
        return cls.WEB_4_CSS
    
    @classmethod
    def apply_theme(cls, st, is_dark_theme=False):
        """Apply theme to Streamlit app"""
        st.markdown(cls.get_theme_css(is_dark_theme), unsafe_allow_html=True)
