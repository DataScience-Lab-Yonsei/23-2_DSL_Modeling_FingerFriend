from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import tqdm.notebook as tqdm
from bs4 import BeautifulSoup

if __name__ == "__main__":
    ## 학부 공지
    web = '응용통계학과'
    sub = "학부"
    
    driver = webdriver.Chrome('chromedriver.exe')
    
    n = 0
    data_학부 = []
    num = 100_000
    
    while True:
        if num < 2:
            break
            
        url_학부 = f"https://stat.yonsei.ac.kr/stat/board/under_notice.do?mode=list&&articleLimit=10&article.offset={n}"
        driver.get(url_학부)
        n += 10
    
        wait = WebDriverWait(driver, 3)
        tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#jwxe_main_content > div > div > div > table > tbody")))
    
        rows = tbody.find_elements(By.TAG_NAME, "tr")
    
        for row in rows:
            number = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
        
            if number != "공지":
                num = int(number)
                title = row.find_element(By.CSS_SELECTOR, "td.text-left > div.c-board-title-wrap").text.strip()
                link = row.find_element(By.CSS_SELECTOR, "td.text-left > div.c-board-title-wrap > a").get_attribute("href").strip()
                date = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
            
                data_학부.append([web, sub, num, title, link, date])
        
    driver.quit()
    
    df_학부 = pd.DataFrame(data_학부, columns=["학과", "서브", "id", "제목", "링크", "등록일"])

    ## 대학원 공지
    web = '응용통계학과'
    sub = "대학원"
    
    driver = webdriver.Chrome('chromedriver.exe')
    
    n = 0
    data_대학원 = []
    num = 100_000
    
    while True:
        if num < 2:
            break
            
        url_대학원 = f"https://stat.yonsei.ac.kr/stat/board/grad_notice.do?mode=list&&articleLimit=10&article.offset={n}"
        driver.get(url_대학원)
        n += 10
    
        wait = WebDriverWait(driver, 3)
        tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#jwxe_main_content > div > div > div > table > tbody")))
    
        rows = tbody.find_elements(By.TAG_NAME, "tr")
    
        for row in rows:
            number = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
        
            if number != "공지":
                num = int(number)
                title = row.find_element(By.CSS_SELECTOR, "td.text-left > div.c-board-title-wrap").text.strip()
                link = row.find_element(By.CSS_SELECTOR, "td.text-left > div.c-board-title-wrap > a").get_attribute("href").strip()
                date = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
            
                data_대학원.append([web, sub, num, title, link, date])
        
    driver.quit()
    
    df_대학원 = pd.DataFrame(data_대학원, columns=["학과", "서브", "id", "제목", "링크", "등록일"])

    ## 취업 공지
    web = '응용통계학과'
    sub = "취업"
    
    driver = webdriver.Chrome('chromedriver.exe')
    
    n = 0
    data_취업 = []
    num = 100_000
    
    while True:
        if num < 2:
            break
            
        url_취업 = f"https://stat.yonsei.ac.kr/stat/board/job.do?mode=list&&articleLimit=10&article.offset={n}"
        driver.get(url_취업)
        n += 10
    
        wait = WebDriverWait(driver, 3)
        tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#jwxe_main_content > div > div > div > table > tbody")))
    
        rows = tbody.find_elements(By.TAG_NAME, "tr")
    
        for row in rows:
            number = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
        
            if number != "공지":
                num = int(number)
                title = row.find_element(By.CSS_SELECTOR, "td.text-left > div.c-board-title-wrap").text.strip()
                link = row.find_element(By.CSS_SELECTOR, "td.text-left > div.c-board-title-wrap > a").get_attribute("href").strip()
                date = row.find_element(By.CSS_SELECTOR, "td:nth-child(5)").text.strip()
            
                data_취업.append([web, sub, num, title, link, date])
        
    driver.quit()
    
    df_취업 = pd.DataFrame(data_취업, columns=["학과", "서브", "id", "제목", "링크", "등록일"])

    ## concat them all
    df_응통 = pd.concat([df_학부, df_대학원, df_취업])
    df_응통.to_csv('응통.csv', index = False)