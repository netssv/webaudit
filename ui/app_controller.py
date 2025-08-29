"""
Application Controller Module
Contains main application logic and workflow
"""

import streamlit as st
from datetime import datetime
import time

# Import our modular components
from ui.styles import apply_theme_styles
from ui.displays import (
    initialize_session_state,
    display_header, 
    display_search_interface,
    display_loading_progress,
    display_audit_results
)
from ui.ai_analysis import display_ai_analysis
from web_auditor import WebAuditor


def validate_url(url):
    """Validate URL format"""
    if not url:
        return False, "Please enter a URL"
    
    if not url.startswith(('http://', 'https://')):
        return False, "URL must start with http:// or https://"
    
    # Basic URL validation
    if '.' not in url:
        return False, "Invalid URL format"
    
    return True, ""


def run_audit(url, selected_modules):
    """Run the audit with selected modules"""
    auditor = WebAuditor()
    
    try:
        # Convert module names to match WebAuditor format
        module_mapping = {
            'Performance': 'performance',
            'SEO': 'seo_marketing', 
            'Security': 'ssl',
            'DNS': 'dns',
            'Ranking': 'ranking'
        }
        
        # Create modules dict for WebAuditor
        modules_dict = {}
        for module in selected_modules:
            if module in module_mapping:
                modules_dict[module_mapping[module]] = True
        
        with st.spinner("Running comprehensive audit..."):
            # Use the comprehensive_audit method
            audit_results = auditor.comprehensive_audit(url, modules_dict)
            
            if 'error' in audit_results:
                st.error(f"Audit error: {audit_results['error']}")
                return None
            
            # Return just the results portion for compatibility
            return audit_results.get('results', {})
        
    except Exception as e:
        st.error(f"Error during audit: {str(e)}")
        return None


def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Apply theme styles
    apply_theme_styles(st.session_state.dark_mode)
    
    # Display header
    display_header()
    
    # Sidebar for module selection
    with st.sidebar:
        st.markdown("### 🔧 Analysis Modules")
        st.markdown("Select which analyses to run:")
        
        modules = {
            'Performance': st.checkbox('⚡ Performance Analysis', value=True),
            'SEO': st.checkbox('🔍 SEO Analysis', value=True),
            'Security': st.checkbox('🔒 Security Analysis', value=True),
            'DNS': st.checkbox('🌐 DNS Analysis', value=True),
            'Ranking': st.checkbox('📈 Ranking Analysis', value=False)
        }
        
        selected_modules = [name for name, selected in modules.items() if selected]
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This tool performs comprehensive website analysis including:
        - **Performance**: Page speed, Core Web Vitals
        - **SEO**: Meta tags, content optimization
        - **Security**: SSL certificates, headers
        - **DNS**: Domain configuration
        - **Ranking**: Authority metrics (optional)
        """)
    
    # Main content area
    if not st.session_state.audit_in_progress:
        # Display search interface
        display_search_interface()
        
        # Audit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Start Audit", type="primary", disabled=not st.session_state.url_input):
                # Validate URL
                is_valid, error_msg = validate_url(st.session_state.url_input)
                
                if not is_valid:
                    st.error(f"❌ {error_msg}")
                elif not selected_modules:
                    st.error("❌ Please select at least one analysis module")
                else:
                    # Start audit
                    st.session_state.audit_in_progress = True
                    st.session_state.audit_results = None
                    st.rerun()
        
        # Display previous results if available
        if st.session_state.audit_results:
            st.markdown("---")
            st.markdown("### 📋 Previous Results")
            display_audit_results(st.session_state.audit_results)
    
    else:
        # Show loading progress
        display_loading_progress()
        
        # Run the audit
        results = run_audit(st.session_state.url_input, selected_modules)
        
        # Update session state
        st.session_state.audit_in_progress = False
        st.session_state.audit_results = results
        
        # Show results
        if results:
            st.success("✅ Audit completed successfully!")
            time.sleep(1)
            st.rerun()
        else:
            st.error("❌ Audit failed. Please try again.")
            time.sleep(2)
            st.rerun()


if __name__ == "__main__":
    main()
