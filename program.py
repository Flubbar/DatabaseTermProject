from datetime import timedelta
import pymysql
db = pymysql.connect(host='192.168.59.4', user='Seonyul', password = '1234', db = 'astrolabe', charset='utf8',port=4567)
cur = db.cursor()

query = " "

def search():
    while(True):
        print("검색 =======================================================")
        print("1. 이름으로 행성 찾기")
        print("2. 이름으로 위성 찾기")
        print("3. 행성 별 관측 가능 시간")
        print("4. 행성 별 관측회 스케줄")
        print("5. 관측회 참석자")
        print("0. 뒤로")
        command = int(input())
        if command == 1:
            name = input("찾으려는 행성 이름 입력 : ")
            query = "SELECT * FROM PLANET WHERE Name = \"" + name + "\""
            cur.execute(query)
            db.commit()
            fetched = cur.fetchall()
            if len(fetched) == 0:
                print("검색 결과가 없습니다.")
            else:
                result = fetched[0]
                print("행성 이름 : ", result[0])
                print("공전 주기 : ", result[1], "년")
                print("지름 : ", result[2], "km")
                print("지구로부터 거리 : ", result[3], "AU (약", result[3]*1.5, "억 km)")

        elif command == 2:
            name = input("찾으려는 위성 이름 입력 : ")
            query = "SELECT * FROM SATELITE WHERE Name = \"" + name + "\""
            cur.execute(query)
            db.commit()
            fetched = cur.fetchall()
            if len(fetched) == 0:
                print("검색 결과가 없습니다.")
            else:
                result = fetched[0]
                print("위성 이름 : ", result[0])
                print("공전 주기 : ", result[1], "년")
                print("지름 : ", result[2], "km")
                print("공전 기준 행성 : ", result[4])
                print(result[4], "(으)로부터 거리 : ", result[3], "km")

        elif command == 3:
            name = input("관측하려는 행성 이름 입력 : ")
            query = "SELECT * FROM OBSERVABLE_TIME WHERE Planet_name = \"" + name + "\""
            cur.execute(query)
            db.commit()
            fetched = cur.fetchall()
            if len(fetched) == 0:
                print("검색 결과가 없습니다.")
            else:
                print(name + "을(를) 관측할 수 있는 날짜")
                for result in fetched:
                    print(result[0], ". ", result[1] , "부터" , result[1] + timedelta(days=result[2]) , "까지")

        elif command == 4:
            name = input("관측하려는 행성 이름 입력 : ")
            query = "SELECT * FROM OBSERVATION_SCHEDULE WHERE Planet_name = \"" + name + "\""
            cur.execute(query)
            db.commit()
            fetched = cur.fetchall()
            if len(fetched) == 0:
                print("검색 결과가 없습니다.")
            else:
                print(name + "을(를) 관측하는 관측회")
                for result in fetched:
                    print("ID :", result[0], "시간 :", result[1] , ", 장소 :" , result[2])

        elif command == 5:
            sch_no = input("관측회 ID 입력 : ")
            query = "SELECT * FROM PARTICIPANTS WHERE Sch_no = \"" + sch_no + "\""
            cur.execute(query)
            db.commit()
            fetched = cur.fetchall()
            if len(fetched) == 0:
                print("검색 결과가 없습니다.")
            else:
                print(sch_no, "번 관측회에 참여하는 인원")
                for result in fetched:
                    print("ID :", result[0], "이름 :", result[1])

        elif command == 0:
            return
        else:
            print("알 수 없는 커맨드입니다.")
            continue


def adv_search():
    print("고급 검색 =======================================================")
    print("1. 행성으로 위성 찾기")
    print("2. 특정 날짜에 관측 가능한 행성 찾기")
    print("3. 관측회에서 관측 가능한 다른 행성 찾기")
    print("4. 1명이 참석하는 모든 관측회 찾기")
    print("5. 1명이 관측할 수 있는 모든 행성 찾기")
    print("0. 뒤로")

def add_record():
    print("추가 =======================================================")
    print("1. 행성 추가")
    print("2. 위성 추가")
    print("3. 관측 가능 시간 추가")
    print("4. 관측회 스케줄 추가")
    print("5. 관측회 참석자 추가")
    print("0. 뒤로") 

def delete_record():
    print("삭제 =======================================================")
    print("1. 행성 삭제")
    print("2. 위성 삭제")
    print("3. 관측 가능 시간 삭제")
    print("4. 관측회 스케줄 삭제")
    print("5. 관측회 참석자 삭제")
    print("0. 뒤로")   

while(True):
    print("커맨드 선택 =======================================================")
    print("1. 검색")
    print("2. 고급 검색")
    print("3. 추가")
    print("4. 삭제")
    print("0. 종료")
    command = int(input())
    if command == 1:
        search()
    elif command == 2:
        adv_search()
    elif command == 3:
        add_record()
    elif command == 4:
        pass
    elif command == 0:
        break
    else:
        print("알 수 없는 커맨드입니다.")
        continue


query = input("\n\nEnter Query... (type 'exit' to exit)\n")
if query == "exit":
    pass
cur.execute(query)
db.commit()
result = cur.fetchall()
for data in result:
    print(*data)

