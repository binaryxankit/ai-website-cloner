import os
import requests
from typing import Dict, Any
import json
from bs4 import BeautifulSoup
import re

class LLMService:
    def __init__(self):
        self.api_key = os.getenv('GOOGLE_API_KEY', '')
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        
    def _create_prompt(self, website_data: Dict[str, Any]) -> str:
        return f"""You are an expert web developer. Create an exact HTML clone of this website based on its design context:

URL: {website_data['url']}
Title: {website_data['title']}

Meta Tags:
{json.dumps(website_data['meta_tags'], indent=2)}

Website Structure:
{json.dumps(website_data['elements'], indent=2)}

Images and Assets:
{json.dumps(website_data['images'], indent=2)}

SVG Elements:
{json.dumps(website_data['svgs'], indent=2)}

Icons:
{json.dumps(website_data['icons'], indent=2)}

CSS Styles:
{website_data['styles']}

Please create an exact HTML clone that matches the original website's appearance. Follow these guidelines:
1. Use modern HTML5 and CSS3
2. Maintain the exact same visual hierarchy and layout
3. Include all necessary CSS styles inline or in a style tag
4. Preserve all image dimensions, alt text, and styling
5. Keep the exact same color scheme and typography
6. Ensure the clone is responsive
7. Include all meta tags and viewport settings
8. Preserve all SVG elements and icons
9. Maintain the exact same class names and IDs
10. Keep all original attributes and data attributes

Return only the complete HTML code, including all necessary CSS and structure. Do not include any explanations or markdown formatting. The HTML should be a pixel-perfect clone of the original website."""

    async def generate_website_clone(self, website_data: Dict[str, Any]) -> str:
        try:
            prompt = self._create_prompt(website_data)
            
            # Prepare the request payload
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
            
            # Make the API request
            response = requests.post(
                self.api_url,
                headers={'Content-Type': 'application/json'},
                json=payload
            )
            
            if not response.ok:
                print(f"API Error: {response.status_code} - {response.text}")
                return self._create_basic_html(website_data)
            
            response_data = response.json()
            
            # Extract the generated text from the response
            if 'candidates' in response_data and len(response_data['candidates']) > 0:
                generated_text = response_data['candidates'][0]['content']['parts'][0]['text']
                
                # Extract HTML content from the response
                html_match = re.search(r'```html\n(.*?)\n```', generated_text, re.DOTALL)
                if html_match:
                    return html_match.group(1)
            
            print("No HTML content found in API response")
            return self._create_basic_html(website_data)
            
        except Exception as e:
            print(f"Error generating clone: {str(e)}")
            return self._create_basic_html(website_data)

    def _create_basic_html(self, website_data: Dict[str, Any]) -> str:
        """Create a basic HTML structure when API fails."""
        styles = self._extract_styles(website_data['styles'])
        soup = BeautifulSoup(website_data['html'], 'html.parser')
        
        # Create a new HTML document
        new_soup = BeautifulSoup('<!DOCTYPE html>', 'html.parser')
        html = new_soup.new_tag('html', lang='en')
        new_soup.append(html)
        
        # Add head
        head = new_soup.new_tag('head')
        html.append(head)
        
        # Add meta tags
        for meta in website_data['meta_tags']:
            meta_tag = new_soup.new_tag('meta')
            for key, value in meta.items():
                if value:
                    meta_tag[key] = value
            head.append(meta_tag)
        
        # Add title
        if website_data['title']:
            title = new_soup.new_tag('title')
            title.string = website_data['title']
            head.append(title)
        
        # Add favicon
        if website_data['favicon']:
            link = new_soup.new_tag('link', rel='icon', href=website_data['favicon'])
            head.append(link)
        
        # Add styles
        style = new_soup.new_tag('style')
        style.string = f"""
            {styles}
            
            /* Additional responsive styles */
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            
            img {{
                max-width: 100%;
                height: auto;
            }}
        """
        head.append(style)
        
        # Add body
        body = new_soup.new_tag('body')
        html.append(body)
        
        # Add main content
        main_content = soup.body if soup.body else soup
        body.append(main_content)
        
        return str(new_soup)

    def _extract_styles(self, styles: list) -> str:
        """Extract and combine all CSS styles."""
        combined_styles = []
        for style in styles:
            if style and isinstance(style, str):
                style = style.strip()
                if style.startswith('/*'):
                    continue
                combined_styles.append(style)
        return '\n'.join(combined_styles)

# Create a singleton instance
llm_service = LLMService() 