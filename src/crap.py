import requests
import pandas as pd
import html
from lxml import etree
import re
import time
import csv
import json
import warnings


requests.adapters.DEFAULT_RETRIES = 5
ID = [86, 87, 88, 90, 91, 92, 95, 115, 101, 108, 116, 104]

def get_html(info_id):
#     url = f'https://www.che168.com/china/a0_0msdgscncgpi1ltocsp{page}exx0/'
#     url = f'https://www.che168.com/china/{brand}/a0_0msdgscncgpi1ltocsp{page}exx0/?pvareaid=102179#currengpostion'
    url = f'https://www.che168.com/CarConfig/CarConfig.html?infoid={info_id}'
    r = requests.get(url, verify=False)
    r = html.unescape(r.text)
    return r
def get_json(sid):
    url_config = f'https://cacheapigo.che168.com/CarProduct/GetParam.ashx?specid={sid}&callback=configTitle'
    r = requests.get(url_config, timeout=2, verify=False)
    r = html.unescape(r.text)
    r = json.loads(r[12:-1])
    return r

# Implement
def run(index) :
    warnings.filterwarnings("ignore")
    print("正在尝试爬去取第" + str(index) + "个页面")
    raw_html = get_html(index)
    t_html = etree.HTML(raw_html)

    brand_name = t_html.xpath('.//div[@class="breadnav content"]/a[@target="_blank"]')
    basic_info = t_html.xpath('.//div[@class="source-info-con"]/p')
    price = t_html.xpath('.//div[@class="source-info-con"]/p[@class="sp-margin"]/span')
    
    if(len(brand_name) == 0) :
#         continue
        return
    print("Find it!")
    specid = t_html.xpath('.//input[@id="CarSpecid"]/@value')
    
    try:
        # 处理直辖市
        if (len(brand_name) == 7) :
            province = brand_name[1].text
            city = brand_name[2].text.replace("二手车","")
            brand = brand_name[3].text.replace("二手","")
            series = brand_name[4].text.replace("二手","")
            car_name = brand_name[5].text
        else:
            province = brand_name[1].text
            city = province
            brand = brand_name[2].text.replace("二手","")
            series = brand_name[3].text.replace("二手","")
            car_name = brand_name[4].text
            
        
        miles = basic_info[0].text.split('／')[0].replace("万公里","")
        date = basic_info[0].text.split('／')[1]
        price = price[0].text.replace("￥","")
        
        car_config = get_json(specid[0])
        result = {}
        
        for item in car_config["result"]["paramtypeitems"][0]['paramitems']:
            if item['id'] in ID:
                a = item['name']
                b = item['value']
                result[a] = b
        
        # 有些车型信息不全直接丢弃
        if len(result) == len(ID):
            print("输出输出")
            with open("whole_car.csv", 'a', encoding = "utf-8") as f:
                csv_write = csv.writer(f, delimiter=',')
                data_row = [brand, series, car_name, province, city, miles, date, price]
                for data in result.values():
                    data_row.append(data)
                csv_write.writerow(data_row)
    except:
        pass
