import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def launch_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def scrape_bproperty_dhaka():
    driver = launch_driver(headless=False)  # set headless=True to run without UI
    wait = WebDriverWait(driver, 20)

    # 1. Navigate to homepage and search "Dhaka"
    driver.get("https://www.bproperty.com/")
    loc_input = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'input[aria-label="Enter location, project or developer name"]')
    ))
    loc_input.clear()
    loc_input.send_keys("Dhaka")

    # 2. Wait for autocomplete, select first suggestion
    first_sugg = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'ul[role="listbox"] li')
    ))
    first_sugg.click()

    # 3. Click search
    search_btn = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'button[type="submit"]')
    ))
    search_btn.click()

    # 4. Wait for listing cards
    wait.until(EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "li.search-card-list__item")
    ))
    cards = driver.find_elements(By.CSS_SELECTOR, "li.search-card-list__item")
    links = []
    for card in cards:
        try:
            href = card.find_element(By.TAG_NAME, "a").get_attribute("href")
            links.append(href)
        except:
            continue

    properties = []
    # 5. Visit each detail page
    for link in links:
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        time.sleep(2)  # allow JS to load

        def get_text(css=None, xpath=None):
            try:
                if css:
                    return driver.find_element(By.CSS_SELECTOR, css).text.strip()
                if xpath:
                    return driver.find_element(By.XPATH, xpath).text.strip()
            except:
                return ""

        def get_list(css):
            try:
                return [el.text.strip() for el in driver.find_elements(By.CSS_SELECTOR, css)]
            except:
                return []

        def get_imgs(css):
            try:
                return [img.get_attribute("src") for img in driver.find_elements(By.CSS_SELECTOR, css)]
            except:
                return []

        title        = get_text(css="h1[data-testid='listing-details__title']")
        price        = get_text(css="span[data-testid='listing-details__price']")
        location     = get_text(css="div[data-testid='listing-details__location']")
        area         = get_text(xpath="//span[contains(text(),'Area')]/following-sibling::span")
        beds         = get_text(xpath="//span[contains(text(),'Beds')]/following-sibling::span")
        baths        = get_text(xpath="//span[contains(text(),'Baths')]/following-sibling::span")
        features     = get_list(css="ul[data-testid='features-list'] li")
        description  = get_text(css="div[data-testid='listing-details__description']")
        images       = get_imgs(css="div[data-testid='listing-details__gallery'] img")
        agent_name   = get_text(css="div[data-testid='agent-info__name']")
        contact      = get_text(css="a[data-testid='agent-info__phone']")
        listing_date = get_text(xpath="//span[contains(text(),'Listed on')]/following-sibling::span")
        property_id  = get_text(xpath="//span[contains(text(),'Property ID')]/following-sibling::span")

        properties.append({
            "Title": title,
            "Price": price,
            "Location": location,
            "Area": area,
            "Bedrooms": beds,
            "Bathrooms": baths,
            "Features": features,
            "Description": description,
            "Images": images,
            "Agent Name": agent_name,
            "Contact": contact,
            "Listing Date": listing_date,
            "Property ID": property_id,
            "Link": link
        })

        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    # 6. Save to CSV
    df = pd.DataFrame(properties)
    df.to_csv("bproperty_full_listings.csv", index=False)
    print(f"Saved {len(df)} listings to bproperty_full_listings.csv")

    driver.quit()

if __name__ == "__main__":
    scrape_bproperty_dhaka()
