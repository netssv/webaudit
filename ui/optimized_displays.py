"""
Optimized Display Components Module
Streamlined display functions using shared components to minimize code duplication
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
from utils.shared_components import SharedUIComponents, DataValidation

class OptimizedDisplays:
    """Optimized display components with minimal code duplication"""
    
    @staticmethod
    def display_audit_results(results):
        """Display main audit results with tabs"""
        if not results:
            st.warning("⚠️ No audit results to display")
            return
        
        st.markdown("### 📊 Analysis Results")
        
        # Work with flattened results structure for better compatibility
        audit_data = results
        
        # Create tabs based on available data
        available_tabs = []
        tab_data = {}
        
        # Tab mapping with emojis and data keys
        tab_mapping = {
            "performance": ("⚡ Performance", OptimizedDisplays.display_performance_analysis),
            "seo_marketing": ("🔍 SEO Analysis", OptimizedDisplays.display_seo_marketing_analysis),
            "ssl": ("🔒 Security", OptimizedDisplays.display_security_analysis),
            "dns": ("🌐 DNS", OptimizedDisplays.display_dns_analysis),
            "ranking": ("📈 Ranking", OptimizedDisplays.display_ranking_analysis)
        }
        
        # Build available tabs based on actual audit data
        for key, (tab_name, display_func) in tab_mapping.items():
            # Special handling for performance - include even if it has errors
            if key == "performance" and key in audit_data:
                available_tabs.append(tab_name)
                tab_data[tab_name] = (audit_data[key], display_func)
            elif key != "performance" and key in audit_data and audit_data[key]:
                available_tabs.append(tab_name)
                tab_data[tab_name] = (audit_data[key], display_func)
        
        # Add additional tabs
        available_tabs.extend(["📋 Technical", "📊 Dashboard", "🤖 AI Analysis", "📄 Raw Data"])
        
        if not available_tabs:
            st.error("❌ No valid data found in audit results")
            return
        
        # Create and display tabs
        tabs = st.tabs(available_tabs)
        
        for i, tab_name in enumerate(available_tabs):
            with tabs[i]:
                if tab_name in tab_data:
                    data, display_func = tab_data[tab_name]
                    display_func(data)
                elif tab_name == "📋 Technical":
                    OptimizedDisplays.display_technical_analysis(results)
                elif tab_name == "📊 Dashboard":
                    OptimizedDisplays.display_metrics_dashboard(results)
                elif tab_name == "🤖 AI Analysis":
                    from ui.ai_components import AIAnalysisComponents
                    AIAnalysisComponents.display_ai_analysis(results)
                elif tab_name == "📄 Raw Data":
                    from ui.ai_components import AIAnalysisComponents
                    AIAnalysisComponents.display_raw_data_only(results)
    
    @staticmethod
    def display_performance_analysis(performance_data):
        """Optimized performance analysis display"""
        # Special handling for performance data - show it even if there are errors
        if not performance_data:
            SharedUIComponents.display_no_data_warning("Performance")
            return
        
        st.markdown("### ⚡ Performance Analysis")
        
        # Show error message if there's an error but continue with available data
        if isinstance(performance_data, dict) and 'error' in performance_data:
            st.warning(f"⚠️ Performance analysis encountered an issue: {performance_data['error']}")
            # Still try to show any available data
        
        # Display the actual performance data structure we're receiving
        st.markdown("#### 🎯 Core Performance Metrics")
        
        # Create metrics from the actual data structure
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            response_time = performance_data.get('response_time', 0)
            if response_time:
                st.metric(
                    label="Server Response (TTFB)", 
                    value=f"{response_time:.0f} ms",
                    help="Time to First Byte - actual server response time"
                )
        
        with col2:
            total_load_time = performance_data.get('total_load_time', 0)
            if total_load_time:
                st.metric(
                    label="Total Load Time", 
                    value=f"{total_load_time:.0f} ms",
                    help="Complete download time including all content"
                )
        
        with col3:
            page_size = performance_data.get('page_size', 0)
            if page_size:
                size_kb = page_size / 1024
                st.metric(
                    label="Page Size", 
                    value=f"{size_kb:.1f} KB",
                    help="Total size of the webpage"
                )
        
        with col4:
            status_code = performance_data.get('status_code', 'N/A')
            status_color = "🟢" if status_code == 200 else "🟡" if str(status_code).startswith('3') else "🔴"
            st.metric(
                label="Status Code", 
                value=f"{status_color} {status_code}",
                help="HTTP response status code"
            )
        
        with col5:
            redirect_count = performance_data.get('redirect_count', 0)
            redirect_color = "🟢" if redirect_count <= 1 else "🟡" if redirect_count <= 3 else "🔴"
            st.metric(
                label="Redirects", 
                value=f"{redirect_color} {redirect_count}",
                help="Number of HTTP redirects"
            )
        
        # Server Information
        if 'server_info' in performance_data:
            st.markdown("#### 🖥️ Server Information")
            server_info = performance_data['server_info']
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**Server:** {server_info.get('server', 'Unknown')}")
            with col2:
                st.info(f"**Content Type:** {server_info.get('content_type', 'Unknown')}")
            with col3:
                st.info(f"**Powered By:** {server_info.get('powered_by', 'Unknown')}")
        
        # Compression and Caching
        st.markdown("#### 🗜️ Optimization Details")
        col1, col2 = st.columns(2)
        
        with col1:
            compression = performance_data.get('compression', 'None')
            compression_icon = "🟢" if compression and compression != 'None' else "🔴"
            st.metric(
                label="Compression", 
                value=f"{compression_icon} {compression}",
                help="Content compression method used"
            )
        
        with col2:
            if 'cache_headers' in performance_data:
                cache_info = performance_data['cache_headers']
                cache_control = cache_info.get('cache_control', 'None')
                cache_icon = "🟢" if cache_control and cache_control != 'None' else "🔴"
                st.metric(
                    label="Cache Control", 
                    value=f"{cache_icon} {len(cache_control) if cache_control else 0} chars",
                    help=f"Cache headers: {cache_control}"
                )
        
        # Performance Analysis
        st.markdown("#### � Performance Analysis")
        
        # Response time analysis
        if response_time:
            if response_time < 200:
                st.success("🚀 **Excellent Response Time** - Very fast server response")
            elif response_time < 500:
                st.info("✅ **Good Response Time** - Acceptable server performance")
            elif response_time < 1000:
                st.warning("⚠️ **Moderate Response Time** - Could be improved")
            else:
                st.error("❌ **Slow Response Time** - Server optimization needed")
        
        # Page size analysis
        if page_size:
            size_mb = page_size / (1024 * 1024)
            if size_mb < 1:
                st.success("🟢 **Good Page Size** - Fast loading expected")
            elif size_mb < 3:
                st.info("🟡 **Moderate Page Size** - Consider optimization")
            else:
                st.warning("🔴 **Large Page Size** - Optimization recommended")
        
        # PageSpeed Score (if available)
        pagespeed_score = performance_data.get('pagespeed_score')
        if pagespeed_score:
            st.markdown("#### 🏆 PageSpeed Score")
            if pagespeed_score >= 90:
                st.success(f"🟢 **Excellent:** {pagespeed_score}/100")
            elif pagespeed_score >= 50:
                st.warning(f"🟡 **Needs Improvement:** {pagespeed_score}/100")
            else:
                st.error(f"🔴 **Poor:** {pagespeed_score}/100")
        else:
            st.info("📊 **PageSpeed Score:** Not available (requires Google PageSpeed API)")
        
        # Recommendations
        st.markdown("#### 💡 Optimization Recommendations")
        recommendations = []
        
        if response_time and response_time > 500:
            recommendations.append("🔧 **Server Response:** Consider upgrading server resources or optimizing backend code")
        
        if page_size and page_size > 1024 * 1024:  # > 1MB
            recommendations.append("📦 **Page Size:** Compress images, minify CSS/JS, remove unused resources")
        
        if not performance_data.get('compression') or performance_data.get('compression') == 'None':
            recommendations.append("🗜️ **Compression:** Enable Gzip or Brotli compression on your server")
        
        if redirect_count and redirect_count > 1:
            recommendations.append("🔄 **Redirects:** Minimize redirect chains to improve loading speed")
        
        if not recommendations:
            st.success("🎉 **Great Performance!** Your website is well-optimized.")
        else:
            for rec in recommendations:
                st.warning(rec)
    
    @staticmethod
    def display_seo_marketing_analysis(seo_data):
        """Optimized SEO analysis display"""
        is_valid, error_msg = DataValidation.validate_audit_data(seo_data, "SEO")
        if not is_valid:
            if error_msg:
                SharedUIComponents.display_error_state("SEO", error_msg)
            else:
                SharedUIComponents.display_no_data_warning("SEO")
            return
        
        # Check if comprehensive or basic SEO data
        if any(key in seo_data for key in ['categories', 'overall_score', 'meta_tags', 'headings']):
            OptimizedDisplays._display_comprehensive_seo(seo_data)
        else:
            OptimizedDisplays._display_basic_seo(seo_data)
    
    @staticmethod
    def _display_comprehensive_seo(seo_data):
        """Display comprehensive SEO analysis"""
        st.markdown("### 🔍 Comprehensive SEO Analysis")
        
        # Overall metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            overall_score = seo_data.get('overall_score', 0)
            SharedUIComponents.create_score_metric(overall_score, "Overall SEO Score")
        
        with col2:
            issues = seo_data.get('issues', {})
            critical_count = issues.get('critical', 0)
            error_count = issues.get('errors', 0)
            total_issues = critical_count + error_count
            st.metric("Critical Issues", total_issues, delta=f"{critical_count} critical")
        
        with col3:
            warnings = issues.get('warnings', 0)
            st.metric("Warnings", warnings, delta="⚠️" if warnings > 0 else "✅")
        
        with col4:
            page_info = seo_data.get('page_info', {})
            lang = page_info.get('language', 'Unknown')
            st.metric("Language", lang.upper() if lang != 'unknown' else 'Not Set')
        
        # Category breakdown using shared component
        categories = seo_data.get('categories', {})
        if categories:
            SharedUIComponents.display_category_breakdown(categories)
        
        # Social media and marketing tools
        social_links = seo_data.get('social_media_links', {})
        if social_links:
            SharedUIComponents.display_social_media_links(social_links)
        
        marketing_tools = seo_data.get('marketing_tools', [])
        if marketing_tools:
            SharedUIComponents.display_marketing_tools(marketing_tools)
        
        # TODO list
        todo_list = seo_data.get('todo_list', [])
        if todo_list:
            SharedUIComponents.display_todo_list(todo_list)
    
    @staticmethod
    def _display_basic_seo(seo_data):
        """Display basic SEO analysis"""
        st.markdown("### 🔍 SEO Analysis")
        
        # SEO Score
        seo_score = seo_data.get('seo_score', 0)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            SharedUIComponents.create_score_metric(seo_score, "SEO Score")
        
        # Basic elements
        st.subheader("📝 Basic SEO Elements")
        col1, col2 = st.columns(2)
        
        with col1:
            title = seo_data.get('title')
            if title:
                st.write(f"**Title:** {title}")
                st.write(f"**Length:** {len(title)} characters")
            else:
                st.warning("❌ No title tag found")
        
        with col2:
            description = seo_data.get('meta_description')
            if description:
                st.write(f"**Meta Description:** {description[:100]}...")
                st.write(f"**Length:** {len(description)} characters")
            else:
                st.warning("❌ No meta description found")
        
        # Marketing tools and social media using shared components
        marketing_tools = seo_data.get('marketing_tools', [])
        if marketing_tools:
            SharedUIComponents.display_marketing_tools(marketing_tools)
        
        social_links = seo_data.get('social_media_links', {})
        if social_links:
            SharedUIComponents.display_social_media_links(social_links)
    
    @staticmethod
    def display_security_analysis(ssl_data):
        """Optimized security analysis display"""
        is_valid, error_msg = DataValidation.validate_audit_data(ssl_data, "Security")
        if not is_valid:
            if error_msg:
                SharedUIComponents.display_error_state("Security", error_msg)
            else:
                SharedUIComponents.display_no_data_warning("Security")
            return
        
        st.markdown("### 🔒 Security Analysis")
        SharedUIComponents.display_ssl_metrics(ssl_data)
    
    @staticmethod
    def display_dns_analysis(dns_data):
        """Optimized DNS analysis display"""
        is_valid, error_msg = DataValidation.validate_audit_data(dns_data, "DNS")
        if not is_valid:
            if error_msg:
                SharedUIComponents.display_error_state("DNS", error_msg)
            else:
                SharedUIComponents.display_no_data_warning("DNS")
            return
        
        st.markdown("### 🌐 DNS Analysis")
        SharedUIComponents.display_dns_records(dns_data)
    
    @staticmethod
    def display_ranking_analysis(ranking_data):
        """Optimized ranking analysis display"""
        is_valid, error_msg = DataValidation.validate_audit_data(ranking_data, "Ranking")
        if not is_valid:
            if error_msg:
                SharedUIComponents.display_error_state("Ranking", error_msg)
            else:
                SharedUIComponents.display_no_data_warning("Ranking")
            return
        
        st.markdown("### 📈 Ranking Analysis")
        SharedUIComponents.display_authority_metrics(ranking_data)
        
        # Traffic and backlinks
        st.subheader("📊 Traffic & Backlinks")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            traffic = ranking_data.get('organic_traffic_estimate', 0)
            st.metric("Organic Traffic Est.", f"{traffic:,}")
        
        with col2:
            backlinks = ranking_data.get('backlink_estimate', 0)
            st.metric("Backlinks Est.", f"{backlinks:,}")
        
        with col3:
            domains = ranking_data.get('referring_domains', 0)
            st.metric("Referring Domains", f"{domains:,}")
    
    @staticmethod
    def display_technical_analysis(audit_data):
        """Display technical analysis summary"""
        st.markdown("### 📋 Technical Analysis")
        
        if not audit_data:
            st.info("🔍 **Ready to analyze!** Enter a website URL above and click 'Analyze Website' to begin.")
            
            # Show available modules instead of "No Data"
            st.markdown("#### 📊 Available Analysis Modules")
            modules = [
                ("⚡ Performance Analysis", "Page load times, Core Web Vitals, optimization metrics"),
                ("🔍 SEO & Marketing", "Meta tags, schema markup, social media integration"), 
                ("🔒 Security Analysis", "SSL/TLS certificates, security headers, HTTPS status"),
                ("🌐 DNS Analysis", "DNS records, WHOIS data, domain configuration"),
                ("📈 Ranking Analysis", "Search visibility, ranking factors, competition analysis")
            ]
            
            for name, description in modules:
                st.success(f"✅ {name} - Ready")
                st.caption(f"   {description}")
            return
        
        # Show actual results when available (flattened structure)
        st.markdown("#### 📊 Analysis Results")
        
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
                st.warning(f"⚠️ {module} Analysis - Not Selected")
    
    @staticmethod
    def display_metrics_dashboard(audit_data):
        """Display comprehensive metrics dashboard with detailed information"""
        st.markdown("### 📊 Metrics Dashboard")
        
        # Check if we have any audit data at all (flattened structure)
        has_data = bool(audit_data and (
            audit_data.get('performance') or 
            audit_data.get('seo_marketing') or 
            audit_data.get('ssl') or 
            audit_data.get('dns') or
            audit_data.get('ranking')
        ))
        
        if not has_data:
            st.info("📊 **Metrics Dashboard** - Complete an audit to see detailed metrics and performance scores here.")
            
            # Show what will be available
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Performance Score", "⏳", help="Lighthouse performance score")
            with col2:
                st.metric("SEO Score", "⏳", help="SEO optimization rating")
            with col3:
                st.metric("Security Rating", "⏳", help="SSL/TLS security grade")
            with col4:
                st.metric("DNS Health", "⏳", help="DNS configuration status")
            return

        # Main overview metrics - top row
        st.markdown("#### 🎯 Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        
        # Performance score
        with col1:
            perf_data = audit_data.get('performance', {})
            if perf_data and perf_data.get('response_time'):
                response_time = perf_data['response_time']
                color = "🟢" if response_time < 500 else "🟡" if response_time < 1000 else "🔴"
                st.metric("Response Time", f"{color} {response_time}ms", help="Server response time")
            else:
                st.metric("Performance", "N/A")
        
        # SEO score
        with col2:
            seo_data = audit_data.get('seo_marketing', {})
            if seo_data:
                score = seo_data.get('overall_score', seo_data.get('seo_score', 0))
                color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                st.metric("SEO Score", f"{color} {score}%")
            else:
                st.metric("SEO", "N/A")
        
        # Security status
        with col3:
            ssl_data = audit_data.get('ssl', {})
            if ssl_data and ssl_data.get('ssl_valid'):
                grade = ssl_data.get('ssl_grade', 'Valid')
                color = "🟢" if grade in ['A+', 'A'] else "🟡" if grade == 'B' else "🔴"
                st.metric("Security", f"{color} {grade}")
            elif ssl_data:
                st.metric("Security", "🔴 Issues")
            else:
                st.metric("Security", "N/A")
        
        # DNS status
        with col4:
            dns_data = audit_data.get('dns', {})
            if dns_data:
                total_records = (len(dns_data.get('a_records', [])) + 
                               len(dns_data.get('mx_records', [])) + 
                               len(dns_data.get('ns_records', [])) +
                               len(dns_data.get('cname_records', [])))
                st.metric("DNS Records", f"🟢 {total_records} total")
            else:
                st.metric("DNS", "N/A")

        st.divider()

        # Detailed Performance Metrics
        if perf_data:
            st.markdown("#### ⚡ Performance Breakdown")
            perf_col1, perf_col2, perf_col3, perf_col4 = st.columns(4)
            
            with perf_col1:
                ttfb = perf_data.get('time_to_first_byte', 'N/A')
                if ttfb != 'N/A':
                    color = "🟢" if ttfb < 200 else "🟡" if ttfb < 500 else "🔴"
                    st.metric("TTFB", f"{color} {ttfb}ms", help="Time to First Byte")
                else:
                    st.metric("TTFB", "N/A")
            
            with perf_col2:
                load_time = perf_data.get('page_load_time', 'N/A')
                if load_time != 'N/A':
                    color = "🟢" if load_time < 2000 else "🟡" if load_time < 4000 else "🔴"
                    st.metric("Load Time", f"{color} {load_time}ms")
                else:
                    st.metric("Load Time", "N/A")
            
            with perf_col3:
                # Check for compression
                compression = perf_data.get('compression_enabled', False)
                comp_status = "🟢 Enabled" if compression else "🔴 Disabled"
                st.metric("Compression", comp_status)
            
            with perf_col4:
                # Check for caching
                caching = perf_data.get('caching_enabled', False)
                cache_status = "🟢 Enabled" if caching else "🔴 Disabled"
                st.metric("Caching", cache_status)

        # SEO Details
        if seo_data:
            st.markdown("#### 🔍 SEO Analysis Details")
            seo_col1, seo_col2, seo_col3, seo_col4 = st.columns(4)
            
            with seo_col1:
                title_score = seo_data.get('title_tag_score', 0)
                color = "🟢" if title_score >= 80 else "🟡" if title_score >= 60 else "🔴"
                st.metric("Title Tag", f"{color} {title_score}%")
            
            with seo_col2:
                meta_score = seo_data.get('meta_description_score', 0)
                color = "🟢" if meta_score >= 80 else "🟡" if meta_score >= 60 else "🔴"
                st.metric("Meta Description", f"{color} {meta_score}%")
            
            with seo_col3:
                headings_score = seo_data.get('headings_score', 0)
                color = "🟢" if headings_score >= 80 else "🟡" if headings_score >= 60 else "🔴"
                st.metric("Headings", f"{color} {headings_score}%")
            
            with seo_col4:
                images_score = seo_data.get('images_score', 0)
                color = "🟢" if images_score >= 80 else "🟡" if images_score >= 60 else "🔴"
                st.metric("Image SEO", f"{color} {images_score}%")

        # Security Details
        if ssl_data:
            st.markdown("#### 🔒 Security Analysis Details")
            sec_col1, sec_col2, sec_col3, sec_col4 = st.columns(4)
            
            with sec_col1:
                ssl_valid = ssl_data.get('ssl_valid', False)
                ssl_status = "🟢 Valid" if ssl_valid else "🔴 Invalid"
                st.metric("SSL Certificate", ssl_status)
            
            with sec_col2:
                protocol = ssl_data.get('protocol_version', 'Unknown')
                if protocol in ['TLSv1.3', 'TLSv1.2']:
                    prot_status = f"🟢 {protocol}"
                elif protocol in ['TLSv1.1']:
                    prot_status = f"🟡 {protocol}"
                else:
                    prot_status = f"🔴 {protocol}"
                st.metric("TLS Protocol", prot_status)
            
            with sec_col3:
                expires_in = ssl_data.get('expires_in_days', 'N/A')
                if expires_in != 'N/A':
                    color = "🟢" if expires_in > 30 else "🟡" if expires_in > 7 else "🔴"
                    st.metric("Cert Expiry", f"{color} {expires_in} days")
                else:
                    st.metric("Cert Expiry", "N/A")
            
            with sec_col4:
                issuer = ssl_data.get('issuer', {})
                issuer_name = issuer.get('organizationName', 'Unknown') if isinstance(issuer, dict) else 'Unknown'
                if len(issuer_name) > 15:
                    issuer_name = issuer_name[:12] + "..."
                st.metric("Issuer", issuer_name)

        # DNS Details
        if dns_data:
            st.markdown("#### 🌐 DNS Configuration Overview")
            dns_col1, dns_col2, dns_col3, dns_col4 = st.columns(4)
            
            with dns_col1:
                a_count = len(dns_data.get('a_records', []))
                st.metric("A Records", f"🟢 {a_count}")
            
            with dns_col2:
                mx_count = len(dns_data.get('mx_records', []))
                mx_status = f"🟢 {mx_count}" if mx_count > 0 else "🔴 0"
                st.metric("MX Records", mx_status)
            
            with dns_col3:
                ns_count = len(dns_data.get('ns_records', []))
                ns_status = f"🟢 {ns_count}" if ns_count >= 2 else f"🟡 {ns_count}"
                st.metric("NS Records", ns_status)
            
            with dns_col4:
                cname_count = len(dns_data.get('cname_records', []))
                st.metric("CNAME Records", f"🔵 {cname_count}")

        # Ranking Information if available
        ranking_data = audit_data.get('ranking', {})
        if ranking_data:
            st.markdown("#### 📈 Authority & Ranking Metrics")
            rank_col1, rank_col2, rank_col3, rank_col4 = st.columns(4)
            
            with rank_col1:
                da = ranking_data.get('domain_authority', 'N/A')
                if da != 'N/A':
                    color = "🟢" if da >= 50 else "🟡" if da >= 30 else "🔴"
                    st.metric("Domain Authority", f"{color} {da}")
                else:
                    st.metric("Domain Authority", "N/A")
            
            with rank_col2:
                backlinks = ranking_data.get('backlinks', 'N/A')
                if backlinks != 'N/A':
                    if backlinks > 1000:
                        bl_display = f"🟢 {backlinks:,}"
                    elif backlinks > 100:
                        bl_display = f"🟡 {backlinks}"
                    else:
                        bl_display = f"🔴 {backlinks}"
                    st.metric("Backlinks", bl_display)
                else:
                    st.metric("Backlinks", "N/A")
            
            with rank_col3:
                organic_traffic = ranking_data.get('organic_traffic', 'N/A')
                if organic_traffic != 'N/A':
                    st.metric("Organic Traffic", f"📊 {organic_traffic}")
                else:
                    st.metric("Organic Traffic", "N/A")
            
            with rank_col4:
                keywords = ranking_data.get('ranking_keywords', 'N/A')
                if keywords != 'N/A':
                    st.metric("Ranking Keywords", f"🔍 {keywords}")
                else:
                    st.metric("Ranking Keywords", "N/A")

        # Summary recommendations
        st.divider()
        st.markdown("#### 💡 Quick Recommendations")
        
        recommendations = []
        
        # Performance recommendations
        if perf_data:
            response_time = perf_data.get('response_time', 0)
            if response_time > 1000:
                recommendations.append("🔴 **Performance**: Server response time is slow (>1s). Consider optimizing server or using a CDN.")
            elif response_time > 500:
                recommendations.append("🟡 **Performance**: Response time could be improved (<500ms is ideal).")
            
            if not perf_data.get('compression_enabled', True):
                recommendations.append("🔴 **Performance**: Enable compression to reduce file sizes and improve load times.")
        
        # SEO recommendations
        if seo_data:
            overall_score = seo_data.get('overall_score', 100)
            if overall_score < 70:
                recommendations.append("🔴 **SEO**: Overall SEO score is low. Focus on improving title tags, meta descriptions, and content structure.")
            elif overall_score < 85:
                recommendations.append("🟡 **SEO**: Good SEO foundation, but there's room for improvement in optimization.")
        
        # Security recommendations
        if ssl_data:
            if not ssl_data.get('ssl_valid', False):
                recommendations.append("🔴 **Security**: SSL certificate is invalid or missing. This is critical for user trust and SEO.")
            
            expires_in = ssl_data.get('expires_in_days', 999)
            if expires_in < 30:
                recommendations.append("🟡 **Security**: SSL certificate expires soon. Plan for renewal to avoid service disruption.")
        
        # DNS recommendations
        if dns_data:
            mx_count = len(dns_data.get('mx_records', []))
            if mx_count == 0:
                recommendations.append("🟡 **DNS**: No MX records found. Add MX records if you need email functionality.")
        
        if recommendations:
            for rec in recommendations[:5]:  # Show top 5 recommendations
                st.markdown(f"• {rec}")
        else:
            st.success("✅ **Excellent!** All major areas are well-optimized. Keep monitoring for continuous improvement.")

        # Performance chart if detailed data available
        if perf_data and any(key in perf_data for key in ['response_time', 'page_load_time', 'time_to_first_byte']):
            st.markdown("#### 📊 Performance Metrics Chart")
            OptimizedDisplays._create_enhanced_performance_chart(perf_data)
    
    @staticmethod
    def _create_enhanced_performance_chart(perf_data):
        """Create enhanced performance metrics visualization"""
        import plotly.graph_objects as go
        
        # Collect performance metrics
        metrics = []
        values = []
        colors = []
        
        # Response time
        response_time = perf_data.get('response_time', 0)
        if response_time:
            metrics.append('Response Time (ms)')
            values.append(response_time)
            colors.append('#4CAF50' if response_time < 500 else '#FFC107' if response_time < 1000 else '#F44336')
        
        # TTFB
        ttfb = perf_data.get('time_to_first_byte', 0)
        if ttfb:
            metrics.append('TTFB (ms)')
            values.append(ttfb)
            colors.append('#4CAF50' if ttfb < 200 else '#FFC107' if ttfb < 500 else '#F44336')
        
        # Load time
        load_time = perf_data.get('page_load_time', 0)
        if load_time:
            metrics.append('Load Time (ms)')
            values.append(load_time)
            colors.append('#4CAF50' if load_time < 2000 else '#FFC107' if load_time < 4000 else '#F44336')
        
        if metrics:
            fig = go.Figure(data=[
                go.Bar(
                    x=metrics,
                    y=values,
                    marker_color=colors,
                    text=[f'{v}ms' for v in values],
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Performance Metrics Overview",
                xaxis_title="Metrics",
                yaxis_title="Time (milliseconds)",
                height=400,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No detailed performance metrics available for visualization.")

# Backward compatibility - expose functions at module level
display_audit_results = OptimizedDisplays.display_audit_results
display_performance_analysis = OptimizedDisplays.display_performance_analysis
display_seo_marketing_analysis = OptimizedDisplays.display_seo_marketing_analysis
display_security_analysis = OptimizedDisplays.display_security_analysis
display_dns_analysis = OptimizedDisplays.display_dns_analysis
display_ranking_analysis = OptimizedDisplays.display_ranking_analysis
display_technical_analysis = OptimizedDisplays.display_technical_analysis
display_metrics_dashboard = OptimizedDisplays.display_metrics_dashboard
