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
            'ssl_valid': False,
            'has_ssl': False,
            'certificate_info': None,
            'certificate_details': {},
            'ssl_grade': None,
            'ssl_labs_grade': None,
            'protocol_version': None,
            'cipher_suite': None,
            'certificate_chain': [],
            'expiration_date': None,
            'days_until_expiry': None,
            'expires_in_days': None,
            'issuer': None,
            'subject': None,
            'key_size': None,
            'signature_algorithm': None,
            'security_issues': [],
            'recommendations': [],
        }

        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.netloc or parsed_url.path

            # Clean hostname (remove port if present)
            if ':' in hostname and not hostname.startswith('['):  # Not IPv6
                hostname = hostname.split(':')[0]

            port = 443

            # Check if SSL is available
            context = ssl.create_default_context()

            with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    ssl_info['has_ssl'] = True
                    ssl_info['ssl_valid'] = True  # SSL connection successful
                    cert = ssock.getpeercert()
                    ssl_info['protocol_version'] = ssock.version()
                    ssl_info['cipher_suite'] = ssock.cipher()

                    if cert:
                        ssl_info['certificate_info'] = cert

                        # Enhanced certificate details
                        cert_details = {}

                        # Parse subject and issuer safely
                        try:
                            subject = cert.get('subject', [])
                            if subject:
                                subject_dict = {key: value for key, value in subject[0]}
                                ssl_info['subject'] = subject_dict
                                cert_details['subject'] = subject_dict.get('commonName', 'N/A')
                        except Exception:
                            ssl_info['subject'] = {}
                            cert_details['subject'] = 'N/A'

                        try:
                            issuer = cert.get('issuer', [])
                            if issuer:
                                issuer_dict = {key: value for key, value in issuer[0]}
                                ssl_info['issuer'] = issuer_dict
                                cert_details['issuer'] = issuer_dict.get('organizationName', 'N/A')
                        except Exception:
                            ssl_info['issuer'] = {}
                            cert_details['issuer'] = 'N/A'

                        # Parse expiration date
                        try:
                            not_after = cert.get('notAfter')
                            if not_after and isinstance(not_after, str):
                                expiry_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
                                ssl_info['expiration_date'] = expiry_date
                                days_until_expiry = (expiry_date - datetime.now()).days
                                ssl_info['days_until_expiry'] = days_until_expiry
                                ssl_info['expires_in_days'] = days_until_expiry
                                cert_details['expires_in_days'] = days_until_expiry

                                # Add expiry warnings
                                if days_until_expiry < 7:
                                    ssl_info['security_issues'].append("Certificate expires in less than 7 days")
                                elif days_until_expiry < 30:
                                    ssl_info['security_issues'].append("Certificate expires in less than 30 days")
                        except Exception:
                            ssl_info['expiration_date'] = None
                            ssl_info['days_until_expiry'] = None

                        # Add protocol and cipher information
                        cert_details['protocol_version'] = ssl_info['protocol_version']
                        if ssl_info['cipher_suite']:
                            cipher_info = ssl_info['cipher_suite']
                            if isinstance(cipher_info, tuple) and len(cipher_info) >= 3:
                                cert_details['signature_algorithm'] = cipher_info[0]
                                cert_details['key_size'] = cipher_info[2] if cipher_info[2] else 'N/A'

                        # Security recommendations
                        if ssl_info['protocol_version'] in ['TLSv1', 'TLSv1.1']:
                            ssl_info['security_issues'].append("Using outdated TLS protocol")
                            ssl_info['recommendations'].append("Upgrade to TLS 1.2 or higher")

                        ssl_info['certificate_details'] = cert_details

                    # Derive SSL grade from gathered protocol/cipher info to avoid a second connection
                    ssl_info['ssl_grade'] = self._derive_grade_from_connection(ssl_info['protocol_version'], ssl_info.get('cipher_suite'))

        except Exception as e:
            ssl_info['error'] = str(e)

        return ssl_info

    def get_ssl_labs_grade(self, domain):
        """Get SSL Labs grade (simplified assessment)"""
        # Backwards-compatible wrapper that uses a derived grade when possible
        # Keep for API compatibility; prefer _derive_grade_from_connection
        return "N/A"

    def _derive_grade_from_connection(self, protocol, cipher):
        """Derive a simple grade from protocol and cipher info"""
        try:
            if protocol in ['TLSv1.3']:
                return "A+"
            elif protocol in ['TLSv1.2']:
                if cipher and isinstance(cipher, tuple) and len(cipher) >= 3 and cipher[2] and isinstance(cipher[2], int) and cipher[2] >= 256:
                    return "A"
                else:
                    return "B"
            elif protocol in ['TLSv1.1', 'TLSv1']:
                return "C"
            else:
                return "F"
        except Exception:
            return "N/A"
