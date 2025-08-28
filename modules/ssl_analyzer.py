"""SSL/TLS Analysis Module"""
import ssl
import socket
import requests
from datetime import datetime
from urllib.parse import urlparse

class SSLAnalyzer:
    def __init__(self):
        self.timeout = 10
        
    def analyze_ssl(self, url):
        """Comprehensive SSL/TLS analysis"""
        ssl_info = {
            'has_ssl': False,
            'certificate_info': None,
            'ssl_labs_grade': None,
            'protocol_version': None,
            'cipher_suite': None,
            'certificate_chain': [],
            'expiration_date': None,
            'days_until_expiry': None,
            'issuer': None,
            'subject': None
        }
        
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.netloc or parsed_url.path
            port = 443
            
            # Check if SSL is available
            context = ssl.create_default_context()
            
            with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    ssl_info['has_ssl'] = True
                    cert = ssock.getpeercert()
                    ssl_info['protocol_version'] = ssock.version()
                    ssl_info['cipher_suite'] = ssock.cipher()
                    
                    if cert:
                        ssl_info['certificate_info'] = cert
                        
                        # Parse subject and issuer safely
                        try:
                            subject = cert.get('subject', [])
                            if subject:
                                ssl_info['subject'] = {key: value for key, value in subject[0]}
                        except:
                            ssl_info['subject'] = {}
                        
                        try:
                            issuer = cert.get('issuer', [])
                            if issuer:
                                ssl_info['issuer'] = {key: value for key, value in issuer[0]}
                        except:
                            ssl_info['issuer'] = {}
                        
                        # Parse expiration date
                        try:
                            not_after = cert.get('notAfter')
                            if not_after and isinstance(not_after, str):
                                expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                                ssl_info['expiration_date'] = expiry_date
                                ssl_info['days_until_expiry'] = (expiry_date - datetime.now()).days
                        except:
                            ssl_info['expiration_date'] = None
                            ssl_info['days_until_expiry'] = None
                        
        except Exception as e:
            ssl_info['error'] = str(e)
            
        return ssl_info
        
    def get_ssl_labs_grade(self, domain):
        """Get SSL Labs grade (simplified)"""
        try:
            # This would normally call SSL Labs API
            # For now, return a mock grade based on SSL availability
            return "A"  # Placeholder
        except:
            return None
