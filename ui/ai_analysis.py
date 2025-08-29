"""
AI Analysis Module
Contains AI analysis and summary generation functions
"""

import streamlit as st
import json
from datetime import datetime


def json_serializer(obj):
    """JSON serializer for objects not serializable by default"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif hasattr(obj, '__dict__'):
        return obj.__dict__
    else:
        return str(obj)


def generate_comprehensive_summary(domain, audit_results, active_modules):
    """Generate a comprehensive, optimized summary for AI analysis"""
    
    def safe_extract(data, keys, default=None):
        """Safely extract nested dictionary values"""
        try:
            if not isinstance(data, dict):
                return default if default is not None else "N/A"
            current = data
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return default if default is not None else "N/A"
            return current if current is not None else (default if default is not None else "N/A")
        except:
            return default if default is not None else "N/A"
    
    def format_metric(value, unit="", format_type="number"):
        """Format metrics consistently"""
        try:
            if value == "N/A" or value is None:
                return "N/A"
            if format_type == "percentage":
                return f"{float(value):.1f}%"
            elif format_type == "seconds":
                return f"{float(value):.2f}s"
            elif format_type == "size":
                # Convert to KB/MB
                size_mb = float(value) / (1024 * 1024)
                if size_mb >= 1:
                    return f"{size_mb:.1f}MB"
                else:
                    return f"{float(value) / 1024:.1f}KB"
            else:
                return f"{value}{unit}"
        except:
            return str(value)
    
    summary_parts = []
    
    # Domain and timestamp
    summary_parts.append(f"🌐 **Domain Analysis: {domain}**")
    summary_parts.append(f"📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    summary_parts.append(f"🔧 Active Modules: {', '.join(active_modules)}")
    summary_parts.append("")
    
    # Performance Analysis (Priority 1)
    if "performance" in audit_results:
        perf = audit_results["performance"]
        summary_parts.append("⚡ **PERFORMANCE METRICS**")
        
        # Core Web Vitals
        lcp = safe_extract(perf, ["metrics", "largest_contentful_paint"])
        fid = safe_extract(perf, ["metrics", "first_input_delay"])
        cls = safe_extract(perf, ["metrics", "cumulative_layout_shift"])
        
        if lcp != "N/A" or fid != "N/A" or cls != "N/A":
            summary_parts.append("📊 Core Web Vitals:")
            if lcp != "N/A":
                summary_parts.append(f"  • LCP: {format_metric(lcp, 's', 'seconds')}")
            if fid != "N/A":
                summary_parts.append(f"  • FID: {format_metric(fid, 'ms')}")
            if cls != "N/A":
                summary_parts.append(f"  • CLS: {format_metric(cls)}")
        
        # Key Performance Metrics
        load_time = safe_extract(perf, ["metrics", "page_load_time"])
        ttfb = safe_extract(perf, ["metrics", "time_to_first_byte"])
        speed_score = safe_extract(perf, ["lighthouse_score"])
        
        summary_parts.append("🚀 Key Metrics:")
        if load_time != "N/A":
            summary_parts.append(f"  • Load Time: {format_metric(load_time, 's', 'seconds')}")
        if ttfb != "N/A":
            summary_parts.append(f"  • TTFB: {format_metric(ttfb, 'ms')}")
        if speed_score != "N/A":
            summary_parts.append(f"  • Speed Score: {format_metric(speed_score, '/100')}")
        
        # Performance Issues
        issues = safe_extract(perf, ["issues"], [])
        if isinstance(issues, list) and issues:
            summary_parts.append("⚠️  Critical Issues:")
            for issue in issues[:3]:  # Limit to top 3
                if isinstance(issue, dict):
                    issue_text = issue.get('description', str(issue))
                else:
                    issue_text = str(issue)
                summary_parts.append(f"  • {issue_text[:80]}...")
        
        summary_parts.append("")
    
    # SEO Analysis (Priority 2)
    if "seo_marketing" in audit_results:
        seo = audit_results["seo_marketing"]
        summary_parts.append("🔍 **SEO ANALYSIS**")
        
        # Basic SEO Elements
        title = safe_extract(seo, ["title"])
        meta_desc = safe_extract(seo, ["meta_description"])
        h1_count = safe_extract(seo, ["h1_tags"])
        
        summary_parts.append("📝 Content Elements:")
        if title != "N/A":
            title_length = len(str(title)) if title else 0
            summary_parts.append(f"  • Title: {str(title)[:50]}... ({title_length} chars)")
        if meta_desc != "N/A":
            desc_length = len(str(meta_desc)) if meta_desc else 0
            summary_parts.append(f"  • Meta Description: {str(meta_desc)[:50]}... ({desc_length} chars)")
        if h1_count != "N/A":
            summary_parts.append(f"  • H1 Tags: {h1_count}")
        
        # Keywords and Links
        keywords = safe_extract(seo, ["keywords"], [])
        internal_links = safe_extract(seo, ["internal_links"])
        external_links = safe_extract(seo, ["external_links"])
        
        if keywords and isinstance(keywords, list):
            summary_parts.append(f"🔑 Top Keywords: {', '.join(str(k) for k in keywords[:5])}")
        if internal_links != "N/A":
            summary_parts.append(f"🔗 Internal Links: {internal_links}")
        if external_links != "N/A":
            summary_parts.append(f"🌐 External Links: {external_links}")
        
        # SEO Issues
        seo_issues = safe_extract(seo, ["issues"], [])
        if isinstance(seo_issues, list) and seo_issues:
            summary_parts.append("⚠️  SEO Issues:")
            for issue in seo_issues[:3]:
                if isinstance(issue, dict):
                    issue_text = issue.get('description', str(issue))
                else:
                    issue_text = str(issue)
                summary_parts.append(f"  • {issue_text[:60]}...")
        
        summary_parts.append("")
    
    # Security Analysis (Priority 3)
    if "ssl" in audit_results:
        ssl = audit_results["ssl"]
        summary_parts.append("🔒 **SECURITY STATUS**")
        
        ssl_valid = safe_extract(ssl, ["ssl_valid"])
        ssl_grade = safe_extract(ssl, ["ssl_grade"])
        cert_expiry = safe_extract(ssl, ["certificate_expiry"])
        
        if ssl_valid != "N/A":
            status = "✅ Valid" if ssl_valid else "❌ Invalid"
            summary_parts.append(f"🛡️  SSL Certificate: {status}")
        if ssl_grade != "N/A":
            summary_parts.append(f"📋 SSL Grade: {ssl_grade}")
        if cert_expiry != "N/A":
            summary_parts.append(f"⏰ Certificate Expires: {cert_expiry}")
        
        # Security Headers
        headers = safe_extract(ssl, ["security_headers"], {})
        if isinstance(headers, dict):
            header_count = len([h for h in headers.values() if h])
            summary_parts.append(f"🔧 Security Headers: {header_count} present")
        
        summary_parts.append("")
    
    # DNS Analysis (Priority 4)
    if "dns" in audit_results:
        dns = audit_results["dns"]
        summary_parts.append("🌐 **DNS CONFIGURATION**")
        
        # A Records
        a_records = safe_extract(dns, ["a_records"], [])
        if isinstance(a_records, list) and a_records:
            summary_parts.append(f"📍 A Records: {len(a_records)} found")
            summary_parts.append(f"  Primary IP: {a_records[0] if a_records else 'N/A'}")
        
        # Other DNS Records
        mx_records = safe_extract(dns, ["mx_records"], [])
        ns_records = safe_extract(dns, ["ns_records"], [])
        
        if isinstance(mx_records, list):
            summary_parts.append(f"📧 MX Records: {len(mx_records)}")
        if isinstance(ns_records, list):
            summary_parts.append(f"🗄️  NS Records: {len(ns_records)}")
        
        summary_parts.append("")
    
    # Ranking Analysis (Priority 5)
    if "ranking" in audit_results:
        ranking = audit_results["ranking"]
        summary_parts.append("📈 **RANKING METRICS**")
        
        domain_authority = safe_extract(ranking, ["domain_authority"])
        page_authority = safe_extract(ranking, ["page_authority"])
        backlinks = safe_extract(ranking, ["backlinks"])
        
        if domain_authority != "N/A":
            summary_parts.append(f"🏆 Domain Authority: {domain_authority}")
        if page_authority != "N/A":
            summary_parts.append(f"📄 Page Authority: {page_authority}")
        if backlinks != "N/A":
            summary_parts.append(f"🔗 Backlinks: {backlinks}")
        
        summary_parts.append("")
    
    # Priority Recommendations
    summary_parts.append("🎯 **PRIORITY RECOMMENDATIONS**")
    
    # Performance Recommendations
    if "performance" in audit_results:
        perf = audit_results["performance"]
        load_time = safe_extract(perf, ["metrics", "page_load_time"])
        try:
            if load_time != "N/A" and isinstance(load_time, (int, float, str)):
                load_time_float = float(load_time)
                if load_time_float > 3.0:
                    summary_parts.append("1. 🚨 CRITICAL: Optimize page load time (>3s)")
        except (ValueError, TypeError):
            pass
    
    # SEO Recommendations
    if "seo_marketing" in audit_results:
        seo = audit_results["seo_marketing"]
        title = safe_extract(seo, ["title"])
        meta_desc = safe_extract(seo, ["meta_description"])
        
        if title == "N/A" or not title:
            summary_parts.append("2. 📝 HIGH: Add missing page title")
        elif len(str(title)) > 60:
            summary_parts.append("2. 📝 HIGH: Optimize title length (<60 chars)")
        
        if meta_desc == "N/A" or not meta_desc:
            summary_parts.append("3. 📋 MEDIUM: Add meta description")
        elif len(str(meta_desc)) > 160:
            summary_parts.append("3. 📋 MEDIUM: Optimize meta description length (<160 chars)")
    
    # Security Recommendations
    if "ssl" in audit_results:
        ssl = audit_results["ssl"]
        ssl_valid = safe_extract(ssl, ["ssl_valid"])
        if ssl_valid == False:
            summary_parts.append("4. 🔒 CRITICAL: Fix SSL certificate issues")
    
    # Generate analysis timestamp
    summary_parts.append("")
    summary_parts.append(f"🔍 **Analysis completed at {datetime.now().strftime('%H:%M:%S')}**")
    summary_parts.append("💡 This summary is optimized for AI analysis and ChatGPT processing")
    
    return "\n".join(summary_parts)


def display_ai_analysis(results):
    """Display AI analysis section with enhanced styling and error handling"""
    try:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        ">
            <h2 style="
                color: #ffffff !important;
                margin: 0;
                font-size: 24px;
                font-weight: 600;
                text-align: center;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            ">🤖 AI Analysis & Summary</h2>
            <p style="
                color: #ffffff !important;
                margin: 10px 0 0 0;
                text-align: center;
                opacity: 0.9;
                font-size: 14px;
            ">Comprehensive analysis optimized for ChatGPT and AI processing</p>
        </div>
        """, unsafe_allow_html=True)
        
        if not results:
            st.warning("⚠️ No audit results available for AI analysis")
            return
        
        # Get domain from results or session state
        domain = "Unknown Domain"
        if hasattr(st.session_state, 'url_input') and st.session_state.url_input:
            domain = st.session_state.url_input
        elif isinstance(results, dict) and 'domain' in results:
            domain = results['domain']
        
        # Determine active modules
        active_modules = []
        if isinstance(results, dict):
            active_modules = [key for key in results.keys() if key != 'domain' and results.get(key)]
        
        if not active_modules:
            st.info("ℹ️ No analysis modules were active. Please run an audit first.")
            return
        
        # Generate comprehensive summary
        try:
            summary = generate_comprehensive_summary(domain, results, active_modules)
            
            # Display summary in a nice container
            st.markdown("""
            <div style="
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                padding: 20px;
                margin: 20px 0;
                font-family: 'Segoe UI', Arial, sans-serif;
            ">
            """, unsafe_allow_html=True)
            
            # Text area for easy copying
            st.text_area(
                "📋 **Comprehensive Analysis Summary**",
                value=summary,
                height=400,
                help="Copy this optimized summary for ChatGPT analysis",
                label_visibility="visible"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📊 Summary Length",
                    value=f"{len(summary)} chars",
                    delta=f"{len(summary.split())} words"
                )
            
            with col2:
                st.metric(
                    label="🔧 Active Modules",
                    value=len(active_modules),
                    delta=", ".join(active_modules[:2]) + ("..." if len(active_modules) > 2 else "")
                )
            
            with col3:
                compression_ratio = (1 - len(summary) / len(json.dumps(results, default=json_serializer))) * 100
                st.metric(
                    label="📉 Compression",
                    value=f"{compression_ratio:.1f}%",
                    delta="vs raw data"
                )
            
            with col4:
                st.metric(
                    label="⏱️ Analysis Time",
                    value=datetime.now().strftime("%H:%M"),
                    delta="Current"
                )
            
            # Additional actions
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🔄 Regenerate Summary", help="Generate a new optimized summary"):
                    st.rerun()
            
            with col2:
                # Download button for summary
                st.download_button(
                    label="💾 Download Summary",
                    data=summary,
                    file_name=f"web_audit_summary_{domain.replace('https://', '').replace('http://', '').replace('/', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    help="Download the summary as a text file"
                )
            
            with col3:
                if st.button("Show Raw Data", help="Toggle raw data view"):
                    if "show_raw_ai_data" not in st.session_state:
                        st.session_state.show_raw_ai_data = False
                    st.session_state.show_raw_ai_data = not st.session_state.show_raw_ai_data
                    st.rerun()
            
            # Show raw data if requested
            if st.session_state.get("show_raw_ai_data", False):
                st.markdown("### Raw Audit Data")
                with st.expander("View Complete Raw Data", expanded=False):
                    try:
                        st.json(results)
                    except Exception as e:
                        st.error(f"Error displaying raw data: {str(e)}")
                        st.text("Raw data preview:")
                        st.code(str(results)[:1000] + "..." if len(str(results)) > 1000 else str(results))
            
        except Exception as e:
            st.error(f"❌ Error generating AI analysis: {str(e)}")
            st.info("📝 Showing simplified summary instead...")
            
            # Fallback simple summary
            simple_summary = f"""
🌐 **Quick Analysis Summary for {domain}**

📅 Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
🔧 Available Data: {', '.join(active_modules)}

📊 **Available Analysis Modules:**
{chr(10).join([f"• {module.title()}: Available" for module in active_modules])}

⚠️ Note: Detailed analysis temporarily unavailable. Raw data is accessible below.

💡 This is a simplified summary. For detailed analysis, please retry or check the raw data.
            """.strip()
            
            st.text_area(
                "📋 **Simplified Summary**",
                value=simple_summary,
                height=200,
                help="Basic summary - detailed analysis will be restored shortly"
            )
    
    except Exception as e:
        st.error(f"❌ Critical error in AI analysis display: {str(e)}")
        st.info("🔄 Please refresh the page and try again.")


def display_raw_data_only(results):
    """Display only raw data in a clean format"""
    try:
        st.markdown("### 📋 Raw Audit Data")
        
        if not results:
            st.warning("⚠️ No data available to display")
            return
        
        # Format and display JSON
        try:
            formatted_json = json.dumps(results, indent=2, default=json_serializer, ensure_ascii=False)
            st.code(formatted_json, language="json")
        except Exception as e:
            st.error(f"❌ Error formatting JSON: {str(e)}")
            st.text("Raw data (fallback):")
            st.write(results)
            
    except Exception as e:
        st.error(f"❌ Error displaying raw data: {str(e)}")
