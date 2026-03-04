"""Email Diagnostics Module - MX, SPF, DKIM, DMARC analysis"""
import dns.resolver
import socket
import re


class EmailDiagnostics:
    """Analyze email infrastructure: MX records, SPF, DKIM, DMARC."""

    # Common DKIM selectors to probe
    DKIM_SELECTORS = [
        'default', 'google', 'selector1', 'selector2',
        'k1', 'mail', 'dkim', 'smtp', 'mandrill', 'ses',
    ]

    def __init__(self):
        self.timeout = 5

    def analyze_email(self, domain):
        """Full email diagnostics for a domain."""
        results = {
            'domain': domain,
            'mx': self._check_mx(domain),
            'spf': self._check_spf(domain),
            'dkim': self._check_dkim(domain),
            'dmarc': self._check_dmarc(domain),
            'overall_status': 'unknown',
        }

        # Calculate overall health
        statuses = [
            results['mx']['status'],
            results['spf']['status'],
            results['dmarc']['status'],
        ]
        if all(s == 'pass' for s in statuses):
            results['overall_status'] = 'healthy'
        elif any(s == 'fail' for s in statuses):
            results['overall_status'] = 'issues'
        else:
            results['overall_status'] = 'warning'

        return results

    # ── MX Records ──────────────────────────────────────────────
    def _check_mx(self, domain):
        """Check MX records and mail server reachability."""
        result = {
            'status': 'fail',
            'records': [],
            'details': '',
        }
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = self.timeout
            resolver.lifetime = self.timeout
            answers = resolver.resolve(domain, 'MX')
            for rdata in answers:
                mx_host = str(rdata.exchange).rstrip('.')
                priority = rdata.preference
                reachable = self._check_smtp_banner(mx_host)
                result['records'].append({
                    'host': mx_host,
                    'priority': priority,
                    'reachable': reachable,
                    'ttl': answers.rrset.ttl,
                })
            if result['records']:
                result['status'] = 'pass'
                result['details'] = f'{len(result["records"])} MX record(s) found'
            else:
                result['details'] = 'No MX records found'
        except dns.resolver.NoAnswer:
            result['details'] = 'No MX records configured'
        except dns.resolver.NXDOMAIN:
            result['details'] = 'Domain does not exist'
        except Exception as e:
            result['details'] = f'Error querying MX: {e}'
        return result

    def _check_smtp_banner(self, host, port=25, timeout=3):
        """Attempt to connect to SMTP and read banner."""
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                banner = sock.recv(1024).decode('utf-8', errors='replace').strip()
                return bool(banner)
        except Exception:
            return False

    # ── SPF Record ──────────────────────────────────────────────
    def _check_spf(self, domain):
        """Check for SPF record in TXT records."""
        result = {
            'status': 'fail',
            'record': None,
            'details': '',
            'mechanisms': [],
        }
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = self.timeout
            resolver.lifetime = self.timeout
            answers = resolver.resolve(domain, 'TXT')
            for rdata in answers:
                txt = str(rdata).strip('"')
                if txt.lower().startswith('v=spf1'):
                    result['record'] = txt
                    result['status'] = 'pass'
                    # Parse mechanisms
                    parts = txt.split()
                    result['mechanisms'] = parts[1:]  # skip v=spf1
                    # Check for common issues
                    if '+all' in txt:
                        result['status'] = 'warning'
                        result['details'] = 'SPF uses +all (permits any sender — insecure)'
                    elif '~all' in txt:
                        result['details'] = 'SPF configured with soft-fail (~all)'
                    elif '-all' in txt:
                        result['details'] = 'SPF configured with hard-fail (-all) ✓'
                    elif '?all' in txt:
                        result['status'] = 'warning'
                        result['details'] = 'SPF uses ?all (neutral — weak)'
                    else:
                        result['details'] = 'SPF record found'
                    break
            if not result['record']:
                result['details'] = 'No SPF record found'
        except Exception as e:
            result['details'] = f'Error querying SPF: {e}'
        return result

    # ── DKIM ────────────────────────────────────────────────────
    def _check_dkim(self, domain):
        """Probe common DKIM selectors."""
        result = {
            'status': 'warning',
            'selectors_found': [],
            'details': '',
        }
        resolver = dns.resolver.Resolver()
        resolver.timeout = self.timeout
        resolver.lifetime = self.timeout

        for selector in self.DKIM_SELECTORS:
            try:
                qname = f'{selector}._domainkey.{domain}'
                answers = resolver.resolve(qname, 'TXT')
                for rdata in answers:
                    txt = str(rdata).strip('"')
                    if 'v=DKIM1' in txt or 'p=' in txt:
                        result['selectors_found'].append({
                            'selector': selector,
                            'record': txt[:120] + ('…' if len(txt) > 120 else ''),
                        })
            except Exception:
                continue

        if result['selectors_found']:
            result['status'] = 'pass'
            result['details'] = f'{len(result["selectors_found"])} DKIM selector(s) found'
        else:
            result['details'] = 'No common DKIM selectors detected (may use custom selector)'
        return result

    # ── DMARC ───────────────────────────────────────────────────
    def _check_dmarc(self, domain):
        """Check for DMARC record."""
        result = {
            'status': 'fail',
            'record': None,
            'policy': None,
            'details': '',
        }
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = self.timeout
            resolver.lifetime = self.timeout
            qname = f'_dmarc.{domain}'
            answers = resolver.resolve(qname, 'TXT')
            for rdata in answers:
                txt = str(rdata).strip('"')
                if txt.lower().startswith('v=dmarc1'):
                    result['record'] = txt
                    result['status'] = 'pass'
                    # Extract policy
                    match = re.search(r'p\s*=\s*(\w+)', txt, re.IGNORECASE)
                    if match:
                        result['policy'] = match.group(1).lower()
                    if result['policy'] == 'none':
                        result['status'] = 'warning'
                        result['details'] = 'DMARC policy is "none" (monitoring only)'
                    elif result['policy'] == 'quarantine':
                        result['details'] = 'DMARC policy: quarantine'
                    elif result['policy'] == 'reject':
                        result['details'] = 'DMARC policy: reject ✓'
                    else:
                        result['details'] = 'DMARC record found'
                    break
            if not result['record']:
                result['details'] = 'No DMARC record found'
        except dns.resolver.NXDOMAIN:
            result['details'] = 'No DMARC record found'
        except dns.resolver.NoAnswer:
            result['details'] = 'No DMARC record found'
        except Exception as e:
            result['details'] = f'Error querying DMARC: {e}'
        return result
