"""
Shared UI Utilities Module
Contains reusable components and utilities to minimize code duplication
"""

import streamlit as st
import plotly.graph_objects as go

class SharedUIComponents:
    """Shared UI components to minimize code duplication across the application"""
    
    class MockColumn:
        """Mock column object for non-UI environments"""
        def __enter__(self):
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
    
    # Social media platform icons - centralized definition
    PLATFORM_ICONS = {
        'Facebook': '📘', 'X (Twitter)': '❌', 'LinkedIn': '💼', 
        'Instagram': '📷', 'YouTube': '🎥', 'TikTok': '🎵',
        'Pinterest': '📌', 'Snapchat': '👻', 'WhatsApp': '💬',
        'Telegram': '✈️', 'Discord': '🎮', 'Reddit': '🤖',
        'Tumblr': '🎨', 'Twitch': '🎯', 'Vimeo': '🎬',
        'GitHub': '👨‍💻', 'GitLab': '🦊', 'Behance': '🎨',
        'Dribbble': '🏀', 'Medium': '📝', 'Mastodon': '🐘',
        'Threads': '🧵', 'Gmail': '📧', 'Email': '✉️',
        'Twitter': '❌'  # Legacy support
    }
    
    @staticmethod
    def _safe_st_call(func, *args, **kwargs):
        """Safely call streamlit functions with fallback to print"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Fallback to print for non-UI environments
            if func.__name__ in ['warning', 'error', 'success', 'info']:
                print(f"⚠️ {args[0] if args else 'Streamlit message'}")
            elif func.__name__ == 'metric':
                print(f"📊 {args[0] if args else 'Metric'}: {args[1] if len(args) > 1 else 'N/A'}")
            elif func.__name__ == 'subheader':
                print(f"📋 {args[0] if args else 'Header'}")
            elif func.__name__ == 'write':
                print(args[0] if args else '')
            elif func.__name__ == 'caption':
                print(f"💡 {args[0] if args else ''}")
            elif func.__name__ == 'columns':
                # Return mock column objects for columns
                num_cols = args[0] if args else 1
                return [SharedUIComponents.MockColumn() for _ in range(num_cols)]
            elif func.__name__ == 'markdown':
                print(args[0] if args else '')
            return None
    
    @staticmethod
    def display_no_data_warning(module_name):
        """Standardized warning for missing data"""
        SharedUIComponents._safe_st_call(st.warning, f"⚠️ No {module_name.lower()} data available")
    
    @staticmethod
    def display_error_state(module_name, error_msg=None):
        """Standardized error display"""
        if error_msg:
            SharedUIComponents._safe_st_call(st.error, f"❌ {module_name} analysis failed: {error_msg}")
        else:
            SharedUIComponents._safe_st_call(st.error, f"❌ {module_name} analysis failed")
    
    @staticmethod
    def create_metric_columns(num_metrics, labels, values, deltas=None, helps=None):
        """Create standardized metric columns with consistent layout"""
        cols = st.columns(num_metrics)
        
        for i, (label, value) in enumerate(zip(labels, values)):
            with cols[i]:
                delta = deltas[i] if deltas and i < len(deltas) else None
                help_text = helps[i] if helps and i < len(helps) else None
                st.metric(label, value, delta=delta, help=help_text)
    
    @staticmethod
    def create_score_metric(score, label="Score", max_score=100):
        """Create a standardized score metric with color coding"""
        if isinstance(score, (int, float)):
            # Color coding based on score
            if score >= 80:
                color = "🟢"
            elif score >= 60:
                color = "🟡"
            else:
                color = "🔴"
            
            display_value = f"{color} {score}"
            if max_score != 100:
                display_value += f"/{max_score}"
            else:
                display_value += "%"
                
            st.metric(label, display_value)
            
            # Add progress bar
            progress_value = score / max_score if max_score != 100 else score / 100
            st.progress(min(progress_value, 1.0))
        else:
            st.metric(label, str(score))
    
    @staticmethod
    def display_social_media_links(social_links, max_columns=4):
        """Standardized social media links display"""
        if not social_links:
            return
        
        st.subheader("📱 Social Media Presence")
        social_cols = st.columns(min(len(social_links), max_columns))
        
        for i, (platform, link) in enumerate(social_links.items()):
            with social_cols[i % max_columns]:
                icon = SharedUIComponents.PLATFORM_ICONS.get(platform, '🔗')
                st.write(f"{icon} **{platform}**")
                
                # For email, display email address
                if platform in ['Gmail', 'Email']:
                    st.write(f"📧 {link}")
                else:
                    st.write(f"[Visit Profile]({link})")
    
    @staticmethod
    def display_marketing_tools(marketing_tools, max_columns=4):
        """Standardized marketing tools display"""
        if not marketing_tools:
            return
        st.subheader("🎯 Marketing Tools Detected")
        cols = st.columns(min(len(marketing_tools), max_columns))

        for i, tool in enumerate(marketing_tools):
            with cols[i % max_columns]:
                # Support both legacy string entries and new dict entries
                if isinstance(tool, dict):
                    name = tool.get('name', 'Unknown')
                    evidence = tool.get('evidence', '')
                    confidence = (tool.get('confidence') or 'unknown').lower()

                    if confidence == 'high':
                        st.success(f"✅ {name} — {confidence.upper()}")
                    elif confidence == 'medium':
                        st.info(f"⚠️ {name} — {confidence}")
                    else:
                        st.warning(f"❕ {name} — {confidence}")

                    if evidence:
                        st.caption(evidence)
                else:
                    # Fallback for older string-based lists
                    st.success(f"✅ {str(tool)}")
    
    @staticmethod
    def create_gauge_chart(value, title, max_value=100, color_scheme="auto"):
        """Create a standardized gauge chart for scores"""
        if not isinstance(value, (int, float)):
            st.metric(title, str(value))
            return
        
        # Determine color based on value
        if color_scheme == "auto":
            if value >= 80:
                bar_color = "darkgreen"
            elif value >= 50:
                bar_color = "orange"
            else:
                bar_color = "red"
        else:
            bar_color = color_scheme
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={'text': title},
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, max_value]},
                'bar': {'color': bar_color},
                'steps': [
                    {'range': [0, max_value * 0.5], 'color': "lightgray"},
                    {'range': [max_value * 0.5, max_value * 0.8], 'color': "gray"},
                    {'range': [max_value * 0.8, max_value], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': max_value * 0.9
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def display_category_breakdown(categories, category_names=None):
        """Standardized category breakdown display"""
        if not categories:
            return
        
        if not category_names:
            category_names = {
                'meta_data': 'Meta Data',
                'page_quality': 'Page Quality', 
                'page_structure': 'Page Structure',
                'links': 'Links',
                'server': 'Server Config',
                'external_factors': 'External Factors'
            }
        
        st.subheader("📊 Categories Breakdown")
        cols = st.columns(3)
        
        for i, (key, category) in enumerate(categories.items()):
            with cols[i % 3]:
                score = category.get('score', 0)
                name = category_names.get(key, key.replace('_', ' ').title())
                # Ensure name is always a string
                if name is None:
                    name = key.replace('_', ' ').title()
                SharedUIComponents.create_score_metric(score, str(name))
    
    @staticmethod
    def display_dns_records(dns_data):
        """Clean DNS records display with detailed information only"""
        if not dns_data:
            SharedUIComponents.display_no_data_warning("DNS")
            return

        # DNS Records Overview - Simple metrics
        st.markdown("#### 📊 DNS Records Summary")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            a_records = dns_data.get("a_records", [])
            record_count = len(a_records) if isinstance(a_records, list) else a_records
            st.metric("A Records", record_count)

        with col2:
            mx_records = dns_data.get("mx_records", [])
            record_count = len(mx_records) if isinstance(mx_records, list) else mx_records
            st.metric("MX Records", record_count)

        with col3:
            ns_records = dns_data.get("ns_records", [])
            record_count = len(ns_records) if isinstance(ns_records, list) else ns_records
            st.metric("NS Records", record_count)

        with col4:
            cname_records = dns_data.get("cname_records", [])
            record_count = len(cname_records) if isinstance(cname_records, list) else cname_records
            st.metric("CNAME Records", record_count)

        # Detailed DNS Records - Clean expandable section
        with st.expander("🔍 Detailed DNS Records", expanded=False):
            # Display A Records with TTL
            if dns_data.get("a_records") and isinstance(dns_data["a_records"], list):
                st.markdown("**A Records (IPv4 Addresses)**")
                for i, record in enumerate(dns_data["a_records"], 1):
                    if isinstance(record, dict):
                        ip = record.get("address", record.get("ip", "N/A"))
                        ttl = record.get("ttl", "N/A")
                        st.text(f"{i}. {ip} (TTL: {ttl})")
                    else:
                        st.text(f"{i}. {record}")

            # Display AAAA Records (IPv6)
            if dns_data.get("aaaa_records") and isinstance(dns_data["aaaa_records"], list):
                st.markdown("**AAAA Records (IPv6 Addresses)**")
                for i, record in enumerate(dns_data["aaaa_records"], 1):
                    if isinstance(record, dict):
                        ip = record.get("address", record.get("ip", "N/A"))
                        ttl = record.get("ttl", "N/A")
                        st.text(f"{i}. {ip} (TTL: {ttl})")
                    else:
                        st.text(f"{i}. {record}")

            # Display MX Records with priority and TTL
            if dns_data.get("mx_records") and isinstance(dns_data["mx_records"], list):
                st.markdown("**MX Records (Mail Exchange)**")
                for i, record in enumerate(dns_data["mx_records"], 1):
                    if isinstance(record, dict):
                        server = record.get("exchange", record.get("server", "N/A"))
                        priority = record.get("priority", "N/A")
                        ttl = record.get("ttl", "N/A")
                        st.text(f"{i}. {server} (Priority: {priority}, TTL: {ttl})")
                    else:
                        st.text(f"{i}. {record}")

            # Display NS Records with TTL
            if dns_data.get("ns_records") and isinstance(dns_data["ns_records"], list):
                st.markdown("**NS Records (Name Servers)**")
                for i, record in enumerate(dns_data["ns_records"], 1):
                    if isinstance(record, dict):
                        server = record.get("target", record.get("server", "N/A"))
                        ttl = record.get("ttl", "N/A")
                        st.text(f"{i}. {server} (TTL: {ttl})")
                    else:
                        st.text(f"{i}. {record}")

            # Display CNAME Records with TTL
            if dns_data.get("cname_records") and isinstance(dns_data["cname_records"], list):
                st.markdown("**CNAME Records (Canonical Names)**")
                for i, record in enumerate(dns_data["cname_records"], 1):
                    if isinstance(record, dict):
                        target = record.get("target", record.get("cname", "N/A"))
                        ttl = record.get("ttl", "N/A")
                        st.text(f"{i}. {target} (TTL: {ttl})")
                    else:
                        st.text(f"{i}. {record}")

            # Display TXT Records
            if dns_data.get("txt_records") and isinstance(dns_data["txt_records"], list):
                st.markdown("**TXT Records (Text Records)**")
                for i, record in enumerate(dns_data["txt_records"], 1):
                    text = str(record)[:80]
                    if len(str(record)) > 80:
                        text += "..."
                    st.text(f"{i}. {text}")

            # Display SOA Record
            if dns_data.get("soa_record"):
                st.markdown("**SOA Record (Start of Authority)**")
                soa = dns_data["soa_record"]
                if isinstance(soa, dict):
                    st.text(f"Primary NS: {soa.get('mname', 'N/A')}")
                    st.text(f"Admin Email: {soa.get('rname', 'N/A')}")
                    st.text(f"Serial: {soa.get('serial', 'N/A')}")
                    st.text(f"Refresh: {soa.get('refresh', 'N/A')}s")
                    st.text(f"Retry: {soa.get('retry', 'N/A')}s")
                    st.text(f"Expire: {soa.get('expire', 'N/A')}s")
                    st.text(f"Minimum TTL: {soa.get('minimum', 'N/A')}s")
        
        # DNS Server Performance Analysis (outside expander)
        performance_data = dns_data.get("dns_server_performance", [])
        if performance_data and isinstance(performance_data, list) and len(performance_data) > 0:
            st.markdown("#### ⚡ DNS Server Performance Analysis")
            st.markdown("*Response times from popular public DNS servers*")
            
            for result in performance_data:
                if result.get('status') == 'success':
                    server_name = result.get('server_name', 'Unknown')
                    server_ip = result.get('server_ip', 'N/A')
                    response_time_ms = result.get('response_time_ms', 0)
                    resolved_ip = result.get('resolved_ip', 'N/A')
                    
                    time_str = f"{response_time_ms:.1f}ms" if response_time_ms else "N/A"
                    st.markdown(f"**{server_name}** [{server_ip}]: {time_str} -> {resolved_ip}")
                else:
                    server_name = result.get('server_name', 'Unknown')
                    server_ip = result.get('server_ip', 'N/A')
                    st.markdown(f"**{server_name}** [{server_ip}]: ❌ Failed")
            
            # Performance insights
            successful_times = [r.get('response_time_ms', 0) for r in performance_data if r.get('status') == 'success' and r.get('response_time_ms')]
            if successful_times:
                avg_time = sum(successful_times) / len(successful_times)
                fastest_time = min(successful_times)
                
                st.markdown("**📈 Insights:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Average", f"{avg_time:.1f}ms")
                with col2:
                    st.metric("Fastest", f"{fastest_time:.1f}ms")
    
    @staticmethod
    def display_authority_metrics(ranking_data):
        """Standardized authority metrics display"""
        if not ranking_data:
            SharedUIComponents.display_no_data_warning("Ranking")
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            da = ranking_data.get("domain_authority", "N/A")
            if da != "N/A":
                color = "🟢" if da >= 50 else "🟡" if da >= 30 else "🔴"
                st.metric("Domain Authority", f"{color} {da}")
            else:
                st.metric("Domain Authority", "N/A")
        
        with col2:
            pa = ranking_data.get("page_authority", "N/A")
            if pa != "N/A":
                color = "🟢" if pa >= 40 else "🟡" if pa >= 20 else "🔴"
                st.metric("Page Authority", f"{color} {pa}")
            else:
                st.metric("Page Authority", "N/A")
        
        with col3:
            backlinks = ranking_data.get("backlinks", "N/A")
            st.metric("Backlinks", backlinks)
        
        with col4:
            referring_domains = ranking_data.get("referring_domains", "N/A")
            st.metric("Referring Domains", referring_domains)
    
    @staticmethod
    def display_performance_vitals(metrics):
        """Standardized Core Web Vitals display"""
        if not metrics:
            return
        
        st.markdown("#### 📊 Core Web Vitals")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            lcp = metrics.get("largest_contentful_paint", "N/A")
            value = f"{lcp}s" if lcp != "N/A" else "N/A"
            st.metric("LCP (Largest Contentful Paint)", value)
        
        with col2:
            fid = metrics.get("first_input_delay", "N/A")
            value = f"{fid}ms" if fid != "N/A" else "N/A"
            st.metric("FID (First Input Delay)", value)
        
        with col3:
            cls = metrics.get("cumulative_layout_shift", "N/A")
            value = str(cls) if cls != "N/A" else "N/A"
            st.metric("CLS (Cumulative Layout Shift)", value)
    
    @staticmethod
    def display_ssl_metrics(ssl_data):
        """Enhanced SSL metrics display with detailed information"""
        if not ssl_data:
            SharedUIComponents.display_no_data_warning("Security")
            return
        
        # Basic SSL status
        cols = SharedUIComponents._safe_st_call(st.columns, 3)
        if not cols:
            cols = [SharedUIComponents.MockColumn() for _ in range(3)]
        col1, col2, col3 = cols
        
        with col1:
            ssl_valid = ssl_data.get("ssl_valid", False)
            if ssl_valid:
                SharedUIComponents._safe_st_call(st.success, "✅ SSL Certificate Valid")
            else:
                SharedUIComponents._safe_st_call(st.error, "❌ SSL Certificate Invalid")
        
        with col2:
            ssl_grade = ssl_data.get("ssl_grade", "N/A")
            if ssl_grade != "N/A":
                grade_color = "🟢" if ssl_grade in ["A+", "A"] else "🟡" if ssl_grade == "B" else "🔴"
                SharedUIComponents._safe_st_call(st.metric, "SSL Grade", f"{grade_color} {ssl_grade}")
            else:
                SharedUIComponents._safe_st_call(st.metric, "SSL Grade", "Not Available")
        
        with col3:
            SharedUIComponents._safe_st_call(st.metric, "Security Status", "Checked" if ssl_valid else "Issues Found")
        
        # Enhanced SSL details if available
        if ssl_data.get("certificate_details"):
            SharedUIComponents._safe_st_call(st.markdown, "#### 🔒 Certificate Details")
            cert_details = ssl_data["certificate_details"]
            
            cols = SharedUIComponents._safe_st_call(st.columns, 3)
            if not cols:
                cols = [SharedUIComponents.MockColumn() for _ in range(3)]
            col1, col2, col3 = cols
            with col1:
                if cert_details.get("issuer"):
                    SharedUIComponents._safe_st_call(st.metric, "Issued By", cert_details["issuer"])
                if cert_details.get("subject"):
                    SharedUIComponents._safe_st_call(st.metric, "Subject", cert_details["subject"])
            
            with col2:
                if cert_details.get("expires_in_days"):
                    days = cert_details["expires_in_days"]
                    color = "🟢" if days > 30 else "🟡" if days > 7 else "🔴"
                    SharedUIComponents._safe_st_call(st.metric, "Expires In", f"{color} {days} days")
                if cert_details.get("signature_algorithm"):
                    SharedUIComponents._safe_st_call(st.metric, "Algorithm", cert_details["signature_algorithm"])
            
            with col3:
                if cert_details.get("key_size"):
                    SharedUIComponents._safe_st_call(st.metric, "Key Size", f"{cert_details['key_size']} bits")
                if cert_details.get("protocol_version"):
                    SharedUIComponents._safe_st_call(st.metric, "TLS Version", cert_details["protocol_version"])
        
        # Security recommendations
        if ssl_data.get("security_issues"):
            SharedUIComponents._safe_st_call(st.markdown, "#### ⚠️ Security Issues")
            for issue in ssl_data["security_issues"]:
                SharedUIComponents._safe_st_call(st.warning, f"• {issue}")
                
        if ssl_data.get("recommendations"):
            SharedUIComponents._safe_st_call(st.markdown, "#### 💡 Security Recommendations")
            for rec in ssl_data["recommendations"]:
                SharedUIComponents._safe_st_call(st.info, f"• {rec}")
    
    @staticmethod
    def display_todo_list(todo_list, max_items=5):
        """Standardized TODO list display"""
        if not todo_list:
            return
        
        st.subheader("📋 Priority To-Do List")
        
        # Group by importance
        errors = [item for item in todo_list if item.get('importance') == 'error']
        warnings = [item for item in todo_list if item.get('importance') == 'warning']
        
        if errors:
            st.error("🔴 **Critical Issues** (Fix Immediately)")
            for i, item in enumerate(errors[:max_items], 1):
                st.write(f"{i}. {item.get('action', 'Unknown action')}")
        
        if warnings:
            st.warning("🟡 **Warnings** (Consider Fixing)")
            for i, item in enumerate(warnings[:max_items], 1):
                st.write(f"{i}. {item.get('action', 'Unknown action')}")
    
    @staticmethod
    def display_issues_list(issues, title="Issues", max_items=10):
        """Standardized issues list display"""
        if not issues:
            return
        
        st.markdown(f"#### ⚠️ {title}")
        
        for i, issue in enumerate(issues[:max_items], 1):
            if isinstance(issue, dict):
                description = issue.get('description', str(issue))
                severity = issue.get('severity', 'info')
                
                if severity == 'error':
                    st.error(f"{i}. {description}")
                elif severity == 'warning':
                    st.warning(f"{i}. {description}")
                else:
                    st.info(f"{i}. {description}")
            else:
                st.error(f"{i}. {str(issue)}")
    
    @staticmethod
    def format_metric_value(value, unit="", format_type="auto"):
        """Format metric values consistently"""
        if value == "N/A" or value is None:
            return "N/A"
        
        if format_type == "bytes":
            try:
                bytes_val = float(value)
                if bytes_val >= 1024 * 1024:
                    return f"{bytes_val / (1024 * 1024):.2f} MB"
                elif bytes_val >= 1024:
                    return f"{bytes_val / 1024:.2f} KB"
                else:
                    return f"{bytes_val:.0f} B"
            except:
                return str(value)
        
        elif format_type == "time_ms":
            try:
                ms_val = float(value)
                if ms_val >= 1000:
                    return f"{ms_val / 1000:.2f}s"
                else:
                    return f"{ms_val:.0f}ms"
            except:
                return str(value)
        
        elif format_type == "percentage":
            try:
                return f"{float(value):.1f}%"
            except:
                return str(value)
        
        else:
            return f"{value}{unit}" if unit else str(value)

class DataValidation:
    """Shared data validation utilities"""
    
    @staticmethod
    def validate_audit_data(data, module_name):
        """Validate audit data structure"""
        if not data:
            return False, f"No {module_name} data provided"
        
        if isinstance(data, dict) and 'error' in data:
            return False, f"{module_name} analysis failed: {data['error']}"
        
        # Allow data through if it's a non-empty dict or has any content
        if isinstance(data, dict) and len(data) > 0:
            return True, None
        elif data:  # Any truthy value
            return True, None
        
        return False, f"Empty {module_name} data"
    
    @staticmethod
    def safe_get_value(data, key, default="N/A"):
        """Safely get value from data dictionary"""
        try:
            return data.get(key, default) if isinstance(data, dict) else default
        except:
            return default
    
    @staticmethod
    def safe_get_list_length(data, key, default=0):
        """Safely get list length from data"""
        try:
            value = data.get(key, []) if isinstance(data, dict) else []
            return len(value) if isinstance(value, list) else value
        except:
            return default
