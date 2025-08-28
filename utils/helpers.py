"""Helper utilities for the web audit application"""
import re
from urllib.parse import urlparse

class URLValidator:
    """URL validation and normalization utilities"""
    
    @staticmethod
    def validate_and_normalize(url):
        """Validate and normalize URL"""
        if not url:
            return None, "URL is required"
        
        # Remove whitespace
        url = url.strip()
        
        # Add protocol if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Parse URL
        try:
            parsed = urlparse(url)
            if not parsed.netloc:
                return None, "Invalid URL format"
            
            # Reconstruct clean URL
            clean_url = f"{parsed.scheme}://{parsed.netloc}"
            if parsed.path and parsed.path != '/':
                clean_url += parsed.path
            
            return clean_url, None
            
        except Exception as e:
            return None, f"URL validation error: {str(e)}"
    
    @staticmethod
    def extract_domain(url):
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc.replace('www.', '')
        except:
            return url

class DataFormatter:
    """Data formatting utilities"""
    
    @staticmethod
    def format_bytes(bytes_value):
        """Format bytes to human readable format"""
        if not bytes_value:
            return "0 B"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} TB"
    
    @staticmethod
    def format_duration(seconds):
        """Format duration in seconds to human readable format"""
        if not seconds:
            return "0s"
        
        if seconds < 1:
            return f"{seconds*1000:.0f}ms"
        elif seconds < 60:
            return f"{seconds:.1f}s"
        else:
            minutes = seconds // 60
            secs = seconds % 60
            return f"{minutes:.0f}m {secs:.0f}s"
    
    @staticmethod
    def format_score(score, max_score=100):
        """Format score with color coding"""
        if not score:
            return "N/A"
        
        percentage = (score / max_score) * 100
        if percentage >= 90:
            color = "green"
        elif percentage >= 70:
            color = "orange"
        else:
            color = "red"
        
        return f"<span style='color: {color}'>{score}/{max_score}</span>"
