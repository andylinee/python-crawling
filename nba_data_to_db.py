import sqlite3
import requests
import json
import time
import random

custom_headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

conn = sqlite3.connect('/Users/andylin/demo/nba.db')
cur = conn.cursor()
try:
    # general 數據的 API 網址
    gen_url = 'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2018-19&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&TwoWay=0&VsConference=&VsDivision=&Weight='
    # 用 API 網址及 header 透過 get 取得回傳的 response
    gen_resp = requests.get(gen_url, headers = custom_headers)
    # 將回傳的 json 字串轉換成物件
    gen_datas = json.loads(gen_resp.text)
    # 目前在處理 general 頁面資料
    print('insert general table')
    # 透過 JSON Viewer 找到球員資料的位置
    for gen_data in gen_datas['resultSets'][0]['rowSet']:
        cur.execute('insert into nba_general(player_id, player_name, gp, pts, fgm, fga, fg_per) values (?, ?, ?, ?, ?, ?, ?)', 
                   (gen_data[0], gen_data[1], gen_data[5], gen_data[29], gen_data[10], gen_data[11], gen_data[12]))


    
    # shooting 數據的 API 網址
    sho_url = 'https://stats.nba.com/stats/leaguedashplayershotlocations?College=&Conference=&Country=&DateFrom=&DateTo=&DistanceRange=By+Zone&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=2018-19&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
    # 用 API 網址及 header 透過 get 取得回傳的 response
    sho_resp = requests.get(sho_url, headers = custom_headers)
    sho_datas = json.loads(sho_resp.text)
    # 目前在處理 shooting 頁面資料
    print('insert shooting table')
    # 透過 JSON Viewer 找到球員資料的位置
    for sho_data in sho_datas['resultSets']['rowSet']:
        cur.execute('insert into nba_shooting (player_id, res_fgm, res_fga, res_fg_per, pai_fgm, pai_fga, pai_fg_per, mid_fgm, mid_fga, mid_fg_per, left3_fgm, left3_fga, left3_fg_per, right3_fgm, right3_fga, right3_fg_per, pt3_fgm, pt3_fga, pt3_fg_per) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (sho_data[0], sho_data[5], sho_data[6], sho_data[7], sho_data[8], sho_data[9], sho_data[10], sho_data[11], sho_data[12], sho_data[13], sho_data[14], sho_data[15], sho_data[16], sho_data[17], sho_data[18], sho_data[19], sho_data[20], sho_data[21], sho_data[22]))
        
    # 用 commit 將資料存到實體檔案中
    conn.commit()                
                    
                    
finally:
    # 關閉資料庫
    conn.close()
    print('finish')