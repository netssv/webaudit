"""
Core UI Components            <h1 class="main-title" style="
                color: var(--primary-text, #1a1a1a) !important;
                margin: 0;
                font-size: 2.2rem;
                font-weight: 400;
                background: none !important;
                background-color: transparent !important;
                letter-spacing: -0.02em;
            ">Web Audit Tool</h1>ontains core interface components for the web audit application
"""

import streamlit as st
from datetime import datetime

class CoreUI:
    """Core UI components for the web audit application"""
    
    @staticmethod
    def display_header():
        """Display the application header with clean Web 4.0 design"""
        # App header with ultra-compact spacing
        st.markdown("""
        <div class="header-container" style="
            text-align: center;
            padding: 0;
            margin: -2rem 0 0 0;
            border-bottom: 1px solid var(--border-color, #e5e5e5);
        ">
            <h1 class="main-title">Web Audit Tool</h1>
            <p class="main-subtitle">Comprehensive website analysis and optimization insights</p>
        </div>
        
        <style>
            /* Main title styling - will be overridden by dark mode */
            .main-title {
                color: #1a1a1a;
                margin: 0;
                font-size: 2.2rem;
                font-weight: 400;
                background: none !important;
                background-color: transparent !important;
                letter-spacing: -0.02em;
            }
            
            /* Main subtitle styling - will be overridden by dark mode */
            .main-subtitle {
                color: #666666;
                margin: 0;
                font-size: 0.85rem;
                font-weight: 300;
                letter-spacing: 0.01em;
                padding-bottom: 0.5rem;
            }
            
            /* Header container border */
            .header-container {
                border-bottom: 1px solid #e5e5e5;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def display_search_interface():
        """Display the clean search interface without module selection"""
        
        # URL Input Section - Clean Web 4.0 design
        col1, col2 = st.columns([4, 1])
        # Check if an example URL was selected
        example_url = ""
        if hasattr(st.session_state, 'example_url') and st.session_state.example_url:
            example_url = st.session_state.example_url
            # Clear the example URL after using it
            del st.session_state.example_url
        
        with col1:
            url_input = st.text_input(
                "Enter website URL",
                placeholder="https://example.com",
                value=example_url,  # Pre-fill with example URL if selected
                help="Enter the full URL of the website you want to analyze",
                label_visibility="collapsed"
            )
        
        with col2:
            audit_button = st.button(
                "Analyze",
                type="primary",
                use_container_width=True,
                help="Start website analysis"
            )
        
        # Example domains for quick testing
        st.markdown('<div style="text-align: center; margin: 0.5rem 0; padding: 0;"><p style="margin: 0; padding: 0; color: #666; font-size: 0.85rem;">Quick examples: <span style="color: #1976d2; text-decoration: underline; margin: 0 8px;">google.com</span> | <span style="color: #1976d2; text-decoration: underline; margin: 0 8px;">github.com</span> | <span style="color: #1976d2; text-decoration: underline; margin: 0 8px;">stackoverflow.com</span></p></div>', unsafe_allow_html=True)
        
        # Google-style input override - clean and simple
        st.markdown("""
        <style>
        /* Google-style search input */
        .stTextInput > div > div > input, 
        .stTextInput input, 
        [data-testid="stTextInput"] input,
        [data-testid="stTextInput"] > div > div > input {
            border: 1px solid #dadce0 !important;
            background-color: #ffffff !important;
            color: #202124 !important;
            border-radius: 24px !important;
            padding: 12px 16px !important;
            font-size: 16px !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
            box-shadow: none !important;
            font-weight: 400 !important;
        }
        
        .stTextInput > div > div > input:focus, 
        .stTextInput input:focus, 
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextInput"] > div > div > input:focus {
            border-color: #4285f4 !important;
            box-shadow: 0 1px 6px rgba(32,33,36,.28) !important;
            outline: none !important;
        }
        
        .stTextInput > div > div > input:hover, 
        .stTextInput input:hover, 
        [data-testid="stTextInput"] input:hover,
        [data-testid="stTextInput"] > div > div > input:hover {
            border-color: #4285f4 !important;
            box-shadow: 0 1px 6px rgba(32,33,36,.28) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        return url_input, st.session_state.get('selected_modules', {}), audit_button
    
    @staticmethod
    def display_loading_progress():
        """Display loading progress for audit"""
        # Create progress indicators
        progress_steps = [
            "🔍 Analyzing URL structure...",
            "⚡ Testing performance metrics...",
            "🔒 Checking security certificates...",
            "🌐 Resolving DNS records...",
            "📊 Gathering SEO data...",
            "📈 Analyzing ranking factors...",
            "✅ Compiling results..."
        ]
        
        # Show progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Simulate progress through steps
        import time
        for i, step in enumerate(progress_steps):
            status_text.text(step)
            progress_bar.progress((i + 1) / len(progress_steps))
            time.sleep(0.3)  # Small delay for visual effect
        
        status_text.text("🎉 Analysis complete!")
        time.sleep(0.5)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()
    
    @staticmethod
    def display_sidebar_settings():
        """Display sidebar with module controls and theme settings"""
        with st.sidebar:
            # Main Sidebar Title
            st.markdown("## Settings")
            
            # Theme Settings - Using radio buttons instead of buttons
            st.markdown("### Appearance")
            
            # Theme selection with radio buttons (cleaner than buttons)
            current_theme = "Dark" if st.session_state.get('dark_mode', False) else "Light"
            theme_choice = st.radio(
                "Theme",
                options=["Light", "Dark"],
                index=0 if current_theme == "Light" else 1,
                horizontal=True,
                label_visibility="collapsed"
            )
            
            if theme_choice != current_theme:
                st.session_state.dark_mode = (theme_choice == "Dark")
                st.rerun()
            
            st.divider()
            
            # Analysis Modules - Primary feature in sidebar
            st.markdown("### Analysis Modules")
            st.markdown("*Select which analyses to perform*")
            
            # Initialize session state for modules if not exists
            if 'selected_modules' not in st.session_state:
                st.session_state.selected_modules = {
                    'performance': True,
                    'seo_marketing': True,
                    'ssl': True,
                    'dns': True,
                    'ranking': True
                }
            
            # Module checkboxes with clean labels
            st.session_state.selected_modules['performance'] = st.checkbox(
                "Performance Analysis", 
                value=st.session_state.selected_modules.get('performance', True),
                help="Page load times, Core Web Vitals, optimization metrics",
                key="sidebar_module_performance"
            )
            
            st.session_state.selected_modules['seo_marketing'] = st.checkbox(
                "SEO & Marketing", 
                value=st.session_state.selected_modules.get('seo_marketing', True),
                help="Meta tags, schema markup, social media integration",
                key="sidebar_module_seo"
            )
            
            st.session_state.selected_modules['ssl'] = st.checkbox(
                "Security Analysis", 
                value=st.session_state.selected_modules.get('ssl', True),
                help="SSL/TLS certificates, security headers, HTTPS status",
                key="sidebar_module_ssl"
            )
            
            st.session_state.selected_modules['dns'] = st.checkbox(
                "DNS Analysis", 
                value=st.session_state.selected_modules.get('dns', True),
                help="DNS records, WHOIS data, domain configuration",
                key="sidebar_module_dns"
            )
            
            st.session_state.selected_modules['ranking'] = st.checkbox(
                "Ranking Analysis", 
                value=st.session_state.selected_modules.get('ranking', True),
                help="Search visibility, ranking factors, competition analysis",
                key="sidebar_module_ranking"
            )
            
            # Quick action controls 
            st.markdown("**Quick Actions:**")
            
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button("Select All", key="select_all_modules", use_container_width=True):
                    for key in st.session_state.selected_modules:
                        st.session_state.selected_modules[key] = True
                    st.rerun()
            
            with col2:
                if st.button("Clear All", key="clear_all_modules", use_container_width=True):
                    for key in st.session_state.selected_modules:
                        st.session_state.selected_modules[key] = False
                    st.rerun()
            
            st.divider()
            
            # System Information
            st.markdown("### About")
            st.markdown("""
            **Web Audit Tool v2.0**  
            Optimized edition (linux roots)  
            
            **Features:**
            • 96.5% code reduction
            • Web UX design standards
            • Maximum readability
            • Modular architecture
            
            **Active Modules:** {count}/5
            
            **Author:** [Rodrigo Martel](https://github.com/netssv)
            """.format(count=sum(1 for v in st.session_state.selected_modules.values() if v)))
            
            # Footer
            st.markdown("---")
            st.markdown("*Built with Streamlit & Python*")
    
    @staticmethod
    def initialize_session_state():
        """Initialize session state variables"""
        if 'audit_results' not in st.session_state:
            st.session_state.audit_results = None
        if 'audit_in_progress' not in st.session_state:
            st.session_state.audit_in_progress = False
        if 'url_input' not in st.session_state:
            st.session_state.url_input = ""
        if 'dark_mode' not in st.session_state:
            st.session_state.dark_mode = False
        if 'show_raw_ai_data' not in st.session_state:
            st.session_state.show_raw_ai_data = False
        if 'selected_modules' not in st.session_state:
            st.session_state.selected_modules = {
                'dns': True,
                'ssl': True,
                'seo_marketing': True,
                'performance': True,
                'ranking': True
            }
    
    @staticmethod
    def display_error_message(error_text, error_type="error"):
        """Display standardized error messages"""
        if error_type == "error":
            st.error(f"❌ {error_text}")
        elif error_type == "warning":
            st.warning(f"⚠️ {error_text}")
        elif error_type == "info":
            st.info(f"ℹ️ {error_text}")
        else:
            st.write(f"📝 {error_text}")
    
    @staticmethod
    def display_success_message(success_text):
        """Display standardized success messages"""
        st.success(f"✅ {success_text}")
    
    @staticmethod
    def display_metric_card(title, value, delta=None, help_text=None):
        """Display a standardized metric card"""
        st.metric(
            label=title,
            value=value,
            delta=delta,
            help=help_text
        )
