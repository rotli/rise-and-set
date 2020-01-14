import requests
from lxml import etree
from datetime import datetime, timedelta
import csv

root = "https://www.timeanddate.com/sun/"
citys = ["china/shenzhen","usa/los-angeles", "australia/sydney", "russia/moscow", "uk/london"]
years = ["2016","2017","2018","2019"]
months = ["1","2","3","4","5","6","7","8","9","10","11","12"]
timeZone = {"china/shenzhen" : 8, "usa/los-angeles" : -8, "ustralia/sydney" : 10, "russia/moscow" : 3, "uk/london" : 0}

# 1. 创建文件对象
file = open('Oslo.csv', 'w', encoding='utf-8')
# 2. 基于文件对象构建csv写入对象
csv_writter = csv.writer(file)
# 3. 构建列表头
csv_writter.writerow(['City','Date', 'SunRise/SunSet','LocalTime','UTCTime'])



for city in citys:
    print("当前城市为：" + city)
    for year in years:
        print("当前年份为:" + year)
        for month in months:
            print("当前月份为：" + month)
            url = root + city + "?month=" + month + "&year=" + year
            print(url)
            html = requests.get(url)
            etree_html = etree.HTML(html.text)
            xpathRoot = '//*[@id="as-monthsun"]/tbody/tr/'
            tds = ["td[1]/text()", "td[2]/text()"]
            for td in tds:
                xpath = xpathRoot + td
                content = etree_html.xpath(xpath)
                riseDay = 1
                setDay = 1
                for each in content:
                    replace = each.replace('\n', '').replace(" ", "")
                    if replace == '\n' or replace == '':
                        continue
                    else:
                        if td == "td[1]/text()" and " " != each:
                            localTimeStr = year + "-" + month + "-" + str(riseDay)
                            localTime = datetime.strptime(localTimeStr + " " + replace + ":00", '%Y-%m-%d %H:%M:%S')
                            utcTime = localTime - timedelta(hours=timeZone.get(city))
                            #print(city + " " + localTimeStr + " 【日出】" + "当地时间：" + replace + " UTC时间：" + str(utcTime))
                            # 4. 写入csv
                            csv_writter.writerow([city,localTimeStr,'SunRise',replace,str(utcTime)])
                            riseDay += 1
                        elif td == "td[2]/text()" and " " != each:
                            localTimeStr = year + "-" + month + "-" + str(setDay)
                            localTime = datetime.strptime(localTimeStr + " " + replace + ":00", '%Y-%m-%d %H:%M:%S')
                            utcTime = localTime - timedelta(hours=timeZone.get(city))
                            #print(city + " " + localTimeStr + " 【日落】"  + "当地时间：" + replace + " UTC时间：" + str(utcTime))
                            csv_writter.writerow([city, localTimeStr, 'SunSet', replace, str(utcTime)])
                            setDay += 1
# 5.关闭文件
file.close()