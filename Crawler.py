import json
import requests
from requests.exceptions import RequestException
import re
import time

def get_page(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_page(html):
   pattern = re.compile('<li>.*?<em class="">(.*?)</em>.*?title.*?>(.*?)</span>.*? <span class="rating_num" property="v:average">(.*?)</span>.*?<span class="inq">(.*?)</span>',re.S)
   items = re.findall(pattern, html)
   for item in items:
        yield {'index': item[0],
            'title': item[1],
            'score': item[2],
            'comment':item[3]
               }


def write_to_file(content):
  with open('douban.txt', 'a', encoding='utf-8') as f:
    f.write(json.dumps(content, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    for i in range(10):
        url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='
        html = get_page(url)
        for item in parse_page(html):
            print(item)
            write_to_file(item)
        time.sleep(1)