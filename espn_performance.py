from selenium import webdriver
from bs4 import BeautifulSoup
import time
import random

url = 'http://insider.espn.com/nba/hollinger/statistics/_/page/'

try:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    chrome = webdriver.Chrome(options=options,
                             executable_path='/Users/andylin/chromedriver')
    chrome.set_page_load_timeout(10)
    
    for i in range(1, 8):
        _url = url + str(i)
        print(_url)
        # 透過 get 取得頁面資訊後，交由 BeautifulSoup 解析
        chrome.get(_url)
        soup = BeautifulSoup(chrome.page_source, 'html5lib')
        # 數據資訊在 tbody 標籤裡
        trs = soup.find('tbody').find_all('tr')
        for tr in trs:
            # 將所有 td 存成 list
            tds = [td for td in tr.children]
            # 取得第一欄為 rk
            rk = tds[0].text.strip()
            # 若為 'RK' ，則為項目欄，不是球員數據欄位；若長度小於2，則為標題欄，亦不是球員數據欄位 -> 都跳過
            if rk =='RK' or len(tds)<2:
                continue
            # 取得 球員名稱與 PER 值，並印出
            name = tds[1].text
            per = tds[11].text
            print('%s :%s' % (name, per))
        # 等待幾秒後再繼續執行下一次，避免被網站阻擋
        wait = random.randint(2,6)
        print('wait time : %d' % wait)
        time.sleep(wait)
    
    
finally:
    chrome.quit()