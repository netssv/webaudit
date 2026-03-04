"""
Core UI Components — Google-Inspired Clean Interface
Centered search, simplified layout, quick-tool buttons
"""

import streamlit as st
from datetime import datetime


class CoreUI:
    """Core UI components for the web audit application"""

    @staticmethod
    def display_header():
        """Display centered Google-style header"""
        st.markdown("""
        <div class="app-header">
            <h1>🌐 Web Audit</h1>
            <div class="subtitle">Comprehensive website analysis — SEO, security, email & network diagnostics</div>
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def display_search_interface(show_pills=True):
        """Display the centered search bar with analyze button"""
        # Check for example URL from session state
        example_url = ""
        if hasattr(st.session_state, 'example_url') and st.session_state.example_url:
            example_url = st.session_state.example_url
            del st.session_state.example_url

        col1, col2 = st.columns([5, 1])
        with col1:
            url_input = st.text_input(
                "URL",
                placeholder="Enter domain or URL — e.g. example.com",
                value=example_url,
                label_visibility="collapsed"
            )
        with col2:
            audit_button = st.button(
                "🔍 Analyze",
                type="primary",
                use_container_width=True,
            )

        # Quick-tool labels below search — only on landing page (no results yet)
        if show_pills:
            st.markdown("""
            <div class="quick-tools">
                <span class="quick-tool-btn">⚡ Performance</span>
                <span class="quick-tool-btn">🔍 SEO</span>
                <span class="quick-tool-btn">🔒 Security</span>
                <span class="quick-tool-btn">🌐 DNS</span>
                <span class="quick-tool-btn">🛡️ Blacklist</span>
                <span class="quick-tool-btn">📧 Email</span>
                <span class="quick-tool-btn">🔗 Tools</span>
            </div>
            """, unsafe_allow_html=True)

        return url_input, st.session_state.get('selected_modules', {}), audit_button

    @staticmethod
    def display_loading_progress():
        """Display loading progress for audit"""
        import time
        steps = [
            "🔍 Resolving domain...",
            "⚡ Measuring performance...",
            "🔒 Checking SSL certificate...",
            "🌐 Analyzing DNS records...",
            "📊 Evaluating SEO...",
            "🛡️ Checking blacklists...",
            "📧 Diagnosing email...",
            "🔗 Generating tool links...",
            "✅ Done!"
        ]
        bar = st.progress(0)
        status = st.empty()
        for i, step in enumerate(steps):
            status.text(step)
            bar.progress((i + 1) / len(steps))
            time.sleep(0.25)
        bar.empty()
        status.empty()

    @staticmethod
    def display_sidebar_settings():
        """Sidebar with module toggles"""
        with st.sidebar:
            st.markdown("## ⚙️ Modules")
            st.caption("Toggle which analyses to run")

            if 'selected_modules' not in st.session_state:
                st.session_state.selected_modules = {
                    'performance': True, 'seo_marketing': True,
                    'ssl': True, 'dns': True, 'ranking': True,
                    'blacklist': True, 'email': True, 'tools': True,
                }

            mods = st.session_state.selected_modules

            mods['performance'] = st.checkbox("⚡ Performance", value=mods.get('performance', True), key="m_perf")
            mods['seo_marketing'] = st.checkbox("🔍 SEO & Marketing", value=mods.get('seo_marketing', True), key="m_seo")
            mods['ssl'] = st.checkbox("🔒 Security (SSL)", value=mods.get('ssl', True), key="m_ssl")
            mods['dns'] = st.checkbox("🌐 DNS & WHOIS", value=mods.get('dns', True), key="m_dns")
            mods['ranking'] = st.checkbox("📊 Ranking", value=mods.get('ranking', True), key="m_rank")
            mods['blacklist'] = st.checkbox("🛡️ Blacklist Check", value=mods.get('blacklist', True), key="m_bl")
            mods['email'] = st.checkbox("📧 Email Diagnostics", value=mods.get('email', True), key="m_email")
            mods['tools'] = st.checkbox("🔗 External Tools", value=mods.get('tools', True), key="m_tools")

            st.divider()
            c1, c2 = st.columns(2)
            with c1:
                if st.button("All On", key="all_on", use_container_width=True):
                    for k in mods: mods[k] = True
                    st.rerun()
            with c2:
                if st.button("All Off", key="all_off", use_container_width=True):
                    for k in mods: mods[k] = False
                    st.rerun()

            st.divider()
            active = sum(1 for v in mods.values() if v)
            st.markdown(f"""
            **Web Audit Tool v3.0**  
            *{active}/8 modules active*  
            
            Built by [netssv](https://github.com/netssv)
            """)

    @staticmethod
    def initialize_session_state():
        """Initialize session state variables"""
        defaults = {
            'audit_results': None,
            'audit_in_progress': False,
            'url_input': '',
            'selected_modules': {
                'performance': True, 'seo_marketing': True,
                'ssl': True, 'dns': True, 'ranking': True,
                'blacklist': True, 'email': True, 'tools': True,
            }
        }
        for k, v in defaults.items():
            if k not in st.session_state:
                st.session_state[k] = v

    @staticmethod
    def display_error_message(error_text, error_type="error"):
        """Display standardized error messages"""
        fn = {'error': st.error, 'warning': st.warning, 'info': st.info}.get(error_type, st.write)
        icon = {'error': '❌', 'warning': '⚠️', 'info': 'ℹ️'}.get(error_type, '📝')
        fn(f"{icon} {error_text}")

    @staticmethod
    def display_success_message(success_text):
        st.success(f"✅ {success_text}")
