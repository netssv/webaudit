"""DNS Analysis Module"""
import socket
import dns.resolver
import whois
from datetime import datetime

class DNSAnalyzer:
    def __init__(self):
        self.dns_resolver = dns.resolver.Resolver()
        
    def analyze_dns(self, domain):
        """Comprehensive DNS analysis"""
        dns_info = {
            'ip_address': None,
            'a_records': [],
            'mx_records': [],
            'ns_records': [],
            'txt_records': [],
            'whois_info': None,
            'dns_response_time': None
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
            except:
                pass
                
            # Get MX records
            try:
                mx_records = self.dns_resolver.resolve(domain, 'MX')
                dns_info['mx_records'] = [f"{record.preference} {record.exchange}" for record in mx_records]
            except:
                pass
                
            # Get NS records
            try:
                ns_records = self.dns_resolver.resolve(domain, 'NS')
                dns_info['ns_records'] = [str(record) for record in ns_records]
            except:
                pass
                
            # Get TXT records
            try:
                txt_records = self.dns_resolver.resolve(domain, 'TXT')
                dns_info['txt_records'] = [str(record) for record in txt_records]
            except:
                pass
                
        except Exception as e:
            dns_info['error'] = str(e)
            
        return dns_info
        
    def get_whois_info(self, domain):
        """Get WHOIS information"""
        try:
            w = whois.whois(domain)
            return {
                'registrar': w.registrar,
                'creation_date': w.creation_date,
                'expiration_date': w.expiration_date,
                'name_servers': w.name_servers,
                'status': w.status
            }
        except:
            return None
