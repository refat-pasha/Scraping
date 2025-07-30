import os
import time
import requests
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def download_images_from_website(url, download_folder="Acne vulgaris images"):
    # Create download folder if it doesn't exist
    os.makedirs(download_folder, exist_ok=True)

    # Set up Chrome options (headless mode)
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # Initialize the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # Find all image elements
        img_elements = driver.find_elements(By.TAG_NAME, "img")
        print(f"Found {len(img_elements)} images")

        for i, img in enumerate(img_elements):
            src = img.get_attribute("src")
            if not src:
                continue
            # Convert to absolute URL
            img_url = urljoin(driver.current_url, src)
            # Generate filename
            parsed_url = urlparse(img_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                filename = f"image_{i}.jpg"
            filepath = os.path.join(download_folder, filename)
            # Download the image
            try:
                response = requests.get(img_url, timeout=10)
                response.raise_for_status()
                with open(filepath, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
            except Exception as e:
                print(f"Error downloading {img_url}: {e}")
            time.sleep(1)  # Be respectful to the server
    finally:
        driver.quit()

# Usage
download_images_from_website("https://dermnetnz.org/images/acne-vulgaris-images")
