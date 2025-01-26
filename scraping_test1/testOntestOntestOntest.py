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
base_url = "https://www.rokomari.com/book/category/6994/boimela-2024-religious-books?sort=DISCOUNT_DESC&ratings=&page="

# Initialize lists to store data
titles = []
authors = []
original_prices = []
discounted_prices = []


# Loop through the first 5 pages
for page in range(1, 35):  # Loop over pages 1 to 5
    # Construct the URL for the current page
    url = base_url + str(page)
    driver.get(url)

    # Find all book containers
    book_containers = driver.find_elements(By.CLASS_NAME, 'book-text-area')

    # Extract data for each book
    for book in book_containers:
        # Extract title
        title = book.find_element(By.TAG_NAME, 'h4').text

        # Extract author (if available)
        try:
            author = book.find_element(By.TAG_NAME, 'p').text
        except:
            author = "N/A"

        # Extract original price (if available)
        try:
            original_price = book.find_element(By.CLASS_NAME, 'original-price').text.split()[-1]
        except:
            original_price = "N/A"

        # Extract discounted price
        try:
            # Get the text and split to take only the discounted price
            discounted_price = book.find_element(By.CLASS_NAME, 'book-price').text.split()[-1]
        except:
            discounted_price = "N/A"


        # Append data to lists
        titles.append(title)
        authors.append(author)
        original_prices.append(original_price)
        discounted_prices.append(discounted_price)


# Create a DataFrame
df = pd.DataFrame({
    "Title": titles,
    "Author": authors,
    "Original_prices": original_prices,
    "Discounted_price": discounted_prices
})

# Save the DataFrame to an Excel file
df.to_excel("books_info_final_test_2.xlsx", index=False, engine="xlsxwriter")

# Quit the driver
driver.quit()

print("Data saved to books_info_final_test_2.xlsx")
