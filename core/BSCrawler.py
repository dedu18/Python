import requests
from bs4 import BeautifulSoup

downUrl = 'http://movie.douban.com/top250/' 

def parse(pra):
    soup = BeautifulSoup(pra, 'html.parser')
    ol = soup.find('ol', class_='grid_view')
    name = []  # 名字
    nameEn = []  # 英文名字
    nameOther = []  # 其他名字
    score = []  # 评分
    scorepersons = []  # 评分人数
    reviewList = []  # 短评
    categoryList = [] # 类别
    image = [] # 图片
    # Unicode编码与ASCII编码的不兼容
    for i in ol.find_all('li'):
        # 获取div标签class=pic代码
        cover = i.find('div', attrs={'class': 'pic'}).find('img').get('src')
        image.append(cover)

        # 获取div标签class=hd代码
        detail = i.find('div', attrs={'class': 'hd'})
        movieNameList = detail.find_all('span')
        movieName = movieNameList[0].get_text()# 电影名字
        movieNameEn = ''
        movieNameOther = ''
        if len(movieNameList) > 1:
            movieNameEn = movieNameList[1].get_text()  # 电影英文名字
        if len(movieNameList) > 2:
            movieNameOther = movieNameList[2].get_text()  # 电影其他名字

        # 获取div标签class=star代码
        scoreList = i.find('div', attrs={'class': 'star'}).find_all('span')
        scorenum = scoreList[1].get_text() #评分
        # 评价人数
        scorepersonnum = scoreList[3].get_text()
        # 短评
        review = i.find('span', attrs={'class': 'inq'})
        # 类别
        category = i.find('div', attrs={'class' : 'bd'}).find('p').get_text()
        # category = str(category[category.rfind('/')+2 : len(str(category))].replace(' ', '').strip())
        if review:  # 判断是否有短评
            reviewList.append(review.get_text())
        else:
            reviewList.append('无')

        name.append(movieName)
        nameEn.append(movieNameEn)
        nameOther.append(movieNameOther)
        score.append(scorenum)
        scorepersons.append(scorepersonnum)
        categoryList.append(category)

    page = soup.find('span', attrs={'class': 'next'}).find('a')  # 获取下一页
    result = [name, nameEn, nameOther, score, scorepersons, reviewList, categoryList, image]
    if page:
        result.append(downUrl + page['href'])
    else:
        result.append(None)
    return result

if __name__ == '__main__':

    url = downUrl
    name = []
    nameEn = []
    nameOther = []
    score = []
    score_persons = []
    review = []
    category = []
    image = []
    i = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }

    while i < 5:
        if (url == None):
            break
        html = requests.get(url, headers=headers).content
        result = parse(html)
        name = name + result[0]
        nameEn = nameEn + result[1]
        nameOther = nameOther + result[2]
        score = score + result[3]
        score_persons = score_persons + result[4]
        review = review + result[5]
        category = category + result[6]
        image = result[7]
        url = result[8]
        i = i + 1

    for (i, e, o, s, sp, r, c, m) in zip(name, nameEn, nameOther, score, score_persons, review, category, image):
        print(i, " ", e, " ", o, " ", s, " ", sp, " ", r, " ", c, " ", m)
