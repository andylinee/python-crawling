import requests
from bs4 import BeautifulSoup
import time

# 今天日期，扣掉最前面的 0
today = time.strftime('%m/%d').lstrip('0')

def pttNBAOverTen(url):
    resp = requests.get(url)
    # 確認 server 是否正常運作
    if resp.status_code != 200:
        print('URL 發生錯誤：' + url)
        return
    
    soup = BeautifulSoup(resp.text, 'html5lib')
    # 上一頁的連結
    paging = soup.find('div', 'btn-group btn-group-paging').find_all('a')[1]['href']
    
    # 存放文章的 list
    articles = []
    rents = soup.find_all('div', 'r-ent')
    for rent in rents:
        # 將文章的 "title", "count", "date" 合成字串
        title = rent.find('div', 'title').text.strip()
        count = rent.find('div', 'nrec').text.strip()
        date = rent.find('div', 'meta').find('div', 'date').text.strip()
        article = '%s %s:%s' % (date, count, title)
        
        try:
            # 選擇推文數超過 10 的文章，加進 articles 串列中
            if today == date and int(count) > 10:
                articles.append(article)
        except:
            # 選擇推文數為 "爆" 的文章，加進 articles 串列中
            if today == date and count == '爆':
                articles.append(article)
    
    if len(articles) != 0:
        for article in articles:
            print(article)
        # 當頁文章都掃完之後，換至上一頁
        pttNBA('https://www.ptt.cc' + paging)
    else:
        return
    
pttNBAOverTen('https://www.ptt.cc/bbs/NBA/index.html')