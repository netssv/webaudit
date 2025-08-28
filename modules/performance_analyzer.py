"""Performance Analysis Module"""
import time
import requests
from datetime import datetime

class PerformanceAnalyzer:
    def __init__(self):
        self.timeout = 30
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
    def analyze_performance(self, url):
        """Comprehensive performance analysis"""
        performance_info = {
            'response_time': None,
            'page_size': None,
            'status_code': None,
            'redirect_count': 0,
            'server_info': {},
            'compression': None,
            'cache_headers': {},
            'pagespeed_score': None
        }
        
        try:
            # Measure response time
            start_time = time.time()
            response = requests.get(
                url, 
                timeout=self.timeout,
                headers={'User-Agent': self.user_agent},
                allow_redirects=True
            )
            end_time = time.time()
            
            performance_info['response_time'] = round((end_time - start_time) * 1000, 2)  # ms
            performance_info['status_code'] = response.status_code
            performance_info['page_size'] = len(response.content)
            performance_info['redirect_count'] = len(response.history)
            
            # Server information
            headers = response.headers
            performance_info['server_info'] = {
                'server': headers.get('Server', 'Unknown'),
                'powered_by': headers.get('X-Powered-By', 'Unknown'),
                'content_type': headers.get('Content-Type', 'Unknown')
            }
            
            # Compression
            performance_info['compression'] = headers.get('Content-Encoding', 'none')
            
            # Cache headers
            performance_info['cache_headers'] = {
                'cache_control': headers.get('Cache-Control'),
                'expires': headers.get('Expires'),
                'etag': headers.get('ETag'),
                'last_modified': headers.get('Last-Modified')
            }
            
        except Exception as e:
            performance_info['error'] = str(e)
            
        return performance_info
        
    def get_pagespeed_score(self, url):
        """Get PageSpeed Insights score (mock implementation)"""
        try:
            # This would normally call Google PageSpeed Insights API
            # For now, return a score based on response time
            perf_info = self.analyze_performance(url)
            if perf_info.get('response_time'):
                if perf_info['response_time'] < 1000:
                    return {'mobile': 85, 'desktop': 90}
                elif perf_info['response_time'] < 2000:
                    return {'mobile': 70, 'desktop': 80}
                else:
                    return {'mobile': 50, 'desktop': 60}
            return {'mobile': 0, 'desktop': 0}
        except:
            return {'mobile': 0, 'desktop': 0}
