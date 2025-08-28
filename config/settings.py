"""Configuration settings for the web audit application"""

class AppConfig:
    """Main application configuration"""
    
    # App Information
    APP_TITLE = "🌐 WEB AUDIT ANALYZER"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "Advanced Web Analysis & Optimization Tool"
    
    # Default Settings
    DEFAULT_TIMEOUT = 30
    DEFAULT_USER_AGENT = "WebAuditAnalyzer/1.0"
    
    # Audit Configuration
    AUDIT_MODES = {
        "Quick Scan": {
            "description": "Basic analysis for quick overview",
            "modules": ["dns_analyzer", "ssl_analyzer"]
        },
        "Standard Audit": {
            "description": "Comprehensive analysis for most needs", 
            "modules": ["dns_analyzer", "ssl_analyzer", "seo_marketing_analyzer", "performance_analyzer"]
        },
        "Deep Analysis": {
            "description": "Complete analysis with all modules",
            "modules": ["dns_analyzer", "ssl_analyzer", "seo_marketing_analyzer", "performance_analyzer", "ranking_analyzer"]
        },
        "Security Focus": {
            "description": "Security-focused analysis",
            "modules": ["ssl_analyzer", "dns_analyzer"]
        },
        "SEO Focus": {
            "description": "SEO and marketing analysis",
            "modules": ["seo_marketing_analyzer", "ranking_analyzer"]
        },
        "Performance Focus": {
            "description": "Performance optimization analysis",
            "modules": ["performance_analyzer", "dns_analyzer"]
        }
    }
    
    # Export Configuration
    EXPORT_FORMATS = ["JSON", "CSV", "Summary Report"]
    
    # ChatGPT Configuration
    CHATGPT_SYSTEM_PROMPT = """You are a web audit and SEO expert assistant. 
    You have access to comprehensive web audit data and should provide actionable, 
    technical insights and recommendations based on the audit results. 
    Focus on practical solutions and industry best practices."""
    
    # UI Configuration
    SIDEBAR_WIDTH = 300
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    # Security Configuration
    ALLOWED_SCHEMES = ["http", "https"]
    MAX_REDIRECTS = 10
    
    @classmethod
    def get_audit_modules(cls, mode):
        """Get modules for specific audit mode"""
        return cls.AUDIT_MODES.get(mode, {}).get("modules", [])
    
    @classmethod
    def get_mode_description(cls, mode):
        """Get description for specific audit mode"""
        return cls.AUDIT_MODES.get(mode, {}).get("description", "")

class SessionConfig:
    """Session state configuration and keys"""
    
    # Session State Keys
    AUDIT_RESULT = "audit_result"
    LAST_URL = "last_url"
    THEME_MODE = "theme_mode"
    CHATGPT_API_KEY = "chatgpt_api_key"
    SELECTED_MODE = "selected_audit_mode"
    EXPORT_FORMAT = "export_format"
    
    # Default Values
    DEFAULT_THEME = False  # Light theme
    DEFAULT_MODE = "Standard Audit"
    DEFAULT_EXPORT = "JSON"
    
    @classmethod
    def initialize_session(cls, st):
        """Initialize session state with default values"""
        defaults = {
            cls.AUDIT_RESULT: None,
            cls.LAST_URL: "",
            cls.THEME_MODE: cls.DEFAULT_THEME,
            cls.CHATGPT_API_KEY: "",
            cls.SELECTED_MODE: cls.DEFAULT_MODE,
            cls.EXPORT_FORMAT: cls.DEFAULT_EXPORT
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
