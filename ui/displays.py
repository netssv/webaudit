"""
Display Components Module
Contains all display functions for different analysis sections
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json


def initialize_session_state():
    """Initialize session state variables"""
    if 'audit_results' not in st.session_state:
        st.session_state.audit_results = None
    if 'audit_in_progress' not in st.session_state:
        st.session_state.audit_in_progress = False
    if 'url_input' not in st.session_state:
        st.session_state.url_input = ""
    if 'show_raw_ai_data' not in st.session_state:
        st.session_state.show_raw_ai_data = False


def display_header():
    """Display the application header"""
    st.markdown("""
    <div class="header-container" style="
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    ">
        <h1 style="
            color: #ffffff !important;
            margin: 0;
                font-size: 48px;
                font-weight: 700;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            ">🕸️ Web Audit Tool</h1>
            <p style="
                color: #ffffff !important;
                margin: 10px 0 0 0;
                font-size: 18px;
                opacity: 0.9;
            ">Comprehensive website analysis and optimization insights</p>
        </div>
        """, unsafe_allow_html=True)


def display_search_interface():
    """Display the search interface and controls"""
    st.markdown("### 🔍 Website Analysis")
    
    # URL input
    url = st.text_input(
        "Enter website URL:",
        value=st.session_state.url_input,
        placeholder="https://example.com",
        help="Enter the full URL including https://",
        key="url_input_field"
    )
    
    # Update session state
    if url != st.session_state.url_input:
        st.session_state.url_input = url


def display_loading_progress():
    """Display loading progress for audit"""
    st.markdown("### ⏳ Analysis in Progress")
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulate progress steps
    steps = [
        "Initializing analysis...",
        "Checking SSL certificate...",
        "Analyzing DNS configuration...",
        "Testing performance metrics...",
        "Scanning SEO elements...",
        "Evaluating ranking factors...",
        "Generating comprehensive report..."
    ]
    
    for i, step in enumerate(steps):
        status_text.text(step)
        progress_bar.progress((i + 1) / len(steps))
        
    status_text.text("✅ Analysis complete!")
    return progress_bar, status_text


def display_audit_results(results):
    """Display main audit results with tabs"""
    if not results:
        st.warning("⚠️ No audit results to display")
        return
    
    st.markdown("### 📊 Analysis Results")
    
    # Create tabs based on available data
    available_tabs = []
    tab_data = {}
    
    if "performance" in results and results["performance"]:
        available_tabs.append("⚡ Performance")
        tab_data["⚡ Performance"] = results["performance"]
    
    if "seo_marketing" in results and results["seo_marketing"]:
        available_tabs.append("🔍 SEO Analysis")
        tab_data["🔍 SEO Analysis"] = results["seo_marketing"]
    
    if "ssl" in results and results["ssl"]:
        available_tabs.append("🔒 Security")
        tab_data["🔒 Security"] = results["ssl"]
    
    if "dns" in results and results["dns"]:
        available_tabs.append("🌐 DNS")
        tab_data["🌐 DNS"] = results["dns"]
    
    if "ranking" in results and results["ranking"]:
        available_tabs.append("📈 Ranking")
        tab_data["📈 Ranking"] = results["ranking"]
    
    # Add general tabs
    available_tabs.extend(["📋 Technical", "📊 Dashboard", "🤖 AI Analysis", "📄 Raw Data"])
    
    if not available_tabs:
        st.error("❌ No valid data found in audit results")
        return
    
    # Create and display tabs
    tabs = st.tabs(available_tabs)
    
    for i, tab_name in enumerate(available_tabs):
        with tabs[i]:
            if tab_name == "⚡ Performance" and "⚡ Performance" in tab_data:
                display_performance_analysis(tab_data["⚡ Performance"])
            elif tab_name == "🔍 SEO Analysis" and "🔍 SEO Analysis" in tab_data:
                display_seo_marketing_analysis(tab_data["🔍 SEO Analysis"])
            elif tab_name == "🔒 Security" and "🔒 Security" in tab_data:
                display_security_analysis(tab_data["🔒 Security"])
            elif tab_name == "🌐 DNS" and "🌐 DNS" in tab_data:
                display_dns_analysis(tab_data["🌐 DNS"])
            elif tab_name == "📈 Ranking" and "📈 Ranking" in tab_data:
                display_ranking_analysis(tab_data["📈 Ranking"])
            elif tab_name == "📋 Technical":
                display_technical_analysis(results)
            elif tab_name == "📊 Dashboard":
                display_metrics_dashboard(results)
            elif tab_name == "🤖 AI Analysis":
                from .ai_components import AIAnalysisComponents
                AIAnalysisComponents.display_ai_analysis(results)
            elif tab_name == "📄 Raw Data":
                from .ai_components import AIAnalysisComponents
                AIAnalysisComponents.display_raw_data_only(results)


def display_performance_analysis(performance_data):
    """Display performance analysis with charts and metrics"""
    if not performance_data:
        st.warning("⚠️ No performance data available")
        return
    
    st.markdown("### ⚡ Performance Analysis")
    
    # Performance metrics
    if "metrics" in performance_data:
        metrics = performance_data["metrics"]
        
        # Core Web Vitals
        st.markdown("#### 📊 Core Web Vitals")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lcp = metrics.get("largest_contentful_paint", "N/A")
            st.metric("LCP (Largest Contentful Paint)", f"{lcp}s" if lcp != "N/A" else "N/A")
        
        with col2:
            fid = metrics.get("first_input_delay", "N/A")
            st.metric("FID (First Input Delay)", f"{fid}ms" if fid != "N/A" else "N/A")
        
        with col3:
            cls = metrics.get("cumulative_layout_shift", "N/A")
            st.metric("CLS (Cumulative Layout Shift)", str(cls) if cls != "N/A" else "N/A")
        
        # Additional metrics
        st.markdown("#### 🚀 Additional Metrics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            load_time = metrics.get("page_load_time", "N/A")
            st.metric("Page Load Time", f"{load_time}s" if load_time != "N/A" else "N/A")
        
        with col2:
            ttfb = metrics.get("time_to_first_byte", "N/A")
            st.metric("TTFB", f"{ttfb}ms" if ttfb != "N/A" else "N/A")
        
        with col3:
            dom_content = metrics.get("dom_content_loaded", "N/A")
            st.metric("DOM Content Loaded", f"{dom_content}s" if dom_content != "N/A" else "N/A")
        
        with col4:
            page_size = metrics.get("page_size", "N/A")
            if page_size != "N/A":
                try:
                    size_mb = float(page_size) / (1024 * 1024)
                    st.metric("Page Size", f"{size_mb:.2f} MB")
                except:
                    st.metric("Page Size", str(page_size))
            else:
                st.metric("Page Size", "N/A")
    
    # Performance score
    if "lighthouse_score" in performance_data:
        score = performance_data["lighthouse_score"]
        st.markdown("#### 📈 Performance Score")
        
        # Create gauge chart for score
        if isinstance(score, (int, float)):
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                title={'text': "Lighthouse Performance Score"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen" if score >= 80 else "orange" if score >= 50 else "red"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 80], 'color': "gray"},
                        {'range': [80, 100], 'color': "lightgreen"}
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
        else:
            st.metric("Performance Score", str(score))
    
    # Performance issues
    if "issues" in performance_data and performance_data["issues"]:
        st.markdown("#### ⚠️ Performance Issues")
        for i, issue in enumerate(performance_data["issues"], 1):
            if isinstance(issue, dict):
                st.error(f"{i}. {issue.get('description', str(issue))}")
            else:
                st.error(f"{i}. {str(issue)}")


def display_seo_marketing_analysis(seo_data):
    """Display SEO analysis with comprehensive or basic view"""
    if not seo_data:
        st.warning("⚠️ No SEO data available")
        return
    
    # Check if this is comprehensive SEO data
    if any(key in seo_data for key in ['meta_tags', 'headings', 'images', 'internal_links', 'external_links']):
        display_comprehensive_seo_analysis(seo_data)
    else:
        display_basic_seo_analysis(seo_data)


def display_comprehensive_seo_analysis(seo_data):
    """Display comprehensive SEO analysis with detailed breakdown"""
    st.markdown("### 🔍 Comprehensive SEO Analysis")
    
    # Meta Information
    st.markdown("#### 📝 Meta Information")
    col1, col2 = st.columns(2)
    
    with col1:
        # Title analysis
        title = seo_data.get("title", "Not found")
        title_length = len(title) if title != "Not found" else 0
        
        st.markdown("**Page Title:**")
        if title != "Not found":
            title_status = "✅" if 30 <= title_length <= 60 else "⚠️"
            st.write(f"{title_status} {title}")
            st.caption(f"Length: {title_length} characters {'(Good)' if 30 <= title_length <= 60 else '(Too short)' if title_length < 30 else '(Too long)'}")
        else:
            st.error("❌ No title tag found")
    
    with col2:
        # Meta description analysis
        meta_desc = seo_data.get("meta_description", "Not found")
        desc_length = len(meta_desc) if meta_desc != "Not found" else 0
        
        st.markdown("**Meta Description:**")
        if meta_desc != "Not found":
            desc_status = "✅" if 120 <= desc_length <= 160 else "⚠️"
            st.write(f"{desc_status} {meta_desc}")
            st.caption(f"Length: {desc_length} characters {'(Good)' if 120 <= desc_length <= 160 else '(Too short)' if desc_length < 120 else '(Too long)'}")
        else:
            st.error("❌ No meta description found")

    # Marketing tools (if any)
    marketing = seo_data.get("marketing_tools", [])
    if marketing:
        st.markdown("#### 📣 Marketing & Tracking Tools Detected")
        for tool in marketing:
            name = tool.get("name", "Unknown")
            evidence = tool.get("evidence", "No evidence")
            confidence = tool.get("confidence", "unknown")
            st.markdown(f"- **{name}** — _{evidence}_ — Confidence: **{confidence}**")


def display_basic_seo_analysis(seo_data):
    """Display basic SEO analysis for simple data structure"""
    st.markdown("### 🔍 SEO Analysis")
    
    # Basic SEO elements
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📝 Basic Elements")
        
        title = seo_data.get("title", "Not found")
        if title != "Not found":
            st.success(f"**Title:** {title}")
            st.caption(f"Length: {len(title)} characters")
        else:
            st.error("❌ Title tag missing")
        
        meta_desc = seo_data.get("meta_description", "Not found")
        if meta_desc != "Not found":
            st.success(f"**Meta Description:** {meta_desc}")
            st.caption(f"Length: {len(meta_desc)} characters")
        else:
            st.error("❌ Meta description missing")
    
    with col2:
        st.markdown("#### 📊 Quick Stats")
        
        # Keywords
        keywords = seo_data.get("keywords", [])
        if keywords:
            st.metric("Keywords Found", len(keywords))
            if len(keywords) > 0:
                top_keywords = keywords[:5] if isinstance(keywords, list) else [str(keywords)]
                st.write("**Top Keywords:**")
                for keyword in top_keywords:
                    st.write(f"• {keyword}")
        
        # H1 tags
        h1_tags = seo_data.get("h1_tags", 0)
        st.metric("H1 Tags", h1_tags)
        
        if h1_tags == 0:
            st.warning("⚠️ No H1 tags found")
        elif h1_tags > 1:
            st.warning("⚠️ Multiple H1 tags found")
        else:
            st.success("✅ Single H1 tag found")

    # Basic marketing tools display (if present)
    marketing = seo_data.get("marketing_tools", [])
    if marketing:
        render_marketing_tools(marketing)


def render_marketing_tools(marketing):
    """Render marketing/tracking tools with UX-focused badges and evidence."""
    if not marketing:
        return

    st.markdown("#### 📣 Marketing & Tracking Tools Detected")
    for tool in marketing:
        name = tool.get("name", "Unknown")
        evidence = tool.get("evidence", "No evidence")
        confidence = (tool.get("confidence") or "unknown").lower()

        # Visual treatment by confidence
        if confidence == "high":
            st.success(f"✅ {name} — {confidence.upper()}")
            st.caption(evidence)
        elif confidence == "medium":
            st.info(f"⚠️ {name} — {confidence}")
            st.caption(evidence)
        else:
            st.warning(f"❕ {name} — {confidence}")
            st.caption(evidence)

        # Small separator for readability
        st.write("---")


def display_security_analysis(ssl_data):
    """Display SSL/Security analysis"""
    if not ssl_data:
        st.warning("⚠️ No security data available")
        return
    
    st.markdown("### 🔒 Security Analysis")
    
    # SSL Status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ssl_valid = ssl_data.get("ssl_valid", False)
        if ssl_valid:
            st.success("✅ SSL Certificate Valid")
        else:
            st.error("❌ SSL Certificate Invalid")
    
    with col2:
        ssl_grade = ssl_data.get("ssl_grade", "N/A")
        if ssl_grade != "N/A":
            grade_color = "🟢" if ssl_grade in ["A+", "A"] else "🟡" if ssl_grade == "B" else "🔴"
            st.metric("SSL Grade", f"{grade_color} {ssl_grade}")
        else:
            st.metric("SSL Grade", "Not Available")
    
    with col3:
        cert_expiry = ssl_data.get("certificate_expiry", "N/A")
        if cert_expiry != "N/A":
            st.metric("Certificate Expires", cert_expiry)
        else:
            st.metric("Certificate Expires", "Unknown")


def display_dns_analysis(dns_data):
    """Display DNS analysis"""
    if not dns_data:
        st.warning("⚠️ No DNS data available")
        return
    
    st.markdown("### 🌐 DNS Analysis")
    
    # DNS Records Overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        a_records = dns_data.get("a_records", [])
        st.metric("A Records", len(a_records) if isinstance(a_records, list) else a_records)
    
    with col2:
        mx_records = dns_data.get("mx_records", [])
        st.metric("MX Records", len(mx_records) if isinstance(mx_records, list) else mx_records)
    
    with col3:
        ns_records = dns_data.get("ns_records", [])
        st.metric("NS Records", len(ns_records) if isinstance(ns_records, list) else ns_records)
    
    with col4:
        cname_records = dns_data.get("cname_records", [])
        st.metric("CNAME Records", len(cname_records) if isinstance(cname_records, list) else cname_records)


def display_ranking_analysis(ranking_data):
    """Display ranking analysis"""
    if not ranking_data:
        st.warning("⚠️ No ranking data available")
        return
    
    st.markdown("### 📈 Ranking Analysis")
    
    # Authority Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        domain_authority = ranking_data.get("domain_authority", "N/A")
        if domain_authority != "N/A":
            da_color = "🟢" if domain_authority >= 50 else "🟡" if domain_authority >= 30 else "🔴"
            st.metric("Domain Authority", f"{da_color} {domain_authority}")
        else:
            st.metric("Domain Authority", "N/A")
    
    with col2:
        page_authority = ranking_data.get("page_authority", "N/A")
        if page_authority != "N/A":
            pa_color = "🟢" if page_authority >= 40 else "🟡" if page_authority >= 20 else "🔴"
            st.metric("Page Authority", f"{pa_color} {page_authority}")
        else:
            st.metric("Page Authority", "N/A")
    
    with col3:
        backlinks = ranking_data.get("backlinks", "N/A")
        st.metric("Backlinks", backlinks)
    
    with col4:
        referring_domains = ranking_data.get("referring_domains", "N/A")
        st.metric("Referring Domains", referring_domains)


def display_technical_analysis(audit_data):
    """Display technical analysis summary"""
    st.markdown("### 📋 Technical Analysis")
    
    if not audit_data:
        st.warning("⚠️ No technical data available")
        return
    
    # Summary of all available data
    st.markdown("#### 📊 Available Analysis Modules")
    
    modules = {
        "Performance": "performance" in audit_data and audit_data["performance"],
        "SEO": "seo_marketing" in audit_data and audit_data["seo_marketing"],
        "Security": "ssl" in audit_data and audit_data["ssl"],
        "DNS": "dns" in audit_data and audit_data["dns"],
        "Ranking": "ranking" in audit_data and audit_data["ranking"]
    }
    
    for module, available in modules.items():
        if available:
            st.success(f"✅ {module} Analysis - Data Available")
        else:
            st.error(f"❌ {module} Analysis - No Data")


def display_metrics_dashboard(audit_data):
    """Display comprehensive metrics dashboard"""
    st.markdown("### 📊 Metrics Dashboard")
    
    if not audit_data:
        st.warning("⚠️ No data available for dashboard")
        return
    
    # Collect all metrics
    metrics = {}
    
    # Performance metrics
    if "performance" in audit_data and audit_data["performance"]:
        perf = audit_data["performance"]
        if "metrics" in perf:
            perf_metrics = perf["metrics"]
            metrics.update({
                "Page Load Time": f"{perf_metrics.get('page_load_time', 'N/A')}s",
                "TTFB": f"{perf_metrics.get('time_to_first_byte', 'N/A')}ms",
                "LCP": f"{perf_metrics.get('largest_contentful_paint', 'N/A')}s",
                "Performance Score": perf.get("lighthouse_score", "N/A")
            })
    
    # SEO metrics
    if "seo_marketing" in audit_data and audit_data["seo_marketing"]:
        seo = audit_data["seo_marketing"]
        title_length = len(seo.get("title", "")) if seo.get("title") else 0
        desc_length = len(seo.get("meta_description", "")) if seo.get("meta_description") else 0
        
        metrics.update({
            "Title Length": f"{title_length} chars",
            "Meta Desc Length": f"{desc_length} chars",
            "H1 Tags": seo.get("h1_tags", 0),
            "Keywords": len(seo.get("keywords", [])) if isinstance(seo.get("keywords"), list) else seo.get("keywords", "N/A")
        })
    
    # Security metrics
    if "ssl" in audit_data and audit_data["ssl"]:
        ssl = audit_data["ssl"]
        metrics.update({
            "SSL Valid": "✅" if ssl.get("ssl_valid") else "❌",
            "SSL Grade": ssl.get("ssl_grade", "N/A")
        })
    
    # DNS metrics
    if "dns" in audit_data and audit_data["dns"]:
        dns = audit_data["dns"]
        metrics.update({
            "A Records": len(dns.get("a_records", [])) if isinstance(dns.get("a_records"), list) else dns.get("a_records", "N/A"),
            "MX Records": len(dns.get("mx_records", [])) if isinstance(dns.get("mx_records"), list) else dns.get("mx_records", "N/A")
        })
    
    # Display metrics in a grid
    cols = st.columns(4)
    for i, (key, value) in enumerate(metrics.items()):
        with cols[i % 4]:
            st.metric(key, value)
