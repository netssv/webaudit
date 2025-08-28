"""
Streamlit Web Audit Tool - Modular Version
Optimized and organized for better maintainability and performance
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the modular app controller
from ui.app_controller import main

# Page configuration
st.set_page_config(
    page_title="Web Audit Tool - Modular",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if __name__ == "__main__":
    main()
