import requests
from bs4 import BeautifulSoup
import time

# 台鐵網站首頁
url = 'https://tip.railway.gov.tw/tra-tip-web/tip'

# 之後要放入 站名:車站代碼 的 dict
staDic = {}
today = time.strftime('%Y/%m/%d')
sTime = '06:00'
eTime = '12:00'

def getTrip():
    resp = requests.get(url)
    if resp.status_code != 200:
        print('URL發生錯誤：' + url)
        return
    
    soup = BeautifulSoup(resp.text, 'html5lib')
    # 站名資訊的位置
    stations = soup.find(id = 'cityHot').ul.find_all('li')
    for station in stations:
        # 站名
        stationName = station.button.text
        # 車站代碼
        stationId = station.button['title']
        # 將 站名:車站代碼 填入 dict
        staDic[stationName] = stationId
    
    # 找到並記住 csrf 值
    csrf = soup.find(id = 'queryForm').find('input',{'name':'_csrf'})['value']
    # 需要回傳的值，前三行為固定值
    formData = {
        'trainTypeList':'ALL',
        'transfer':'ONE',
        'startOrEndTime':'true',
        'startStation':staDic['臺北'],
        'endStation':staDic['臺南'],
        'rideDate':today,
        'startTime':sTime,
        'endTime':eTime
    }
    
    # 要 query 的網址
    queryUrl = soup.find(id='queryForm')['action']
    # 用 post 去互動，第一個參數為 query 網址，第二個參數為回傳資料
    qResp = requests.post('https://tip.railway.gov.tw'+queryUrl, data=formData)
    qSoup = BeautifulSoup(qResp.text, 'html5lib')
    # 班次資料
    trs = qSoup.find_all('tr', 'trip-column')
    for tr in trs:
        td = tr.find_all('td')
        # 分別印出 班次、出發時間、抵達時間
        print('%s : %s, %s' % (td[0].ul.li.a.text, td[1].text, td[2].text)) 
        
getTrip()