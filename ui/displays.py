"""Display components for audit results"""
import streamlit as st
from utils.helpers import DataFormatter

class DisplayManager:
    """Manages display of audit results and components"""
    
    def __init__(self):
        self.formatter = DataFormatter()
    
    def display_dns_results(self, dns_data):
        """Display DNS analysis results"""
        if not dns_data:
            st.warning("No DNS data available")
            return
        
        st.subheader("🌐 DNS ANALYSIS")
        
        # DNS Records
        if 'records' in dns_data:
            with st.expander("DNS RECORDS", expanded=True):
                records = dns_data['records']
                
                # A Records
                if 'A' in records and records['A']:
                    st.write("**A Records:**")
                    for ip in records['A']:
                        st.code(f"A    {ip}")
                
                # AAAA Records
                if 'AAAA' in records and records['AAAA']:
                    st.write("**AAAA Records:**")
                    for ip in records['AAAA']:
                        st.code(f"AAAA {ip}")
                
                # CNAME Records
                if 'CNAME' in records and records['CNAME']:
                    st.write("**CNAME Records:**")
                    for cname in records['CNAME']:
                        st.code(f"CNAME {cname}")
                
                # MX Records
                if 'MX' in records and records['MX']:
                    st.write("**MX Records:**")
                    for mx in records['MX']:
                        st.code(f"MX   {mx}")
                
                # TXT Records
                if 'TXT' in records and records['TXT']:
                    st.write("**TXT Records:**")
                    for txt in records['TXT']:
                        st.code(f"TXT  {txt}")
        
        # DNS Performance
        if 'performance' in dns_data:
            perf = dns_data['performance']
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'query_time' in perf:
                    st.metric("Query Time", self.formatter.format_duration(perf['query_time']))
            
            with col2:
                if 'nameservers' in perf:
                    st.metric("Nameservers", len(perf['nameservers']))
            
            with col3:
                if 'ttl' in perf:
                    st.metric("TTL", f"{perf['ttl']}s")
    
    def display_ssl_results(self, ssl_data):
        """Display SSL analysis results"""
        if not ssl_data:
            st.warning("No SSL data available")
            return
        
        st.subheader("🔒 SSL/TLS ANALYSIS")
        
        # Certificate Info
        if 'certificate' in ssl_data:
            cert = ssl_data['certificate']
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'subject' in cert:
                    st.metric("Subject", cert['subject'])
                if 'issuer' in cert:
                    st.metric("Issuer", cert['issuer'])
            
            with col2:
                if 'valid_from' in cert:
                    st.metric("Valid From", cert['valid_from'])
                if 'valid_to' in cert:
                    st.metric("Valid To", cert['valid_to'])
        
        # Security Assessment
        if 'security' in ssl_data:
            security = ssl_data['security']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'grade' in security:
                    st.metric("SSL Grade", security['grade'])
            
            with col2:
                if 'protocol_version' in security:
                    st.metric("Protocol", security['protocol_version'])
            
            with col3:
                if 'cipher_suite' in security:
                    st.metric("Cipher Suite", security['cipher_suite'])
    
    def display_seo_results(self, seo_data):
        """Display SEO analysis results"""
        if not seo_data:
            st.warning("No SEO data available")
            return
        
        st.subheader("📈 SEO & MARKETING ANALYSIS")
        
        # Meta Tags
        if 'meta_tags' in seo_data:
            meta = seo_data['meta_tags']
            
            with st.expander("META TAGS", expanded=True):
                if 'title' in meta:
                    st.write(f"**Title:** {meta['title']}")
                    st.write(f"**Title Length:** {len(meta['title'])} chars")
                
                if 'description' in meta:
                    st.write(f"**Description:** {meta['description']}")
                    st.write(f"**Description Length:** {len(meta['description'])} chars")
                
                if 'keywords' in meta:
                    st.write(f"**Keywords:** {meta['keywords']}")
        
        # Social Media
        if 'social_media' in seo_data:
            social = seo_data['social_media']
            
            with st.expander("SOCIAL MEDIA TAGS"):
                if 'og_title' in social:
                    st.write(f"**OG Title:** {social['og_title']}")
                if 'og_description' in social:
                    st.write(f"**OG Description:** {social['og_description']}")
                if 'twitter_card' in social:
                    st.write(f"**Twitter Card:** {social['twitter_card']}")
        
        # Performance Metrics
        if 'performance' in seo_data:
            perf = seo_data['performance']
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if 'load_time' in perf:
                    st.metric("Load Time", self.formatter.format_duration(perf['load_time']))
            
            with col2:
                if 'page_size' in perf:
                    st.metric("Page Size", self.formatter.format_bytes(perf['page_size']))
            
            with col3:
                if 'images_count' in perf:
                    st.metric("Images", perf['images_count'])
            
            with col4:
                if 'links_count' in perf:
                    st.metric("Links", perf['links_count'])
    
    def display_performance_results(self, perf_data):
        """Display performance analysis results"""
        if not perf_data:
            st.warning("No performance data available")
            return
        
        st.subheader("⚡ PERFORMANCE ANALYSIS")
        
        # Core Web Vitals
        if 'core_web_vitals' in perf_data:
            vitals = perf_data['core_web_vitals']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'lcp' in vitals:
                    st.metric("LCP", self.formatter.format_duration(vitals['lcp']), 
                             help="Largest Contentful Paint")
            
            with col2:
                if 'fid' in vitals:
                    st.metric("FID", self.formatter.format_duration(vitals['fid']),
                             help="First Input Delay")
            
            with col3:
                if 'cls' in vitals:
                    st.metric("CLS", f"{vitals['cls']:.3f}",
                             help="Cumulative Layout Shift")
        
        # Resource Analysis
        if 'resources' in perf_data:
            resources = perf_data['resources']
            
            with st.expander("RESOURCE ANALYSIS"):
                if 'total_requests' in resources:
                    st.metric("Total Requests", resources['total_requests'])
                
                if 'total_size' in resources:
                    st.metric("Total Size", self.formatter.format_bytes(resources['total_size']))
                
                if 'compression_ratio' in resources:
                    st.metric("Compression Ratio", f"{resources['compression_ratio']:.1%}")
    
    def display_ranking_results(self, ranking_data):
        """Display ranking analysis results"""
        if not ranking_data:
            st.warning("No ranking data available")
            return
        
        st.subheader("🏆 RANKING ANALYSIS")
        
        # SEO Scores
        if 'seo_score' in ranking_data:
            score = ranking_data['seo_score']
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'overall' in score:
                    st.metric("Overall Score", f"{score['overall']}/100")
            
            with col2:
                if 'content' in score:
                    st.metric("Content Score", f"{score['content']}/100")
            
            with col3:
                if 'technical' in score:
                    st.metric("Technical Score", f"{score['technical']}/100")
        
        # Recommendations
        if 'recommendations' in ranking_data:
            recommendations = ranking_data['recommendations']
            
            with st.expander("RECOMMENDATIONS", expanded=True):
                for i, rec in enumerate(recommendations, 1):
                    st.write(f"**{i}.** {rec}")
    
    def display_audit_summary(self, audit_result):
        """Display complete audit summary"""
        if not audit_result:
            st.error("No audit results available")
            return
        
        # Handle error case
        if 'error' in audit_result:
            st.error(f"❌ **Analysis Failed:** {audit_result['error']}")
            return
        
        st.header("📊 AUDIT SUMMARY")
        
        # URL Info
        if 'url' in audit_result:
            st.info(f"**Analyzed URL:** {audit_result['url']}")
        
        if 'timestamp' in audit_result:
            st.info(f"**Analysis Date:** {audit_result['timestamp']}")
        
        if 'audit_mode' in audit_result:
            st.info(f"**Audit Mode:** {audit_result['audit_mode'].title()}")
        
        # Get results from nested structure
        results = audit_result.get('results', {})
        
        # Display each module's results
        if 'dns' in results:
            self.display_dns_results(results['dns'])
            st.divider()
        
        if 'ssl' in results:
            self.display_ssl_results(results['ssl'])
            st.divider()
        
        if 'seo_marketing' in results:
            self.display_seo_results(results['seo_marketing'])
            st.divider()
        
        if 'performance' in results:
            self.display_performance_results(results['performance'])
            st.divider()
        
        if 'ranking' in results:
            self.display_ranking_results(results['ranking'])
    
    def display_error_message(self, error_msg):
        """Display error message with styling"""
        st.error(f"❌ **Analysis Failed**\n\n{error_msg}")
    
    def display_loading_message(self, message="Analyzing website..."):
        """Display loading message with progress"""
        with st.spinner(message):
            st.info("🔍 This may take a few moments depending on the website size and complexity.")
    
    def display_success_message(self, message="Analysis completed successfully!"):
        """Display success message"""
        st.success(f"✅ {message}")
