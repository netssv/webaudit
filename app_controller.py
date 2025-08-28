"""Main application controller for the web audit tool"""
import streamlit as st
from datetime import datetime
import asyncio
import traceback
import json

# Import modular components
from config import AppConfig, SessionConfig, ThemeConfig
from ui import UIComponents, DisplayManager
from utils import URLValidator, ExportManager
from web_auditor import WebAuditor

class WebAuditApp:
    """Main application controller"""
    
    def __init__(self):
        self.ui_components = UIComponents()
        self.display_manager = DisplayManager()
        self.url_validator = URLValidator()
        self.export_manager = ExportManager()
        self.web_auditor = WebAuditor()
        
        # Initialize session state
        SessionConfig.initialize_session(st)
    
    def run(self):
        """Main application entry point"""
        # Configure page
        st.set_page_config(
            page_title="Web Audit Analyzer",
            page_icon="🌐",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Apply theme
        current_theme = st.session_state.get(SessionConfig.THEME_MODE, SessionConfig.DEFAULT_THEME)
        ThemeConfig.apply_theme(st, current_theme)
        
        # Render main UI
        self._render_main_interface()
    
    def _render_main_interface(self):
        """Render the main application interface"""
        # Header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            self.ui_components.render_header()
        
        with col2:
            self.ui_components.render_theme_toggle()
        
        # Sidebar
        url, selected_mode, analyze_button = self.ui_components.render_sidebar()
        
        # Main content area
        if analyze_button and url:
            self._handle_analysis(url, selected_mode)
        
        # Display results if available
        audit_result = st.session_state.get(SessionConfig.AUDIT_RESULT)
        if audit_result:
            self._display_results(audit_result)
        
        # ChatGPT Integration (outside of tabs)
        if audit_result:
            st.markdown("---")
            api_key, question = self.ui_components.render_chatgpt_integration()
            if api_key and question:
                self._handle_chatgpt_query(api_key, question, audit_result)
        
        # Footer
        self.ui_components.render_footer()
    
    def _handle_analysis(self, url, mode):
        """Handle website analysis"""
        # Validate URL
        clean_url, error = self.url_validator.validate_and_normalize(url)
        if error:
            st.error(f"❌ **URL Error:** {error}")
            return
        
        # Store URL in session
        st.session_state[SessionConfig.LAST_URL] = clean_url
        
        # Get modules for selected mode
        modules = AppConfig.get_audit_modules(mode)
        
        # Display loading message
        self.display_manager.display_loading_message(f"Analyzing {clean_url} with {mode}...")
        
        try:
            # Progress bar
            progress_bar = st.progress(0, text="Initializing analysis...")
            
            # Run analysis
            progress_bar.progress(20, text="Starting web audit...")
            audit_result = self.web_auditor.comprehensive_audit(clean_url, audit_mode=mode.lower().replace(' ', '_'))
            progress_bar.progress(100, text="Analysis complete!")
            
            if audit_result:
                # Add metadata
                audit_result['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                audit_result['mode'] = mode
                audit_result['modules_used'] = modules
                
                # Store in session state
                st.session_state[SessionConfig.AUDIT_RESULT] = audit_result
                
                # Success message
                self.display_manager.display_success_message()
                
                # Rerun to display results
                st.rerun()
            else:
                st.error("❌ **Analysis Failed:** No results returned from audit")
                
        except Exception as e:
            error_msg = f"Analysis error: {str(e)}"
            st.error(f"❌ **Analysis Failed:** {error_msg}")
            
            # Log detailed error for debugging
            if st.session_state.get('debug_mode', False):
                st.code(traceback.format_exc())
    
    def _display_results(self, audit_result):
        """Display audit results"""
        st.markdown("---")
        
        # Export options
        export_format = self.ui_components.render_export_options(audit_result)
        if export_format:
            self._handle_export(audit_result, export_format)
        
        # Display results
        self.display_manager.display_audit_summary(audit_result)
    
    def _handle_export(self, audit_result, format_type):
        """Handle result export"""
        try:
            if format_type == "JSON":
                json_data = json.dumps(audit_result, indent=2, default=str)
                st.download_button(
                    label="💾 Download JSON",
                    data=json_data,
                    file_name=f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
            
            elif format_type == "CSV":
                # Use web_auditor's export functionality
                csv_filename = self.web_auditor.export_to_json(audit_result)
                if csv_filename:
                    st.success(f"Results exported to {csv_filename}")
                else:
                    st.error("Failed to export CSV")
            
            elif format_type == "Summary Report":
                summary_data = self.web_auditor.generate_summary_report(audit_result)
                st.download_button(
                    label="💾 Download Summary",
                    data=summary_data,
                    file_name=f"audit_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain"
                )
            
        except Exception as e:
            st.error(f"❌ **Export Failed:** {str(e)}")
    
    def _handle_chatgpt_query(self, api_key, question, audit_result):
        """Handle ChatGPT integration"""
        if not api_key or not question:
            return
        
        try:
            # Initialize ChatGPT client (this would need actual OpenAI integration)
            st.info("🤖 **AI Analysis:** This feature requires OpenAI API integration.")
            
            # Placeholder for actual ChatGPT integration
            with st.container():
                st.markdown('<div class="chatgpt-container">', unsafe_allow_html=True)
                st.markdown("**Your Question:**")
                st.write(question)
                
                st.markdown("**AI Response:**")
                st.markdown('<div class="chatgpt-response">', unsafe_allow_html=True)
                st.write("ChatGPT integration is ready for implementation. "
                        "This would analyze your audit results and provide personalized recommendations.")
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ **AI Query Failed:** {str(e)}")

def main():
    """Application entry point"""
    app = WebAuditApp()
    app.run()

if __name__ == "__main__":
    main()
