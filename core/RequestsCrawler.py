import requests
from lxml import etree
### BeautifulSoup库和etree和lxml都是比较流行的解析库

urls = "https://item.jd.com/2967929.html"
result = requests.get(urls)
print(type(result))
print(result.status_code)
print(result.encoding)
# print(result.text)
html = etree.parse(result.text)
print(html)
