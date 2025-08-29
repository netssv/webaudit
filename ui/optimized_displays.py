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
        if not dns_data:
            st.warning("⚠️ No DNS data available")
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
                st.warning(f"⚠️ {module} Analysis - No Data")
    
    @staticmethod
    def display_metrics_dashboard(audit_data):
        """Display comprehensive digital marketing dashboard with actionable insights"""
        st.markdown("### 📊 Digital Marketing Intelligence Dashboard")

        # Check if we have any audit data at all (flattened structure)
        has_data = bool(audit_data and (
            audit_data.get('performance') or
            audit_data.get('seo_marketing') or
            audit_data.get('ssl') or
            audit_data.get('dns') or
            audit_data.get('ranking')
        ))

        if not has_data:
            OptimizedDisplays._display_dashboard_placeholder()
            return

        # Executive Summary - Top Priority Insights
        OptimizedDisplays._display_executive_summary(audit_data)

        # Key Performance Indicators with Trends
        OptimizedDisplays._display_kpi_overview(audit_data)

        # SEO Opportunity Analysis
        OptimizedDisplays._display_seo_opportunities(audit_data)

        # Performance Impact Analysis
        OptimizedDisplays._display_performance_impact(audit_data)

        # Action Priority Matrix
        OptimizedDisplays._display_action_priority_matrix(audit_data)

        # Revenue Impact Estimation
        OptimizedDisplays._display_revenue_impact(audit_data)

        # Technical Health Score
        OptimizedDisplays._display_technical_health_score(audit_data)

        # Mobile vs Desktop Analysis
        OptimizedDisplays._display_mobile_desktop_comparison(audit_data)

        # Content Performance Insights
        OptimizedDisplays._display_content_insights(audit_data)

    @staticmethod
    def _display_dashboard_placeholder():
        """Display placeholder when no data is available"""
        st.info("🚀 **Digital Marketing Intelligence Dashboard** - Complete an audit to unlock powerful marketing insights!")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("#### 🎯 Executive Summary")
            st.write("• Key performance insights")
            st.write("• Revenue impact analysis")
            st.write("• Action priority matrix")

        with col2:
            st.markdown("#### 📈 SEO Opportunities")
            st.write("• Keyword optimization gaps")
            st.write("• Content performance")
            st.write("• Technical SEO issues")

        with col3:
            st.markdown("#### 💰 Revenue Impact")
            st.write("• Traffic potential")
            st.write("• Conversion optimization")
            st.write("• Competitive analysis")

    @staticmethod
    def _display_executive_summary(audit_data):
        """Display executive summary with key insights"""
        st.markdown("#### 🎯 Executive Summary")

        # Calculate overall health score
        health_score = OptimizedDisplays._calculate_overall_health_score(audit_data)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            score_color = "🟢" if health_score >= 80 else "🟡" if health_score >= 60 else "🔴"
            st.metric("Overall Health Score", f"{score_color} {health_score}%")

        with col2:
            perf_data = audit_data.get('performance', {})
            response_time = perf_data.get('response_time', 0)
            impact = "High" if response_time > 1000 else "Medium" if response_time > 500 else "Low"
            st.metric("Performance Impact", f"⚡ {impact}")

        with col3:
            seo_data = audit_data.get('seo_marketing', {})
            seo_score = seo_data.get('overall_score', 0)
            opportunity = "High" if seo_score < 70 else "Medium" if seo_score < 85 else "Low"
            st.metric("SEO Opportunity", f"🎯 {opportunity}")

        with col4:
            ssl_data = audit_data.get('ssl', {})
            security_risk = "High" if not ssl_data.get('ssl_valid', False) else "Low"
            st.metric("Security Risk", f"🔒 {security_risk}")

        # Key insights
        st.markdown("**🔑 Key Insights:**")
        insights = OptimizedDisplays._generate_key_insights(audit_data)
        for insight in insights[:3]:  # Show top 3 insights
            st.markdown(f"• {insight}")

    @staticmethod
    def _display_kpi_overview(audit_data):
        """Display KPI overview with trend indicators"""
        st.markdown("#### 📈 Key Performance Indicators")

        # Performance KPIs
        perf_data = audit_data.get('performance', {})
        seo_data = audit_data.get('seo_marketing', {})
        ssl_data = audit_data.get('ssl', {})
        dns_data = audit_data.get('dns', {})
        ranking_data = audit_data.get('ranking', {})

        # Create KPI cards with trend indicators
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            response_time = perf_data.get('response_time', 0)
            if response_time:
                trend = "↗️" if response_time > 1000 else "➡️" if response_time > 500 else "↘️"
                st.metric("Page Speed", f"{trend} {response_time}ms",
                         help="Server response time - affects user experience and SEO")

        with col2:
            seo_score = seo_data.get('overall_score', 0)
            if seo_score:
                trend = "↗️" if seo_score >= 80 else "➡️" if seo_score >= 60 else "↘️"
                st.metric("SEO Score", f"{trend} {seo_score}%",
                         help="Overall SEO optimization score")

        with col3:
            da = ranking_data.get('domain_authority', 0)
            if da:
                trend = "↗️" if da >= 50 else "➡️" if da >= 30 else "↘️"
                st.metric("Domain Authority", f"{trend} {da}",
                         help="Moz Domain Authority score")

        with col4:
            backlinks = ranking_data.get('backlinks', 0)
            if backlinks:
                trend = "↗️" if backlinks > 1000 else "➡️" if backlinks > 100 else "↘️"
                st.metric("Backlinks", f"{trend} {backlinks:,}",
                         help="Total number of backlinks")

    @staticmethod
    def _display_seo_opportunities(audit_data):
        """Display SEO opportunities and content insights"""
        st.markdown("#### 🎯 SEO Opportunities & Content Insights")

        seo_data = audit_data.get('seo_marketing', {})

        if seo_data:
            # SEO Opportunity Score
            opportunity_score = OptimizedDisplays._calculate_seo_opportunity_score(seo_data)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("SEO Opportunity Score", f"🎯 {opportunity_score}%",
                         help="Potential SEO improvements available")

            with col2:
                content_score = seo_data.get('content_score', 0)
                st.metric("Content Optimization", f"📝 {content_score}%")

            with col3:
                technical_seo = seo_data.get('technical_seo_score', 0)
                st.metric("Technical SEO", f"⚙️ {technical_seo}%")

            # Content Performance Radar Chart
            OptimizedDisplays._create_content_performance_radar(seo_data)

            # Top SEO Recommendations
            st.markdown("**🚀 Top SEO Recommendations:**")
            recommendations = OptimizedDisplays._generate_seo_recommendations(seo_data)
            for rec in recommendations[:4]:
                st.markdown(f"• {rec}")
        else:
            st.info("Complete an SEO audit to see detailed opportunities and recommendations.")

    @staticmethod
    def _display_performance_impact(audit_data):
        """Display performance impact analysis"""
        st.markdown("#### ⚡ Performance Impact Analysis")

        perf_data = audit_data.get('performance', {})

        if perf_data:
            # Performance Impact Calculator
            response_time = perf_data.get('response_time', 0)
            load_time = perf_data.get('page_load_time', 0)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                # Estimated traffic loss due to slow speed
                if response_time > 1000:
                    traffic_loss = "15-25%"
                    impact_level = "🔴 High"
                elif response_time > 500:
                    traffic_loss = "5-15%"
                    impact_level = "🟡 Medium"
                else:
                    traffic_loss = "<5%"
                    impact_level = "🟢 Low"
                st.metric("Traffic Impact", f"{impact_level} {traffic_loss}")

            with col2:
                # SEO ranking impact
                if load_time > 4000:
                    ranking_impact = "Significant"
                    rank_color = "🔴"
                elif load_time > 2000:
                    ranking_impact = "Moderate"
                    rank_color = "🟡"
                else:
                    ranking_impact = "Minimal"
                    rank_color = "🟢"
                st.metric("SEO Impact", f"{rank_color} {ranking_impact}")

            with col3:
                # User experience score
                ux_score = 100 - min(100, (response_time / 20))
                st.metric("UX Score", f"👥 {ux_score:.0f}%")

            with col4:
                # Conversion impact
                conversion_impact = max(0, (response_time - 500) / 20)  # Rough estimate
                st.metric("Conversion Loss", f"💰 {conversion_impact:.1f}%")

            # Performance vs Competitors
            OptimizedDisplays._create_performance_comparison_chart(perf_data)
        else:
            st.info("Performance data needed for impact analysis.")

    @staticmethod
    def _display_action_priority_matrix(audit_data):
        """Display action priority matrix for quick decision making"""
        st.markdown("#### 🎯 Action Priority Matrix")

        # Calculate priority scores for different areas
        priorities = OptimizedDisplays._calculate_action_priorities(audit_data)

        # Create priority matrix visualization
        fig = go.Figure()

        # Add scatter plot for priority matrix
        impact_scores = [p['impact'] for p in priorities.values()]
        effort_scores = [p['effort'] for p in priorities.values()]
        labels = list(priorities.keys())

        # Color coding based on priority
        colors = []
        for impact, effort in zip(impact_scores, effort_scores):
            if impact >= 7 and effort <= 3:
                colors.append('#FF4444')  # High impact, low effort - Quick wins
            elif impact >= 7 and effort >= 7:
                colors.append('#FFA500')  # High impact, high effort - Major projects
            elif impact <= 3 and effort <= 3:
                colors.append('#90EE90')  # Low impact, low effort - Nice to have
            else:
                colors.append('#87CEEB')  # Medium priority

        fig.add_trace(go.Scatter(
            x=effort_scores,
            y=impact_scores,
            mode='markers+text',
            text=labels,
            textposition="top center",
            marker=dict(size=12, color=colors),
            name='Actions'
        ))

        # Add quadrants
        fig.add_shape(type="rect", x0=0, y0=0, x1=5, y1=5,
                     line=dict(color="lightgray", width=1), fillcolor="lightgreen", opacity=0.1)
        fig.add_shape(type="rect", x0=5, y0=0, x1=10, y1=5,
                     line=dict(color="lightgray", width=1), fillcolor="lightyellow", opacity=0.1)
        fig.add_shape(type="rect", x0=0, y0=5, x1=5, y1=10,
                     line=dict(color="lightgray", width=1), fillcolor="lightcoral", opacity=0.1)
        fig.add_shape(type="rect", x0=5, y0=5, x1=10, y1=10,
                     line=dict(color="lightgray", width=1), fillcolor="lightsalmon", opacity=0.1)

        fig.update_layout(
            title="Action Priority Matrix",
            xaxis=dict(title="Effort Required", range=[0, 10]),
            yaxis=dict(title="Business Impact", range=[0, 10]),
            height=400,
            showlegend=False
        )

        # Add quadrant labels
        fig.add_annotation(x=2.5, y=2.5, text="Nice to Have", showarrow=False, font=dict(size=10))
        fig.add_annotation(x=7.5, y=2.5, text="Low Impact", showarrow=False, font=dict(size=10))
        fig.add_annotation(x=2.5, y=7.5, text="Quick Wins", showarrow=False, font=dict(size=10))
        fig.add_annotation(x=7.5, y=7.5, text="Major Projects", showarrow=False, font=dict(size=10))

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def _display_revenue_impact(audit_data):
        """Display revenue impact estimation"""
        st.markdown("#### 💰 Revenue Impact Estimation")

        # Calculate potential revenue impact
        perf_data = audit_data.get('performance', {})
        seo_data = audit_data.get('seo_marketing', {})
        ranking_data = audit_data.get('ranking', {})

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            # Traffic increase potential from SEO improvements
            seo_score = seo_data.get('overall_score', 0)
            traffic_potential = min(50, (100 - seo_score) * 0.5)  # Rough estimate
            st.metric("Traffic Potential", f"📈 +{traffic_potential}%")

        with col2:
            # Conversion rate improvement potential
            response_time = perf_data.get('response_time', 0)
            conversion_potential = min(25, max(0, (1000 - response_time) / 40))
            st.metric("Conversion Lift", f"🎯 +{conversion_potential:.1f}%")

        with col3:
            # Estimated monthly revenue impact
            current_traffic = ranking_data.get('organic_traffic', 1000)
            avg_order_value = 50  # Assumed
            conversion_rate = 0.02  # Assumed 2%

            potential_traffic = current_traffic * (1 + traffic_potential/100)
            potential_revenue = potential_traffic * conversion_rate * avg_order_value * (1 + conversion_potential/100)
            current_revenue = current_traffic * conversion_rate * avg_order_value

            revenue_increase = potential_revenue - current_revenue
            st.metric("Revenue Impact", f"💵 +${revenue_increase:,.0f}/mo")

        with col4:
            # ROI timeline
            implementation_time = 30  # days
            st.metric("Break-even Period", f"📅 {implementation_time} days")

        # Revenue projection chart
        OptimizedDisplays._create_revenue_projection_chart(current_revenue, potential_revenue)

    @staticmethod
    def _display_technical_health_score(audit_data):
        """Display technical health score with breakdown"""
        st.markdown("#### 🔧 Technical Health Score")

        # Calculate technical health components
        health_components = OptimizedDisplays._calculate_technical_health(audit_data)

        # Overall health score
        overall_score = sum(component['score'] * component['weight'] for component in health_components.values())
        overall_score = min(100, max(0, overall_score))

        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            score_color = "🟢" if overall_score >= 80 else "🟡" if overall_score >= 60 else "🔴"
            st.metric("Technical Health", f"{score_color} {overall_score:.1f}%")

        with col2:
            critical_issues = sum(1 for comp in health_components.values() if comp['score'] < 50)
            st.metric("Critical Issues", f"🚨 {critical_issues}")

        with col3:
            health_trend = "Improving" if overall_score >= 70 else "Needs Attention"
            st.metric("Health Trend", f"📊 {health_trend}")

        # Health breakdown chart
        OptimizedDisplays._create_technical_health_chart(health_components)

    @staticmethod
    def _display_mobile_desktop_comparison(audit_data):
        """Display mobile vs desktop performance comparison"""
        st.markdown("#### 📱 Mobile vs Desktop Performance")

        perf_data = audit_data.get('performance', {})

        if perf_data:
            # Simulate mobile vs desktop data (in real implementation, this would come from actual audits)
            desktop_score = 85
            mobile_score = 72

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Desktop Score", f"🖥️ {desktop_score}%")

            with col2:
                st.metric("Mobile Score", f"📱 {mobile_score}%")

            with col3:
                gap = desktop_score - mobile_score
                gap_status = "🔴 Large Gap" if gap > 20 else "🟡 Moderate" if gap > 10 else "🟢 Minimal"
                st.metric("Performance Gap", f"{gap_status} {gap}%")

            # Mobile vs Desktop comparison chart
            OptimizedDisplays._create_mobile_desktop_chart(desktop_score, mobile_score)
        else:
            st.info("Performance data needed for mobile/desktop comparison.")

    @staticmethod
    def _display_content_insights(audit_data):
        """Display content performance insights"""
        st.markdown("#### 📝 Content Performance Insights")

        seo_data = audit_data.get('seo_marketing', {})

        if seo_data:
            # Content quality metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                readability_score = seo_data.get('readability_score', 75)
                st.metric("Readability", f"📖 {readability_score}%")

            with col2:
                content_depth = seo_data.get('content_depth_score', 68)
                st.metric("Content Depth", f"📚 {content_depth}%")

            with col3:
                keyword_optimization = seo_data.get('keyword_optimization_score', 72)
                st.metric("Keyword Optimization", f"🔍 {keyword_optimization}%")

            with col4:
                user_engagement = seo_data.get('user_engagement_score', 80)
                st.metric("User Engagement", f"👥 {user_engagement}%")

            # Content opportunity analysis
            st.markdown("**📈 Content Opportunities:**")
            opportunities = [
                "Add more comprehensive guides and tutorials",
                "Improve internal linking structure",
                "Create pillar content for main topics",
                "Add schema markup for better rich snippets",
                "Optimize for featured snippets"
            ]

            for opp in opportunities[:3]:
                st.markdown(f"• {opp}")
        else:
            st.info("SEO data needed for content insights.")

    # Helper methods for calculations and visualizations

    @staticmethod
    def _calculate_overall_health_score(audit_data):
        """Calculate overall health score"""
        scores = []
        weights = []

        perf_data = audit_data.get('performance', {})
        if perf_data:
            response_time = perf_data.get('response_time', 0)
            # More realistic performance scoring: 0-2000ms range
            perf_score = max(0, 100 - (response_time / 20))
            scores.append(perf_score)
            weights.append(0.3)

        seo_data = audit_data.get('seo_marketing', {})
        if seo_data:
            seo_score = seo_data.get('overall_score', 0)
            scores.append(seo_score)
            weights.append(0.3)

        ssl_data = audit_data.get('ssl', {})
        if ssl_data:
            ssl_score = 100 if ssl_data.get('ssl_valid', False) else 0
            scores.append(ssl_score)
            weights.append(0.2)

        ranking_data = audit_data.get('ranking', {})
        if ranking_data:
            da = ranking_data.get('domain_authority', 0)
            rank_score = min(100, da * 2)
            scores.append(rank_score)
            weights.append(0.2)

        if scores:
            return sum(score * weight for score, weight in zip(scores, weights))
        return 0

    @staticmethod
    def _generate_key_insights(audit_data):
        """Generate key insights from audit data"""
        insights = []

        perf_data = audit_data.get('performance', {})
        if perf_data:
            response_time = perf_data.get('response_time', 0)
            if response_time > 1000:
                insights.append("🔴 **Critical**: Slow server response time is hurting user experience and SEO rankings")
            elif response_time > 500:
                insights.append("🟡 **Opportunity**: Response time could be improved for better performance")

        seo_data = audit_data.get('seo_marketing', {})
        if seo_data:
            seo_score = seo_data.get('overall_score', 0)
            if seo_score < 70:
                insights.append("🎯 **High Impact**: Significant SEO optimization opportunities available")
            elif seo_score < 85:
                insights.append("📈 **Growth**: Good SEO foundation with room for improvement")

        ssl_data = audit_data.get('ssl', {})
        if ssl_data and not ssl_data.get('ssl_valid', False):
            insights.append("🔒 **Security**: SSL certificate issues need immediate attention")

        ranking_data = audit_data.get('ranking', {})
        if ranking_data:
            da = ranking_data.get('domain_authority', 0)
            if da < 30:
                insights.append("📊 **Authority**: Focus on building domain authority through quality backlinks")

        return insights

    @staticmethod
    def _calculate_seo_opportunity_score(seo_data):
        """Calculate SEO opportunity score"""
        base_score = seo_data.get('overall_score', 0)
        opportunity_score = min(100, 100 - base_score + 20)  # Add some buffer
        return opportunity_score

    @staticmethod
    def _generate_seo_recommendations(seo_data):
        """Generate SEO recommendations"""
        recommendations = []

        title_score = seo_data.get('title_tag_score', 0)
        if title_score < 80:
            recommendations.append("Optimize title tags for better click-through rates")

        meta_score = seo_data.get('meta_description_score', 0)
        if meta_score < 80:
            recommendations.append("Improve meta descriptions for higher search visibility")

        headings_score = seo_data.get('headings_score', 0)
        if headings_score < 80:
            recommendations.append("Enhance heading structure for better content hierarchy")

        images_score = seo_data.get('images_score', 0)
        if images_score < 80:
            recommendations.append("Optimize images with alt text and compression")

        return recommendations

    @staticmethod
    def _calculate_action_priorities(audit_data):
        """Calculate action priorities for priority matrix"""
        priorities = {}

        # Performance optimization
        perf_data = audit_data.get('performance', {})
        if perf_data:
            response_time = perf_data.get('response_time', 0)
            priorities['Performance'] = {
                'impact': min(10, response_time / 100),
                'effort': 6
            }

        # SEO improvements
        seo_data = audit_data.get('seo_marketing', {})
        if seo_data:
            seo_score = seo_data.get('overall_score', 0)
            priorities['SEO Optimization'] = {
                'impact': min(10, (100 - seo_score) / 5),
                'effort': 4
            }

        # Security fixes
        ssl_data = audit_data.get('ssl', {})
        if ssl_data and not ssl_data.get('ssl_valid', False):
            priorities['SSL Security'] = {
                'impact': 9,
                'effort': 2
            }

        # Content improvements
        priorities['Content Enhancement'] = {
            'impact': 7,
            'effort': 5
        }

        # Technical fixes
        priorities['Technical SEO'] = {
            'impact': 6,
            'effort': 7
        }

        return priorities

    @staticmethod
    def _calculate_technical_health(audit_data):
        """Calculate technical health components"""
        components = {}

        # Performance health
        perf_data = audit_data.get('performance', {})
        if perf_data:
            response_time = perf_data.get('response_time', 0)
            perf_score = max(0, 100 - (response_time / 20))
            components['Performance'] = {'score': perf_score, 'weight': 0.3}

        # SEO health
        seo_data = audit_data.get('seo_marketing', {})
        if seo_data:
            seo_score = seo_data.get('overall_score', 0)
            components['SEO'] = {'score': seo_score, 'weight': 0.3}

        # Security health
        ssl_data = audit_data.get('ssl', {})
        if ssl_data:
            ssl_score = 100 if ssl_data.get('ssl_valid', False) else 0
            components['Security'] = {'score': ssl_score, 'weight': 0.2}

        # DNS health
        dns_data = audit_data.get('dns', {})
        if dns_data:
            dns_score = 80 if len(dns_data.get('a_records', [])) > 0 else 0
            components['DNS'] = {'score': dns_score, 'weight': 0.1}

        # Mobile health (simulated)
        components['Mobile'] = {'score': 75, 'weight': 0.1}

        return components

    # Chart creation methods

    @staticmethod
    def _create_content_performance_radar(seo_data):
        """Create content performance radar chart"""
        import plotly.graph_objects as go

        categories = ['Title Tags', 'Meta Descriptions', 'Headings', 'Images', 'Content Depth', 'Readability']

        values = [
            seo_data.get('title_tag_score', 0),
            seo_data.get('meta_description_score', 0),
            seo_data.get('headings_score', 0),
            seo_data.get('images_score', 0),
            seo_data.get('content_depth_score', 70),
            seo_data.get('readability_score', 75)
        ]

        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Current Performance'
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            title="Content Performance Radar",
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def _create_performance_comparison_chart(perf_data):
        """Create performance comparison chart"""
        import plotly.graph_objects as go

        # Simulated competitor data
        competitors = ['Your Site', 'Competitor A', 'Competitor B', 'Competitor C']
        response_times = [
            perf_data.get('response_time', 800),
            650,  # Competitor A
            920,  # Competitor B
            480   # Competitor C
        ]

        colors = ['#4CAF50' if rt < 500 else '#FFC107' if rt < 1000 else '#F44336' for rt in response_times]

        fig = go.Figure(data=[
            go.Bar(
                x=competitors,
                y=response_times,
                marker_color=colors,
                text=[f'{rt}ms' for rt in response_times],
                textposition='auto'
            )
        ])

        fig.update_layout(
            title="Performance vs Competitors",
            xaxis_title="Site",
            yaxis_title="Response Time (ms)",
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def _create_revenue_projection_chart(current_revenue, potential_revenue):
        """Create revenue projection chart"""
        import plotly.graph_objects as go

        months = ['Current', 'Month 1', 'Month 2', 'Month 3', 'Month 6', 'Month 12']
        current_values = [current_revenue] * len(months)
        projected_values = []

        # Gradual improvement over time
        for i, month in enumerate(months):
            if i == 0:
                projected_values.append(current_revenue)
            else:
                improvement_rate = min(0.8, i * 0.1)  # Gradual improvement
                projected = current_revenue + (potential_revenue - current_revenue) * improvement_rate
                projected_values.append(projected)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=months,
            y=current_values,
            mode='lines',
            name='Current Performance',
            line=dict(color='#F44336', dash='dash')
        ))

        fig.add_trace(go.Scatter(
            x=months,
            y=projected_values,
            mode='lines+markers',
            name='Projected Performance',
            line=dict(color='#4CAF50')
        ))

        fig.update_layout(
            title="Revenue Projection with Improvements",
            xaxis_title="Time",
            yaxis_title="Monthly Revenue ($)",
            height=300
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def _create_technical_health_chart(health_components):
        """Create technical health breakdown chart"""
        import plotly.graph_objects as go

        components = list(health_components.keys())
        scores = [comp['score'] for comp in health_components.values()]

        colors = ['#4CAF50' if score >= 80 else '#FFC107' if score >= 60 else '#F44336' for score in scores]

        fig = go.Figure(data=[
            go.Bar(
                x=components,
                y=scores,
                marker_color=colors,
                text=[f'{score:.1f}%' for score in scores],
                textposition='auto'
            )
        ])

        fig.update_layout(
            title="Technical Health Breakdown",
            xaxis_title="Component",
            yaxis_title="Health Score (%)",
            height=300,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)

    @staticmethod
    def _create_mobile_desktop_chart(desktop_score, mobile_score):
        """Create mobile vs desktop comparison chart"""
        import plotly.graph_objects as go

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=['Desktop', 'Mobile'],
            y=[desktop_score, mobile_score],
            marker_color=['#4CAF50', '#2196F3'],
            text=[f'{desktop_score}%', f'{mobile_score}%'],
            textposition='auto'
        ))

        fig.update_layout(
            title="Desktop vs Mobile Performance",
            yaxis_title="Performance Score (%)",
            height=300,
            showlegend=False
        )

        st.plotly_chart(fig, use_container_width=True)
    
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
