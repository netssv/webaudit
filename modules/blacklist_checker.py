"""IP/Domain Blacklist Checker Module - DNSBL Lookup"""
import socket
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed


class BlacklistChecker:
    """Check if an IP or domain is listed on major DNS-based blacklists (DNSBL)."""

    # Major DNSBL providers
    DNSBL_LISTS = {
        'Spamhaus ZEN': 'zen.spamhaus.org',
        'Barracuda': 'b.barracudacentral.org',
        'SpamCop': 'bl.spamcop.net',
        'SORBS': 'dnsbl.sorbs.net',
        'UCEPROTECT L1': 'dnsbl-1.uceprotect.net',
        'Spamhaus SBL': 'sbl.spamhaus.org',
        'Spamhaus XBL': 'xbl.spamhaus.org',
        'PSBL': 'psbl.surriel.com',
        'Truncate': 'truncate.gbudb.net',
        'JustSpam': 'dnsbl.justspam.org',
    }

    def __init__(self):
        self.timeout = 3

    def check_blacklists(self, domain):
        """Check domain IP against all DNSBL lists. Returns structured results."""
        results = {
            'domain': domain,
            'ip': None,
            'total_lists': len(self.DNSBL_LISTS),
            'listed_count': 0,
            'clean_count': 0,
            'error_count': 0,
            'checks': [],
            'status': 'clean',  # clean | listed | error
        }

        # Resolve domain to IP
        try:
            ip = socket.gethostbyname(domain)
            results['ip'] = ip
        except Exception as e:
            results['status'] = 'error'
            results['error'] = f'Could not resolve domain: {e}'
            return results

        # Reverse IP for DNSBL query
        reversed_ip = '.'.join(reversed(ip.split('.')))

        # Query all DNSBL lists in parallel
        def _check_single(name, zone):
            query = f'{reversed_ip}.{zone}'
            try:
                resolver = dns.resolver.Resolver()
                resolver.timeout = self.timeout
                resolver.lifetime = self.timeout
                answers = resolver.resolve(query, 'A')
                return {
                    'list_name': name,
                    'zone': zone,
                    'listed': True,
                    'response': str(answers[0]),
                    'status': 'listed',
                }
            except dns.resolver.NXDOMAIN:
                return {
                    'list_name': name,
                    'zone': zone,
                    'listed': False,
                    'response': None,
                    'status': 'clean',
                }
            except Exception as e:
                return {
                    'list_name': name,
                    'zone': zone,
                    'listed': False,
                    'response': None,
                    'status': 'timeout',
                    'error': str(e),
                }

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {
                executor.submit(_check_single, name, zone): name
                for name, zone in self.DNSBL_LISTS.items()
            }
            for future in as_completed(futures):
                check = future.result()
                results['checks'].append(check)
                if check['status'] == 'listed':
                    results['listed_count'] += 1
                elif check['status'] == 'clean':
                    results['clean_count'] += 1
                else:
                    results['error_count'] += 1

        # Sort: listed first, then clean, then errors
        order = {'listed': 0, 'clean': 1, 'timeout': 2}
        results['checks'].sort(key=lambda c: order.get(c['status'], 3))

        if results['listed_count'] > 0:
            results['status'] = 'listed'
        elif results['error_count'] == results['total_lists']:
            results['status'] = 'error'

        return results
