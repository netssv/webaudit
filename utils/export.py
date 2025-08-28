"""Export utilities for audit reports"""
import json
import csv
import pandas as pd
from datetime import datetime
import os

class ExportManager:
    """Handle various export formats for audit results"""
    
    def __init__(self):
        self.export_dir = "exports"
        self._ensure_export_dir()
    
    def _ensure_export_dir(self):
        """Create export directory if it doesn't exist"""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    def export_to_json(self, results, filename=None):
        """Export results to JSON format"""
        if not filename:
            domain = results.get('domain', 'unknown')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.export_dir}/audit_{domain}_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str, ensure_ascii=False)
            return filename
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            return None
    
    def export_to_csv(self, results, filename=None):
        """Export results to CSV format (flattened)"""
        if not filename:
            domain = results.get('domain', 'unknown')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{self.export_dir}/audit_{domain}_{timestamp}.csv"
        
        try:
            # Flatten the results for CSV
            flattened_data = self._flatten_dict(results.get('results', {}))
            df = pd.DataFrame([flattened_data])
            df.to_csv(filename, index=False)
            return filename
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return None
    
    def _flatten_dict(self, data, prefix=''):
        """Flatten nested dictionary for CSV export"""
        items = []
        for key, value in data.items():
            new_key = f"{prefix}_{key}" if prefix else key
            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, new_key).items())
            elif isinstance(value, list):
                items.append((new_key, ', '.join(map(str, value))))
            else:
                items.append((new_key, str(value)))
        return dict(items)
    
    def generate_summary_report(self, results):
        """Generate a human-readable summary report"""
        domain = results.get('domain', 'Unknown')
        audit_mode = results.get('audit_mode', 'comprehensive')
        timestamp = results.get('timestamp', 'Unknown')
        
        summary = f"""
=== WEB AUDIT SUMMARY REPORT ===
Domain: {domain}
Audit Type: {audit_mode.title()}
Generated: {timestamp}

=== PERFORMANCE ANALYSIS ===
"""
        
        performance = results.get('results', {}).get('performance', {})
        if performance and 'error' not in performance:
            summary += f"Performance Score: {performance.get('score', 'N/A')}/100\n"
            summary += f"Load Time: {performance.get('load_time', 'N/A')} seconds\n"
        else:
            summary += "Performance data not available\n"
        
        summary += "\n=== SEO ANALYSIS ===\n"
        seo = results.get('results', {}).get('seo_marketing', {})
        if seo and 'error' not in seo:
            summary += f"Title: {seo.get('title', 'N/A')}\n"
            summary += f"Meta Description: {seo.get('meta_description', 'N/A')}\n"
            summary += f"H1 Tags: {len(seo.get('h1_tags', []))}\n"
        else:
            summary += "SEO data not available\n"
        
        summary += "\n=== SECURITY ANALYSIS ===\n"
        ssl = results.get('results', {}).get('ssl', {})
        if ssl and 'error' not in ssl:
            summary += f"SSL Status: {'Valid' if ssl.get('valid') else 'Invalid'}\n"
            summary += f"Certificate Issuer: {ssl.get('issuer', 'N/A')}\n"
        else:
            summary += "SSL data not available\n"
        
        return summary
