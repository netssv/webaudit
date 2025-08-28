# Web Audit Tool

A comprehensive web audit tool built with Streamlit that analyzes websites for SEO, performance, security, and social media presence.

## Features

- **SEO Analysis**: Comprehensive SEO scoring with 6 categories (Meta Data, Page Quality, Page Structure, Links, Server, External Factors)
- **Performance Analysis**: Page load time, response time, and performance metrics
- **Security Analysis**: SSL/TLS certificate validation and security headers
- **DNS Analysis**: DNS record lookup and validation
- **Social Media Detection**: Automatic detection of social media links (Facebook, X/Twitter, LinkedIn, Instagram, YouTube, TikTok, and 20+ more platforms)
- **Marketing Tools Detection**: Identifies Google Analytics, Facebook Pixel, and other marketing tools
- **AI Analysis**: AI-powered website analysis and recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/netssv/webaudit.git
cd webaudit
```

2. Create a virtual environment:
```bash
python3 -m venv web_audit_env
source web_audit_env/bin/activate  # On Windows: web_audit_env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run streamlit_web_audit.py
```

## Usage

1. Open your browser and go to `http://localhost:8501`
2. Enter a website URL in the input field
3. Click "Analyze Website" to start the audit
4. Review the comprehensive analysis across multiple tabs:
   - **SEO Analysis**: Detailed SEO scoring and recommendations
   - **Performance**: Load times and performance metrics
   - **Security**: SSL/TLS and security analysis
   - **DNS**: DNS records and configuration
   - **AI Analysis**: AI-powered insights and recommendations

## Requirements

- Python 3.8+
- Streamlit 1.49.0+
- See `requirements.txt` for complete dependencies

## Project Structure

```
webaudit/
├── streamlit_web_audit.py      # Main Streamlit application
├── web_auditor.py              # Core audit functionality
├── modules/                    # Analysis modules
│   ├── seo_marketing_analyzer.py
│   ├── performance_analyzer.py
│   ├── ssl_analyzer.py
│   ├── dns_analyzer.py
│   └── ranking_analyzer.py
├── config/                     # Configuration files
├── ui/                         # UI components
├── utils/                      # Utility functions
└── requirements.txt            # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see LICENSE file for details
