"""
AI Analysis Components Module
Contains all AI analysis and summary generation components
"""

import streamlit as st
import json
from datetime import datetime

class AIAnalysisComponents:
    """AI Analysis and summary components for the web audit application"""
    
    @staticmethod
    def generate_summary_for_chatgpt(audit_data):
        """Generate a comprehensive but concise summary for ChatGPT analysis"""
        if not audit_data:
            return "No audit data available for analysis."
        
        summary_parts = []
        
        # Website basic info
        url = audit_data.get('url', 'Unknown URL')
        summary_parts.append(f"Website: {url}")
        
        # Performance Analysis
        if 'performance' in audit_data and audit_data['performance']:
            perf = audit_data['performance']
            if isinstance(perf, dict) and 'error' not in perf:
                response_time = perf.get('response_time', 'N/A')
                status_code = perf.get('status_code', 'N/A')
                page_size = perf.get('page_size', 'N/A')
                
                summary_parts.append(f"Performance: {response_time}ms response, {status_code} status, {page_size}B size")
                
                # Add metrics if available
                if 'metrics' in perf:
                    metrics = perf['metrics']
                    lcp = metrics.get('largest_contentful_paint', 'N/A')
                    fid = metrics.get('first_input_delay', 'N/A')
                    cls = metrics.get('cumulative_layout_shift', 'N/A')
                    if any(x != 'N/A' for x in [lcp, fid, cls]):
                        summary_parts.append(f"Core Vitals: LCP {lcp}s, FID {fid}ms, CLS {cls}")
        
        # SEO Analysis
        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']
            if isinstance(seo, dict) and 'error' not in seo:
                # Basic SEO elements with safe string handling
                title = seo.get('title', 'Missing')
                meta_desc = seo.get('meta_description', 'Missing')
                
                # Safely handle None values
                title_text = str(title)[:50] if title else 'Missing'
                desc_text = str(meta_desc)[:50] if meta_desc else 'Missing'
                
                summary_parts.append(f"SEO: Title: {title_text}... Description: {desc_text}...")
                
                # SEO score if available
                if 'overall_score' in seo:
                    score = seo.get('overall_score', 0)
                    summary_parts.append(f"SEO Score: {score}%")
                elif 'seo_score' in seo:
                    score = seo.get('seo_score', 0)
                    summary_parts.append(f"SEO Score: {score}/100")
                
                # Social media presence
                social_links = seo.get('social_media_links', {})
                if social_links:
                    platforms = list(social_links.keys())[:3]  # First 3 platforms
                    summary_parts.append(f"Social: {', '.join(platforms)}")
        
        # SSL/Security Analysis
        if 'ssl' in audit_data and audit_data['ssl']:
            ssl = audit_data['ssl']
            if isinstance(ssl, dict) and 'error' not in ssl:
                ssl_valid = ssl.get('ssl_valid', False)
                ssl_grade = ssl.get('ssl_grade', 'N/A')
                ssl_status = "Valid" if ssl_valid else "Invalid"
                summary_parts.append(f"Security: SSL {ssl_status}, Grade {ssl_grade}")
        
        # DNS Analysis
        if 'dns' in audit_data and audit_data['dns']:
            dns = audit_data['dns']
            if isinstance(dns, dict) and 'error' not in dns:
                a_records = len(dns.get('a_records', [])) if isinstance(dns.get('a_records', []), list) else dns.get('a_records', 0)
                mx_records = len(dns.get('mx_records', [])) if isinstance(dns.get('mx_records', []), list) else dns.get('mx_records', 0)
                summary_parts.append(f"DNS: {a_records} A records, {mx_records} MX records")
        
        # Ranking Analysis
        if 'ranking' in audit_data and audit_data['ranking']:
            ranking = audit_data['ranking']
            if isinstance(ranking, dict) and 'error' not in ranking:
                da = ranking.get('domain_authority', 'N/A')
                pa = ranking.get('page_authority', 'N/A')
                backlinks = ranking.get('backlinks', 'N/A')
                summary_parts.append(f"Authority: DA {da}, PA {pa}, {backlinks} backlinks")
        
        # Join all parts
        if summary_parts:
            final_summary = " | ".join(summary_parts)
            
            # Truncate if too long (keep under 1000 chars for URL efficiency)
            if len(final_summary) > 1000:
                final_summary = final_summary[:997] + "..."
            
            return final_summary
        else:
            return "Basic website audit completed. Limited data available for analysis."
    
    @staticmethod
    def display_ai_analysis(audit_data):
        """Display AI analysis section with ChatGPT integration"""
        st.markdown("### 🤖 AI Analysis")
        
        if not audit_data:
            st.warning("⚠️ No audit data available for AI analysis")
            return
        
        # Generate summary
        summary = AIAnalysisComponents.generate_summary_for_chatgpt(audit_data)
        
        # Display summary section
        st.markdown("#### 📋 Analysis Summary")
        
        # Show summary in an expandable section
        with st.expander("View Generated Summary", expanded=False):
            st.write(summary)
            
            # Copy to clipboard functionality
            if st.button("📋 Copy Summary", help="Copy summary to clipboard", key="copy_ai_summary"):
                # Note: This creates a text area that users can manually copy from
                st.text_area("Copy this text:", value=summary, height=100, key="copy_summary")
        
        # ChatGPT Integration Section
        st.markdown("#### 🧠 Get AI Insights")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown("""
            <div style="
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                border-left: 4px solid #0969da;
                margin: 10px 0;
                color: #1a1a1a;
            ">
                <strong>🔗 Analyze with ChatGPT</strong><br>
                Click the button below to open ChatGPT with your website analysis summary.
                Get AI-powered insights, recommendations, and optimization suggestions.
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Create ChatGPT URL with pre-filled prompt
            chatgpt_prompt = f"Please analyze this website audit data and provide insights, recommendations, and optimization suggestions: {summary}"
            
            # URL encode the prompt
            import urllib.parse
            encoded_prompt = urllib.parse.quote(chatgpt_prompt)
            chatgpt_url = f"https://chat.openai.com/?q={encoded_prompt}"
            
            # Create a clickable button/link
            st.markdown(f"""
            <a href="{chatgpt_url}" target="_blank" style="text-decoration: none;">
                <button style="
                    background: linear-gradient(135deg, #10a37f 0%, #1a7f5f 100%);
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-weight: 600;
                    width: 100%;
                    font-size: 14px;
                    box-shadow: 0 2px 4px rgba(16, 163, 127, 0.2);
                ">
                    🚀 Analyze with ChatGPT
                </button>
            </a>
            """, unsafe_allow_html=True)
        
        # Alternative analysis options
        st.markdown("#### 🔧 Analysis Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Performance Focus", help="Analyze performance metrics in detail", key="ai_performance_focus"):
                perf_summary = AIAnalysisComponents._generate_performance_focused_summary(audit_data)
                st.text_area("Performance Analysis Summary:", value=perf_summary, height=150, key="perf_analysis_summary")
        
        with col2:
            if st.button("🔍 SEO Focus", help="Analyze SEO and marketing aspects", key="ai_seo_focus"):
                seo_summary = AIAnalysisComponents._generate_seo_focused_summary(audit_data)
                st.text_area("SEO Analysis Summary:", value=seo_summary, height=150, key="seo_analysis_summary")
        
        with col3:
            if st.button("🔒 Security Focus", help="Analyze security and technical aspects", key="ai_security_focus"):
                security_summary = AIAnalysisComponents._generate_security_focused_summary(audit_data)
                st.text_area("Security Analysis Summary:", value=security_summary, height=150, key="security_analysis_summary")
        
        # Raw data toggle
        st.markdown("#### 🗂️ Raw Data")
        
        show_raw = st.checkbox("Show raw audit data", value=False, key="show_raw_data_ai")
        
        if show_raw:
            AIAnalysisComponents.display_raw_data_only(audit_data)
    
    @staticmethod
    def display_raw_data_only(audit_data):
        """Display raw audit data in a formatted way"""
        st.markdown("### 📄 Raw Data")
        
        if not audit_data:
            st.warning("⚠️ No raw data available")
            return
        
        # Display raw data in expandable sections
        for section, data in audit_data.items():
            if data and section != 'url':
                with st.expander(f"{section.replace('_', ' ').title()} Data", expanded=False):
                    if isinstance(data, dict):
                        st.json(data)
                    else:
                        st.write(data)
        
        # Download raw data option with improved UI
        st.markdown("---")
        st.markdown("#### 📥 Export Options")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Generate truly unique keys using session ID and timestamp
            import time
            session_id = getattr(st.session_state, 'session_id', id(st.session_state))
            unique_suffix = f"{session_id}_{int(time.time() * 1000000) % 1000000}"
            download_key = f"download_raw_data_json_{hash(str(audit_data))}_{unique_suffix}"
            
            if st.button("💾 Download as JSON", key=download_key, type="primary", use_container_width=True):
                json_data = json.dumps(audit_data, indent=2, default=str)
                download_file_key = f"download_json_file_{hash(str(audit_data))}_{unique_suffix}"
                st.download_button(
                    label="📥 Download JSON File",
                    data=json_data,
                    file_name=f"audit_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    key=download_file_key,
                    use_container_width=True
                )
        
        with col2:
            # Copy to clipboard functionality
            copy_key = f"copy_raw_data_{hash(str(audit_data))}_{unique_suffix}"
            if st.button("📋 Copy to Clipboard", key=copy_key, use_container_width=True):
                json_data = json.dumps(audit_data, indent=2, default=str)
                st.code(json_data[:500] + "..." if len(json_data) > 500 else json_data, language="json")
                st.success("✅ Data preview shown above. Use browser copy function to copy the JSON data.")
    
    @staticmethod
    def _generate_performance_focused_summary(audit_data):
        """Generate a performance-focused summary"""
        if not audit_data or 'performance' not in audit_data:
            return "No performance data available for analysis."
        
        perf = audit_data['performance']
        if not isinstance(perf, dict) or 'error' in perf:
            return "Performance analysis failed or returned errors."
        
        summary_parts = [
            f"URL: {audit_data.get('url', 'Unknown')}",
            f"Response Time: {perf.get('response_time', 'N/A')}ms",
            f"Status Code: {perf.get('status_code', 'N/A')}",
            f"Page Size: {perf.get('page_size', 'N/A')} bytes"
        ]
        
        # Add metrics if available
        if 'metrics' in perf:
            metrics = perf['metrics']
            summary_parts.extend([
                f"LCP: {metrics.get('largest_contentful_paint', 'N/A')}s",
                f"FID: {metrics.get('first_input_delay', 'N/A')}ms",
                f"CLS: {metrics.get('cumulative_layout_shift', 'N/A')}"
            ])
        
        # Add server info if available
        if 'server_info' in perf:
            server_info = perf['server_info']
            summary_parts.append(f"Server: {server_info.get('server', 'Unknown')}")
        
        return " | ".join(summary_parts)
    
    @staticmethod
    def _generate_seo_focused_summary(audit_data):
        """Generate an SEO-focused summary"""
        if not audit_data or 'seo_marketing' not in audit_data:
            return "No SEO data available for analysis."
        
        seo = audit_data['seo_marketing']
        if not isinstance(seo, dict) or 'error' in seo:
            return "SEO analysis failed or returned errors."
        
        summary_parts = [
            f"URL: {audit_data.get('url', 'Unknown')}",
            f"Title: {seo.get('title', 'Missing')}",
            f"Meta Description: {seo.get('meta_description', 'Missing')}"
        ]
        
        # Add score if available
        if 'overall_score' in seo:
            summary_parts.append(f"SEO Score: {seo['overall_score']}%")
        elif 'seo_score' in seo:
            summary_parts.append(f"SEO Score: {seo['seo_score']}/100")
        
        # Add social media
        social_links = seo.get('social_media_links', {})
        if social_links:
            platforms = list(social_links.keys())
            summary_parts.append(f"Social Platforms: {', '.join(platforms)}")
        
        # Add marketing tools
        marketing_tools = seo.get('marketing_tools', [])
        if marketing_tools:
            summary_parts.append(f"Marketing Tools: {', '.join(marketing_tools)}")
        
        return " | ".join(summary_parts)
    
    @staticmethod
    def _generate_security_focused_summary(audit_data):
        """Generate a security-focused summary"""
        summary_parts = [f"URL: {audit_data.get('url', 'Unknown')}"]
        
        # SSL Analysis
        if 'ssl' in audit_data and audit_data['ssl']:
            ssl = audit_data['ssl']
            if isinstance(ssl, dict) and 'error' not in ssl:
                ssl_valid = ssl.get('ssl_valid', False)
                ssl_grade = ssl.get('ssl_grade', 'N/A')
                summary_parts.extend([
                    f"SSL Valid: {ssl_valid}",
                    f"SSL Grade: {ssl_grade}"
                ])
        
        # DNS Security
        if 'dns' in audit_data and audit_data['dns']:
            dns = audit_data['dns']
            if isinstance(dns, dict) and 'error' not in dns:
                ns_records = dns.get('ns_records', [])
                mx_records = dns.get('mx_records', [])
                summary_parts.extend([
                    f"NS Records: {len(ns_records) if isinstance(ns_records, list) else ns_records}",
                    f"MX Records: {len(mx_records) if isinstance(mx_records, list) else mx_records}"
                ])
        
        # Performance security aspects
        if 'performance' in audit_data and audit_data['performance']:
            perf = audit_data['performance']
            if isinstance(perf, dict) and 'error' not in perf:
                status_code = perf.get('status_code', 'N/A')
                summary_parts.append(f"HTTP Status: {status_code}")
        
        return " | ".join(summary_parts)
