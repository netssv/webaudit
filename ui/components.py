"""UI Components for Web Audit Tool"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from config.settings import AppConfig, SessionConfig

class UIComponents:
    """Reusable UI components for the web audit application"""
    
    @staticmethod
    def render_sidebar():
        """Render the main sidebar with controls"""
        with st.sidebar:
            st.title("🌐 WEB AUDIT")
            st.markdown("---")
            
            # URL Input
            url = st.text_input(
                "🔗 Enter Website URL",
                placeholder="https://example.com",
                help="Enter the website URL you want to analyze",
                value=st.session_state.get(SessionConfig.LAST_URL, "")
            )
            
            # Audit Mode Selection
            audit_modes = list(AppConfig.AUDIT_MODES.keys())
            
            selected_mode = st.selectbox(
                "📊 Select Audit Mode",
                audit_modes,
                index=audit_modes.index(st.session_state.get(SessionConfig.SELECTED_MODE, SessionConfig.DEFAULT_MODE)),
                help="Choose the type of analysis to perform"
            )
            
            # Mode Description
            st.info(AppConfig.get_mode_description(selected_mode))
            
            # Analysis Button
            analyze_button = st.button(
                "🚀 START ANALYSIS",
                type="primary",
                use_container_width=True,
                help="Begin the website analysis"
            )
            
            # Store selections in session state
            if url != st.session_state.get(SessionConfig.LAST_URL, ""):
                st.session_state[SessionConfig.LAST_URL] = url
            
            if selected_mode != st.session_state.get(SessionConfig.SELECTED_MODE, ""):
                st.session_state[SessionConfig.SELECTED_MODE] = selected_mode
            
            return url, selected_mode, analyze_button
    
    @staticmethod
    def render_theme_toggle():
        """Render theme toggle button"""
        current_theme = st.session_state.get(SessionConfig.THEME_MODE, SessionConfig.DEFAULT_THEME)
        theme_text = "🌙 Dark Theme" if not current_theme else "☀️ Light Theme"
        
        if st.button(theme_text, help="Switch between light and dark themes"):
            st.session_state[SessionConfig.THEME_MODE] = not current_theme
            st.rerun()
    
    @staticmethod
    def render_export_options(audit_result):
        """Render export options for audit results"""
        if not audit_result:
            return None
        
        st.markdown("### 📥 Export Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📄 Export JSON", use_container_width=True):
                return "JSON"
        
        with col2:
            if st.button("📊 Export CSV", use_container_width=True):
                return "CSV"
        
        with col3:
            if st.button("📋 Export Summary", use_container_width=True):
                return "Summary Report"
        
        return None
    
    @staticmethod
    def render_chatgpt_integration():
        """Render ChatGPT integration section"""
        st.markdown("### 🤖 AI Analysis Assistant")
        
        # API Key Input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="sk-...",
            help="Enter your OpenAI API key for AI-powered analysis",
            value=st.session_state.get(SessionConfig.CHATGPT_API_KEY, "")
        )
        
        # Store API key in session state
        if api_key != st.session_state.get(SessionConfig.CHATGPT_API_KEY, ""):
            st.session_state[SessionConfig.CHATGPT_API_KEY] = api_key
        
        # Question Input
        question = st.text_area(
            "Ask about your audit results",
            placeholder="How can I improve my website's SEO score?",
            help="Ask specific questions about your audit results"
        )
        
        # Send Button
        if st.button("🚀 Ask AI", type="primary"):
            return api_key, question
        
        return None, None
    
    @staticmethod
    def render_metrics_grid(metrics_data):
        """Render metrics in a grid layout"""
        if not metrics_data:
            return
        
        # Calculate number of columns based on metrics count
        num_metrics = len(metrics_data)
        cols = st.columns(min(4, num_metrics))
        
        for i, (label, value, delta) in enumerate(metrics_data):
            with cols[i % len(cols)]:
                st.metric(label, value, delta)
    
    @staticmethod
    def render_progress_bar(progress_value, label="Progress"):
        """Render progress bar with label"""
        st.progress(progress_value, text=label)
    
    @staticmethod
    def render_info_card(title, content, icon="ℹ️"):
        """Render an information card"""
        with st.container():
            st.markdown(f"""
            <div class="metric-container">
                <h4>{icon} {title}</h4>
                <p>{content}</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render application header"""
        st.title(AppConfig.APP_TITLE)
        st.markdown(f"**{AppConfig.APP_DESCRIPTION}** - Version {AppConfig.APP_VERSION}")
        st.markdown("---")
    
    @staticmethod
    def render_footer():
        """Render application footer"""
        st.markdown("---")
        st.markdown(
            f"<div style='text-align: center; color: #666;'>"
            f"Web Audit Analyzer v{AppConfig.APP_VERSION} | "
            f"Built with Streamlit</div>",
            unsafe_allow_html=True
        )
    
    @staticmethod
    def display_header():
        """Display the main header"""
        st.markdown("""
        <div class="main-header" style="text-align: center; padding: 2rem 0;">
            <h1>Web Audit Tool</h1>
            <p>Comprehensive website analysis for SEO, performance, and security</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_search_interface():
        """Display the search interface"""
        st.markdown('<div class="search-container">', unsafe_allow_html=True)
        
        # URL input with proper label
        url_input = st.text_input(
            label="Website URL",
            placeholder="Enter website URL (e.g., example.com)",
            label_visibility="hidden",
            key="url_input"
        )
        
        # Example domains
        st.markdown("""
        <div class="example-domains">
            Try these examples: 
            <a href="#" onclick="document.querySelector('[data-testid=\"stTextInput\"] input').value='github.com'">github.com</a>
            <a href="#" onclick="document.querySelector('[data-testid=\"stTextInput\"] input').value='stackoverflow.com'">stackoverflow.com</a>
            <a href="#" onclick="document.querySelector('[data-testid=\"stTextInput\"] input').value='google.com'">google.com</a>
        </div>
        """, unsafe_allow_html=True)
        
        # Audit mode selection
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            audit_mode = st.radio(
                "Select Audit Mode",
                ["quick", "comprehensive", "marketing"],
                format_func=lambda x: {
                    "quick": "Quick Audit (Basic checks)",
                    "comprehensive": "Comprehensive Audit (Full analysis)", 
                    "marketing": "Marketing Focus (SEO & Analytics)"
                }[x],
                key="audit_mode",
                index=0
            )
        
        # Audit button
        audit_button = st.button(
            "Start Audit",
            key="audit_button",
            use_container_width=True,
            type="primary"
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return url_input, audit_mode, audit_button
    
    @staticmethod
    def display_loading_progress():
        """Display loading progress for audit"""
        import time
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        steps = [
            "Validating URL...",
            "Analyzing DNS...",
            "Checking SSL/TLS...",
            "Testing Performance...",
            "Analyzing SEO...",
            "Detecting Marketing Tools...",
            "Gathering Ranking Data...",
            "Generating Report..."
        ]
        
        for i, step in enumerate(steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(steps))
            time.sleep(0.5)
        
        progress_bar.empty()
        status_text.empty()
    
    @staticmethod
    def create_metric_card(title, value, status="info"):
        """Create a styled metric card"""
        status_class = f"status-{status}"
        return f"""
        <div class="metric-card {status_class}">
            <h4>{title}</h4>
            <p>{value}</p>
        </div>
        """
    
    @staticmethod
    def display_performance_chart(performance_data):
        """Display performance metrics chart"""
        if not performance_data or 'error' in performance_data:
            st.warning("Performance data not available")
            return
            
        # Create performance gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = performance_data.get('score', 0),
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Performance Score"},
            delta = {'reference': 80},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
