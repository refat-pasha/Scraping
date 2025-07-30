import os
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin, urlparse
import re

# Configuration
base_url = "https://www.istockphoto.com/search/2/image-film?phrase=acne+face+closeup&page={}"
page_urls = [base_url.format(i) for i in range(1, 101)]
save_dir = "istockphoto"
os.makedirs(save_dir, exist_ok=True)

# Chrome options for better compatibility
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--user (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

driver = webdriver.Chrome(options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

def scroll_and_load_images(driver, max_scrolls=5):
    """Scroll down to load lazy-loaded images"""
    for i in range(max_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        # Scroll back up a bit to load images that might be missed
        driver.execute_script("window.scrollBy(0, -500);")
        time.sleep(1)

def find_images_multiple_selectors(driver):
    """Try multiple CSS selectors to find images"""
    selectors = [
        'img[src*="istockphoto"]',  # Images with istockphoto in src
        'img[data-src*="istockphoto"]',  # Lazy loaded images
        'img.MosaicAsset-module__thumb___yvFP5',  # Original selector
        'div[data-testid="mosaic-asset"] img',  # Common pattern
        'img[alt*="acne"]',  # Images with acne in alt text
        'img[src*="thumbs"]',  # Thumbnail images
        'img',  # All images as fallback
    ]
    
    all_images = []
    for selector in selectors:
        try:
            images = driver.find_elements(By.CSS_SELECTOR, selector)
            if images:
                print(f"Found {len(images)} images with selector: {selector}")
                all_images.extend(images)
                break  # Use first successful selector
        except Exception as e:
            continue
    
    return list(set(all_images))  # Remove duplicates

def get_image_url(img_element):
    """Extract image URL from various attributes"""
    url_attributes = ['src', 'data-src', 'data-lazy-src', 'data-original']
    
    for attr in url_attributes:
        url = img_element.get_attribute(attr)
        if url and not url.startswith('data:') and 'istockphoto' in url:
            return url
    return None

def download_image(img_url, filename):
    """Download image with proper headers"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://www.istockphoto.com/',
        'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
    }
    
    try:
        response = requests.get(img_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        return True
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")
        return False

def clean_filename(filename):
    """Clean filename for safe saving"""
    # Remove invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:90] + ext
    return filename

try:
    for page_num, url in enumerate(page_urls, 1):
        print(f"\nProcessing page {page_num}: {url}")
        
        try:
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
            
            # Scroll to load all images
            scroll_and_load_images(driver)
            
            # Find images using multiple methods
            images = find_images_multiple_selectors(driver)
            
            if not images:
                print(f"No images found on page {page_num}")
                continue
                
            print(f"Found {len(images)} total images on page {page_num}")
            
            downloaded_count = 0
            for idx, img in enumerate(images):
                img_url = get_image_url(img)
                
                if not img_url:
                    continue
                
                # Create filename
                parsed = urlparse(img_url)
                original_name = os.path.basename(parsed.path)
                if not original_name or '.' not in original_name:
                    original_name = f"img_{idx}.jpg"
                
                clean_name = clean_filename(original_name)
                filename = os.path.join(save_dir, f"page{page_num}_{clean_name}")
                
                # Skip if already exists
                if os.path.exists(filename):
                    continue
                
                # Download image
                if download_image(img_url, filename):
                    print(f"✓ Downloaded: {filename}")
                    downloaded_count += 1
                    time.sleep(0.5)  # Be respectful
                
                # Limit downloads per page to avoid overwhelming
                if downloaded_count >= 50:
                    break
            
            print(f"Downloaded {downloaded_count} images from page {page_num}")
            
        except Exception as e:
            print(f"Error processing page {page_num}: {e}")
            continue

finally:
    driver.quit()

print(f"\nFinished! Check the '{save_dir}' folder for downloaded images.")
print("Note: These are preview images for research purposes only.")
print("For commercial use, please purchase proper licenses from iStockPhoto.")
