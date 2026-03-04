"""
Web Audit Tool — Streamlit Application
Google-inspired clean interface for comprehensive website analysis
"""

import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from web_auditor import WebAuditor
from ui.styling import AppStyling
from ui.core_components import CoreUI
from ui.optimized_displays import OptimizedDisplays

# Page config
st.set_page_config(
    page_title="Web Audit Tool",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)


class WebAuditApp:
    """Main web audit application"""

    def __init__(self):
        self.auditor = WebAuditor()
        CoreUI.initialize_session_state()
        if 'auditor' not in st.session_state:
            st.session_state.auditor = self.auditor

    def run(self):
        """Run the application"""
        AppStyling.apply_complete_theme()
        CoreUI.display_header()

        has_results = st.session_state.audit_results is not None
        url_input, selected_modules, audit_button = CoreUI.display_search_interface(show_pills=not has_results)

        # Handle audit — if new results are produced, rerun so pills disappear
        if self._handle_audit(url_input, selected_modules, audit_button):
            st.rerun()

        if st.session_state.audit_results:
            OptimizedDisplays.display_audit_results(st.session_state.audit_results)

        CoreUI.display_sidebar_settings()

    def _handle_audit(self, url_input, selected_modules, audit_button):
        """Process audit request. Returns True if new results were stored."""
        if audit_button and url_input:
            st.session_state.previous_url = url_input

            with st.spinner("Analyzing..."):
                CoreUI.display_loading_progress()
                results = st.session_state.auditor.comprehensive_audit(url_input, selected_modules)

                if results and 'results' in results:
                    st.session_state.audit_results = results['results']
                else:
                    st.session_state.audit_results = results
                return True
        return False


def main():
    app = WebAuditApp()
    app.run()


if __name__ == "__main__":
    main()
