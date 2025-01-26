from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

# Path to the ChromeDriver executable
chrome_driver_path = r"G:\New folder (7)\scraping\scraping_test1\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Base URL
base_url = "https://www.bproperty.com/buy/dhaka/residential/apartments/?page="

# Initialize lists to store data
titles = []
addresses = []
descriptions = []
prices = []
bedrooms = []
bathrooms = []
floor_areas = []
links = []

# Loop through the first 5 pages
for page in range(1, 51):
    # Construct the URL for the current page
    url = base_url + str(page)
    driver.get(url)

    # Find all book containers
    property_info_containers = driver.find_elements(By.CLASS_NAME, 'ListingCell-AllInfo')

    # Extract data for each book
    for propertys in property_info_containers:
        # Extract title
        try:
            title_element = propertys.find_element(By.CLASS_NAME, 'ListingCell-KeyInfo-title')
            title = title_element.text.strip()
        except:
            title = 'N/A'
        # Extract author (if available)
        try:
            address = propertys.find_element(By.CLASS_NAME, 'ListingCell-KeyInfo-address-text').text
        except:
            address = "N/A"
        try:
            description = propertys.find_element(By.CLASS_NAME, 'ListingCell-shortDescription ').text
        except:
            description = "N/A"

        # Extract price (if available)
        try:
            price_element = propertys.find_element(By.CLASS_NAME, 'PriceSection-FirstPrice')
            price = price_element.text.strip()
        except:
            price = "N/A"


        try:
            bedroom = propertys.find_element(
                By.CSS_SELECTOR, "div.KeyInformation-attribute_v2:nth-child(1) span.KeyInformation-value_v2"
            ).text.strip()
        except:
            bedroom = "N/A"
            
        try:
            bathroom = propertys.find_element(
                By.CSS_SELECTOR, "div.KeyInformation-attribute_v2:nth-child(2) span.KeyInformation-value_v2"
            ).text.strip()
        except:
            bathroom = "N/A"
            
        try:
            floor_area = propertys.find_element(
                By.CSS_SELECTOR, "div.KeyInformation-attribute_v2:nth-child(3) span.KeyInformation-value_v2"
            ).text.strip()
        except:
            floor_area = "N/A"

        try:
            link = propertys.find_element(By.CSS_SELECTOR, "a.js-listing-link").get_attribute("href")
        except:
            link = 'N/A'

        #Append data to lists
        titles.append(title)
        addresses.append(address)
        descriptions.append(description)
        prices.append(price)
        bedrooms.append(bedroom)
        bathrooms.append(bathroom)
        floor_areas.append(floor_area)
        links.append(link)

# Create a DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Address": addresses,
    "Description": descriptions,
    "price": prices,
    "Bedroom": bedrooms,
    "Bathroom": bathrooms,
    "Floor_area": floor_areas,
    "link": links
})

# Save the DataFrame to an Excel file
df.to_excel("bdProperty_Apartments_for_Sale_in_Dhaka.xlsx", index=False, engine="xlsxwriter")

# Quit the driver
driver.quit()

print("Data saved to bdProperty_Apartments_for_Sale_in_Dhaka.xlsx")
