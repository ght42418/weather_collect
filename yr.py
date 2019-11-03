import requests
from bs4 import BeautifulSoup
import re
import os
import time
import json

class Yr():
     
    #参数设置默认省份城市，可在参数中进行改变
    def __init__(
        self,province='Heilongjiang',
        city='Mudanjiang_Hailang_International_Airport'
        ):  
        """
        province = 省份,
        city = 城市
        """

        self.url = 'https://www.yr.no/place/China/%s/%s/hour_by_hour_detailed.html?spr=eng'%(province,city)

        #气象要素列表
    
    #访问连接，返回内容
    def __fetch__url(self):
        i = 0
        while i<5:
            try:
                html = requests.get(self.url)
                html.encoding = html.apparent_encoding
                r= html.text  
                print('成功连接')  
                i = 5
            except:
                i+=1
        return r
    
    #运用BeautifulSoup库，进行内容初步筛选,返回初步筛选内容table
    def __get_soup(self,r):
        soup = BeautifulSoup(r,'lxml')
        table = soup.find_all('table',id='detaljert-tabell')
        return table
    
    #获取日期,创建文件夹,返回保存目录文件夹
    def __get_date(self,table):
        caption = table[1].find('caption')
        data = caption.get_text()[19:]
        st = data.split(' ')
        year = st[2]
        month = st[0]
        day = st[1][:-1]
        path = r'D:\weather_map\Yr_forcast\%s\%s\%s'%(year,month,day)
        if not os.path.exists(path):
            os.makedirs(path)
            print('创建成功')
        return path
    
    #通过soup获取一天内24小时气象要素
    def  __get_root_weather(self,table):
        tbody = table[1].find('tbody')
        #tr 为一天23小时的气象要素列表,需要遍历其中内容进行提取保存,时间为 00:00-23:00
        tr_list = tbody.find_all('tr')
        forcast_list = []

        for tr in tr_list:
            forcast = self.__get_childern_weather(tr)
            forcast_list.append(forcast)

        print('资料获取完成')
        return forcast_list
    
    #创建txt文件保存信息
    def __save_weather(self,r,forcast_list,path,table):
        
        caption = table[0].find('caption')
        data = caption.get_text()[19:]
        st = data.split(' ')
        day = st[1][:-1]
        
        time_pattern = '<p>Updated at ([\s\S]*?).</p>'
        time = re.findall(time_pattern,r)[0][:-3]
        #print(time)
        
        #将每一个字典转化为字符串格式保存
        filename = path+'\%s日%s点更新资料.txt'%(day,time)
        print(filename)
        with open(filename,'w+')as file:
            for i in forcast_list:
                file.write('%s\n'%i)
        print('字符资料已保存')
        
        #将字典转换成json格式保存
        jsonname = path+'\%s日%s点更新资料(json格式).txt'%(day,time)
        with open(jsonname,'w+')as file:
            for i in forcast_list:
                js = json.dumps(i,ensure_ascii=False)
                file.write(js)
                file.write('\n')  
        print('json资料已保存')          
    
    #获取一小时的各种气象要素
    def __get_childern_weather(self,tr):
        forcast = {}
        time = tr.find('strong').string    #获取时间
        td = tr.find_all('td')             #气象要素列表
        temperature = td[1].get_text()     #获取温度
        precipitation = td[2].get_text()   #获取降水量
       
       #获取风向风速
        src = td[3]
        #a = 1
        wind_pattren = 'src="/grafikk/sym/vindpiler/32/vindpil.([0-9]*?).([0-9]*?).png"/>'
        wind_direction = re.findall(wind_pattren,str(src))[0][1]    #获取风向
   
        tex = td[3].get_text()
        speed_pattern = '([\d]*?) m/s from'
        wind_speed= re.findall(speed_pattern,tex)[0]       #获取风速       
       
        
        pressure = td[4].get_text()     #获取气压
        humiditiy = td[5].get_text()    #获取湿度
        dew_point = td[6].get_text()    #获取露点温度
        total = td[7].get_text()        #获取总云量
        fog = td[8].get_text()          #获取雾的浓度
        low_clouds = td[9].get_text()   #获取低云量
        medium_clouds = td[10].get_text()  #获取中云量
        high_clouds = td[11].get_text()   #获取高云量
        
        forcast = {
            '时间':time,'温度':temperature,'降水量':precipitation,
            '风向':wind_direction,'风速':wind_speed,
            '气压':pressure,'湿度':humiditiy,'雾浓度':fog,'总云量':total,
            '低云量':low_clouds,'中云量':medium_clouds,'高云量':high_clouds
            }
        
        return forcast


    #入口，总控制程序
    def go(self):
        r = self.__fetch__url() 
        table = self.__get_soup(r)
        path = self.__get_date(table)
        forcast_list = self.__get_root_weather(table)
        self.__save_weather(r,forcast_list,path,table)


if __name__=='__main__':
    yr = Yr()
    yr.go()
    time.sleep(5)

