import os
import time
import requests
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def download_images_from_page(url, download_folder):
    os.makedirs(download_folder, exist_ok=True)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(url)
        time.sleep(3)
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        print(f"[{url}] Found {len(img_elements)} images")
        for i, img in enumerate(img_elements):
            src = img.get_attribute("src")
            if not src:
                continue
            img_url = urljoin(driver.current_url, src)
            parsed_url = urlparse(img_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = f"image_{i}.jpg"
            filepath = os.path.join(download_folder, filename)
            try:
                response = requests.get(img_url, timeout=10)
                response.raise_for_status()
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"[{url}] Downloaded: {filename}")
            except Exception as e:
                print(f"[{url}] Error downloading {img_url}: {e}")
            time.sleep(1)
    finally:
        driver.quit()

# List of URLs and corresponding folders
pages = [
    ("https://dermnetnz.org/images/acne-affecting-the-back-images", "acne_back_images"),
    ("http://dermnetnz.org/image-catalogue/acne-and-other-follicular-disorder-images", "acne_follicular_images"),
    ("https://dermnetnz.org/images/acne-scarring-images", "acne_scarring_images"),
    ("https://dermnetnz.org/images/acne-vulgaris-images", "acne_vulgaris_images"),
]

# Use ThreadPoolExecutor to scrape all pages in parallel
with ThreadPoolExecutor(max_workers=4) as executor:
    futures = []
    for url, folder in pages:
        futures.append(executor.submit(download_images_from_page, url, folder))
    for future in futures:
        future.result()  # Wait for all to finish
