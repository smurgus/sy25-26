import requests
from bs4 import BeautifulSoup
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

def scrape_with_permission(target_url):
    # 1. Setup the User-Agent
    user_agent = "EducationalScraperBot/1.0"
    
    # 2. Find and Parse the robots.txt file
    parsed_url = urlparse(target_url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = f"{base_url}/robots.txt"
    
    rp = RobotFileParser()
    rp.set_url(robots_url)
    
    try:
        rp.read()
        can_scrape = rp.can_fetch(user_agent, target_url)
    except Exception as e:
        print(f"Could not read robots.txt ({e}), proceeding with caution...")
        can_scrape = True
  
    # 3. Logic: Only scrape if allowed
    if can_scrape:
        print(f"✅ Permissions verified for: {target_url}")
        
        try:
            # Set headers to look like a real request
            headers = {'User-Agent': user_agent}
            response = requests.get(target_url, headers=headers, timeout=10)
            
            # Check if the page loaded successfully (Status 200)
            response.raise_for_status()
            
            # 4. Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example Extraction: Page Title and all H1 headers
            print(f"\n--- Scraping Results ---")
            print(f"Site Title: {soup.title.string if soup.title else 'No Title Found'}")
            
            print("Main Headlines (H1):")
            for h1 in soup.find_all('h1'):
                print(f"- {h1.text.strip()}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Failed to fetch the page: {e}")
            
    else:
        print(f"🚫 Access Denied: {target_url} is restricted by robots.txt")
  
# Run the combined script
if __name__ == "__main__":
    # You can change this to any URL you want to test
    scrape_with_permission("https://books.toscrape.com/")
