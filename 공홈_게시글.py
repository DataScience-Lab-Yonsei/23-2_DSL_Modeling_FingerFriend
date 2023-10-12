{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "8d1258c6-f187-4cb5-9a99-243f1053a208",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from selenium import webdriver\n",
    "from selenium.webdriver.common.by import By\n",
    "from selenium.webdriver.support.ui import WebDriverWait\n",
    "from selenium.webdriver.support import expected_conditions as EC\n",
    "from bs4 import BeautifulSoup\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    공홈 = pd.read_csv('공홈.csv')\n",
    "\n",
    "    driver = webdriver.Chrome('chromedriver.exe')\n",
    "\n",
    "    data_text = []\n",
    "\n",
    "    for _ in range(len(공홈)):\n",
    "        url = 공홈['링크'][_]\n",
    "        driver.get(url)\n",
    "        \n",
    "        if _ % 100 == 0:\n",
    "            print(f\"{_}번째 글 크롤링중...\")\n",
    "        \n",
    "        wait = WebDriverWait(driver, 3)\n",
    "        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, \"#jwxe_main_content > div.jwxe_board > div > dl > dd > div.cont_area\")))\n",
    "        soup = BeautifulSoup(element.get_attribute('outerHTML'), 'html.parser')\n",
    "        text = ' '.join(soup.stripped_strings)\n",
    "        data_text.append([url, text])\n",
    "    \n",
    "    driver.quit()\n",
    "\n",
    "    df_게시글 = pd.DataFrame(data_text, columns=[\"링크\", \"본문\"])\n",
    "\n",
    "    공식홈페이지 = pd.merge(공식홈페이지, df_게시글, on = '링크', how = 'left')\n",
    "\n",
    "    공식홈페이지.to_csv('공식홈페이지.csv', index = False)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.15"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
