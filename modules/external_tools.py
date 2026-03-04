"""External Tools & Utility Links Module"""
from urllib.parse import quote_plus


class ExternalTools:
    """Generate useful external tool links for any domain."""

    TOOLS = [
        {
            'name': 'Wayback Machine',
            'icon': '🏛️',
            'category': 'History',
            'description': 'View archived versions of the website over time',
            'url_template': 'https://web.archive.org/web/*/{domain}',
        },
        {
            'name': 'Google Cache',
            'icon': '📸',
            'category': 'Search',
            'description': 'View Google\'s cached version of the page',
            'url_template': 'https://webcache.googleusercontent.com/search?q=cache:{domain}',
        },
        {
            'name': 'PageSpeed Insights',
            'icon': '⚡',
            'category': 'Performance',
            'description': 'Google PageSpeed analysis and Core Web Vitals',
            'url_template': 'https://pagespeed.web.dev/analysis?url=https%3A%2F%2F{domain}',
        },
        {
            'name': 'BuiltWith',
            'icon': '🔧',
            'category': 'Technology',
            'description': 'Discover what technologies the website uses',
            'url_template': 'https://builtwith.com/{domain}',
        },
        {
            'name': 'Security Headers',
            'icon': '🛡️',
            'category': 'Security',
            'description': 'Analyze HTTP security headers',
            'url_template': 'https://securityheaders.com/?q={domain}&followRedirects=on',
        },
        {
            'name': 'Who.is WHOIS',
            'icon': '🔍',
            'category': 'Domain',
            'description': 'Detailed WHOIS domain registration lookup',
            'url_template': 'https://who.is/whois/{domain}',
        },
        {
            'name': 'DNS Checker',
            'icon': '🌐',
            'category': 'DNS',
            'description': 'Check DNS propagation worldwide',
            'url_template': 'https://dnschecker.org/#A/{domain}',
        },
        {
            'name': 'MXToolbox',
            'icon': '📧',
            'category': 'Email',
            'description': 'Complete email deliverability and MX diagnostics',
            'url_template': 'https://mxtoolbox.com/SuperTool.aspx?action=mx%3a{domain}&run=toolpage',
        },
        {
            'name': 'Shodan',
            'icon': '🔎',
            'category': 'Security',
            'description': 'Search for exposed services and open ports',
            'url_template': 'https://www.shodan.io/search?query={domain}',
        },
        {
            'name': 'VirusTotal',
            'icon': '🦠',
            'category': 'Security',
            'description': 'Scan for malware and malicious activity',
            'url_template': 'https://www.virustotal.com/gui/domain/{domain}',
        },
        {
            'name': 'SSL Labs',
            'icon': '🔒',
            'category': 'Security',
            'description': 'Deep SSL/TLS configuration analysis',
            'url_template': 'https://www.ssllabs.com/ssltest/analyze.html?d={domain}',
        },
        {
            'name': 'Google Search Console',
            'icon': '📊',
            'category': 'SEO',
            'description': 'Check Google indexing and search performance',
            'url_template': 'https://search.google.com/search-console?resource_id=sc-domain%3A{domain}',
        },
        # ── Additional Security Testing Tools ────────────────
        {
            'name': 'Mozilla Observatory',
            'icon': '🔬',
            'category': 'Security',
            'description': 'Mozilla HTTP security observatory scan',
            'url_template': 'https://observatory.mozilla.org/analyze/{domain}',
        },
        {
            'name': 'Pentest-Tools',
            'icon': '🧪',
            'category': 'Security',
            'description': 'Website vulnerability scanner and recon tools',
            'url_template': 'https://pentest-tools.com/website-vulnerability-scanning/website-scanner?url=https%3A%2F%2F{domain}',
        },
        {
            'name': 'CRT.sh',
            'icon': '📜',
            'category': 'Security',
            'description': 'Certificate transparency log — find sub-domains',
            'url_template': 'https://crt.sh/?q=%25.{domain}',
        },
        {
            'name': 'Sucuri SiteCheck',
            'icon': '🏥',
            'category': 'Security',
            'description': 'Free malware and security scanner',
            'url_template': 'https://sitecheck.sucuri.net/results/{domain}',
        },
        {
            'name': 'CSP Evaluator',
            'icon': '🔐',
            'category': 'Security',
            'description': 'Evaluate Content Security Policy strength',
            'url_template': 'https://csp-evaluator.withgoogle.com/?url=https://{domain}',
        },
        # ── Additional Marketing / SEO Tools ─────────────────
        {
            'name': 'SimilarWeb',
            'icon': '📈',
            'category': 'Marketing',
            'description': 'Traffic estimates, competitors & audience insights',
            'url_template': 'https://www.similarweb.com/website/{domain}/',
        },
        {
            'name': 'Ahrefs Backlink Checker',
            'icon': '🔗',
            'category': 'SEO',
            'description': 'Free backlink checker and top pages',
            'url_template': 'https://ahrefs.com/backlink-checker/?input={domain}&mode=subdomains',
        },
        {
            'name': 'GTmetrix',
            'icon': '🏎️',
            'category': 'Performance',
            'description': 'Page performance scores with Lighthouse & CWV',
            'url_template': 'https://gtmetrix.com/?url=https%3A%2F%2F{domain}',
        },
    ]

    def generate_links(self, domain):
        """Generate all external tool links for a domain."""
        clean_domain = domain.replace('www.', '').strip('/')
        links = []
        for tool in self.TOOLS:
            links.append({
                'name': tool['name'],
                'icon': tool['icon'],
                'category': tool['category'],
                'description': tool['description'],
                'url': tool['url_template'].format(domain=clean_domain),
            })
        return {
            'domain': clean_domain,
            'tools': links,
            'total': len(links),
        }
