
import os
import datetime
import requests
import time

class Weather():
      
 # （1）获取中央气象台天气图数据     
    #获取当天日期及前四天时间
    def __all_time(self):
        today = datetime.date.today()
        n = 1
        t_list = [today]
        while n <5:
            time = today - datetime.timedelta(days=n)
            t_list.append(time)
            n += 1
        return t_list

    # 遍历每一天时间,中央气象台天气图获取总控
    def __for_cnc(self,t_list):
        for time in t_list:
            self.__get_time(time)    #启动时间格式化方法
            self.__make_path()       #启动建立文件夹方法
            self.__fetch_url_cnc()   #启动天气图获取及保存方法
    
    # 时间格式化
    def __get_time(self,time):
        #self.timt = time 
        self.year = time.year
        self.month = time.month
        self.day = time.day
      
        #获取格式化后的时间，用于url获取对应时间信息
        self.time1 = time.strftime('%Y/%m/%d')
        self.time2 = time.strftime('%Y%m%d')
         
    #建立保存文件夹
    def __make_path(self):
        
        self.cnc_day = 'D:\weather_map\cnc\%s\%s\%s'%(self.year,self.month,self.day)
        if not os.path.exists(self.cnc_day):
            os.makedirs(self.cnc_day) 

    #获取内容，保存数据,若是想获取更多高度层可以在 high 列表添加或修改内容
    def __fetch_url_cnc(self):
        high = ['L00','L92','L85','L70','L50']          #高度层
        ti = ['00','03','06','09','12','15','18','21']  #时间点
        patt = ['EGH','ESPCT']                          #气压分析和叠加卫星云图分析
            
        for h in high:
            for t in ti:
                for p in patt:
                    file_name =  str(self.cnc_day+'\%s_%s_%s_%s.jpg'%(h,self.time2,t,p))
                    try:         
                        if not os.path.exists(file_name):
                            print('\n当前数据时间 :%s'%self.time1)
                            url = 'http://image.nmc.cn/product/%s/WESA/medium/SEVP_NMC_WESA_SFER_%s_ACWP_%s_P9_%s%s0000000.jpg'%(self.time1,p,h,self.time2,t)
                            print('正在下载数据%s'%file_name)
                            print('来源: ',url)
                            self.__get_info(file_name,url)                        
                    except:
                        print('数据未更新或页面不存在')

                                              
    #获取信息并保存
    def __get_info(self,file_name,url):
        r= requests.get(url)
        #通过编码判断是否为图片二进制信息
        if r.encoding == None:
            r = r.content
            with open(file_name,'wb') as file:
                file.write(r)
 
# （2）获取的日本传真图数据   
    def __fetch_japan(self):
        patt = ['FXFE','FEAS']
        numb1 = ['502','504','507','5782','5784','577']
        numb2 = ['50','502','504','507','509','512','514','516','519']
       
        urls1 =list(map(lambda x:'http://www.weather-eye.com/chart_other/img/%s%s_12.png'%(patt[0],x),numb1))
        urls2 =list(map(lambda x:'http://www.weather-eye.com/chart_other/img/%s%s_12.png'%(patt[1],x),numb2))
        urls3 =list(map(lambda x:'http://www.weather-eye.com/chart_other/img/%s%s_00.png'%(patt[0],x),numb1))

        urls = urls1 + urls2 + urls3

        for url in urls:
            self.file_name = url[-14:-4]
            html = requests.get(url)
            # 获取最后修改时间，即发布时间
            h = html.headers['Last-Modified']
            print('传真图内容已获取')    
            picture = html.content
            
            year,month,day = self.__japan_time(h)
            self.__makedir(year,month,day,picture)
     
    def __japan_time(self,h):
        #将GMT时间格式化，+8为中国时间
        gmt_format =  '%a, %d %b %Y %H:%M:%S GMT'
        time = datetime.datetime.strptime(h,gmt_format)
        
        year,month,day = str(time.year),str(time.month),str(time.day)
        return year,month,day
    
    #根据时间日期建立数据保存文件夹
    def __makedir(self,year,month,day,picture):
        path = 'D:\weather_map\japan\%s\%s\%s'%(year,month,day)
        if not os.path.exists(path):
            os.makedirs(path)
        file_name = 'D:\weather_map\japan\%s\%s\%s\%s.jpg'%(year,month,day,self.file_name)
        if not os.path.exists(file_name):
            with open(file_name,'wb') as file:
                file.write(picture)
                print('%s 下载完成'%file_name)

    #入口，总控制程序                       
    def go(self):
        t_list = self.__all_time()
        print('中央气象台天气图数据获取开始')
        self.__for_cnc(t_list)
        print('中央气象台天气图数据获取完成\n')
        
        print('日本传真图分析数据获取开始')
        self.__fetch_japan()
        print('日本传真图分析数据获取完成')
        # time.sleep()


if __name__ == '__main__':
    i = 1
    while i<3:
        weather = Weather()
        weather.go()
        i += 1
        time.sleep(1200)

        
