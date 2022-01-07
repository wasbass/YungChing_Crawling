import requests                 #這個套件比較便捷
import urllib.request as req    #這個套件比較完整
from bs4 import BeautifulSoup
import csv
import time

url_init = "http://rent.yungching.com.tw"
host_key = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"
header = {"User-Agent":host_key}

posturl = "http://rent.yungching.com.tw/Ashx/ShowList.ashx?VID=1250"

sub = []
###reqeusts法

postdata = {"County"        :"台北市",
            "District"      :"",
            "Rooms"         :"",
            "PriceMin"      :"",
            "PriceMax"      :"",
            "AreaNeeds"     :"",
            "Purpose"       :"",
            "CaseType"      :"",
            "BuildAge"      :"",
            "CaseFloor"     :"",
            "DirFace"       :"",
            "ParkingSpace"  :"",
            "KeyWord"       :"",
            "Group"         :"",
            "ListMode"      :"PhotosAndWords",
            "PageCount"     :"40",
            "CurrentPage"   :"1",
            "CurrentRange"  :"1",
            "Sequence"      :"",
            "SearchMode"    :"1",
            "BuildNo"       :"",
            "BuildingID"    :"",
            "RoadName"      :"",
            "MainShopID"    :""}        #條件可自行更改

def into_url_CSV( L:list):
    with open("YC_url.csv", "a", newline='', encoding='utf-8-sig') as file:   #加寫
        writer = csv.writer(file ,delimiter=',')
        writer.writerow(L)
        # file.close()

def into_CSV( L:list):
    with open("YC.csv", "a", newline='', encoding='utf-8-sig') as file:       #加寫
        writer = csv.writer(file ,delimiter=',')
        writer.writerow(L)
        #file.close()   with open會自動關閉

def YCcrawl(endpage):
    global postdata
    for i in range(1,endpage+1):
        print("-" , end = "")
        if i%10==0 :
            print("")
        postdata["CurrentPage"] = i
        res = requests.post( posturl , headers = header , data = postdata)
        res.encoding = "utf-8"

        soup = BeautifulSoup(res.text, "html.parser")

        a_l  = soup.find_all("a")
        sub  = []

        for i in range(len(a_l)):
            try:
                suburl = a_l[i].get("href")
                if suburl != None:
                    #print(suburl)
                    sub.append(suburl)
            except:
                continue
        a_l.clear
        sub.clear

        into_url_CSV(sub)

def housecrawl(url):
    res = requests.get( url , headers = header)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text, "html.parser")

    title    = soup.find("p" , class_ = "font_b").text
    rent     = soup.find("b" , class_ = "red").text
    areatext = soup.find_all("td" ,class_ = "width150 center")[3].text
    area = areatext.split(" ")[0]

    into_CSV([title,rent,area])

with open("YC_url.csv", "w", newline='', encoding='utf-8-sig') as file:   #創建
    file.close()

with open("YC.csv", "w", newline='', encoding='utf-8-sig') as file:       #創建
    file.close()


endpage = 5
YCcrawl(endpage)
print("")

for i in range(1,endpage+1):
    with open("YC_url.csv", "r", newline='', encoding='utf-8-sig') as file:   #讀取
        filerows = csv.reader(file)
        j = 1
        for row in filerows :
            if i == j:
                u_l = row
                break
            else:
                j += 1
        file.close()
    l = len(u_l)
    for a in range(l):
        print("*",end = "")
        url = url_init + u_l[a]
        housecrawl(url)
        time.sleep(2)
    print("")


