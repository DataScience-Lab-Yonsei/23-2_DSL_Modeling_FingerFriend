import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

if __name__ == "__main__":
    응통 = pd.read_csv('응통.csv')

    driver = webdriver.Chrome('chromedriver.exe')
    
    data_text = []
    
    for _ in range(len(응통)):
        url = 응통['링크'][_]
        driver.get(url)
        
        wait = WebDriverWait(driver, 3)
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#jwxe_main_content > div > div.board-wrap > div > dl.board-write-box.board-write-box-v03 > dd > div")))
        soup = BeautifulSoup(element.get_attribute('outerHTML'), 'html.parser')
        text = ' '.join(soup.stripped_strings)
        data_text.append([url, text])
    
    driver.quit()

    df_게시글 = pd.DataFrame(data_text, columns=["링크", "본문"])

    응용통계학과 = pd.merge(응통, df_게시글, on = '링크', how = 'left')

    응용통계학과.to_csv('응용통계학과.csv', index = False)