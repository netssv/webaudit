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
    def generate_marketing_audit_insights(audit_data):
        """Generate comprehensive marketing audit insights as a digital marketing auditor"""
        if not audit_data:
            return "No audit data available for marketing analysis."

        insights = []
        url = audit_data.get('url', 'Unknown')

        # Executive Summary
        insights.append(f"🎯 **DIGITAL MARKETING AUDIT REPORT** - {url}")
        insights.append("")

        # 1. PERFORMANCE & CONVERSION ANALYSIS
        if 'performance' in audit_data and audit_data['performance']:
            perf = audit_data['performance']
            if isinstance(perf, dict) and 'error' not in perf:
                response_time = perf.get('response_time', 0)
                status_code = perf.get('status_code', 200)

                insights.append("⚡ **PERFORMANCE & CONVERSION INSIGHTS**")

                # Speed Analysis
                if response_time > 3000:
                    insights.append(f"🚨 CRITICAL: Slow loading ({response_time}ms) - Implement caching, CDN, image optimization")
                elif response_time > 2000:
                    insights.append(f"⚠️ WARNING: Moderate loading time ({response_time}ms) - Optimize images, minify code")
                else:
                    insights.append(f"✅ GOOD: Fast loading ({response_time}ms) - Maintain current optimizations")

                # Core Web Vitals Analysis
                if 'metrics' in perf:
                    metrics = perf['metrics']
                    lcp = metrics.get('largest_contentful_paint', 0)
                    fid = metrics.get('first_input_delay', 0)
                    cls = metrics.get('cumulative_layout_shift', 0)

                    if lcp > 2.5:
                        insights.append("🚨 POOR LCP: Large content takes too long to load - Optimize hero images, server response")
                    elif lcp > 1.5:
                        insights.append("⚠️ NEEDS IMPROVEMENT: LCP could be faster - Consider image optimization")

                    if fid > 100:
                        insights.append("🚨 POOR FID: Slow interactivity - Reduce JavaScript execution, optimize event handlers")
                    elif fid > 50:
                        insights.append("⚠️ NEEDS IMPROVEMENT: FID could be better - Minimize main thread work")

                    if cls > 0.1:
                        insights.append("🚨 POOR CLS: Layout shifts - Fix unstable elements, reserve space for dynamic content")
                    elif cls > 0.05:
                        insights.append("⚠️ NEEDS IMPROVEMENT: CLS could be more stable - Reserve space for images/ads")

                # Conversion Impact
                insights.append("💰 **CONVERSION IMPACT**: Fast sites convert 2-3x better. Focus on mobile optimization.")
                insights.append("")

        # 2. SEO & MARKETING ANALYSIS
        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']
            if isinstance(seo, dict) and 'error' not in seo:
                insights.append("🎯 **SEO & DIGITAL MARKETING ANALYSIS**")

                # Title & Meta Analysis
                title = seo.get('title', '')
                meta_desc = seo.get('meta_description', '')

                if len(str(title)) < 30:
                    insights.append("🚨 SEO ISSUE: Title too short - Should be 50-60 characters for better CTR")
                elif len(str(title)) > 60:
                    insights.append("⚠️ SEO WARNING: Title too long - May get truncated in search results")

                if len(str(meta_desc)) < 120:
                    insights.append("🚨 SEO ISSUE: Meta description too short - Should be 150-160 characters")
                elif len(str(meta_desc)) > 160:
                    insights.append("⚠️ SEO WARNING: Meta description too long - May get truncated")

                # Content Analysis
                word_count = seo.get('word_count', 0)
                if word_count < 300:
                    insights.append("🚨 CONTENT ISSUE: Page too short for SEO - Aim for 300+ words")
                elif word_count > 2000:
                    insights.append("⚠️ CONTENT WARNING: Very long page - Consider breaking into sections")

                # Social Media Presence
                social_links = seo.get('social_media_links', {})
                if not social_links:
                    insights.append("🚨 SOCIAL ISSUE: No social media links found - Add social proof and sharing options")
                elif len(social_links) < 3:
                    insights.append("⚠️ SOCIAL WARNING: Limited social presence - Expand to major platforms")

                # Marketing Tools Detection
                marketing_tools = seo.get('marketing_tools', [])
                if not marketing_tools:
                    insights.append("🚨 ANALYTICS ISSUE: No marketing/analytics tools detected - Implement Google Analytics, Search Console")
                else:
                    insights.append(f"✅ ANALYTICS: {len(marketing_tools)} marketing tools detected")

                insights.append("")

        # 3. SECURITY & TRUST ANALYSIS
        if 'ssl' in audit_data and audit_data['ssl']:
            ssl = audit_data['ssl']
            if isinstance(ssl, dict) and 'error' not in ssl:
                insights.append("🔒 **SECURITY & TRUST ANALYSIS**")

                ssl_valid = ssl.get('ssl_valid', False)
                ssl_grade = ssl.get('ssl_grade', 'F')

                if not ssl_valid:
                    insights.append("🚨 SECURITY ISSUE: Invalid SSL certificate - Implement HTTPS immediately")
                else:
                    insights.append(f"✅ SSL: Valid certificate (Grade: {ssl_grade})")

                insights.append("🔐 **TRUST SIGNALS**: SSL builds customer confidence and improves conversions")
                insights.append("")

        # 4. DNS & INFRASTRUCTURE ANALYSIS
        if 'dns' in audit_data and audit_data['dns']:
            dns = audit_data['dns']
            if isinstance(dns, dict) and 'error' not in dns:
                insights.append("🌐 **DNS & INFRASTRUCTURE ANALYSIS**")

                # DNS Records
                a_records = dns.get('a_records', [])
                if not a_records:
                    insights.append("🚨 DNS ISSUE: No A records found - Website may not be accessible")
                else:
                    insights.append(f"✅ DNS: {len(a_records)} A records configured")

                # DNS Performance
                dns_perf = dns.get('dns_server_performance', [])
                if dns_perf:
                    successful_times = [r.get('response_time_ms', 0) for r in dns_perf if r.get('status') == 'success']
                    if successful_times:
                        avg_dns_time = sum(successful_times) / len(successful_times)
                        if avg_dns_time > 100:
                            insights.append(f"🚨 DNS PERFORMANCE: Slow DNS resolution ({avg_dns_time:.1f}ms) - Consider faster DNS provider")
                        else:
                            insights.append(f"✅ DNS PERFORMANCE: Fast resolution ({avg_dns_time:.1f}ms)")

                insights.append("")

        # 5. AUTHORITY & BACKLINK ANALYSIS
        if 'ranking' in audit_data and audit_data['ranking']:
            ranking = audit_data['ranking']
            if isinstance(ranking, dict) and 'error' not in ranking:
                insights.append("📈 **AUTHORITY & COMPETITIVE ANALYSIS**")

                da = ranking.get('domain_authority', 0)
                pa = ranking.get('page_authority', 0)
                backlinks = ranking.get('backlinks', 0)

                if da < 20:
                    insights.append(f"🚨 AUTHORITY ISSUE: Low Domain Authority ({da}) - Focus on quality backlinks and content")
                elif da < 40:
                    insights.append(f"⚠️ AUTHORITY WARNING: Moderate DA ({da}) - Continue building authority")
                else:
                    insights.append(f"✅ AUTHORITY: Strong Domain Authority ({da}) - Maintain link building efforts")

                if backlinks < 100:
                    insights.append(f"🚨 BACKLINKS ISSUE: Very few backlinks ({backlinks}) - Implement link building strategy")
                elif backlinks < 1000:
                    insights.append(f"⚠️ BACKLINKS WARNING: Limited backlinks ({backlinks}) - Expand outreach efforts")
                else:
                    insights.append(f"✅ BACKLINKS: Good backlink profile ({backlinks}) - Monitor and maintain")

                insights.append("")

        # 6. PRIORITIZED RECOMMENDATIONS
        insights.append("🎯 **PRIORITY RECOMMENDATIONS**")
        insights.append("")

        # High Priority Issues
        high_priority = []
        if 'performance' in audit_data and audit_data['performance']:
            perf = audit_data['performance']
            if perf.get('response_time', 0) > 3000:
                high_priority.append("🚨 HIGH: Optimize loading speed (currently >3s)")
            if 'metrics' in perf:
                metrics = perf['metrics']
                if metrics.get('largest_contentful_paint', 0) > 2.5:
                    high_priority.append("🚨 HIGH: Fix Largest Contentful Paint (>2.5s)")

        if 'ssl' in audit_data and audit_data['ssl']:
            ssl = audit_data['ssl']
            if not ssl.get('ssl_valid', True):
                high_priority.append("🚨 HIGH: Fix SSL certificate issues")

        if high_priority:
            insights.append("**🔴 HIGH PRIORITY:**")
            for item in high_priority:
                insights.append(f"• {item}")
            insights.append("")

        # Medium Priority Issues
        medium_priority = []
        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']
            if len(str(seo.get('title', ''))) < 30:
                medium_priority.append("⚠️ MEDIUM: Improve page title length")
            if len(str(seo.get('meta_description', ''))) < 120:
                medium_priority.append("⚠️ MEDIUM: Enhance meta description")

        if medium_priority:
            insights.append("**🟡 MEDIUM PRIORITY:**")
            for item in medium_priority:
                insights.append(f"• {item}")
            insights.append("")

        # Business Impact Summary
        insights.append("💼 **BUSINESS IMPACT SUMMARY**")
        insights.append("• **Revenue Potential**: Fast, secure sites convert 2-3x better")
        insights.append("• **SEO Benefits**: Proper optimization can increase organic traffic by 200-500%")
        insights.append("• **Trust & Credibility**: SSL and good UX build customer confidence")
        insights.append("• **Competitive Advantage**: Technical excellence differentiates from competitors")

        return "\n".join(insights)
    
    @staticmethod
    def display_ai_analysis(audit_data):
        """Display AI analysis section with ChatGPT integration"""
        st.markdown("### 🤖 AI Analysis")
        
        if not audit_data:
            st.warning("⚠️ No audit data available for AI analysis")
            return
        
        # Generate comprehensive marketing audit insights
        insights = AIAnalysisComponents.generate_marketing_audit_insights(audit_data)
        
        # Display insights section
        st.markdown("#### 📊 Marketing Audit Insights")

        # Show insights in an expandable section
        with st.expander("View Complete Marketing Audit Report", expanded=False):
            st.markdown(insights)
            
        # ChatGPT Integration Section
        st.markdown("#### Get AI Insights")
        
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
                <strong>🤖 Get AI-Powered Marketing Insights</strong><br>
                Click the button below to open ChatGPT with your comprehensive marketing audit report.
                Get professional recommendations for SEO, conversion optimization, security, and performance improvements.
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Create a professional ChatGPT prompt with full marketing audit
            full_audit_insights = AIAnalysisComponents.generate_marketing_audit_insights(audit_data)
            chatgpt_prompt = f"""As a senior digital marketing auditor and technical SEO expert, please analyze this comprehensive website audit and provide strategic recommendations:

COMPREHENSIVE AUDIT DATA:
{full_audit_insights}

Please provide:
1. 🔍 Critical Issues & Immediate Actions Required
2. 📈 SEO & Marketing Optimization Strategy  
3. ⚡ Performance & Technical Improvements
4. 💰 Conversion Rate Optimization Recommendations
5. 🔒 Security & Trust Enhancement Suggestions
6. 📊 Priority Implementation Roadmap with Timeline
7. 🎯 Competitive Advantage Opportunities

Focus on actionable insights that drive measurable business results."""

            # URL encode the prompt
            import urllib.parse
            encoded_prompt = urllib.parse.quote(chatgpt_prompt)

            # Check URL length and truncate if necessary
            max_url_length = 2000  # Safe limit for most browsers
            if len(f"https://chat.openai.com/?q={encoded_prompt}") > max_url_length:
                # Truncate the prompt if too long
                truncated_prompt = chatgpt_prompt[:1000] + "..."
                encoded_prompt = urllib.parse.quote(truncated_prompt)

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
                    🚀 Get Marketing Insights
                </button>
            </a>
            """, unsafe_allow_html=True)
        if 'performance' in audit_data and audit_data['performance']:
            perf = audit_data['performance']
            if isinstance(perf, dict) and 'error' not in perf:
                response_time = perf.get('response_time', 0)
                status_code = perf.get('status_code', 200)

                insights.append("⚡ **PERFORMANCE & CONVERSION INSIGHTS**")

                # Speed Analysis
                if response_time > 3000:
                    insights.append(f"🚨 CRITICAL: Slow loading ({response_time}ms) - Implement caching, CDN, image optimization")
                elif response_time > 2000:
                    insights.append(f"⚠️ WARNING: Moderate loading time ({response_time}ms) - Optimize images, minify code")
                else:
                    insights.append(f"✅ GOOD: Fast loading ({response_time}ms) - Maintain current optimizations")

                # Core Web Vitals Analysis
                if 'metrics' in perf:
                    metrics = perf['metrics']
                    lcp = metrics.get('largest_contentful_paint', 0)
                    fid = metrics.get('first_input_delay', 0)
                    cls = metrics.get('cumulative_layout_shift', 0)

                    if lcp > 2.5:
                        insights.append("🚨 POOR LCP: Large content takes too long to load - Optimize hero images, server response")
                    elif lcp > 1.5:
                        insights.append("⚠️ NEEDS IMPROVEMENT: LCP could be faster - Consider image optimization")

                    if fid > 100:
                        insights.append("🚨 POOR FID: Slow interactivity - Reduce JavaScript execution, optimize event handlers")
                    elif fid > 50:
                        insights.append("⚠️ NEEDS IMPROVEMENT: FID could be better - Minimize main thread work")

                    if cls > 0.1:
                        insights.append("🚨 POOR CLS: Layout shifts - Fix unstable elements, reserve space for dynamic content")
                    elif cls > 0.05:
                        insights.append("⚠️ NEEDS IMPROVEMENT: CLS could be more stable - Reserve space for images/ads")

                # Conversion Impact
                insights.append("💰 **CONVERSION IMPACT**: Fast sites convert 2-3x better. Focus on mobile optimization.")
                insights.append("")

        # 2. SEO & MARKETING ANALYSIS
        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']
            if isinstance(seo, dict) and 'error' not in seo:
                insights.append("🎯 **SEO & DIGITAL MARKETING ANALYSIS**")

                # Title & Meta Analysis
                title = seo.get('title', '')
                meta_desc = seo.get('meta_description', '')

                if len(str(title)) < 30:
                    insights.append("🚨 SEO ISSUE: Title too short - Should be 50-60 characters for better CTR")
                elif len(str(title)) > 60:
                    insights.append("⚠️ SEO WARNING: Title too long - May get truncated in search results")

                if len(str(meta_desc)) < 120:
                    insights.append("🚨 SEO ISSUE: Meta description too short - Should be 150-160 characters")
                elif len(str(meta_desc)) > 160:
                    insights.append("⚠️ SEO WARNING: Meta description too long - May get truncated")

                # Content Analysis
                word_count = seo.get('word_count', 0)
                if word_count < 300:
                    insights.append("🚨 CONTENT ISSUE: Page too short for SEO - Aim for 300+ words")
                elif word_count > 2000:
                    insights.append("⚠️ CONTENT WARNING: Very long page - Consider breaking into sections")

                # Social Media Presence
                social_links = seo.get('social_media_links', {})
                if not social_links:
                    insights.append("🚨 SOCIAL ISSUE: No social media links found - Add social proof and sharing options")
                elif len(social_links) < 3:
                    insights.append("⚠️ SOCIAL WARNING: Limited social presence - Expand to major platforms")

                # Marketing Tools Detection
                marketing_tools = seo.get('marketing_tools', [])
                if not marketing_tools:
                    insights.append("🚨 ANALYTICS ISSUE: No marketing/analytics tools detected - Implement Google Analytics, Search Console")
                else:
                    insights.append(f"✅ ANALYTICS: {len(marketing_tools)} marketing tools detected")

                insights.append("")

        # 3. SECURITY & TRUST ANALYSIS
        if 'ssl' in audit_data and audit_data['ssl']:
            ssl = audit_data['ssl']
            if isinstance(ssl, dict) and 'error' not in ssl:
                insights.append("🔒 **SECURITY & TRUST ANALYSIS**")

                ssl_valid = ssl.get('ssl_valid', False)
                ssl_grade = ssl.get('ssl_grade', 'F')

                if not ssl_valid:
                    insights.append("🚨 CRITICAL SECURITY: Invalid SSL certificate - Users will see security warnings")
                elif ssl_grade in ['F', 'E', 'D']:
                    insights.append(f"🚨 SECURITY ISSUE: Poor SSL grade ({ssl_grade}) - Upgrade certificate and configuration")
                elif ssl_grade in ['C', 'B']:
                    insights.append(f"⚠️ SECURITY WARNING: SSL grade could be better ({ssl_grade}) - Consider upgrading")
                else:
                    insights.append(f"✅ SECURITY: Good SSL grade ({ssl_grade}) - Maintain current security practices")

                # Trust Signals
                insights.append("🛡️ **TRUST SIGNALS**: SSL is critical for conversions. Consider trust badges, reviews, guarantees.")
                insights.append("")

        # 4. TECHNICAL INFRASTRUCTURE ANALYSIS
        if 'dns' in audit_data and audit_data['dns']:
            dns = audit_data['dns']
            if isinstance(dns, dict) and 'error' not in dns:
                insights.append("🌐 **TECHNICAL INFRASTRUCTURE ANALYSIS**")

                a_records = len(dns.get('a_records', [])) if isinstance(dns.get('a_records', []), list) else 0
                mx_records = len(dns.get('mx_records', [])) if isinstance(dns.get('mx_records', []), list) else 0

                if a_records == 0:
                    insights.append("🚨 DNS ISSUE: No A records found - Domain not properly configured")
                elif a_records > 1:
                    insights.append(f"ℹ️ DNS INFO: Multiple A records ({a_records}) - Ensure load balancing is working")

                if mx_records == 0:
                    insights.append("🚨 EMAIL ISSUE: No MX records - Email delivery may fail")
                else:
                    insights.append(f"✅ EMAIL: {mx_records} MX records configured")

                # DNS Performance
                dns_perf = dns.get('dns_server_performance', [])
                if dns_perf:
                    successful_times = [r.get('response_time_ms', 0) for r in dns_perf if r.get('status') == 'success']
                    if successful_times:
                        avg_dns_time = sum(successful_times) / len(successful_times)
                        if avg_dns_time > 100:
                            insights.append(f"🚨 DNS PERFORMANCE: Slow DNS resolution ({avg_dns_time:.1f}ms) - Consider faster DNS provider")
                        else:
                            insights.append(f"✅ DNS PERFORMANCE: Fast resolution ({avg_dns_time:.1f}ms)")

                insights.append("")

        # 5. AUTHORITY & BACKLINK ANALYSIS
        if 'ranking' in audit_data and audit_data['ranking']:
            ranking = audit_data['ranking']
            if isinstance(ranking, dict) and 'error' not in ranking:
                insights.append("📈 **AUTHORITY & COMPETITIVE ANALYSIS**")

                da = ranking.get('domain_authority', 0)
                pa = ranking.get('page_authority', 0)
                backlinks = ranking.get('backlinks', 0)

                if da < 20:
                    insights.append(f"🚨 AUTHORITY ISSUE: Low Domain Authority ({da}) - Focus on quality backlinks and content")
                elif da < 40:
                    insights.append(f"⚠️ AUTHORITY WARNING: Moderate DA ({da}) - Continue building authority")
                else:
                    insights.append(f"✅ AUTHORITY: Strong Domain Authority ({da}) - Maintain link building efforts")

                if backlinks < 100:
                    insights.append(f"🚨 BACKLINKS ISSUE: Very few backlinks ({backlinks}) - Implement link building strategy")
                elif backlinks < 1000:
                    insights.append(f"⚠️ BACKLINKS WARNING: Limited backlinks ({backlinks}) - Expand outreach efforts")
                else:
                    insights.append(f"✅ BACKLINKS: Good backlink profile ({backlinks}) - Monitor and maintain")

                insights.append("")

        # 6. PRIORITIZED RECOMMENDATIONS
        insights.append("🎯 **PRIORITY RECOMMENDATIONS**")
        insights.append("")

        # High Priority Issues
        high_priority = []
        if 'performance' in audit_data and audit_data['performance']:
            perf = audit_data['performance']
            if perf.get('response_time', 0) > 3000:
                high_priority.append("🚨 HIGH: Optimize loading speed (currently >3s)")
            if 'metrics' in perf:
                metrics = perf['metrics']
                if metrics.get('largest_contentful_paint', 0) > 2.5:
                    high_priority.append("🚨 HIGH: Fix Largest Contentful Paint (>2.5s)")

        if 'ssl' in audit_data and audit_data['ssl']:
            ssl = audit_data['ssl']
            if not ssl.get('ssl_valid', True):
                high_priority.append("🚨 HIGH: Fix SSL certificate issues")

        if high_priority:
            insights.append("**🔴 HIGH PRIORITY:**")
            for item in high_priority:
                insights.append(f"• {item}")
            insights.append("")

        # Medium Priority Issues
        medium_priority = []
        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']
            if len(str(seo.get('title', ''))) < 30:
                medium_priority.append("⚠️ MEDIUM: Improve page title length")
            if len(str(seo.get('meta_description', ''))) < 120:
                medium_priority.append("⚠️ MEDIUM: Enhance meta description")

        if medium_priority:
            insights.append("**🟡 MEDIUM PRIORITY:**")
            for item in medium_priority:
                insights.append(f"• {item}")
            insights.append("")

        # Business Impact Summary
        insights.append("💼 **BUSINESS IMPACT SUMMARY**")
        insights.append("• **Revenue Potential**: Fast, secure sites convert 2-3x better")
        insights.append("• **SEO Benefits**: Proper optimization can increase organic traffic by 200-500%")
        insights.append("• **Trust & Credibility**: SSL and good UX build customer confidence")
        insights.append("• **Competitive Advantage**: Technical excellence differentiates from competitors")

        return "\n".join(insights)
    
    @staticmethod
    def display_ai_analysis(audit_data):
        """Display AI analysis section with ChatGPT integration"""
        st.markdown("### 🤖 AI Analysis")
        
        if not audit_data:
            st.warning("⚠️ No audit data available for AI analysis")
            return
        
        # Generate comprehensive marketing audit insights
        insights = AIAnalysisComponents.generate_marketing_audit_insights(audit_data)
        
        # Display insights section
        st.markdown("#### 📊 Marketing Audit Insights")

        # Show insights in an expandable section
        with st.expander("View Complete Marketing Audit Report", expanded=False):
            st.markdown(insights)        # ChatGPT Integration Section
        st.markdown("#### Get AI Insights")
        
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
                <strong>🤖 Get AI-Powered Marketing Insights</strong><br>
                Click the button below to open ChatGPT with your comprehensive marketing audit report.
                Get professional recommendations for SEO, conversion optimization, security, and performance improvements.
            </div>
            """, unsafe_allow_html=True)

        with col2:
            # Create a professional ChatGPT prompt with full marketing audit
            full_audit_insights = AIAnalysisComponents.generate_marketing_audit_insights(audit_data)
            chatgpt_prompt = f"""As a senior digital marketing auditor and technical SEO expert, please analyze this comprehensive website audit and provide strategic recommendations:

COMPREHENSIVE AUDIT DATA:
{full_audit_insights}

Please provide:
1. 🔍 Critical Issues & Immediate Actions Required
2. 📈 SEO & Marketing Optimization Strategy  
3. ⚡ Performance & Technical Improvements
4. 💰 Conversion Rate Optimization Recommendations
5. 🔒 Security & Trust Enhancement Suggestions
6. 📊 Priority Implementation Roadmap with Timeline
7. 🎯 Competitive Advantage Opportunities

Focus on actionable insights that drive measurable business results."""

            # URL encode the prompt
            import urllib.parse
            encoded_prompt = urllib.parse.quote(chatgpt_prompt)

            # Check URL length and truncate if necessary
            max_url_length = 2000  # Safe limit for most browsers
            if len(f"https://chat.openai.com/?q={encoded_prompt}") > max_url_length:
                # Truncate the prompt if too long
                truncated_prompt = chatgpt_prompt[:1000] + "..."
                encoded_prompt = urllib.parse.quote(truncated_prompt)

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
                    🚀 Get Marketing Insights
                </button>
            </a>
            """, unsafe_allow_html=True)








        st.info("� **Pro Tip**: Select all the text above (Ctrl+A) and copy it (Ctrl+C) to share with your team or use in other tools.")
    
    @staticmethod
    def display_raw_data_only(audit_data):
        """Display raw audit data in a formatted way with optimized state management"""
        st.markdown("### 📄 Raw Audit Data")
        
        if not audit_data:
            st.warning("⚠️ No raw data available")
            return
        
        # Add a note about tab behavior
        st.info("💡 **Tip**: This tab shows complete audit data. Use the expanders below to view different sections.")
        
        # Display raw data in expandable sections (these don't cause full reruns)
        for section, data in audit_data.items():
            if data and section != 'url':
                with st.expander(f"{section.replace('_', ' ').title()} Data", expanded=False):
                    if isinstance(data, dict):
                        st.json(data)
                    else:
                        st.write(data)
        
        # Export section with stable keys
        st.markdown("---")
        st.markdown("#### 📥 Export Options")
        
        # Use stable keys to prevent unnecessary reruns
        if 'export_keys' not in st.session_state:
            st.session_state.export_keys = {}
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Generate download button with unique key based on timestamp
            json_data = json.dumps(audit_data, indent=2, default=str)
            download_key = f"raw_data_download_{hash(str(audit_data)[:50])}_{datetime.now().strftime('%H%M%S')}"
            
            st.download_button(
                label="📥 Download Complete JSON",
                data=json_data,
                file_name=f"web_audit_complete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                key=download_key,
                use_container_width=True,
                type="primary",
                help="Download the complete audit data as JSON file"
            )
        
        with col2:
            # JSON preview section
            with st.expander("� JSON Preview (Copy Manually)", expanded=False):
                st.code(json_data, language="json")
                st.info("💡 Select the JSON text above and use Ctrl+C (Cmd+C on Mac) to copy")

    @staticmethod
    def _generate_conversion_focused_analysis(audit_data):
        """Generate conversion-focused analysis for CRO specialists"""
        if not audit_data:
            return "No data available for conversion analysis."

        analysis = ["🎯 CONVERSION RATE OPTIMIZATION ANALYSIS", ""]

        # Performance Impact on Conversions
        if 'performance' in audit_data and audit_data['performance']:
            perf = audit_data['performance']
            response_time = perf.get('response_time', 0)

            if response_time > 3000:
                analysis.append("🚨 CRITICAL: Loading speed >3s reduces conversions by 50-70%")
                analysis.append("   • SOLUTION: Implement caching, CDN, image optimization")
            elif response_time > 2000:
                analysis.append("⚠️ WARNING: Loading speed >2s reduces conversions by 20-30%")
                analysis.append("   • SOLUTION: Optimize images, minify CSS/JS")

            # Core Web Vitals for UX
            if 'metrics' in perf:
                metrics = perf['metrics']
                cls = metrics.get('cumulative_layout_shift', 0)
                if cls > 0.1:
                    analysis.append("🚨 CRO ISSUE: Layout shifts annoy users and hurt conversions")
                    analysis.append("   • SOLUTION: Reserve space for dynamic content, fix unstable elements")

        # Trust & Credibility Factors
        if 'ssl' in audit_data and audit_data['ssl']:
            ssl = audit_data['ssl']
            if not ssl.get('ssl_valid', True):
                analysis.append("🚨 TRUST ISSUE: Invalid SSL shows security warnings")
                analysis.append("   • IMPACT: Users abandon immediately, 0% conversion potential")
                analysis.append("   • SOLUTION: Install valid SSL certificate immediately")

        # Content & UX Analysis
        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']
            word_count = seo.get('word_count', 0)

            if word_count < 300:
                analysis.append("🚨 CONTENT ISSUE: Page too short for conversion optimization")
                analysis.append("   • SOLUTION: Add compelling copy, social proof, clear CTAs")

            # Check for conversion elements
            if 'marketing_tools' in seo:
                tools = seo['marketing_tools']
                # Handle both string and dict formats for marketing tools
                if tools and isinstance(tools[0], dict):
                    # New format: list of dicts with 'name' key
                    tool_names = [str(tool.get('name', '')) for tool in tools if tool and isinstance(tool, dict)]
                else:
                    # Legacy format: list of strings
                    tool_names = [str(tool) for tool in tools if tool is not None]
                
                has_analytics = any('analytics' in name.lower() or 'gtag' in name.lower() for name in tool_names)
                if not has_analytics:
                    analysis.append("⚠️ TRACKING ISSUE: No conversion tracking detected")
                    analysis.append("   • SOLUTION: Implement Google Analytics 4, conversion goals")

        analysis.append("")
        analysis.append("💡 KEY CRO PRINCIPLES:")
        analysis.append("• Fast sites convert 2-3x better than slow ones")
        analysis.append("• Trust signals (SSL, reviews) increase conversions by 20-30%")
        analysis.append("• Clear CTAs and compelling copy drive action")
        analysis.append("• Mobile optimization is critical (60%+ of traffic)")

        return "\n".join(analysis)

    @staticmethod
    def _generate_seo_strategy_analysis(audit_data):
        """Generate SEO strategy analysis for content marketers"""
        if not audit_data:
            return "No data available for SEO strategy analysis."

        analysis = ["🎯 SEO & CONTENT MARKETING STRATEGY ANALYSIS", ""]

        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']

            # Title & Meta Strategy
            title = seo.get('title', '')
            meta_desc = seo.get('meta_description', '')

            analysis.append("📝 ON-PAGE SEO STRATEGY:")

            if len(str(title)) < 30:
                analysis.append("🚨 TITLE ISSUE: Too short for search visibility")
                analysis.append("   • STRATEGY: Include primary keyword + benefit/value prop")
                analysis.append("   • EXAMPLE: 'Best SEO Tools 2024: Boost Rankings by 300%'")
            elif len(str(title)) > 60:
                analysis.append("⚠️ TITLE WARNING: May get truncated in search results")
                analysis.append("   • STRATEGY: Keep under 60 chars, focus on key terms")

            if len(str(meta_desc)) < 120:
                analysis.append("🚨 META DESC ISSUE: Too short for CTR optimization")
                analysis.append("   • STRATEGY: Include keyword + compelling call-to-action")
                analysis.append("   • EXAMPLE: 'Discover top SEO tools that increased our rankings by 300%. Free trial available.'")

            # Content Strategy
            word_count = seo.get('word_count', 0)
            if word_count < 300:
                analysis.append("🚨 CONTENT ISSUE: Too short for comprehensive topic coverage")
                analysis.append("   • STRATEGY: Create pillar content (1500-2500 words)")
                analysis.append("   • BENEFIT: Higher rankings, more backlinks, authority")

            # Social Media Strategy
            social_links = seo.get('social_media_links', {})
            if not social_links:
                analysis.append("🚨 SOCIAL ISSUE: No social signals for SEO")
                analysis.append("   • STRATEGY: Add social sharing buttons, create shareable content")
                analysis.append("   • BENEFIT: Increased visibility, backlinks, engagement")

        # Authority & Link Building Strategy
        if 'ranking' in audit_data and audit_data['ranking']:
            ranking = audit_data['ranking']
            backlinks = ranking.get('backlinks', 0)
            da = ranking.get('domain_authority', 0)

            analysis.append("")
            analysis.append("🔗 LINK BUILDING & AUTHORITY STRATEGY:")

            if backlinks < 100:
                analysis.append("🚨 BACKLINK ISSUE: Insufficient link profile")
                analysis.append("   • STRATEGY: Guest posting, resource pages, broken link building")
                analysis.append("   • GOAL: 100+ quality backlinks in 6 months")

            if da < 30:
                analysis.append("⚠️ AUTHORITY ISSUE: Low domain authority")
                analysis.append("   • STRATEGY: Create cornerstone content, earn editorial links")
                analysis.append("   • FOCUS: Quality over quantity, relevant industries")

        analysis.append("")
        analysis.append("📈 CONTENT MARKETING ROADMAP:")
        analysis.append("1. Keyword Research: Use Ahrefs, SEMrush for target keywords")
        analysis.append("2. Content Creation: Pillar pages + cluster content model")
        analysis.append("3. Technical SEO: Core Web Vitals, site speed, mobile-first")
        analysis.append("4. Link Building: Guest posts, partnerships, digital PR")
        analysis.append("5. Monitoring: Track rankings, traffic, conversions monthly")

        return "\n".join(analysis)

    @staticmethod
    def _generate_security_trust_analysis(audit_data):
        """Generate security and trust analysis for business owners"""
        if not audit_data:
            return "No data available for security analysis."

        analysis = ["🔒 SECURITY & TRUST ANALYSIS", ""]

        # SSL Security Analysis
        if 'ssl' in audit_data and audit_data['ssl']:
            ssl = audit_data['ssl']
            ssl_valid = ssl.get('ssl_valid', False)
            ssl_grade = ssl.get('ssl_grade', 'F')

            analysis.append("🛡️ SSL SECURITY STATUS:")

            if not ssl_valid:
                analysis.append("🚨 CRITICAL: Invalid SSL certificate")
                analysis.append("   • BUSINESS IMPACT: Users see security warnings, abandon site")
                analysis.append("   • CONVERSION LOSS: 70%+ of visitors leave immediately")
                analysis.append("   • SOLUTION: Install valid SSL certificate (Let's Encrypt is free)")
            elif ssl_grade in ['A', 'A+']:
                analysis.append("✅ EXCELLENT: High-grade SSL certificate")
                analysis.append("   • TRUST SIGNAL: Green padlock builds customer confidence")
                analysis.append("   • SEO BENEFIT: Google favors HTTPS sites")
            else:
                analysis.append(f"⚠️ WARNING: SSL grade {ssl_grade} could be better")
                analysis.append("   • RECOMMENDATION: Upgrade to higher-grade certificate")

        # Technical Security Indicators
        analysis.append("")
        analysis.append("🔧 TECHNICAL SECURITY MEASURES:")

        # Check for security headers (if available in data)
        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']
            # This would be expanded with actual security header checks
            analysis.append("• HTTPS Implementation: " + ("✅ Active" if ssl_valid else "❌ Missing"))
            analysis.append("• SSL Certificate: " + (f"Grade {ssl_grade}" if ssl_valid else "❌ Invalid"))

        # Trust Signals Analysis
        analysis.append("")
        analysis.append("🤝 TRUST & CREDIBILITY SIGNALS:")

        trust_signals = []

        # SSL is a trust signal
        if ssl_valid:
            trust_signals.append("✅ SSL Certificate (Security)")
        else:
            trust_signals.append("❌ SSL Certificate (Missing)")

        # Social proof (from SEO data)
        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']
            social_links = seo.get('social_media_links', {})
            if social_links:
                trust_signals.append(f"✅ Social Media Presence ({len(social_links)} platforms)")
            else:
                trust_signals.append("❌ Social Media Presence (Missing)")

        # Authority indicators
        if 'ranking' in audit_data and audit_data['ranking']:
            ranking = audit_data['ranking']
            da = ranking.get('domain_authority', 0)
            if da > 40:
                trust_signals.append(f"✅ High Domain Authority ({da})")
            elif da > 20:
                trust_signals.append(f"⚠️ Moderate Domain Authority ({da})")
            else:
                trust_signals.append(f"❌ Low Domain Authority ({da})")

        for signal in trust_signals:
            analysis.append(f"• {signal}")

        # Business Impact
        analysis.append("")
        analysis.append("💼 BUSINESS IMPACT OF SECURITY:")
        analysis.append("• TRUST = CONVERSIONS: Secure sites convert 2-3x better")
        analysis.append("• GOOGLE RANKING: HTTPS is a ranking factor")
        analysis.append("• CUSTOMER CONFIDENCE: Security builds long-term relationships")
        analysis.append("• COMPETITIVE ADVANTAGE: Most sites still lack proper security")

        # Action Items
        analysis.append("")
        analysis.append("🎯 IMMEDIATE ACTION ITEMS:")
        if not ssl_valid:
            analysis.append("1. 🚨 PRIORITY: Install SSL certificate immediately")
            analysis.append("2. 🔒 Update all internal links to HTTPS")
            analysis.append("3. 🛡️ Implement security headers (HSTS, CSP, X-Frame-Options)")
        else:
            analysis.append("1. ✅ SSL: Good foundation, maintain certificate renewal")
            analysis.append("2. 🛡️ Add security headers for additional protection")
            analysis.append("3. 🔍 Regular security audits and monitoring")

        return "\n".join(analysis)
    
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
            # Normalize to names only to avoid printing raw dicts
            names = []
            for t in marketing_tools:
                if isinstance(t, dict):
                    names.append(t.get('name', str(t)))
                else:
                    names.append(str(t))
            summary_parts.append(f"Marketing Tools: {', '.join(names)}")
        
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

    @staticmethod
    def _generate_concise_summary_for_chatgpt(audit_data):
        """Generate a concise summary optimized for ChatGPT URL (under 1000 chars)"""
        if not audit_data:
            return "No audit data available for analysis."

        summary_parts = []
        url = audit_data.get('url', 'Unknown')

        # Professional header
        summary_parts.append(f"🌐 WEBSITE AUDIT: {url}")

        # Performance metrics
        if 'performance' in audit_data and audit_data['performance']:
            perf = audit_data['performance']
            if isinstance(perf, dict) and 'error' not in perf:
                response_time = perf.get('response_time', 0)
                status_code = perf.get('status_code', 200)
                page_size = perf.get('page_size', 0)
                summary_parts.append(f"⚡ PERFORMANCE: {response_time}ms load time, HTTP {status_code}, {page_size} bytes")

                # Core Web Vitals
                if 'metrics' in perf:
                    metrics = perf['metrics']
                    lcp = metrics.get('largest_contentful_paint', 0)
                    if lcp > 0:
                        summary_parts.append(f"📊 CORE WEB VITALS: LCP {lcp}s")

        # SEO & Marketing
        if 'seo_marketing' in audit_data and audit_data['seo_marketing']:
            seo = audit_data['seo_marketing']
            if isinstance(seo, dict) and 'error' not in seo:
                title = seo.get('title', '')[:40] if seo.get('title') else 'Missing'
                score = seo.get('overall_score', seo.get('seo_score', 0))
                word_count = seo.get('word_count', 0)
                summary_parts.append(f"🎯 SEO: Score {score}%, Title '{title}...', {word_count} words")

                # Social media
                social_links = seo.get('social_media_links', {})
                if social_links:
                    platforms = list(social_links.keys())[:3]
                    summary_parts.append(f"📱 SOCIAL: {', '.join(platforms)}")

        # Security
        if 'ssl' in audit_data and audit_data['ssl']:
            ssl = audit_data['ssl']
            if isinstance(ssl, dict) and 'error' not in ssl:
                ssl_valid = ssl.get('ssl_valid', False)
                ssl_grade = ssl.get('ssl_grade', 'F')
                summary_parts.append(f"🔒 SECURITY: SSL {'Valid' if ssl_valid else 'Invalid'} (Grade {ssl_grade})")

        # Authority & Backlinks
        if 'ranking' in audit_data and audit_data['ranking']:
            ranking = audit_data['ranking']
            if isinstance(ranking, dict) and 'error' not in ranking:
                da = ranking.get('domain_authority', 0)
                pa = ranking.get('page_authority', 0)
                backlinks = ranking.get('backlinks', 0)
                summary_parts.append(f"📈 AUTHORITY: DA {da}, PA {pa}, {backlinks} backlinks")

        # DNS
        if 'dns' in audit_data and audit_data['dns']:
            dns = audit_data['dns']
            if isinstance(dns, dict) and 'error' not in dns:
                a_records = len(dns.get('a_records', [])) if isinstance(dns.get('a_records', []), list) else 0
                mx_records = len(dns.get('mx_records', [])) if isinstance(dns.get('mx_records', []), list) else 0
                summary_parts.append(f"🌐 DNS: {a_records} A records, {mx_records} MX records")

        result = " | ".join(summary_parts)

        # Ensure it's under 800 characters for URL safety
        if len(result) > 800:
            result = result[:797] + "..."

        return result
