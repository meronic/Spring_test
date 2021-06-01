import requests
from bs4 import BeautifulSoup as bs
import sys

size = 400 ## 크롤링 사이즈 !!!!!!!!!!!! 변경해보고 꼭 확인!!! 

headers = {
        'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }




# session add
session = requests.session()

projectList = [] #강의목록 리스트
codeList = []
    
#강의목록까지 로그인 과정
def login() :
    global session
    global projectList #강의목록 리스트
    global codeList #강의고유번호 
    global url
    global responese
    
    projectList = []
    codeList = []
    # 1차 로그인 id,pw 사용
    print("eclass 1차 로그인 중입니다.")
    url = "https://wvu.wku.ac.kr/checklogin_2018.asp"
    

    data = {
        "nextURL" : "https://wvu.wku.ac.kr/clogin.asp",
        "errorURL" : "https://wvu.wku.ac.kr/eclogin.asp",
        "userid" : "hen3633",
        "passwd": "you1288"
    }

    responese = session.post(url, data=data, headers=headers)
    print("응답코드 : ", responese.status_code)
    responese.raise_for_status() # 200이 아닐경우 에러 발동
    responese.encoding = None

    # 2차 로그인 인증
    print("2차 로그인 중입니다.")
    url = "https://wvu.wku.ac.kr/clogin.asp"
    responese = session.get(url)
    responese.encoding = None
    print("응답코드 : ", responese.status_code)


    # 3차 완전 접속
    print("3차 로그인 중입니다.")
    url = "http://wvu.wku.ac.kr/studentlogin/cmdLogin.asp"
    responese = session.get(url)
    responese.encoding = None
    print("응답코드 : ", responese.status_code)


def total_class() :
    global session
    global projectList #강의목록 리스트
    global codeList #강의고유번호 
    global url
    global responese
    # 크롤링시작
    print("\n크롤링 시작\n")
    soup = bs(responese.text, "html.parser")

    # 강의목록 가져오는거 보완 필요 
    projectList = [] #강의목록 리스트
    print("수강강의 목록을 가지고 옵니다.")

    try: # 특별히 지정된게 없어서 직접 카운트하면서 출력함 사이즈 변경해서 출력
        count = 0
        for i in range(size): 
            var = soup.select(".wonkwangGuid2 td")[i].get_text()
            if i%6 == 0 : #계산해보니까 6의 배수였음
            # print(var, "number : ",i)
                count += 1
                projectList.append(var)
    except :
        pass

    print("총 수강 강의 : ", count)

    # 강의코드 가지고 오기
    try:
        for i in range(size):
            project_code = soup.select("input[name=ci]")[i]['value'] #강의코드 가지고 오기
            #print(project_code)
            codeList.append(project_code)
        
    except :
        pass

    for i in range(len(codeList)) : 
        print("[",(i+1),projectList[i],"]", " CODE", codeList[i])
        if i == len(codeList)-1 : 
            print("ex) 1 : 강의번호, CODE : 과목고유코드")
    
    return count        




            
def non_lectures(i) :
    print(projectList[(i-1)],"강의 접속")
    url = "http://wvu.wku.ac.kr/studentlogin/branch.asp"

    data = {
        "mp" : "11",
        "sp" : "1",
        "ci" : codeList[(i-1)], #이게 강의 코드인듯
        "ui" : "20162908"
    }

    responese = session.post(url, data=data, headers=headers)
    print(responese.status_code)
    responese.raise_for_status() # 200이 아닐경우 에러 발동
    responese.encoding = None
    #print(responese.text)

    # 강의목록 가져오기
    print("미수강 강의자료를 가지고 옵니다.")
    url = "http://wvu.wku.ac.kr/lecture/lecture.asp"

    responese = session.post(url,headers=headers)
    print("응답코드 : ", responese.status_code)
    responese.raise_for_status() # 200이 아닐경우 에러 발동
    responese.encoding = None

    print("강의 목록")
    soup = bs(responese.text, "html.parser")
    
    
    try : 
        
        file_Route = open("app/lectures/"+projectList[(i-1)], 'w')
        for i in range(size): 
            var = (soup.select('tr > TD > P > font')[i].get_text()).strip() 
            
            if (len(var) > 0 and var[0] == 'x') :
                
                print( " 미출석 강의 ")
                title = (soup.select('tr > TD > P > font')[i-2].get_text()).strip() 
                attendanceDate = (soup.select('tr > TD > P > font')[i-1].get_text()).strip() 
                attendanceCheck = var
                
                result = title +" " + "["+attendanceDate+"]" + " "+ attendanceCheck + "\n"
                print(result)
                file_Route.write(result)
    
    except : 
        pass
                
                
        file_Route.close()


def print_Project(i) :
    print(projectList[(i-1)],"강의 접속")
    url = "http://wvu.wku.ac.kr/studentlogin/branch.asp"

    data = {
        "mp" : "11",
        "sp" : "1",
        "ci" : codeList[(i-1)], #이게 강의 코드인듯
        "ui" : "20162908"
    }

    responese = session.post(url, data=data, headers=headers)
    print(responese.status_code)
    responese.raise_for_status() # 200이 아닐경우 에러 발동
    responese.encoding = None
    #print(responese.text)

    # 과제목록 가져오기
    print("강의자료를 가지고 옵니다.")
    url = "http://wvu.wku.ac.kr/student/report_bbs/report_list.asp"

    responese = session.post(url,headers=headers)
    print("응답코드 : ", responese.status_code)
    responese.raise_for_status() # 200이 아닐경우 에러 발동
    responese.encoding = None

    print("과제 목록")
    soup = bs(responese.text, "html.parser")
    try:
        count = 1
        f = open("app/reports/"+projectList[(i-1)], 'w')
        for i in range(size): 
            var = soup.select('TD')[i].get_text()
            due_check = soup.select('TD')[i+3].get_text()
            if (i >= 8 and (((i-15) == 0)or((i-15)%8 == 0))) :
                str1 = str(count) + "차 과제 " + " " + str(var) + " " + str(due_check)
               # print(str1)
                count += 1
                f.write(str1+"\n")
                
                
        
    except :
        pass
    
    f.close()
    var = 0
    
    





login() # 로그인
total_count = total_class() # 전체 강의목록 뿌리기


for number in range(total_count) :  
    non_lectures(number) #  과제 뿌리기
    print_Project(number) #  과제 뿌리기

    #######세션 아웃?
    session = requests.session()
    responese = session.get("http://wvu.wku.ac.kr/student/report_bbs/report_list.asp")
    responese.encoding = None
    print("로그아웃", responese.status_code)
    

print(projectList)
print(codeList)
print(total_count)
