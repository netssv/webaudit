"""SEO and Marketing Analysis Module"""
import re
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import json

class SEOMarketingAnalyzer:
    def __init__(self):
        self.timeout = 10
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        
    def analyze_seo_marketing(self, url, soup=None, response=None):
        """Comprehensive SEO and marketing analysis"""
        if soup is None or response is None:
            try:
                response = requests.get(url, timeout=self.timeout, headers={'User-Agent': self.user_agent})
                soup = BeautifulSoup(response.content, 'html.parser')
            except:
                return {'error': 'Failed to fetch content'}
                
        # Get page content and response data
        page_text = soup.get_text()
        word_count = len(page_text.split())
        
        # Basic SEO info
        seo_info = {
            'title': self._get_title(soup),
            'meta_description': self._get_meta_description(soup),
            'meta_keywords': self._get_meta_keywords(soup),
            'headings': self._get_headings(soup),
            'images': self._analyze_images(soup),
            'links': self._analyze_links_basic(soup, url),
            'schema_markup': self._detect_schema_markup(soup),
            'open_graph': self._get_open_graph(soup),
            'twitter_cards': self._get_twitter_cards(soup),
            'canonical_url': self._get_canonical_url(soup),
            'robots_meta': self._get_robots_meta(soup),
            'marketing_tools': self._detect_marketing_tools(soup),
            'social_media_links': self._detect_social_media_links(soup),
            'word_count': word_count,
            'response_time': getattr(response, 'elapsed', None),
            'file_size': len(response.content) if response else None,
            'status_code': response.status_code if response else None,
            'url': url
        }
        
        # Enhanced analysis with detailed scoring
        enhanced_analysis = self._perform_comprehensive_analysis(seo_info, soup, response, url)
        
        # Merge basic info with enhanced analysis
        seo_info.update(enhanced_analysis)
        
        return seo_info
        
    def _get_title(self, soup):
        title_tag = soup.find('title')
        return title_tag.get_text().strip() if title_tag else None
        
    def _get_meta_description(self, soup):
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        return meta_desc.get('content') if meta_desc else None
        
    def _get_meta_keywords(self, soup):
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        return meta_keywords.get('content') if meta_keywords else None
        
    def _get_headings(self, soup):
        headings = {}
        for i in range(1, 7):
            headings[f'h{i}'] = [h.get_text().strip() for h in soup.find_all(f'h{i}')]
        return headings
        
    def _analyze_images(self, soup):
        images = soup.find_all('img')
        total_images = len(images)
        images_with_alt = len([img for img in images if img.get('alt')])
        
        return {
            'total_images': total_images,
            'images_with_alt': images_with_alt,
            'images_without_alt': total_images - images_with_alt,
            'alt_text_ratio': (images_with_alt / total_images * 100) if total_images > 0 else 0
        }
        
    def _analyze_links_basic(self, soup, base_url):
        links = soup.find_all('a', href=True)
        internal_links = []
        external_links = []
        
        parsed_base = urlparse(base_url)
        
        for link in links:
            href = link['href']
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)
            
            if parsed_url.netloc == parsed_base.netloc:
                internal_links.append(href)
            elif parsed_url.netloc:
                external_links.append(href)
                
        return {
            'total_links': len(links),
            'internal_links': len(internal_links),
            'external_links': len(external_links),
            'internal_links_list': internal_links[:10],  # First 10
            'external_links_list': external_links[:10]   # First 10
        }
        
    def _detect_schema_markup(self, soup):
        """Detect Schema.org structured data"""
        schema_types = []
        
        # JSON-LD
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                import json
                data = json.loads(script.string)
                if isinstance(data, dict) and '@type' in data:
                    schema_types.append(data['@type'])
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and '@type' in item:
                            schema_types.append(item['@type'])
            except:
                pass
                
        # Microdata
        microdata_items = soup.find_all(attrs={'itemtype': True})
        for item in microdata_items:
            schema_types.append(item.get('itemtype', '').split('/')[-1])
            
        return list(set(schema_types))
        
    def _get_open_graph(self, soup):
        og_tags = {}
        og_metas = soup.find_all('meta', attrs={'property': re.compile(r'^og:')})
        for meta in og_metas:
            property_name = meta.get('property')
            content = meta.get('content')
            if property_name and content:
                og_tags[property_name] = content
        return og_tags
        
    def _get_twitter_cards(self, soup):
        twitter_tags = {}
        twitter_metas = soup.find_all('meta', attrs={'name': re.compile(r'^twitter:')})
        for meta in twitter_metas:
            name = meta.get('name')
            content = meta.get('content')
            if name and content:
                twitter_tags[name] = content
        return twitter_tags
        
    def _get_canonical_url(self, soup):
        canonical = soup.find('link', rel='canonical')
        return canonical.get('href') if canonical else None
        
    def _get_robots_meta(self, soup):
        robots = soup.find('meta', attrs={'name': 'robots'})
        return robots.get('content') if robots else None
        
    def _detect_marketing_tools(self, soup):
        """Detect marketing and analytics tools"""
        tools = []
        page_content = str(soup)
        
        marketing_patterns = {
            'Google Analytics': [r'google-analytics\.com', r'gtag\(', r'ga\('],
            'Google Tag Manager': [r'googletagmanager\.com'],
            'Facebook Pixel': [r'facebook\.net/en_US/fbevents\.js', r'fbq\('],
            'LinkedIn Insight Tag': [r'snap\.licdn\.com'],
            'X (Twitter) Pixel': [r'static\.ads-twitter\.com'],
            'HubSpot': [r'js\.hs-scripts\.com', r'hubspot'],
            'Mailchimp': [r'mailchimp', r'mc\.us\d+\.list-manage\.com'],
            'Hotjar': [r'hotjar\.com'],
            'Mixpanel': [r'mixpanel\.com'],
            'Segment': [r'segment\.com', r'analytics\.js'],
            'Klaviyo': [r'klaviyo'],
            'Pardot': [r'pardot\.com'],
            'Marketo': [r'marketo\.com', r'munchkin'],
            'Adobe Analytics': [r'omniture\.com', r'adobe\.com.*analytics'],
            'Crazy Egg': [r'crazyegg\.com']
        }
        
        for tool, patterns in marketing_patterns.items():
            for pattern in patterns:
                if re.search(pattern, page_content, re.IGNORECASE):
                    tools.append(tool)
                    break
                    
        return list(set(tools))
        
    def _detect_social_media_links(self, soup):
        """Detect social media platform links"""
        social_links = {}
        links = soup.find_all('a', href=True)
        
        social_patterns = {
            'Facebook': [r'facebook\.com', r'fb\.com'],
            'X (Twitter)': [r'twitter\.com', r'x\.com'],
            'LinkedIn': [r'linkedin\.com'],
            'Instagram': [r'instagram\.com'],
            'YouTube': [r'youtube\.com', r'youtu\.be'],
            'TikTok': [r'tiktok\.com'],
            'Pinterest': [r'pinterest\.com'],
            'Snapchat': [r'snapchat\.com'],
            'WhatsApp': [r'wa\.me', r'whatsapp\.com'],
            'Telegram': [r'telegram\.me', r't\.me'],
            'Discord': [r'discord\.gg', r'discord\.com'],
            'Reddit': [r'reddit\.com'],
            'Tumblr': [r'tumblr\.com'],
            'Twitch': [r'twitch\.tv'],
            'Vimeo': [r'vimeo\.com'],
            'GitHub': [r'github\.com'],
            'GitLab': [r'gitlab\.com'],
            'Behance': [r'behance\.net'],
            'Dribbble': [r'dribbble\.com'],
            'Medium': [r'medium\.com'],
            'Mastodon': [r'mastodon\.'],
            'Threads': [r'threads\.net'],
            'Gmail': [r'mailto:.*@gmail\.com'],
            'Email': [r'mailto:']
        }
        
        for link in links:
            href = link.get('href', '')
            for platform, patterns in social_patterns.items():
                for pattern in patterns:
                    if re.search(pattern, href, re.IGNORECASE):
                        # For email links, clean up the display
                        if platform in ['Gmail', 'Email'] and href.startswith('mailto:'):
                            social_links[platform] = href.replace('mailto:', '')
                        else:
                            social_links[platform] = href
                        break
                        
        return social_links
        
    def _calculate_seo_score(self, seo_info):
        """Calculate SEO score out of 100"""
        score = 0
        
        # Title (20 points)
        if seo_info['title']:
            score += 15
            if 30 <= len(seo_info['title']) <= 60:
                score += 5
                
        # Meta description (15 points)
        if seo_info['meta_description']:
            score += 10
            if 120 <= len(seo_info['meta_description']) <= 160:
                score += 5
                
        # Headings (15 points)
        if seo_info['headings']['h1']:
            score += 10
            if len(seo_info['headings']['h1']) == 1:
                score += 5
                
        # Images with alt text (10 points)
        if seo_info['images']['alt_text_ratio'] >= 80:
            score += 10
        elif seo_info['images']['alt_text_ratio'] >= 50:
            score += 5
            
        # Schema markup (10 points)
        if seo_info['schema_markup']:
            score += 10
            
        # Open Graph (10 points)
        if len(seo_info['open_graph']) >= 3:
            score += 10
        elif seo_info['open_graph']:
            score += 5
            
        # Canonical URL (5 points)
        if seo_info['canonical_url']:
            score += 5
            
        # Internal linking (10 points)
        if seo_info['links']['internal_links'] > 0:
            score += 5
            if seo_info['links']['internal_links'] >= 5:
                score += 5
                
        # Marketing tools (5 points)
        if seo_info['marketing_tools']:
            score += 5
            
        return min(score, 100)

    def _perform_comprehensive_analysis(self, seo_info, soup, response, url):
        """Perform comprehensive SEO analysis with detailed scoring categories"""
        # Defensive check for required parameters
        if not seo_info:
            seo_info = {}
        if not url:
            url = 'unknown'
            
        analysis = {
            'overall_score': 0,
            'issues': {
                'critical': 0,
                'warnings': 0,
                'errors': 0
            },
            'categories': {
                'meta_data': {'score': 0, 'max_score': 100, 'checks': []},
                'page_quality': {'score': 0, 'max_score': 100, 'checks': []},
                'page_structure': {'score': 0, 'max_score': 100, 'checks': []},
                'links': {'score': 0, 'max_score': 100, 'checks': []},
                'server': {'score': 0, 'max_score': 100, 'checks': []},
                'external_factors': {'score': 0, 'max_score': 100, 'checks': []}
            },
            'todo_list': [],
            'page_info': {}
        }
        
        try:
            # Analyze each category with error handling
            self._analyze_meta_data(analysis, seo_info, soup)
            self._analyze_page_quality(analysis, seo_info, soup)
            self._analyze_page_structure(analysis, seo_info, soup)
            self._analyze_links_comprehensive(analysis, seo_info, soup, url)
            self._analyze_server(analysis, seo_info, response, url)
            self._analyze_external_factors(analysis, seo_info, url)
            
            # Calculate overall score
            total_score = sum(cat['score'] for cat in analysis['categories'].values())
            analysis['overall_score'] = total_score // 6  # Average of all categories
            
            # Add page info
            analysis['page_info'] = {
                'language': self._detect_language(soup) if soup else 'unknown',
                'charset': self._get_charset(soup) if soup else 'unknown',
                'doctype': self._get_doctype(soup) if soup else 'unknown',
                'viewport': self._get_viewport(soup) if soup else None,
                'favicon': self._has_favicon(soup) if soup else False,
            }
            
        except Exception as e:
            # If any analysis fails, add error to results but don't crash
            analysis['error'] = f"Analysis error: {str(e)}"
            analysis['overall_score'] = 0
        
        return analysis
    
    def _analyze_meta_data(self, analysis, seo_info, soup):
        """Analyze meta data category"""
        category = analysis['categories']['meta_data']
        score = 0
        
        # Title analysis (20 points)
        title = seo_info.get('title', '')
        if title:
            score += 10
            category['checks'].append({
                'name': 'Title',
                'status': 'pass',
                'importance': 'very_important',
                'message': f'Title present: "{title[:50]}..."',
                'details': f'Length: {len(title)} characters'
            })
            
            # Title length check
            if 30 <= len(title) <= 60:
                score += 10
                category['checks'].append({
                    'name': 'Title Length',
                    'status': 'pass',
                    'importance': 'very_important',
                    'message': 'Title length is optimal',
                    'details': f'{len(title)} characters (optimal: 30-60)'
                })
            else:
                category['checks'].append({
                    'name': 'Title Length',
                    'status': 'warning',
                    'importance': 'very_important',
                    'message': 'Title length should be 30-60 characters',
                    'details': f'Current: {len(title)} characters'
                })
                analysis['todo_list'].append({
                    'action': 'Optimize title length (30-60 characters)',
                    'importance': 'warning',
                    'category': 'meta_data'
                })
        else:
            category['checks'].append({
                'name': 'Title',
                'status': 'error',
                'importance': 'very_important',
                'message': 'Title tag is missing',
                'details': 'Page title is required for SEO'
            })
            analysis['todo_list'].append({
                'action': 'Add a title tag to the page',
                'importance': 'error',
                'category': 'meta_data'
            })
            analysis['issues']['errors'] += 1
        
        # Meta description analysis (20 points)
        meta_desc = seo_info.get('meta_description', '')
        if meta_desc:
            score += 10
            if 120 <= len(meta_desc) <= 160:
                score += 10
                category['checks'].append({
                    'name': 'Meta Description',
                    'status': 'pass',
                    'importance': 'very_important',
                    'message': 'Meta description is optimal',
                    'details': f'{len(meta_desc)} characters (optimal: 120-160)'
                })
            else:
                score += 5
                category['checks'].append({
                    'name': 'Meta Description',
                    'status': 'warning',
                    'importance': 'very_important',
                    'message': 'Meta description length should be 120-160 characters',
                    'details': f'Current: {len(meta_desc)} characters'
                })
        else:
            category['checks'].append({
                'name': 'Meta Description',
                'status': 'error',
                'importance': 'very_important',
                'message': 'Meta description is missing',
                'details': 'Meta description helps search engines understand page content'
            })
            analysis['todo_list'].append({
                'action': 'Add a meta description (120-160 characters)',
                'importance': 'error',
                'category': 'meta_data'
            })
            analysis['issues']['errors'] += 1
        
        # Canonical URL (15 points)
        canonical = seo_info.get('canonical_url', '')
        if canonical:
            score += 15
            category['checks'].append({
                'name': 'Canonical URL',
                'status': 'pass',
                'importance': 'important',
                'message': 'Canonical URL is specified',
                'details': f'Points to: {canonical}'
            })
        else:
            category['checks'].append({
                'name': 'Canonical URL',
                'status': 'warning',
                'importance': 'important',
                'message': 'Canonical URL not specified',
                'details': 'Helps prevent duplicate content issues'
            })
            analysis['todo_list'].append({
                'action': 'Add canonical URL to prevent duplicate content',
                'importance': 'warning',
                'category': 'meta_data'
            })
        
        # Language detection (10 points)
        lang_attr = soup.find('html', lang=True)
        if lang_attr:
            score += 10
            category['checks'].append({
                'name': 'Language',
                'status': 'pass',
                'importance': 'low',
                'message': f'Language specified: {lang_attr.get("lang")}',
                'details': 'Helps search engines understand content language'
            })
        else:
            category['checks'].append({
                'name': 'Language',
                'status': 'warning',
                'importance': 'low',
                'message': 'HTML language not specified',
                'details': 'Add lang attribute to html tag'
            })
        
        # Charset encoding (5 points)
        charset = soup.find('meta', charset=True) or soup.find('meta', attrs={'http-equiv': 'Content-Type'})
        if charset:
            score += 5
            category['checks'].append({
                'name': 'Charset',
                'status': 'pass',
                'importance': 'low',
                'message': 'Character encoding specified',
                'details': 'UTF-8 encoding detected'
            })
        
        # Robots meta (10 points)
        robots = seo_info.get('robots_meta', '')
        if robots and isinstance(robots, str) and 'noindex' not in robots.lower():
            score += 10
            category['checks'].append({
                'name': 'Robots Meta',
                'status': 'pass',
                'importance': 'important',
                'message': 'Page is indexable',
                'details': f'Robots: {robots}'
            })
        elif robots and isinstance(robots, str) and 'noindex' in robots.lower():
            category['checks'].append({
                'name': 'Robots Meta',
                'status': 'warning',
                'importance': 'important',
                'message': 'Page is set to noindex',
                'details': 'This page will not be indexed by search engines'
            })
        
        # Open Graph tags (10 points)
        og_tags = seo_info.get('open_graph', {})
        if len(og_tags) >= 4:
            score += 10
            category['checks'].append({
                'name': 'Open Graph',
                'status': 'pass',
                'importance': 'nice_to_have',
                'message': 'Good Open Graph implementation',
                'details': f'{len(og_tags)} Open Graph tags found'
            })
        elif og_tags:
            score += 5
            category['checks'].append({
                'name': 'Open Graph',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': 'Incomplete Open Graph tags',
                'details': f'Only {len(og_tags)} tags found, recommend og:title, og:description, og:image, og:url'
            })
        
        category['score'] = min(score, 100)
    
    def _analyze_page_quality(self, analysis, seo_info, soup):
        """Analyze page quality category"""
        category = analysis['categories']['page_quality']
        score = 0
        
        # Word count analysis (25 points)
        word_count = seo_info.get('word_count', 0)
        if word_count >= 800:
            score += 25
            category['checks'].append({
                'name': 'Content Length',
                'status': 'pass',
                'importance': 'very_important',
                'message': f'Good content length: {word_count} words',
                'details': 'Sufficient content for SEO (recommended: 800+ words)'
            })
        elif word_count >= 300:
            score += 15
            category['checks'].append({
                'name': 'Content Length',
                'status': 'warning',
                'importance': 'very_important',
                'message': f'Content could be longer: {word_count} words',
                'details': 'Consider adding more relevant content (recommended: 800+ words)'
            })
            analysis['todo_list'].append({
                'action': f'Increase content length from {word_count} to 800+ words',
                'importance': 'warning',
                'category': 'page_quality'
            })
        else:
            category['checks'].append({
                'name': 'Content Length',
                'status': 'error',
                'importance': 'very_important',
                'message': f'Content too short: {word_count} words',
                'details': 'Very thin content may hurt SEO rankings'
            })
            analysis['todo_list'].append({
                'action': f'Add substantial content (current: {word_count} words, target: 800+)',
                'importance': 'error',
                'category': 'page_quality'
            })
            analysis['issues']['errors'] += 1
        
        # H1 heading analysis (20 points)
        h1_tags = seo_info.get('headings', {}).get('h1', [])
        if len(h1_tags) == 1:
            score += 20
            h1_text = h1_tags[0]
            if len(h1_text) >= 20:
                category['checks'].append({
                    'name': 'H1 Heading',
                    'status': 'pass',
                    'importance': 'very_important',
                    'message': f'Single H1 tag found: "{h1_text[:50]}..."',
                    'details': f'Length: {len(h1_text)} characters (good)'
                })
            else:
                score -= 5
                category['checks'].append({
                    'name': 'H1 Heading',
                    'status': 'warning',
                    'importance': 'very_important',
                    'message': f'H1 heading too short: "{h1_text}"',
                    'details': f'Length: {len(h1_text)} characters (recommended: 20+ characters)'
                })
                analysis['todo_list'].append({
                    'action': 'Make H1 heading longer and more descriptive (20+ characters)',
                    'importance': 'warning',
                    'category': 'page_quality'
                })
        elif len(h1_tags) > 1:
            score += 10
            category['checks'].append({
                'name': 'H1 Heading',
                'status': 'warning',
                'importance': 'very_important',
                'message': f'Multiple H1 tags found ({len(h1_tags)})',
                'details': 'Should have only one H1 tag per page'
            })
            analysis['todo_list'].append({
                'action': 'Use only one H1 tag per page',
                'importance': 'warning',
                'category': 'page_quality'
            })
        else:
            category['checks'].append({
                'name': 'H1 Heading',
                'status': 'error',
                'importance': 'very_important',
                'message': 'No H1 heading found',
                'details': 'H1 tag is crucial for SEO'
            })
            analysis['todo_list'].append({
                'action': 'Add an H1 heading to the page',
                'importance': 'error',
                'category': 'page_quality'
            })
            analysis['issues']['errors'] += 1
        
        # Image alt text analysis (15 points)
        images = seo_info.get('images', {})
        alt_ratio = images.get('alt_text_ratio', 0)
        if alt_ratio >= 90:
            score += 15
            category['checks'].append({
                'name': 'Image Alt Text',
                'status': 'pass',
                'importance': 'important',
                'message': f'Excellent alt text usage: {alt_ratio}%',
                'details': f'{images.get("with_alt", 0)}/{images.get("total", 0)} images have alt text'
            })
        elif alt_ratio >= 50:
            score += 10
            category['checks'].append({
                'name': 'Image Alt Text',
                'status': 'warning',
                'importance': 'important',
                'message': f'Some images missing alt text: {alt_ratio}%',
                'details': f'{images.get("with_alt", 0)}/{images.get("total", 0)} images have alt text'
            })
            analysis['todo_list'].append({
                'action': 'Add alt text to all images for accessibility and SEO',
                'importance': 'warning',
                'category': 'page_quality'
            })
        else:
            category['checks'].append({
                'name': 'Image Alt Text',
                'status': 'error',
                'importance': 'important',
                'message': f'Most images missing alt text: {alt_ratio}%',
                'details': f'{images.get("with_alt", 0)}/{images.get("total", 0)} images have alt text'
            })
            analysis['todo_list'].append({
                'action': 'Add descriptive alt text to all images',
                'importance': 'error',
                'category': 'page_quality'
            })
            analysis['issues']['errors'] += 1
        
        # Heading structure analysis (10 points)
        headings = seo_info.get('headings', {})
        total_headings = sum(len(headings.get(f'h{i}', [])) for i in range(1, 7))
        if total_headings >= 3:
            score += 10
            category['checks'].append({
                'name': 'Heading Structure',
                'status': 'pass',
                'importance': 'important',
                'message': f'Good heading structure: {total_headings} headings',
                'details': 'Proper use of heading hierarchy'
            })
        else:
            score += 5
            category['checks'].append({
                'name': 'Heading Structure',
                'status': 'warning',
                'importance': 'important',
                'message': f'Limited heading structure: {total_headings} headings',
                'details': 'Consider using more headings to structure content'
            })
        
        # Mobile optimization (10 points)
        viewport_meta = soup.find('meta', attrs={'name': 'viewport'})
        if viewport_meta:
            score += 10
            category['checks'].append({
                'name': 'Mobile Optimization',
                'status': 'pass',
                'importance': 'important',
                'message': 'Viewport meta tag found',
                'details': 'Page is mobile-optimized'
            })
        else:
            category['checks'].append({
                'name': 'Mobile Optimization',
                'status': 'error',
                'importance': 'important',
                'message': 'No viewport meta tag found',
                'details': 'Add viewport meta tag for mobile optimization'
            })
            analysis['todo_list'].append({
                'action': 'Add viewport meta tag for mobile optimization',
                'importance': 'error',
                'category': 'page_quality'
            })
            analysis['issues']['errors'] += 1
        
        # Schema markup (10 points)
        schema = seo_info.get('schema_markup', [])
        if schema:
            score += 10
            category['checks'].append({
                'name': 'Schema Markup',
                'status': 'pass',
                'importance': 'nice_to_have',
                'message': f'Schema markup found: {", ".join(schema[:3])}',
                'details': f'{len(schema)} schema types detected'
            })
        else:
            category['checks'].append({
                'name': 'Schema Markup',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': 'No schema markup detected',
                'details': 'Schema markup helps search engines understand content'
            })
        
        # Social sharing (10 points)
        social_links = seo_info.get('social_media_links', {})
        if len(social_links) >= 3:
            score += 10
            category['checks'].append({
                'name': 'Social Media',
                'status': 'pass',
                'importance': 'nice_to_have',
                'message': f'Good social media presence: {len(social_links)} platforms',
                'details': f'Found: {", ".join(social_links.keys())}'
            })
        elif social_links:
            score += 5
            category['checks'].append({
                'name': 'Social Media',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': f'Limited social media presence: {len(social_links)} platforms',
                'details': 'Consider adding more social media links'
            })
        else:
            category['checks'].append({
                'name': 'Social Media',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': 'No social media links found',
                'details': 'Social sharing can increase page reach'
            })
        
        category['score'] = min(score, 100)
    
    def _analyze_page_structure(self, analysis, seo_info, soup):
        """Analyze page structure category"""
        category = analysis['categories']['page_structure']
        score = 0
        
        # HTML5 doctype (15 points)
        doctype = str(soup.contents[0]) if soup.contents else ''
        if '<!DOCTYPE html>' in doctype.upper():
            score += 15
            category['checks'].append({
                'name': 'HTML5 Doctype',
                'status': 'pass',
                'importance': 'nice_to_have',
                'message': 'HTML5 doctype correctly specified',
                'details': 'Modern HTML5 doctype detected'
            })
        else:
            score += 5
            category['checks'].append({
                'name': 'HTML5 Doctype',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': 'HTML5 doctype not found or incorrect',
                'details': 'Use <!DOCTYPE html> for HTML5'
            })
        
        # Favicon (10 points)
        favicon = soup.find('link', rel=lambda x: x and 'icon' in x.lower()) if soup else None
        if favicon:
            score += 10
            category['checks'].append({
                'name': 'Favicon',
                'status': 'pass',
                'importance': 'nice_to_have',
                'message': 'Favicon found',
                'details': 'Favicon helps with brand recognition'
            })
        else:
            category['checks'].append({
                'name': 'Favicon',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': 'No favicon found',
                'details': 'Add a favicon for better user experience'
            })
        
        # URL structure (15 points)
        parsed_url = urlparse(seo_info.get('url', ''))
        if len(parsed_url.path.split('/')) <= 4:  # Not too deep
            score += 10
            category['checks'].append({
                'name': 'URL Structure',
                'status': 'pass',
                'importance': 'low',
                'message': 'Good URL structure depth',
                'details': f'URL depth: {len(parsed_url.path.split("/"))} levels'
            })
        else:
            score += 5
            category['checks'].append({
                'name': 'URL Structure',
                'status': 'warning',
                'importance': 'low',
                'message': 'URL structure quite deep',
                'details': f'URL depth: {len(parsed_url.path.split("/"))} levels'
            })
        
        # No URL parameters (5 points)
        if not parsed_url.query:
            score += 5
            category['checks'].append({
                'name': 'URL Parameters',
                'status': 'pass',
                'importance': 'low',
                'message': 'No URL parameters found',
                'details': 'Clean URLs are better for SEO'
            })
        
        # HTTPS (20 points)
        if parsed_url.scheme == 'https':
            score += 20
            category['checks'].append({
                'name': 'HTTPS',
                'status': 'pass',
                'importance': 'important',
                'message': 'Site uses HTTPS encryption',
                'details': 'Secure connection established'
            })
        else:
            category['checks'].append({
                'name': 'HTTPS',
                'status': 'error',
                'importance': 'important',
                'message': 'Site not using HTTPS',
                'details': 'HTTPS is required for security and SEO'
            })
            analysis['todo_list'].append({
                'action': 'Implement HTTPS encryption for security and SEO',
                'importance': 'error',
                'category': 'page_structure'
            })
            analysis['issues']['errors'] += 1
        
        # No frames (10 points)
        frames = soup.find_all(['frame', 'frameset', 'iframe'])
        if not frames:
            score += 10
            category['checks'].append({
                'name': 'Frame Usage',
                'status': 'pass',
                'importance': 'low',
                'message': 'No frames detected',
                'details': 'Modern page structure without frames'
            })
        else:
            score += 5
            category['checks'].append({
                'name': 'Frame Usage',
                'status': 'warning',
                'importance': 'low',
                'message': f'{len(frames)} frames/iframes found',
                'details': 'Frames can impact SEO and accessibility'
            })
        
        # Proper heading hierarchy (15 points)
        headings = seo_info.get('headings', {})
        h1_count = len(headings.get('h1', []))
        h2_count = len(headings.get('h2', []))
        h3_count = len(headings.get('h3', []))
        
        if h1_count == 1 and h2_count > 0:
            score += 15
            category['checks'].append({
                'name': 'Heading Hierarchy',
                'status': 'pass',
                'importance': 'important',
                'message': 'Proper heading hierarchy detected',
                'details': f'H1: {h1_count}, H2: {h2_count}, H3: {h3_count}'
            })
        else:
            score += 8
            category['checks'].append({
                'name': 'Heading Hierarchy',
                'status': 'warning',
                'importance': 'important',
                'message': 'Heading hierarchy could be improved',
                'details': f'H1: {h1_count}, H2: {h2_count}, H3: {h3_count}'
            })
        
        # Internal linking structure (10 points)
        internal_links = seo_info.get('links', {}).get('internal_links', 0)
        if internal_links >= 5:
            score += 10
            category['checks'].append({
                'name': 'Internal Linking',
                'status': 'pass',
                'importance': 'important',
                'message': f'Good internal linking: {internal_links} links',
                'details': 'Internal links help with site navigation and SEO'
            })
        elif internal_links > 0:
            score += 5
            category['checks'].append({
                'name': 'Internal Linking',
                'status': 'warning',
                'importance': 'important',
                'message': f'Limited internal linking: {internal_links} links',
                'details': 'Consider adding more internal links'
            })
        else:
            category['checks'].append({
                'name': 'Internal Linking',
                'status': 'warning',
                'importance': 'important',
                'message': 'No internal links found',
                'details': 'Internal links are important for SEO and navigation'
            })
        
        category['score'] = min(score, 100)
    
    def _analyze_links_comprehensive(self, analysis, seo_info, soup, url):
        """Analyze links category"""
        category = analysis['categories']['links']
        score = 0
        
        links_data = seo_info.get('links', {})
        internal_count = links_data.get('internal_links', 0)
        external_count = links_data.get('external_links', 0)
        
        # Internal links analysis (40 points)
        if internal_count >= 10:
            score += 40
            category['checks'].append({
                'name': 'Internal Links',
                'status': 'pass',
                'importance': 'important',
                'message': f'Excellent internal linking: {internal_count} links',
                'details': 'Good internal link structure for SEO'
            })
        elif internal_count >= 5:
            score += 30
            category['checks'].append({
                'name': 'Internal Links',
                'status': 'pass',
                'importance': 'important',
                'message': f'Good internal linking: {internal_count} links',
                'details': 'Adequate internal link structure'
            })
        elif internal_count > 0:
            score += 20
            category['checks'].append({
                'name': 'Internal Links',
                'status': 'warning',
                'importance': 'important',
                'message': f'Limited internal linking: {internal_count} links',
                'details': 'Consider adding more internal links'
            })
            analysis['todo_list'].append({
                'action': 'Add more internal links to improve site navigation',
                'importance': 'warning',
                'category': 'links'
            })
        else:
            category['checks'].append({
                'name': 'Internal Links',
                'status': 'error',
                'importance': 'important',
                'message': 'No internal links found',
                'details': 'Internal links are crucial for SEO'
            })
            analysis['todo_list'].append({
                'action': 'Add internal links to connect related pages',
                'importance': 'error',
                'category': 'links'
            })
            analysis['issues']['errors'] += 1
        
        # External links analysis (20 points)
        if 1 <= external_count <= 5:
            score += 20
            category['checks'].append({
                'name': 'External Links',
                'status': 'pass',
                'importance': 'nice_to_have',
                'message': f'Good external linking: {external_count} links',
                'details': 'Balanced external link usage'
            })
        elif external_count > 5:
            score += 15
            category['checks'].append({
                'name': 'External Links',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': f'Many external links: {external_count} links',
                'details': 'Consider if all external links are necessary'
            })
        elif external_count == 0:
            score += 10
            category['checks'].append({
                'name': 'External Links',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': 'No external links found',
                'details': 'Some external links can add value to users'
            })
        
        # Link anchor text analysis (20 points)
        all_links = soup.find_all('a', href=True) if soup else []
        anchor_texts = [link.get_text().strip() for link in all_links if link.get_text() and link.get_text().strip()]
        
        if anchor_texts:
            descriptive_count = sum(1 for text in anchor_texts if text and len(text) > 5 and text.lower() not in ['click here', 'read more', 'more'])
            descriptive_ratio = (descriptive_count / len(anchor_texts)) * 100
            
            if descriptive_ratio >= 80:
                score += 20
                category['checks'].append({
                    'name': 'Anchor Text Quality',
                    'status': 'pass',
                    'importance': 'important',
                    'message': f'Good anchor text quality: {descriptive_ratio:.1f}%',
                    'details': f'{descriptive_count}/{len(anchor_texts)} links have descriptive anchor text'
                })
            elif descriptive_ratio >= 50:
                score += 15
                category['checks'].append({
                    'name': 'Anchor Text Quality',
                    'status': 'warning',
                    'importance': 'important',
                    'message': f'Anchor text could be improved: {descriptive_ratio:.1f}%',
                    'details': f'{descriptive_count}/{len(anchor_texts)} links have descriptive anchor text'
                })
            else:
                score += 10
                category['checks'].append({
                    'name': 'Anchor Text Quality',
                    'status': 'warning',
                    'importance': 'important',
                    'message': f'Poor anchor text quality: {descriptive_ratio:.1f}%',
                    'details': 'Use descriptive anchor text instead of generic phrases'
                })
                analysis['todo_list'].append({
                    'action': 'Improve anchor text to be more descriptive',
                    'importance': 'warning',
                    'category': 'links'
                })
        
        # Nofollow links analysis (20 points)
        nofollow_count = len([link for link in all_links if 'nofollow' in link.get('rel', [])])
        if nofollow_count == 0 and external_count > 0:
            score += 15
            category['checks'].append({
                'name': 'Link Attributes',
                'status': 'warning',
                'importance': 'low',
                'message': 'No nofollow attributes found',
                'details': 'Consider adding nofollow to untrusted external links'
            })
        elif nofollow_count > 0:
            score += 20
            category['checks'].append({
                'name': 'Link Attributes',
                'status': 'pass',
                'importance': 'low',
                'message': f'{nofollow_count} links use nofollow attribute',
                'details': 'Good link attribute usage'
            })
        
        category['score'] = min(score, 100)
    
    def _analyze_server(self, analysis, seo_info, response, url):
        """Analyze server configuration category"""
        category = analysis['categories']['server']
        score = 0
        
        # Response time analysis (30 points)
        if response and hasattr(response, 'elapsed'):
            response_time = response.elapsed.total_seconds()
            if response_time <= 0.4:
                score += 30
                category['checks'].append({
                    'name': 'Response Time',
                    'status': 'pass',
                    'importance': 'important',
                    'message': f'Excellent response time: {response_time:.2f}s',
                    'details': 'Response time under 0.4 seconds'
                })
            elif response_time <= 1.0:
                score += 20
                category['checks'].append({
                    'name': 'Response Time',
                    'status': 'warning',
                    'importance': 'important',
                    'message': f'Good response time: {response_time:.2f}s',
                    'details': 'Response time acceptable but could be improved'
                })
            else:
                score += 10
                category['checks'].append({
                    'name': 'Response Time',
                    'status': 'error',
                    'importance': 'important',
                    'message': f'Slow response time: {response_time:.2f}s',
                    'details': 'Response time should be under 1 second'
                })
                analysis['todo_list'].append({
                    'action': f'Improve server response time (current: {response_time:.2f}s)',
                    'importance': 'error',
                    'category': 'server'
                })
                analysis['issues']['errors'] += 1
        
        # File size analysis (20 points)
        if response:
            file_size = len(response.content)
            file_size_kb = file_size / 1024
            
            if file_size_kb <= 100:
                score += 20
                category['checks'].append({
                    'name': 'Page Size',
                    'status': 'pass',
                    'importance': 'low',
                    'message': f'Good page size: {file_size_kb:.1f} KB',
                    'details': 'Page size optimized for fast loading'
                })
            elif file_size_kb <= 500:
                score += 15
                category['checks'].append({
                    'name': 'Page Size',
                    'status': 'warning',
                    'importance': 'low',
                    'message': f'Moderate page size: {file_size_kb:.1f} KB',
                    'details': 'Page size could be optimized further'
                })
            else:
                score += 10
                category['checks'].append({
                    'name': 'Page Size',
                    'status': 'warning',
                    'importance': 'low',
                    'message': f'Large page size: {file_size_kb:.1f} KB',
                    'details': 'Large page size may impact loading speed'
                })
        
        # HTTP status code analysis (20 points)
        if response:
            status_code = response.status_code
            if status_code == 200:
                score += 20
                category['checks'].append({
                    'name': 'HTTP Status',
                    'status': 'pass',
                    'importance': 'very_important',
                    'message': f'HTTP 200 OK',
                    'details': 'Page loads successfully'
                })
            elif 300 <= status_code < 400:
                score += 15
                category['checks'].append({
                    'name': 'HTTP Status',
                    'status': 'warning',
                    'importance': 'very_important',
                    'message': f'HTTP {status_code} (Redirect)',
                    'details': 'Page redirects - ensure redirect is intentional'
                })
            else:
                category['checks'].append({
                    'name': 'HTTP Status',
                    'status': 'error',
                    'importance': 'very_important',
                    'message': f'HTTP {status_code} (Error)',
                    'details': 'Page returns error status'
                })
                analysis['todo_list'].append({
                    'action': f'Fix HTTP {status_code} error',
                    'importance': 'error',
                    'category': 'server'
                })
                analysis['issues']['errors'] += 1
        
        # Compression analysis (15 points)
        if response and response.headers.get('content-encoding'):
            score += 15
            category['checks'].append({
                'name': 'Compression',
                'status': 'pass',
                'importance': 'important',
                'message': 'Content compression enabled',
                'details': f'Compression: {response.headers.get("content-encoding")}'
            })
        else:
            category['checks'].append({
                'name': 'Compression',
                'status': 'warning',
                'importance': 'important',
                'message': 'No content compression detected',
                'details': 'Enable gzip compression to reduce transfer size'
            })
            analysis['todo_list'].append({
                'action': 'Enable gzip compression on server',
                'importance': 'warning',
                'category': 'server'
            })
        
        # Security headers analysis (15 points)
        security_headers = ['x-frame-options', 'x-content-type-options', 'x-xss-protection']
        if response:
            found_headers = sum(1 for header in security_headers if header in response.headers)
            if found_headers >= 2:
                score += 15
                category['checks'].append({
                    'name': 'Security Headers',
                    'status': 'pass',
                    'importance': 'low',
                    'message': f'Good security headers: {found_headers}/3',
                    'details': 'Security headers help protect against attacks'
                })
            elif found_headers > 0:
                score += 10
                category['checks'].append({
                    'name': 'Security Headers',
                    'status': 'warning',
                    'importance': 'low',
                    'message': f'Some security headers: {found_headers}/3',
                    'details': 'Consider adding more security headers'
                })
            else:
                category['checks'].append({
                    'name': 'Security Headers',
                    'status': 'warning',
                    'importance': 'low',
                    'message': 'No security headers found',
                    'details': 'Add security headers for better protection'
                })
        
        category['score'] = min(score, 100)
    
    def _analyze_external_factors(self, analysis, seo_info, url):
        """Analyze external factors category (simulated)"""
        category = analysis['categories']['external_factors']
        score = 0
        
        # Note: These would require external APIs in a real implementation
        # For now, we'll provide placeholder analysis
        
        # Domain age simulation (25 points)
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Simulate domain analysis
        score += 15  # Placeholder score
        category['checks'].append({
            'name': 'Domain Analysis',
            'status': 'warning',
            'importance': 'low',
            'message': f'Domain: {domain}',
            'details': 'External domain metrics would require additional API access'
        })
        
        # Backlink simulation (25 points)
        score += 10  # Placeholder - low score to indicate limited data
        category['checks'].append({
            'name': 'Backlinks',
            'status': 'warning',
            'importance': 'very_important',
            'message': 'Limited backlink data available',
            'details': 'Backlink analysis requires specialized SEO tools'
        })
        analysis['todo_list'].append({
            'action': 'Build quality backlinks from relevant websites',
            'importance': 'warning',
            'category': 'external_factors'
        })
        
        # Social signals simulation (25 points)
        social_links = seo_info.get('social_media_links', {})
        if len(social_links) >= 3:
            score += 20
            category['checks'].append({
                'name': 'Social Presence',
                'status': 'pass',
                'importance': 'nice_to_have',
                'message': f'Good social media presence: {len(social_links)} platforms',
                'details': f'Active on: {", ".join(social_links.keys())}'
            })
        elif social_links:
            score += 15
            category['checks'].append({
                'name': 'Social Presence',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': f'Limited social presence: {len(social_links)} platforms',
                'details': 'Consider expanding social media presence'
            })
        else:
            score += 5
            category['checks'].append({
                'name': 'Social Presence',
                'status': 'warning',
                'importance': 'nice_to_have',
                'message': 'No social media presence detected',
                'details': 'Social media can help with brand awareness and SEO'
            })
        
        # Local SEO simulation (25 points)
        # Check for business-related schema or contact info
        business_indicators = 0
        
        # Check if contact-related meta tags exist
        if seo_info.get('schema_markup') and any('local' in str(schema).lower() or 'business' in str(schema).lower() 
                                                 for schema in seo_info['schema_markup'] if schema):
            business_indicators += 1
        
        # Check if contact-related meta tags exist
        if any(tag in str(seo_info).lower() for tag in ['address', 'phone', 'contact', 'location']):
            business_indicators += 1
        
        if business_indicators >= 2:
            score += 20
            category['checks'].append({
                'name': 'Local SEO',
                'status': 'pass',
                'importance': 'low',
                'message': 'Good local SEO indicators found',
                'details': 'Contact information and local business signals detected'
            })
        elif business_indicators > 0:
            score += 10
            category['checks'].append({
                'name': 'Local SEO',
                'status': 'warning',
                'importance': 'low',
                'message': 'Some local SEO indicators found',
                'details': 'Consider adding more local business information'
            })
        else:
            score += 5
            category['checks'].append({
                'name': 'Local SEO',
                'status': 'warning',
                'importance': 'low',
                'message': 'Limited local SEO information',
                'details': 'Add contact information and location details if applicable'
            })
        
        category['score'] = min(score, 100)
    
    def _detect_language(self, soup):
        """Detect page language"""
        if not soup:
            return 'unknown'
            
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            return html_tag.get('lang')
        
        # Try to detect from meta tags
        meta_lang = soup.find('meta', attrs={'http-equiv': 'content-language'})
        if meta_lang:
            return meta_lang.get('content', 'unknown')
        
        return 'unknown'
    
    def _get_charset(self, soup):
        """Get page charset"""
        if not soup:
            return 'unknown'
            
        charset_meta = soup.find('meta', charset=True)
        if charset_meta:
            return charset_meta.get('charset', 'unknown')
        
        # Try content-type meta
        content_type = soup.find('meta', attrs={'http-equiv': 'content-type'})
        if content_type:
            content = content_type.get('content', '')
            if 'charset=' in content:
                return content.split('charset=')[1].strip()
        
        return 'unknown'
    
    def _get_doctype(self, soup):
        """Get page doctype"""
        if not soup or not soup.contents:
            return 'unknown'
            
        if str(soup.contents[0]).strip().startswith('<!DOCTYPE'):
            return str(soup.contents[0]).strip()
        return 'unknown'
    
    def _get_viewport(self, soup):
        """Get viewport meta tag"""
        if not soup:
            return None
            
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        return viewport.get('content') if viewport else None
    
    def _has_favicon(self, soup):
        """Check if favicon exists"""
        if not soup:
            return False
            
        favicon = soup.find('link', rel=lambda x: x and 'icon' in str(x).lower())
        return favicon is not None
