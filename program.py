from datetime import timedelta
import datetime
import time
import pymysql
db = pymysql.connect(host='192.168.59.4', user='Seonyul', password = '1234', db = 'astrolabe', charset='utf8',port=4567)
cur = db.cursor()

query = " "

def fetch_db(query):
    cur.execute(query)
    db.commit()
    return cur.fetchall()

def search():
    while(True):
        print("\n검색 =======================================================")
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
            fetched = fetch_db(query)
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
            fetched = fetch_db(query)
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
            fetched = fetch_db(query)
            if len(fetched) == 0:
                print("검색 결과가 없습니다.")
            else:
                print(name + "을(를) 관측할 수 있는 날짜")
                for result in fetched:
                    print(result[0], ". ", result[1] , "부터" , result[1] + timedelta(days=result[2]) , "까지")

        elif command == 4:
            name = input("관측하려는 행성 이름 입력 : ")
            query = "SELECT * FROM OBSERVATION_SCHEDULE WHERE Planet_name = \"" + name + "\""
            fetched = fetch_db(query)
            if len(fetched) == 0:
                print("검색 결과가 없습니다.")
            else:
                print(name + "을(를) 관측하는 관측회")
                for result in fetched:
                    print("ID :", result[0], "시간 :", result[1] , ", 장소 :" , result[2])

        elif command == 5:
            sch_no = input("관측회 ID 입력 : ")
            query = "SELECT * FROM PARTICIPANTS WHERE Sch_no = \"" + sch_no + "\""
            fetched = fetch_db(query)
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
    while(True):
        print("\n고급 검색 =======================================================")
        print("1. 행성으로 위성 찾기")
        print("2. 특정 날짜에 관측 가능한 행성 찾기")
        print("3. 관측회에서 관측 가능한 모든 행성 찾기")
        print("4. 1명이 참석하는 모든 관측회 찾기")
        print("5. 1명이 관측할 수 있는 모든 행성 찾기")
        print("0. 뒤로")
        command = int(input())

        if command == 1:
            name = input("위성을 찾으려는 행성 이름 입력 : ")
            query = "SELECT Satelite_name FROM SATELITE WHERE Planet_name = \"" + name + "\""
            fetched = fetch_db(query)
            if len(fetched) == 0:
                print("존재하지 않는 행성이거나, 행성의 위성이 없습니다.")
            else:
                print(name+"이(가) 가지고 있는 위성 목록 :")
                for result in fetched:
                    print(result[0])
        
        elif command == 2:
            date = input("대상 날짜 입력 (YYYY-MM-DD): " )
            query = "SELECT P.Name, O.Time, O.Length_day FROM PLANET P, OBSERVABLE_TIME O WHERE O.Planet_name = P.Name AND \'"\
                 +date+"\' BETWEEN O.Time AND DATE_ADD(O.Time, INTERVAL O.Length_day DAY)"
            fetched = fetch_db(query)
            if len(fetched) == 0:
                print("해당 날짜에 볼 수 있는 행성이 없습니다.")
            else:
                print(date, "에 관측할 수 있는 행성")
                for result in fetched:
                    print(result[0], ": ", result[1] , "부터" , result[1] + timedelta(days=result[2]) , "까지")
        
        elif command == 3:
            sch_no = input("관측회 스케줄 ID 입력 : ")
            sub_query = "SELECT Time FROM OBSERVATION_SCHEDULE WHERE Sch_no = "+str(sch_no)
            query = "SELECT P.Name, O.Time, O.Length_day, OT.Time FROM PLANET P, OBSERVABLE_TIME O, ("+ sub_query +") OT WHERE O.Planet_name = P.Name AND \
                 OT.Time BETWEEN O.Time AND DATE_ADD(O.Time, INTERVAL O.Length_day DAY)"
            fetched = fetch_db(query)
            if len(fetched) == 0:
                print("존재하지 않는 관측회거나, 이때 관측가능한 행성이 없습니다.")
            else:
                print(sch_no, "번 관측회 (", fetched[0][3], ")에 관측할 수 있는 모든 행성")
                for result in fetched:
                    print(result[0], ": ", result[1] , "부터" , result[1] + timedelta(days=result[2]) , "까지")
        
        elif command == 4:
            name = input("검색할 참가자 이름 입력 : ")
            query = "SELECT O.Sch_no, O.Time, O.Location, O.Planet_name FROM OBSERVATION_SCHEDULE O, PARTICIPANTS P WHERE O.Sch_no = P.Sch_no AND P.Part_name = \"" + name + "\""
            fetched = fetch_db(query)
            if len(fetched) == 0:
                print("해당 참가자가 참가하는 관측회가 없습니다.")
            else:
                print(name, "이(가) 참가하는 모든 관측회")
                for result in fetched:
                    print("ID :", result[0], "시간 :", result[1] , ", 장소 :" , result[2], ", 관측 행성 :", result[3])
        
        elif command == 5:
            name = input("검색할 참가자 이름 입력 : ")
            sub_query = "SELECT OB.Time FROM OBSERVATION_SCHEDULE OB, PARTICIPANTS PA WHERE OB.Sch_no = PA.Sch_no AND PA.Part_name = \"" + name + "\""
            query = "SELECT P.Name, OT.Time FROM PLANET P, OBSERVABLE_TIME O, ("+ sub_query +") OT WHERE O.Planet_name = P.Name AND \
                 OT.Time BETWEEN O.Time AND DATE_ADD(O.Time, INTERVAL O.Length_day DAY)"
            fetched = fetch_db(query)
            if len(fetched) == 0:
                print("해당 참가자가 참가하는 관측회가 없습니다.")
            else:
                print(name, "이(가) 관측할 수 있는 행성")
                for result in fetched:
                    print(result[0], ": ", result[1], "에 관측 가능")    
            
        elif command == 0:
            break
        else:
            print("알 수 없는 커맨드입니다.")
            continue

def add_record():
    print("추가 =======================================================")
    print("1. 행성 추가")
    print("2. 위성 추가")
    print("3. 관측 가능 시간 추가")
    print("4. 관측회 스케줄 추가")
    print("5. 관측회 참석자 추가")
    print("0. 뒤로")
    command = int(input())
    if command == 1:
        name = input("새로운 행성 이름 : ")
        orbital = input("공전 주기(년) : ")
        radius = input("지름(km) : ")
        distance = input("지구로부터의 거리(AU) : ")
        print("이름 : "+ name + "/공전 주기: "+ orbital +"년/지름 : "+ radius +"km/ 거리 : "+ distance +"AU")
        confirm = input("위 내용이 맞습니까? (맞을 경우 'Y' 입력)")
        if confirm == 'Y':
            query = "INSERT INTO PLANET VALUES(\'"+name+"\',"+orbital+","+radius+","+distance+")"
            fetch_db(query)
            print("행성 추가 완료!")
        else:
            print("취소되었습니다.")
    
    if command == 2:
        name = input("새로운 위성 이름 : ")
        orbital = input("공전 주기(일) : ")
        radius = input("지름(km) : ")
        distance = input("행성으로부터의 거리(km) : ")
        planet = input("공전하는 행성 : ")
        print("이름 : "+ name + "/공전 주기: "+ orbital +"년/지름 : "+ radius +"km/ 거리 : "+ distance +"AU/행성 : "+planet)
        confirm = input("위 내용이 맞습니까? (맞을 경우 'Y' 입력)")
        if confirm == 'Y':
            query = "INSERT INTO SATELITE VALUES(\'"+name+"\',"+orbital+","+radius+","+distance+","+planet+")"
            fetch_db(query)
            print("위성 추가 완료!")
        else:
            print("취소되었습니다.")
    
    if command == 3:
        planet = input("관측할 행성 : ")
        time = input("관측가능 시간 (YYYY-MM-DD) : ")
        length = input("관측가능 기간(일) : ")
        no = input("기간 번호 : ")
        print("관측 행성 : "+ planet + "/시간: "+ time +"/기간 : "+ length +"일/ID : "+ no)
        confirm = input("위 내용이 맞습니까? (맞을 경우 'Y' 입력)")
        if confirm == 'Y':
            query = "INSERT INTO OBSERVABLE_TIME VALUES("+no+",STR_TO_DATE(\'"+time+"\',\'%%Y-%%m-%%d\'),"+length+",\'"+planet+"\')"
            fetch_db(query)
            print("관측 가능 기간 추가 완료!")
        else:
            print("취소되었습니다.")
    
    if command == 4:
        planet = input("관측할 행성 : ")
        time = input("관측할 시간 (YYYY-MM-DD) : ")
        location = input("관측할 장소 : ")
        sch_no = input("스케줄 번호 : ")
        planet = input("공전하는 행성 : ")
        print("관측 행성 : "+ planet + "/시간: "+ time +"/장소 : "+ location +"/ID : "+ sch_no)
        confirm = input("위 내용이 맞습니까? (맞을 경우 'Y' 입력)")
        if confirm == 'Y':
            query = "INSERT INTO OBSERVATION_SCHEDULE VALUES("+sch_no+",STR_TO_DATE(\'"+time+"\',\'%%Y-%%m-%%d\'),\'"+location+"\',\'"+planet+"\')"
            fetch_db(query)
            print("스케줄 추가 완료!")
        else:
            print("취소되었습니다.")
    
    if command == 5:
        sch_no = input("참가할 관측회 ID : ")
        name = input("참가자 이름 : ")
        part_no = input("참가자 ID : ")
        print("관측회 ID : "+sch_no+"/이름 : "+name+"/참가자 ID : "+part_no)
        confirm = input("위 내용이 맞습니까? (맞을 경우 'Y' 입력)")
        if confirm == 'Y':
            query = "INSERT INTO PARTICIPANTS VALUES("+part_no+",\""+name+"\","+sch_no+")"
            fetch_db(query)
            print("참가자 추가 완료!")
        else:
            print("취소되었습니다.")

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

