import requests
from bs4 import BeautifulSoup
import pymysql
import pika
import json

# 数据格式
# <ol class="grid_view">
#   <li>
#     <div class="item">
#       <div class="pic">
#         <em class="">1</em>
#         <a href="https://movie.douban.com/subject/1292052/">
#           <img alt="肖申克的救赎" class="" src="https://img3.doubanio.com/view/photo/s_ratio_poster/public/p480747492.jpg" width="100" /></a>
#       </div>
#       <div class="info">
#         <div class="hd">
#           <a class="" href="https://movie.douban.com/subject/1292052/">
#             <span class="title">肖申克的救赎</span>
#             <span class="title"> / The Shawshank Redemption</span>
#             <span class="other"> / 月黑高飞(港) / 刺激1995(台)</span></a>
#           <span class="playable">[可播放]</span></div>
#         <div class="bd">
#           <p class="">导演: 弗兰克·德拉邦特 Frank Darabont   主演: 蒂姆·罗宾斯 Tim Robbins /...
#             <br/>1994 / 美国 / 犯罪 剧情</p>
#           <div class="star">
#             <span class="rating5-t"></span>
#             <span class="rating_num" property="v:average">9.7</span>
#             <span content="10.0" property="v:best"></span>
#             <span>1946722人评价</span></div>
#           <p class="quote">
#             <span class="inq">希望让人自由。</span></p>
#         </div>
#       </div>
#     </div>
#   </li>
# </ol>

downUrl = 'http://movie.douban.com/top250/'


def parse(pra):
    soup = BeautifulSoup(pra, 'html.parser')
    ol = soup.find('ol', class_='grid_view')

    result_name = []  # 名字
    result_name_en = []  # 英文名字
    result_name_other = []  # 其他名字
    result_score = []  # 评分
    result_score_number = []  # 评分人数
    result_review = []  # 短评
    result_category = []  # 类别
    result_cover = []  # 封面图片

    # 解析数据
    for li in ol.find_all('li'):
        # 获取封面图（获取div标签class=pic代码）
        img = li.find('div', attrs={'class': 'pic'}).find('img').get('src')
        # 获取电影名称/英文名称/其他名称（获取div标签class=hd代码）
        hd = li.find('div', attrs={'class': 'hd'})
        hd_spans = hd.find_all('span')
        movie_name = hd_spans[0].get_text()  # 电影名字
        movie_name_en = ''
        movie_name_other = ''
        if len(hd_spans) > 2:
            movie_name_en = hd_spans[1].get_text()  # 电影英文名字
            movie_name_other = hd_spans[2].get_text()  # 电影其他名字
        elif len(hd_spans) > 1:
            movie_name_en = hd_spans[1].get_text()  # 电影英文名字
            movie_name_other = '无'
        else:
            movie_name_en = '无'
            movie_name_other = '无'
        # 获取评分评价（获取div标签class=star代码）
        div_star_spans = li.find('div', attrs={'class': 'star'}).find_all('span')
        movie_score = div_star_spans[1].get_text()  # 评分
        movie_score_number = div_star_spans[3].get_text()  # 评价人数
        movie_review = li.find('span', attrs={'class': 'inq'})  # 短评
        # 获取类别
        movie_category = li.find('div', attrs={'class': 'bd'}).find('p').get_text()
        # 组装结果
        result_name.append(movie_name)
        result_name_en.append(movie_name_en)
        result_name_other.append(movie_name_other)
        result_score.append(movie_score)
        result_score_number.append(movie_score_number)
        if movie_review is not None:  # 判断是否有短评
            result_review.append(movie_review.get_text())
        else:
            result_review.append('无')
        result_category.append(movie_category)
        result_cover.append(img)

    # 获取下一页
    page = soup.find('span', attrs={'class': 'next'}).find('a')
    result = [result_name, result_name_en, result_name_other, result_score, result_score_number, result_review, result_category, result_cover]
    if page:
        result.append(downUrl + page['href'])
    else:
        result.append(None)
    return result


def format_comma(string):
    return string.strip().replace("\'", "\\'")


if __name__ == '__main__':
    url = downUrl
    name = []
    name_en = []
    name_other = []
    score = []
    score_number = []
    review = []
    category = []
    image = []
    i = 1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    while i < 2:
        if url is None:
            break
        html = requests.get(url, headers=headers).content
        parse_result = parse(html)
        name = name + parse_result[0]
        name_en = name_en + parse_result[1]
        name_other = name_other + parse_result[2]
        score = score + parse_result[3]
        score_number = score_number + parse_result[4]
        review = review + parse_result[5]
        category = category + parse_result[6]
        image = image + parse_result[7]
        url = parse_result[8]
        i = i + 1

    # 操作MQ存储
    credentials = pika.PlainCredentials('guest', 'guest')  # mq用户名和密码
    # 虚拟队列需要指定参数 virtual_host，如果是默认的可以不填。
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.1.8', port=5672, virtual_host='/', credentials=credentials))
    channel = connection.channel()
    # 声明exchange，由exchange指定消息在哪个队列传递，如不存在，则创建。durable = True 代表exchange持久化存储，False 非持久化存储
    channel.exchange_declare(exchange='ex_film', durable=True, exchange_type='direct')
    for index in range(len(name)):
        data = category[index].strip().replace(' ', '').replace("\n", "").replace("\r", "").replace("\'", "\\'")
        message = json.dumps({
            'cntitle': format_comma(name[index]),
            'entitle': format_comma(name_en[index]),
            'othertitle': format_comma(name_other[index]),
            'genres_id': data,
            'image': format_comma(image[index]),
            'rating': format_comma(score[index]),
            'quote': format_comma(review[index])
        }, ensure_ascii=False)
        channel.basic_publish(exchange='ex_film', routing_key='routingkey_film', body=message)
    connection.close()

    # # 操作数据库存储
    # config = {
    #     "host": "127.0.0.1",
    #     "user": "root",
    #     "password": "Aa123456",
    #     "database": "db_film"
    # }
    # db = pymysql.connect(**config)
    # cursor = db.cursor()
    # sqltemplate = "INSERT INTO `db_film`.`t_film` (`cntitle`, `entitle`, `othertitle`, `genres_id`, `image`, `rating`, `quote`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s');"
    # for index in range(len(name)):
    #     data = category[index].strip().replace(' ', '').replace("\n", "").replace("\r", "").replace("\'", "\\'")
    #     if "..." in data:
    #         pass
    #     sql = sqltemplate % (format_comma(name[index]),
    #                          format_comma(name_en[index]),
    #                          format_comma(name_other[index]),
    #                          data,
    #                          format_comma(image[index]),
    #                          format_comma(score[index]),
    #                          format_comma(review[index]))
    #     print(sql)
    #     cursor.execute(sql)
    #     db.commit()
    #
    # cursor.close()
    # db.close()
