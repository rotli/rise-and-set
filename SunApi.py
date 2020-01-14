import requests
import json
from urllib import parse, request
import urllib
import csv

urlPrefix = "https://api.xmltime.com/astronomy?accesskey=jxKW5TebCJ&expires=2020-01-13T17%3A00%3A58%2B00%3A00&signature=XagszKRLUVja6E7TXTraGljJn18%3D&version=3&out=js&prettyprint=1&object=sun&placeid=sintmaarten%2Fphilipsburg&"
#urlTime = "startdt=2019-11-01&enddt=2020-01-01"
prefix = "startdt="
suffix = "&enddt="
urlSuffix = "&geo=1&isotime=0&lang=en&utctime=1&types=setrise"

years = ["2016","2017","2018","2019"]
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]

# 1. 创建文件对象
file = open('Philipsburg.csv', 'w', encoding='utf-8')
# 2. 基于文件对象构建csv写入对象
csv_writter = csv.writer(file)
# 3. 构建列表头
csv_writter.writerow(['Country','City', 'latitude','Longitude','Date','Type','UTCTime'])

for year in years:
    for month in months:
        urlTime = prefix + year + "-" + month + "-" + "01" + suffix + "2020-01-01"
        url = urlPrefix + urlTime + urlSuffix
        res = str(requests.get(url).text)
        body = res
        # print(body)
        headers = {'content-type' : "application/json"}
        localUrl = "http://127.0.0.1:8080/sun"
        r = requests.post(localUrl, data=body, headers=headers)
        print(r.text)
        list = json.loads(r.text)
        for i in list:
            country = i.get("country")
            city = i.get("city")
            latitude = i.get("latitude")
            longitude = i.get("longitude")
            date = i.get("date")
            type = i.get("type")
            utctime = i.get("utctime")
            csv_writter.writerow([str(country),str(city),str(latitude),str(longitude),str(date),str(type),str(utctime)])