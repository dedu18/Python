from wordcloud import WordCloud


# 读取文本内容
# file = open('e:/wordcloud.txt').read()
chinesefile = open('e:/wordcloud.txt', 'r', encoding='UTF-8').read()
font = r'C:\Windows\Fonts\simfang.ttf'
# 对生成的词云的图片 设置width,height,margin属性 background_color参数为设置背景颜色,默认颜色为黑色 generate 可以对全部文本进行自动分词,但是他对中文支持不好,所以我们使用英文测试
wordcloud = WordCloud( background_color="white", width=1000, height=860, margin=2, font_path=font).generate(chinesefile)

# 你可以通过font_path参数来设置字体集
#wordcloud = WordCloud(font_path = r'D:\Fonts\simkai.ttf').generate(f)

import matplotlib.pyplot as plt
plt.imshow(wordcloud)
plt.axis("off")
plt.show()

# 保存图片
wordcloud.to_file('mywordcloudtest.png')



