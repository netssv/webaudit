"""DNS Analysis Module"""
import socket
import dns.resolver
import time
from datetime import datetime
from functools import lru_cache

class DNSAnalyzer:
    def __init__(self):
        self.dns_resolver = dns.resolver.Resolver()
        # Set conservative timeouts to avoid long blocking
        try:
            self.dns_resolver.timeout = 3
            self.dns_resolver.lifetime = 5
        except Exception:
            pass
        
        # Popular public DNS servers for performance testing
        self.public_dns_servers = {
            'Google': '8.8.8.8',
            'Cloudflare': '1.1.1.1', 
            'Quad9': '9.9.9.9',
            'Yandex': '77.88.8.8',
            'OpenDNS': '208.67.222.222',
            'Comodo': '8.26.56.26'
        }

    def analyze_dns(self, domain):
        """Comprehensive DNS analysis"""
        dns_info = {
            'ip_address': None,
            'a_records': [],
            'mx_records': [],
            'ns_records': [],
            'txt_records': [],
            'whois_info': None,
            'dns_response_time': None,
            'dns_server_performance': []
        }

        try:
            # Get IP address
            start_time = datetime.now()
            ip_address = socket.gethostbyname(domain)
            end_time = datetime.now()
            dns_info['ip_address'] = ip_address
            dns_info['dns_response_time'] = (end_time - start_time).total_seconds() * 1000

            # Get A records
            try:
                a_records = self.dns_resolver.resolve(domain, 'A')
                dns_info['a_records'] = [str(record) for record in a_records]
            except Exception:
                pass

            # Get MX records
            try:
                mx_records = self.dns_resolver.resolve(domain, 'MX')
                dns_info['mx_records'] = [f"{getattr(record, 'preference', '')} {getattr(record, 'exchange', '')}" for record in mx_records]
            except Exception:
                pass

            # Get NS records
            try:
                ns_records = self.dns_resolver.resolve(domain, 'NS')
                dns_info['ns_records'] = [str(record) for record in ns_records]
            except Exception:
                pass

            # Get TXT records
            try:
                txt_records = self.dns_resolver.resolve(domain, 'TXT')
                dns_info['txt_records'] = [str(record) for record in txt_records]
            except Exception:
                pass
            
            # DNS Server Performance Analysis
            try:
                dns_info['dns_server_performance'] = self.analyze_dns_server_performance(domain)
            except Exception as e:
                dns_info['dns_server_performance'] = [{'error': f'Performance analysis failed: {str(e)}'}]

        except Exception as e:
            dns_info['error'] = str(e)

        return dns_info

    def analyze_dns_server_performance(self, domain, max_servers=4):
        """Analyze DNS server response times for a domain"""
        performance_results = []
        
        # Test only the top servers to avoid too many requests
        test_servers = dict(list(self.public_dns_servers.items())[:max_servers])
        
        for server_name, server_ip in test_servers.items():
            try:
                # Create a custom resolver for this server
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [server_ip]
                resolver.timeout = 2  # Shorter timeout for performance testing
                resolver.lifetime = 3
                
                # Measure response time
                start_time = time.time()
                answers = resolver.resolve(domain, 'A')
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                
                # Get the first A record result
                resolved_ip = str(answers[0]) if answers else 'N/A'
                
                performance_results.append({
                    'server_name': server_name,
                    'server_ip': server_ip,
                    'response_time': round(response_time, 3),
                    'response_time_ms': round(response_time, 1),  # For display purposes
                    'resolved_ip': resolved_ip,
                    'status': 'success'
                })
                
            except Exception as e:
                performance_results.append({
                    'server_name': server_name,
                    'server_ip': server_ip,
                    'response_time': None,
                    'resolved_ip': 'ERROR',
                    'status': 'failed',
                    'error': str(e)
                })
        
        # Sort by response time (fastest first)
        successful_results = [r for r in performance_results if r['status'] == 'success']
        failed_results = [r for r in performance_results if r['status'] == 'failed']
        
        successful_results.sort(key=lambda x: x['response_time'])
        
        return successful_results + failed_results

    def get_whois_info(self, domain):
        """Get WHOIS information"""
        # Lazy import whois to avoid heavy import on module load
        try:
            import whois
        except Exception:
            return None

        try:
            w = whois.whois(domain)
            return {
                'registrar': getattr(w, 'registrar', None),
                'creation_date': getattr(w, 'creation_date', None),
                'expiration_date': getattr(w, 'expiration_date', None),
                'name_servers': getattr(w, 'name_servers', None),
                'status': getattr(w, 'status', None),
            }
        except Exception:
            return None

    # Cache WHOIS results to reduce repeated slow lookups
    @lru_cache(maxsize=128)
    def get_whois_info_cached(self, domain):
        return self.get_whois_info(domain)
