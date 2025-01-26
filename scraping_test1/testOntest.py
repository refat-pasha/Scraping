from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

# Path to the ChromeDriver executable
chrome_driver_path = r"G:\New folder (7)\scraping\scraping_test1\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

# Initialize the WebDriver
driver = webdriver.Chrome(service=service)

# Open the target URL
driver.get("https://www.rokomari.com/book/category/6994/boimela-2024-religious-books?sort=DISCOUNT_DESC&ratings=&page=1")

# Initialize lists to store data
titles = []
authors = []
original_prices = []
discounted_prices = []

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

    # Extract price (if available)
    try:
        original_price = book.find_element(By.CLASS_NAME, 'original-price').text
    except:
        original_price = "N/A"
    try:
        discounted_price = book.find_element(By.CLASS_NAME, 'book-price').text
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
df.to_excel("books_info.xlsx", index=False, engine="xlsxwriter")


# Quit the driver
driver.quit()

print("Data saved to books_info.xlsx")
