import sqlite3

# 連結資料庫
conn = sqlite3.connect('/Users/andylin/demo/test.db')
try:
    # 計算好的 bmi 值及相對應的 id 會存放在此 list 中
    info = []
    # 建立物件 cursor，之後執行 SQL 語法都要透過這個 cursor 執行
    cur = conn.cursor()
    # 使用 execute 執行 SQL
    rows = cur.execute('select * from person')
    for row in rows:
        id = row[0]
        height = row[2]
        weight = row[3]
        # 計算 bmi 值
        bmi = round(weight/height**2, 2)
        # 先列印出資料，檢查是否執行成功
        print(id, height, weight, bmi)
        # 將計算好的 bmi 值及相對應的 id 存放到 info 中
        info.append([bmi, id])
    for data in info:
        # 將 bmi 欄位指定新的值
        cur.execute('update person set bmi=%d where id=%d' % (data[0], data[1]))
    # 用連結資料庫的 conn 物件來執行 commit -> 將資料存到實體檔案
    conn.commit()
    
# 關閉資料庫
finally:
    conn.close()