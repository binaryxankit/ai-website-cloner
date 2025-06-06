import requests
from bs4 import BeautifulSoup
from typing import Dict, Any
import json
from urllib.parse import urljoin, urlparse

class WebsiteScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def _get_absolute_url(self, base_url: str, relative_url: str) -> str:
        """Convert relative URL to absolute URL."""
        return urljoin(base_url, relative_url)

    def _is_valid_url(self, url: str) -> bool:
        """Check if URL is valid."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def scrape_website(self, url: str) -> Dict[str, Any]:
        try:
            # Fetch the webpage
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract all CSS
            styles = []
            # Inline styles
            for style in soup.find_all('style'):
                if style.string:
                    styles.append(style.string)
            
            # External stylesheets
            for link in soup.find_all('link', rel='stylesheet'):
                if link.get('href'):
                    try:
                        css_url = self._get_absolute_url(url, link['href'])
                        css_response = requests.get(css_url, headers=self.headers)
                        if css_response.ok:
                            styles.append(css_response.text)
                    except:
                        styles.append(f"/* External stylesheet: {link['href']} */")
            
            # Extract all images
            images = []
            for img in soup.find_all('img'):
                if img.get('src'):
                    img_url = self._get_absolute_url(url, img['src'])
                    if self._is_valid_url(img_url):
                        images.append({
                            'src': img_url,
                            'alt': img.get('alt', ''),
                            'width': img.get('width'),
                            'height': img.get('height'),
                            'class': ' '.join(img.get('class', [])),
                            'id': img.get('id', ''),
                            'style': img.get('style', '')
                        })
            
            # Extract all SVG elements
            svgs = []
            for svg in soup.find_all('svg'):
                svgs.append(str(svg))
            
            # Extract all icons
            icons = []
            for icon in soup.find_all(['link', 'i'], rel=['icon', 'shortcut icon']):
                if icon.get('href'):
                    icon_url = self._get_absolute_url(url, icon['href'])
                    if self._is_valid_url(icon_url):
                        icons.append({
                            'href': icon_url,
                            'type': icon.get('type', ''),
                            'sizes': icon.get('sizes', '')
                        })
            
            # Get all elements and their attributes
            elements = []
            for element in soup.find_all(['div', 'section', 'header', 'footer', 'nav', 'main', 'article', 'aside']):
                element_data = {
                    'tag': element.name,
                    'classes': element.get('class', []),
                    'id': element.get('id', ''),
                    'styles': {},
                    'children': []
                }
                
                # Extract inline styles
                if element.get('style'):
                    style_dict = {}
                    for style in element['style'].split(';'):
                        if ':' in style:
                            prop, value = style.split(':', 1)
                            style_dict[prop.strip()] = value.strip()
                    element_data['styles'] = style_dict
                
                # Get immediate children
                for child in element.find_all(recursive=False):
                    child_data = {
                        'tag': child.name,
                        'classes': child.get('class', []),
                        'id': child.get('id', ''),
                        'text': child.get_text(strip=True) if child.name not in ['script', 'style'] else ''
                    }
                    element_data['children'].append(child_data)
                
                elements.append(element_data)
            
            # Extract meta tags
            meta_tags = []
            for meta in soup.find_all('meta'):
                meta_tags.append({
                    'name': meta.get('name', ''),
                    'content': meta.get('content', ''),
                    'property': meta.get('property', '')
                })
            
            return {
                'html': response.text,
                'styles': styles,
                'images': images,
                'svgs': svgs,
                'icons': icons,
                'elements': elements,
                'meta_tags': meta_tags,
                'url': url,
                'title': soup.title.string if soup.title else '',
                'favicon': soup.find('link', rel='icon')['href'] if soup.find('link', rel='icon') else None
            }
            
        except Exception as e:
            raise Exception(f"Error scraping website: {str(e)}")

def get_website_data(url: str) -> Dict[str, Any]:
    scraper = WebsiteScraper()
    return scraper.scrape_website(url) 