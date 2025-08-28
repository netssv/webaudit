"""Core Web Auditor Class"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.dns_analyzer import DNSAnalyzer
from modules.ssl_analyzer import SSLAnalyzer
from modules.seo_marketing_analyzer import SEOMarketingAnalyzer
from modules.performance_analyzer import PerformanceAnalyzer
from modules.ranking_analyzer import RankingAnalyzer

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import json
from datetime import datetime

class WebAuditor:
    def __init__(self):
        self.dns_analyzer = DNSAnalyzer()
        self.ssl_analyzer = SSLAnalyzer()
        self.seo_analyzer = SEOMarketingAnalyzer()
        self.performance_analyzer = PerformanceAnalyzer()
        self.ranking_analyzer = RankingAnalyzer()
        self.timeout = 10
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
    def validate_url(self, url):
        """Validate and normalize URL"""
        if not url:
            return None
            
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return None
            return url
        except:
            return None
            
    def get_domain_from_url(self, url):
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc.replace('www.', '')
        except:
            return None
            
    def fetch_page_content(self, url):
        """Fetch page content and return BeautifulSoup object"""
        try:
            response = requests.get(
                url, 
                timeout=self.timeout,
                headers={'User-Agent': self.user_agent},
                allow_redirects=True
            )
            return BeautifulSoup(response.content, 'html.parser'), response
        except Exception as e:
            return None, None
            
    def comprehensive_audit(self, url, selected_modules=None):
        """Perform website audit based on selected modules"""
        # Default to all modules if none specified
        if selected_modules is None:
            selected_modules = {
                'dns': True, 'ssl': True, 'seo_marketing': True, 
                'performance': True, 'ranking': True
            }
        
        # Validate URL
        validated_url = self.validate_url(url)
        if not validated_url:
            return {'error': 'Invalid URL provided'}
            
        domain = self.get_domain_from_url(validated_url)
        if not domain:
            return {'error': 'Could not extract domain from URL'}
            
        audit_results = {
            'url': validated_url,
            'domain': domain,
            'selected_modules': selected_modules,
            'timestamp': datetime.now().isoformat(),
            'results': {}
        }
        
        # Fetch page content once
        soup, response = self.fetch_page_content(validated_url)
        
        try:
            # DNS Analysis
            if selected_modules.get('dns', False):
                audit_results['results']['dns'] = self.dns_analyzer.analyze_dns(domain)
                
            # SSL Analysis
            if selected_modules.get('ssl', False):
                audit_results['results']['ssl'] = self.ssl_analyzer.analyze_ssl(validated_url)
                
            # Performance Analysis
            if selected_modules.get('performance', False):
                audit_results['results']['performance'] = self.performance_analyzer.analyze_performance(validated_url)
            
            # SEO and Marketing Analysis
            if selected_modules.get('seo_marketing', False) and soup:
                audit_results['results']['seo_marketing'] = self.seo_analyzer.analyze_seo_marketing(validated_url, soup, response)
                    
            # Website Ranking Analysis
            if selected_modules.get('ranking', False):
                audit_results['results']['ranking'] = self.ranking_analyzer.analyze_website_ranking(domain)
                
            # WHOIS Information (included with DNS)
            if selected_modules.get('dns', False):
                audit_results['results']['whois'] = self.dns_analyzer.get_whois_info(domain)
                
        except Exception as e:
            audit_results['error'] = f"Audit failed: {str(e)}"
            
        return audit_results
        
    def export_to_json(self, audit_results, filename=None):
        """Export audit results to JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = audit_results.get('domain', 'unknown')
            filename = f"audit_{domain}_{timestamp}.json"
            
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(audit_results, f, indent=2, ensure_ascii=False, default=str)
            return filename
        except Exception as e:
            return None
            
    def generate_summary_report(self, audit_results):
        """Generate a summary report from audit results"""
        if 'error' in audit_results:
            return f"Audit failed: {audit_results['error']}"
            
        summary = []
        summary.append(f"Website Audit Report for {audit_results['domain']}")
        
        # Show selected modules
        selected_modules = audit_results.get('selected_modules', {})
        active_modules = [module.replace('_', ' ').title() for module, enabled in selected_modules.items() if enabled]
        summary.append(f"Analyzed Modules: {', '.join(active_modules) if active_modules else 'None'}")
        summary.append(f"Timestamp: {audit_results['timestamp']}")
        summary.append("-" * 50)
        
        results = audit_results.get('results', {})
        
        # Performance Summary
        if 'performance' in results:
            perf = results['performance']
            summary.append(f"🚀 Performance:")
            summary.append(f"  - Response Time: {perf.get('response_time', 'N/A')} ms")
            summary.append(f"  - Status Code: {perf.get('status_code', 'N/A')}")
            summary.append(f"  - Page Size: {perf.get('page_size', 'N/A')} bytes")
            
        # SEO Summary
        if 'seo_marketing' in results:
            seo = results['seo_marketing']
            summary.append(f"🔍 SEO:")
            summary.append(f"  - Title: {seo.get('title', 'N/A')}")
            summary.append(f"  - Meta Description: {'Yes' if seo.get('meta_description') else 'No'}")
            summary.append(f"  - SEO Score: {seo.get('seo_score', 'N/A')}/100")
            summary.append(f"  - Marketing Tools: {len(seo.get('marketing_tools', []))}")
            
        # SSL Summary
        if 'ssl' in results:
            ssl = results['ssl']
            summary.append(f"🔒 SSL:")
            summary.append(f"  - SSL Enabled: {'Yes' if ssl.get('has_ssl') else 'No'}")
            summary.append(f"  - Days Until Expiry: {ssl.get('days_until_expiry', 'N/A')}")
            
        # Ranking Summary
        if 'ranking' in results:
            ranking = results['ranking']
            summary.append(f"📊 Ranking:")
            summary.append(f"  - Domain Authority: {ranking.get('domain_authority', 'N/A')}")
            summary.append(f"  - Page Authority: {ranking.get('page_authority', 'N/A')}")
            summary.append(f"  - Organic Traffic Est.: {ranking.get('organic_traffic_estimate', 'N/A')}")
            
        return "\n".join(summary)
