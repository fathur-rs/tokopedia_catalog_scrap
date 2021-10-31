import csv
import os
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

def katalogScrape(page, keyword, file):
    counting = 0
    for page in range(1, page+1, 1):
        counting += 1
        print(f'Scrapping Page {counting}')
        page_url = f"https://www.tokopedia.com/search?navsource=home&page={page}&q={keyword}&st=product"
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(page_url)
        driver.maximize_window()

        prod = wait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-1sxqhh0')))

        while True:
            driver.execute_script('arguments[0].scrollIntoView();', prod[-1])
            try:
                wait(driver, 15).until(lambda driver: len(wait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-1sxqhh0')))) > len(prod))
                prod = wait(driver, 15).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'css-1sxqhh0')))
            except:
                break

        count = 0
        for item in prod:
            count += 1
            try:
                name = item.find_element_by_class_name("css-1f4mp12")
                price = item.find_element_by_class_name("css-rhd610")
                terjual = item.find_element_by_class_name("css-1kgbcz0")
                rating = item.find_element_by_class_name("css-etd83i")
                print(f"No {count}: {name.text}")
                write = csv.writer(open(f'{file}.csv', 'a', newline='', encoding="utf-8"))
                header = [name.text, price.text.replace('.', '').replace('Rp', ''), terjual.text.replace('Terjual', ''), rating.text]
                write.writerow(header)
            except NoSuchElementException:
                pass

        driver.quit()
    path = os.path.abspath(file)
    print(f'File Dir: {path}.csv')
    print('Scarpping Selesai!')

def main():
    file = input('Nama File: ')
    write = csv.writer(open(f'{file}.csv', 'w', newline='', encoding="utf-8"))
    header = ["name", "price", "sold", "rating"]
    write.writerow(header)
    keyword = input('Search: ')
    page = input('Page: ')
    Tokopedia = katalogScrape(int(page), keyword, file)
    return Tokopedia

if __name__ == '__main__':
    main()