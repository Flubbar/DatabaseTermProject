import pymysql
db = pymysql.connect(host='192.168.59.4', user='Seonyul', password = '1234', db = 'astrolabe', charset='utf8',port=4567)
cur = db.cursor()

query = " "

while(True):
    query = input("\n\nEnter Query... (type 'exit' to exit)\n")
    if query == "exit":
        break
    cur.execute(query)
    db.commit()
    result = cur.fetchall()
    for data in result:
        print(data)