from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import tqdm.notebook as tqdm
from bs4 import BeautifulSoup

if __name__ == "__main__":
    driver = webdriver.Chrome('chromedriver.exe')
    
    n = 0
    cnt = 0
    data_공지 = []
    
    while True:
        url_공지 = f"https://www.yonsei.ac.kr/sc/support/notice.jsp?mode=list&board_no=15&pager.offset={n}"
        driver.get(url_공지)
        cnt += 1
    
        wait = WebDriverWait(driver, 3)
        tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#jwxe_main_content > div.jwxe_board > div > ul")))
    
        rows = tbody.find_elements(By.TAG_NAME, "li")
        
        if len(rows) <= 10:
            break
        elif (n % 100) == 0:
            print(f"{cnt}번 페이지 크롤링중...")
            
        if n == 0:
            for row in rows:
                title = row.find_element(By.CSS_SELECTOR, "a > strong").text.strip()
                link = row.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                web = row.find_element(By.CSS_SELECTOR, "a > span").text.strip()
                sub = row.find_element(By.CSS_SELECTOR, "a > span > span:nth-child(1)").text.strip()
                date = row.find_element(By.CSS_SELECTOR, "a > span > span:nth-child(2)").text.strip()
    
                data_공지.append([web, sub, title, link, date])
        else:
            for row in rows[6:]:
                title = row.find_element(By.CSS_SELECTOR, "a > strong").text.strip()
                link = row.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
                web = row.find_element(By.CSS_SELECTOR, "a > span").text.strip()
                sub = row.find_element(By.CSS_SELECTOR, "a > span > span:nth-child(1)").text.strip()
                date = row.find_element(By.CSS_SELECTOR, "a > span > span:nth-child(2)").text.strip()
    
                data_공지.append([web, sub, title, link, date])      
            
        n += 10
        
    driver.quit()
    
    df_공지 = pd.DataFrame(data_공지, columns=["학과", "서브", "제목", "링크", "등록일"])

    df_공지['학과'] = df_공지['학과'].apply(lambda x: x.split(' ')[0])

    ## 외부 기관 공고
    
    driver = webdriver.Chrome('chromedriver.exe')
    
    n = 0
    cnt = 0
    data_외부 = []
    
    while True:
        url_외부 = f"https://www.yonsei.ac.kr/sc/support/etc_notice.jsp?mode=list&board_no=43&pager.offset={n}"
        driver.get(url_외부)
        cnt += 1
    
        wait = WebDriverWait(driver, 3)
        tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#jwxe_main_content > div.jwxe_board > div > ul")))
    
        rows = tbody.find_elements(By.TAG_NAME, "li")
        
        if len(rows) <= 3:
            break
        elif (n % 100) == 0:
            print(f"{cnt}번 페이지 크롤링중...")
            
        for row in rows:
            title = row.find_element(By.CSS_SELECTOR, "a > strong").text.strip()
            link = row.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            web = row.find_element(By.CSS_SELECTOR, "a > span").text.strip()
            sub = row.find_element(By.CSS_SELECTOR, "a > span > span:nth-child(1)").text.strip()
            date = row.find_element(By.CSS_SELECTOR, "a > span > span:nth-child(2)").text.strip()
    
            data_외부.append([web, sub, title, link, date])    
            
        n += 10
        
    driver.quit()
    
    df_외부 = pd.DataFrame(data_외부, columns=["학과", "서브", "제목", "링크", "등록일"])
    df_외부['학과'] = df_외부['학과'].apply(lambda x: x.split(' ')[0])

    ## 코로나19 관련 공지사항
    
    driver = webdriver.Chrome('chromedriver.exe')
    
    n = 0
    cnt = 0
    data_코로나 = []
    
    while True:
        url_코로나 = f"https://www.yonsei.ac.kr/sc/support/corona_notice.jsp?mode=list&board_no=752&pager.offset={n}"
        driver.get(url_코로나)
        cnt += 1
    
        wait = WebDriverWait(driver, 3)
        tbody = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#jwxe_main_content > div.jwxe_board > div > ul")))
    
        rows = tbody.find_elements(By.TAG_NAME, "li")
        
        if len(rows) <= 3:
            break
        elif (n % 100) == 0:
            print(f"{cnt}번 페이지 크롤링중...")
            
        for row in rows:
            title = row.find_element(By.CSS_SELECTOR, "a > strong").text.strip()
            link = row.find_element(By.CSS_SELECTOR, "a").get_attribute("href").strip()
            web = row.find_element(By.CSS_SELECTOR, "a > span").text.strip()
            sub = row.find_element(By.CSS_SELECTOR, "a > span > span:nth-child(1)").text.strip()
            date = row.find_element(By.CSS_SELECTOR, "a > span > span:nth-child(2)").text.strip()
    
            data_코로나.append([web, sub, title, link, date])    
            
        n += 10
        
    driver.quit()
    
    df_코로나 = pd.DataFrame(data_코로나, columns=["학과", "서브", "제목", "링크", "등록일"])
    df_코로나['학과'] = df_코로나['학과'].apply(lambda x: x.split(' ')[0])

    ## concat 후 저장
    
    df_공홈 = pd.concat([df_공지, df_외부, df_코로나])
    df_공홈.to_csv('공홈.csv', index = False)