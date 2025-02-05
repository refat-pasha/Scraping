from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

from Scraping.scraping_test1.bdproperty_test_dhaka import descriptions

driver_path = "chromedriver.exe"
service = Service(executable_path=driver_path)

driver = webdriver.Chrome(service=service)

base_url = "https://www.ambitionbox.com/list-of-companies?campaign=desktop_nav&page="

company_names = []
ratings = []
reviews = []
descriptions = []
locations = []
pros = []
cons = []
salaries = []
interviews = []
jobs = []
benefits = []
photos = []
links = []


for page in range(1,5):

    url = base_url + str(page)
    driver.get(url)

    job_info_container = driver.find_elements(By.CLASS_NAME, "companyCardWrapper")

    for jobs in job_info_container:
        try:
            company_title = jobs.find_elements(By.CLASS_NAME, "companyCardWrapper__companyName")
            company_name = company_title.text.strip()

        except:
            company_name = "N/A"

        try:
            rating = jobs.find_element(By.CSS_SELECTOR, 'div[style="height: auto; padding-bottom: 1px;"]').text.strip()

        except:
            rating = "N/A"

        try:
            rating = jobs.find_element(By.CSS_SELECTOR, 'div[style="height: auto; padding-bottom: 1px;"]').text.strip()

        except:
            rating = "N/A"


