"""
Optimized Display Components — Google-Inspired Cards & Clean Layout
Displays results for all modules in organized tabs
"""

import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import json


class OptimizedDisplays:
    """Display components for all audit result tabs"""

    # ═══════════════════════════════════════════════════════════
    #  MAIN ENTRY — Tab router
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def display_audit_results(results):
        """Display all audit results organized in tabs"""
        if not results:
            st.info("No results to display. Enter a URL and click Analyze.")
            return

        # Build tab list based on available data
        tab_labels = []
        tab_keys = []

        tab_map = [
            ('performance', '⚡ Performance'),
            ('seo_marketing', '🔍 SEO'),
            ('ssl', '🔒 Security'),
            ('dns', '🌐 DNS'),
            ('ranking', '📊 Ranking'),
            ('blacklist', '🛡️ Blacklist'),
            ('email', '📧 Email'),
            ('tools', '🔗 Tools'),
        ]
        for key, label in tab_map:
            if key in results:
                tab_labels.append(label)
                tab_keys.append(key)

        if not tab_labels:
            st.warning("No analysis modules returned data.")
            return

        tabs = st.tabs(tab_labels)
        dispatch = {
            'performance': OptimizedDisplays.display_performance,
            'seo_marketing': OptimizedDisplays.display_seo,
            'ssl': OptimizedDisplays.display_security,
            'dns': OptimizedDisplays.display_dns,
            'ranking': OptimizedDisplays.display_ranking,
            'blacklist': OptimizedDisplays.display_blacklist,
            'email': OptimizedDisplays.display_email,
            'tools': OptimizedDisplays.display_tools,
        }
        for tab, key in zip(tabs, tab_keys):
            with tab:
                fn = dispatch.get(key)
                if fn:
                    fn(results[key])

    # ═══════════════════════════════════════════════════════════
    #  PERFORMANCE
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def display_performance(data):
        if not data:
            st.info("No performance data available.")
            return

        c1, c2, c3, c4 = st.columns(4)
        resp = data.get('response_time')
        c1.metric("Response (TTFB)", f"{resp:.0f} ms" if resp else "N/A")
        total = data.get('total_load_time')
        c2.metric("Total Load", f"{total:.0f} ms" if total else "N/A")
        c3.metric("Status Code", data.get('status_code', 'N/A'))
        size = data.get('page_size')
        c4.metric("Page Size", f"{size / 1024:.1f} KB" if size else "N/A")

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("##### Server Info")
            srv = data.get('server_info', {})
            _table_rows([
                ("Server", srv.get('server', 'Unknown')),
                ("Powered By", srv.get('powered_by', 'Unknown')),
                ("Content-Type", srv.get('content_type', 'Unknown')),
                ("Compression", data.get('compression', 'none')),
                ("Redirects", data.get('redirect_count', 0)),
            ])

        with col2:
            st.markdown("##### Cache Headers")
            cache = data.get('cache_headers', {})
            _table_rows([
                ("Cache-Control", cache.get('cache_control') or '—'),
                ("Expires", cache.get('expires') or '—'),
                ("ETag", cache.get('etag') or '—'),
                ("Last-Modified", cache.get('last_modified') or '—'),
            ])

        # Simple gauge
        if resp:
            color = "#34a853" if resp < 500 else ("#fbbc04" if resp < 1500 else "#ea4335")
            fig = go.Figure(go.Indicator(
                mode="gauge+number", value=resp,
                title={'text': 'Response Time (ms)'},
                gauge={
                    'axis': {'range': [0, 3000]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 500], 'color': '#e6f4ea'},
                        {'range': [500, 1500], 'color': '#fef7e0'},
                        {'range': [1500, 3000], 'color': '#fce8e6'},
                    ],
                }
            ))
            fig.update_layout(height=250, margin=dict(t=40, b=10, l=30, r=30),
                              font=dict(family='Inter'))
            st.plotly_chart(fig, use_container_width=True)

    # ═══════════════════════════════════════════════════════════
    #  SEO & MARKETING
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def display_seo(data):
        if not data:
            st.info("No SEO data available.")
            return

        # Top metrics
        c1, c2, c3 = st.columns(3)
        score = data.get('seo_score', 0)
        c1.metric("SEO Score", f"{score}/100")
        c2.metric("Title", _trunc(data.get('title', 'N/A'), 40))
        c3.metric("Marketing Tools", len(data.get('marketing_tools', [])))

        st.divider()

        # Meta info
        with st.expander("📝 Meta Data", expanded=True):
            _table_rows([
                ("Title", data.get('title', 'N/A')),
                ("Meta Description", _trunc(data.get('meta_description', 'N/A'), 100)),
                ("Meta Keywords", data.get('meta_keywords', 'N/A')),
                ("Canonical URL", data.get('canonical_url', 'N/A')),
                ("Robots", data.get('robots_meta', 'N/A')),
                ("Language", data.get('language', 'N/A')),
                ("Charset", data.get('charset', 'N/A')),
                ("Viewport", data.get('viewport', 'N/A')),
            ])

        # Headings
        headings = data.get('headings', {})
        if headings and isinstance(headings, dict):
            with st.expander("📑 Headings"):
                for level in ['h1', 'h2', 'h3', 'h4']:
                    items = headings.get(level, [])
                    if items:
                        st.markdown(f"**{level.upper()}** ({len(items)})")
                        for h in items[:5]:
                            st.markdown(f"- {h}")

        # Open Graph & Twitter
        og = data.get('open_graph', {})
        tc = data.get('twitter_cards', {})
        if og or tc:
            with st.expander("🔗 Social Meta Tags"):
                if og and isinstance(og, dict):
                    st.markdown("**Open Graph**")
                    _table_rows([(k, v) for k, v in og.items()])
                if tc and isinstance(tc, dict):
                    st.markdown("**Twitter Cards**")
                    _table_rows([(k, v) for k, v in tc.items()])

        # Images
        images = data.get('images', {})
        if images and isinstance(images, dict):
            with st.expander("🖼️ Images"):
                _table_rows([
                    ("Total Images", images.get('total', 0)),
                    ("Without Alt", images.get('without_alt', 0)),
                    ("External", images.get('external', 0)),
                ])

        # Links
        links = data.get('links', {})
        if links and isinstance(links, dict):
            with st.expander("🔗 Links"):
                _table_rows([
                    ("Internal", links.get('internal', 0)),
                    ("External", links.get('external', 0)),
                    ("No-follow", links.get('nofollow', 0)),
                ])

        # Schema markup
        schema = data.get('schema_markup')
        if schema:
            show_schema = False
            if isinstance(schema, dict) and schema.get('has_schema'):
                show_schema = True
            elif isinstance(schema, list) and len(schema) > 0:
                show_schema = True
            if show_schema:
                with st.expander("🏗️ Schema.org Markup"):
                    st.json(schema)

        # Social media links
        social = data.get('social_media_links', [])
        if social and isinstance(social, list):
            with st.expander("📱 Social Media Links"):
                for s in social:
                    if isinstance(s, dict):
                        platform = s.get('platform', 'Unknown')
                        url = s.get('url', '')
                        st.markdown(f"- **{platform}**: [{url}]({url})")

        # Marketing tools
        mkt = data.get('marketing_tools', [])
        if mkt:
            with st.expander("📈 Marketing Tools Detected"):
                for tool in mkt:
                    name = tool.get('tool', tool) if isinstance(tool, dict) else tool
                    st.markdown(f"- {name}")

        # Comprehensive analysis categories
        analysis = data.get('comprehensive_analysis', {})
        if analysis and isinstance(analysis, dict):
            cats = analysis.get('categories', {})
            if cats and isinstance(cats, dict):
                with st.expander("📊 Detailed SEO Breakdown"):
                    for cat_name, cat_data in cats.items():
                        if not isinstance(cat_data, dict):
                            continue
                        score_val = cat_data.get('score', 0)
                        max_val = cat_data.get('max_score', 100)
                        pct = int((score_val / max_val * 100) if max_val else 0)
                        color = '🟢' if pct >= 70 else ('🟡' if pct >= 40 else '🔴')
                        st.markdown(f"{color} **{cat_name}**: {score_val}/{max_val} ({pct}%)")
                        items_list = cat_data.get('items', [])
                        for item in items_list[:5]:
                            if not isinstance(item, dict):
                                continue
                            status_icon = '✅' if item.get('status') == 'pass' else ('⚠️' if item.get('status') == 'warning' else '❌')
                            st.markdown(f"  {status_icon} {item.get('name', '')}: {item.get('value', '')}")

    # ═══════════════════════════════════════════════════════════
    #  SECURITY (SSL)
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def display_security(data):
        if not data:
            st.info("No security data available.")
            return

        c1, c2, c3, c4 = st.columns(4)
        has_ssl = data.get('has_ssl', False)
        c1.metric("SSL", "✅ Active" if has_ssl else "❌ None")
        c2.metric("Grade", data.get('ssl_grade', 'N/A'))
        days = data.get('days_until_expiry')
        c3.metric("Expires In", f"{days} days" if days is not None else "N/A")
        c4.metric("Protocol", data.get('protocol_version', 'N/A'))

        st.divider()

        cert = data.get('certificate_details', {})
        if cert:
            with st.expander("📜 Certificate Details", expanded=True):
                _table_rows([
                    ("Subject", cert.get('subject', 'N/A')),
                    ("Issuer", cert.get('issuer', 'N/A')),
                    ("Protocol", cert.get('protocol_version', 'N/A')),
                    ("Cipher", cert.get('signature_algorithm', 'N/A')),
                    ("Key Size", cert.get('key_size', 'N/A')),
                    ("Expires In", f"{cert.get('expires_in_days', 'N/A')} days"),
                ])

        issues = data.get('security_issues', [])
        if issues:
            with st.expander("⚠️ Security Issues"):
                for issue in issues:
                    st.markdown(f"🔴 {issue}")

        recs = data.get('recommendations', [])
        if recs:
            with st.expander("💡 Recommendations"):
                for rec in recs:
                    st.markdown(f"💡 {rec}")

    # ═══════════════════════════════════════════════════════════
    #  DNS
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def display_dns(data):
        if not data:
            st.info("No DNS data available.")
            return

        c1, c2, c3 = st.columns(3)
        c1.metric("IP Address", data.get('ip_address', 'N/A'))
        rt = data.get('dns_response_time')
        c2.metric("DNS Response", f"{rt:.1f} ms" if rt else "N/A")
        c3.metric("A Records", len(data.get('a_records', [])))

        st.divider()

        # TTL info
        ttl = data.get('ttl_info', {})
        if ttl:
            with st.expander("⏱️ TTL Values", expanded=True):
                rows = [(f"{rtype} TTL", f"{val} seconds") for rtype, val in ttl.items()]
                _table_rows(rows)

        # Record tables
        record_types = [
            ('a_records', 'A Records'),
            ('mx_records', 'MX Records'),
            ('ns_records', 'NS Records'),
            ('txt_records', 'TXT Records'),
            ('cname_records', 'CNAME Records'),
        ]
        for key, label in record_types:
            records = data.get(key, [])
            if records:
                with st.expander(f"📋 {label} ({len(records)})"):
                    for r in records:
                        st.code(r, language=None)

        # DNS server performance
        perf = data.get('dns_server_performance', [])
        if perf:
            with st.expander("🏎️ DNS Server Performance"):
                html = '<table class="record-table"><tr><th>Server</th><th>IP</th><th>Response</th><th>Resolved IP</th><th>Status</th></tr>'
                for p in perf:
                    status_badge = '<span class="badge-pass">OK</span>' if p.get('status') == 'success' else '<span class="badge-fail">FAIL</span>'
                    rt_val = f"{p.get('response_time_ms', '—')} ms" if p.get('response_time') else '—'
                    html += f"<tr><td>{p.get('server_name','')}</td><td><code>{p.get('server_ip','')}</code></td><td>{rt_val}</td><td><code>{p.get('resolved_ip','')}</code></td><td>{status_badge}</td></tr>"
                html += '</table>'
                st.markdown(html, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    #  RANKING
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def display_ranking(data):
        if not data:
            st.info("No ranking data available.")
            return

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Domain Authority", data.get('domain_authority', 'N/A'))
        c2.metric("Page Authority", data.get('page_authority', 'N/A'))
        c3.metric("Trust Flow", data.get('trust_flow', 'N/A'))
        c4.metric("Citation Flow", data.get('citation_flow', 'N/A'))

        st.divider()

        c1, c2, c3 = st.columns(3)
        c1.metric("SEO Visibility", data.get('seo_visibility', 'N/A'))
        c2.metric("Est. Traffic", f"{data.get('organic_traffic_estimate', 0):,}")
        c3.metric("Backlinks", f"{data.get('backlink_estimate', 0):,}")

        st.caption("⚠️ Ranking data is estimated. Use with caution.")

    # ═══════════════════════════════════════════════════════════
    #  BLACKLIST CHECK (NEW)
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def display_blacklist(data):
        if not data:
            st.info("No blacklist data available.")
            return

        if data.get('error'):
            st.error(f"❌ {data['error']}")
            return

        # Summary metrics
        status = data.get('status', 'unknown')
        c1, c2, c3, c4 = st.columns(4)
        if status == 'clean':
            c1.metric("Status", "✅ Clean")
        elif status == 'listed':
            c1.metric("Status", "🚨 LISTED")
        else:
            c1.metric("Status", "⚠️ Error")

        c2.metric("IP Checked", data.get('ip', 'N/A'))
        c3.metric("Clean", f"{data.get('clean_count', 0)}/{data.get('total_lists', 0)}")
        c4.metric("Listed", data.get('listed_count', 0))

        st.divider()

        # Detailed results table
        checks = data.get('checks', [])
        if checks:
            html = '<table class="record-table"><tr><th>Blacklist</th><th>Zone</th><th>Status</th></tr>'
            for chk in checks:
                if chk['status'] == 'listed':
                    badge = '<span class="badge-listed">⛔ LISTED</span>'
                elif chk['status'] == 'clean':
                    badge = '<span class="badge-clean">✅ Clean</span>'
                else:
                    badge = '<span class="badge-warn">⏱ Timeout</span>'
                html += f"<tr><td><strong>{chk['list_name']}</strong></td><td><code>{chk['zone']}</code></td><td>{badge}</td></tr>"
            html += '</table>'
            st.markdown(html, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════
    #  EMAIL DIAGNOSTICS (NEW)
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def display_email(data):
        if not data:
            st.info("No email diagnostics available.")
            return

        # Overall status
        overall = data.get('overall_status', 'unknown')
        if overall == 'healthy':
            st.success("✅ Email infrastructure looks healthy")
        elif overall == 'issues':
            st.error("🚨 Email configuration has issues")
        else:
            st.warning("⚠️ Some email checks returned warnings")

        # Status summary
        mx = data.get('mx', {})
        spf = data.get('spf', {})
        dkim = data.get('dkim', {})
        dmarc = data.get('dmarc', {})

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("MX", _status_icon(mx.get('status')))
        c2.metric("SPF", _status_icon(spf.get('status')))
        c3.metric("DKIM", _status_icon(dkim.get('status')))
        c4.metric("DMARC", _status_icon(dmarc.get('status')))

        st.divider()

        # MX Details
        with st.expander("📧 MX Records", expanded=True):
            st.markdown(f"**Status:** {_status_badge(mx.get('status'))}  \n{mx.get('details', '')}", unsafe_allow_html=True)
            records = mx.get('records', [])
            if records:
                html = '<table class="record-table"><tr><th>Priority</th><th>Host</th><th>TTL</th><th>Reachable</th></tr>'
                for r in records:
                    reach = '<span class="badge-pass">Yes</span>' if r.get('reachable') else '<span class="badge-fail">No</span>'
                    html += f"<tr><td>{r.get('priority','')}</td><td><code>{r.get('host','')}</code></td><td>{r.get('ttl','—')}</td><td>{reach}</td></tr>"
                html += '</table>'
                st.markdown(html, unsafe_allow_html=True)

        # SPF Details
        with st.expander("📋 SPF Record"):
            st.markdown(f"**Status:** {_status_badge(spf.get('status'))}  \n{spf.get('details', '')}", unsafe_allow_html=True)
            rec = spf.get('record')
            if rec:
                st.code(rec, language=None)
                mechs = spf.get('mechanisms', [])
                if mechs:
                    st.markdown("**Mechanisms:** " + ", ".join(f"`{m}`" for m in mechs))

        # DKIM Details
        with st.expander("🔑 DKIM"):
            st.markdown(f"**Status:** {_status_badge(dkim.get('status'))}  \n{dkim.get('details', '')}", unsafe_allow_html=True)
            selectors = dkim.get('selectors_found', [])
            if selectors:
                for s in selectors:
                    st.markdown(f"**Selector `{s['selector']}`**")
                    st.code(s.get('record', ''), language=None)

        # DMARC Details
        with st.expander("🛡️ DMARC"):
            st.markdown(f"**Status:** {_status_badge(dmarc.get('status'))}  \n{dmarc.get('details', '')}", unsafe_allow_html=True)
            rec = dmarc.get('record')
            if rec:
                st.code(rec, language=None)
            policy = dmarc.get('policy')
            if policy:
                st.markdown(f"**Policy:** `{policy}`")

    # ═══════════════════════════════════════════════════════════
    #  EXTERNAL TOOLS (NEW)
    # ═══════════════════════════════════════════════════════════
    @staticmethod
    def display_tools(data):
        if not data:
            st.info("No tools data available.")
            return

        st.markdown(f"### 🔗 External Tools for **{data.get('domain', '')}**")
        st.caption("Click any card to open the tool in a new tab")

        tools = data.get('tools', [])
        if not tools:
            st.info("No tools generated.")
            return

        # Render as a grid of linked cards
        html = '<div class="tool-grid">'
        for tool in tools:
            html += f"""
            <a href="{tool['url']}" target="_blank" rel="noopener" class="tool-card">
                <div class="tool-icon">{tool['icon']}</div>
                <div>
                    <div class="tool-name">{tool['name']}</div>
                    <div class="tool-desc">{tool['description']}</div>
                    <div class="tool-category">{tool['category']}</div>
                </div>
            </a>"""
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
#  Helper functions
# ═══════════════════════════════════════════════════════════════

def _table_rows(rows):
    """Render key-value rows as a clean HTML table"""
    html = '<table class="record-table">'
    for label, value in rows:
        html += f'<tr><td style="width:40%;font-weight:500;color:#5f6368">{label}</td><td>{value}</td></tr>'
    html += '</table>'
    st.markdown(html, unsafe_allow_html=True)

def _trunc(text, maxlen=60):
    if not text or text == 'N/A':
        return 'N/A'
    return text[:maxlen] + '…' if len(str(text)) > maxlen else str(text)

def _status_icon(status):
    return {'pass': '✅ Pass', 'warning': '⚠️ Warning', 'fail': '❌ Fail'}.get(status, '❓')

def _status_badge(status):
    cls = {'pass': 'badge-pass', 'warning': 'badge-warn', 'fail': 'badge-fail'}.get(status, 'badge-info')
    label = {'pass': 'PASS', 'warning': 'WARNING', 'fail': 'FAIL'}.get(status, status or 'UNKNOWN')
    return f'<span class="{cls}">{label}</span>'
