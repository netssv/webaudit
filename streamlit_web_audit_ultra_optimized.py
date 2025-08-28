"""
Ultra-Optimized Web Audit Tool - Streamlit Application
Maximum code reuse and minimal duplication implementation
"""

import streamlit as st
import sys
import os

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import optimized components
from web_auditor import WebAuditor
from ui.styling import AppStyling
from ui.core_components import CoreUI
from ui.optimized_displays import OptimizedDisplays

# Page configuration
st.set_page_config(
    page_title="Web Audit Tool",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

class WebAuditApp:
    """Ultra-optimized web audit application with maximum code reuse"""
    
    def __init__(self):
        """Initialize the application"""
        self.auditor = WebAuditor()
        CoreUI.initialize_session_state()
        
        # Initialize auditor in session state
        if 'auditor' not in st.session_state:
            st.session_state.auditor = self.auditor
    
    def run(self):
        """Run the main application"""
        # Apply styling
        dark_mode = st.session_state.get('dark_mode', False)
        AppStyling.apply_complete_theme(dark_mode)
        
        # Display header
        CoreUI.display_header()
        
        # Search interface
        url_input, selected_modules, audit_button = CoreUI.display_search_interface()
        
        # Process audit request
        self._handle_audit_request(url_input, selected_modules, audit_button)
        
        # Display results
        if st.session_state.audit_results:
            OptimizedDisplays.display_audit_results(st.session_state.audit_results)
        
        # Sidebar settings
        CoreUI.display_sidebar_settings()
    
    def _handle_audit_request(self, url_input, selected_modules, audit_button):
        """Handle audit request processing"""
        # Check for URL changes or button click
        url_changed = url_input and url_input != st.session_state.get('previous_url', '')
        
        if (audit_button and url_input) or url_changed:
            # Store current URL to track changes
            st.session_state.previous_url = url_input
            
            # Perform audit with loading indicator
            with st.spinner("Performing comprehensive audit..."):
                CoreUI.display_loading_progress()
                results = st.session_state.auditor.comprehensive_audit(url_input, selected_modules)
                st.session_state.audit_results = results

def main():
    """Main application entry point"""
    app = WebAuditApp()
    app.run()

if __name__ == "__main__":
    main()
