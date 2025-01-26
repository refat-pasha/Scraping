from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
chrome_driver_path = r"G:\New folder (7)\scraping\scraping_test1\chromedriver.exe"
service = Service(executable_path=chrome_driver_path)

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=service)
# driver.get("https://www.amazon.com/MSI-Thin-144Hz-Gaming-Laptop/dp/B0CXV8YGLV/ref=sr_1_1?dib=eyJ2IjoiMSJ9.fMp9EfSv-ux71syzZsOBBUmxjQjitfDEKTF6L12bOECfJnr8IoKY6HoIJnDExaKrv5WtOY34ggAmvLozBLlLzTQom1k29Mrvd8KLfNNgLG2x0oKD2WnP7tjTR_9vTy17JICG5xZftIsLzumBLvq5Af-iAOZc9tViQ-jQDJsqJ8MnxW5XPmFGQV6--8cCqLbo5Lajd9QDIJ546gkSsnQGY42wQv8LloFzQP2zcGRlLWQ.yiV_JgRpfNaWr5CJoAI4orbmaxARMxI_IoWG030qyXI&dib_tag=se&keywords=gaming%2Blaptops&pf_rd_i=23508887011&pf_rd_m=ATVPDKIKX0DER&pf_rd_p=434db2ed-6d53-4c59-b173-e8cd550a2e4f&pf_rd_r=KFJ6X0BGK5VHC40CYAZ3&pf_rd_s=merchandised-search-5&pf_rd_t=101&qid=1724336740&sr=8-1&th=1")
driver.get("https://www.rokomari.com/book/category/6994/boimela-2024-religious-books?sort=DISCOUNT_DESC&ratings=&page=1")
# price = driver.find_element(By.CLASS_NAME, 'a-price-whole')
# print(price.text + "$")



# price2 = driver.find_element(By.XPATH, '//*[@id="product"]/div/div[1]/table/tbody/tr[1]/td[2]/ins')
header = driver.find_elements(By.CLASS_NAME, 'book-text-area')
# name = driver.find_elements(By.TAG_NAME, 'p')
# for h in header:
#     print(h.text)
    # for n in name:
    #     print(n.text)


titles = []



for header in header:
    data = header.text.split("\n")
    titles.append(data)

print(titles)
df = pd.DataFrame(titles)

df.to_excel("books_info.xlsx", index=False)

driver.quit()
