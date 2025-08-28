"""
Web Audit Tool - Optimized Modular Application
Streamlined, fast-loading comprehensive website analysis tool
"""

import streamlit as st
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our modules
from web_auditor import WebAuditor
from ui.styling import AppStyling
from ui.core_components import CoreUI
from ui.displays import display_audit_results

# Page configuration
st.set_page_config(
    page_title="Web Audit Tool",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

class WebAuditApp:
    """Main Web Audit Application Class - Optimized for Performance"""
    
    def __init__(self):
        """Initialize the application with lazy loading"""
        # Initialize session state
        CoreUI.initialize_session_state()
        
        # Initialize auditor only when needed
        if 'auditor' not in st.session_state:
            st.session_state.auditor = WebAuditor()
    
    def apply_styling(self):
        """Apply application styling based on current theme"""
        dark_mode = st.session_state.get('dark_mode', False)
        AppStyling.apply_complete_theme(dark_mode=dark_mode)
    
    def handle_audit_request(self, url_input, selected_modules, audit_button):
        """Handle the audit request and process results efficiently"""
        # Check if audit should be triggered
        url_changed = url_input and url_input != st.session_state.get('previous_url', '')
        
        if (audit_button and url_input) or url_changed:
            # Store the current URL to track changes
            st.session_state.previous_url = url_input
            
            # Show loading progress
            with st.spinner("Performing comprehensive audit..."):
                CoreUI.display_loading_progress()
                
                # Perform the audit
                try:
                    results = st.session_state.auditor.comprehensive_audit(url_input, selected_modules)
                    st.session_state.audit_results = results
                    
                    if results:
                        CoreUI.display_success_message("Audit completed successfully!")
                    else:
                        CoreUI.display_error_message("Audit failed to return results", "warning")
                        
                except Exception as e:
                    CoreUI.display_error_message(f"Audit failed: {str(e)}", "error")
                    st.session_state.audit_results = None
    
    def display_results(self):
        """Display audit results if available"""
        if st.session_state.audit_results:
            display_audit_results(st.session_state.audit_results)
        else:
            # Show welcome message when no results
            st.markdown("""
            <div style="
                text-align: center;
                padding: 40px 20px;
                background-color: #f8f9fa;
                border-radius: 10px;
                margin: 20px 0;
                border: 1px solid #e9ecef;
            ">
                <h3 style="color: #6c757d; margin-bottom: 20px;">🌐 Welcome to Web Audit Tool</h3>
                <p style="color: #6c757d; font-size: 16px; margin-bottom: 15px;">
                    Enter a website URL above to begin comprehensive analysis
                </p>
                <p style="color: #6c757d; font-size: 14px;">
                    We'll analyze performance, SEO, security, DNS, and ranking factors
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    def run(self):
        """Run the main application with optimized flow"""
        # Apply styling first for immediate visual feedback
        self.apply_styling()
        
        # Display header
        CoreUI.display_header()
        
        # Display search interface
        url_input, selected_modules, audit_button = CoreUI.display_search_interface()
        
        # Handle audit request
        self.handle_audit_request(url_input, selected_modules, audit_button)
        
        # Display results
        self.display_results()
        
        # Display sidebar settings (lazy loaded)
        CoreUI.display_sidebar_settings()

def main():
    """Main application entry point - Optimized startup"""
    try:
        # Create and run the application
        app = WebAuditApp()
        app.run()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.stop()

if __name__ == "__main__":
    main()
