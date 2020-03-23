import pandas as pd
import time
import requests
# encoding=utf-8
import pandas as pd
import time
import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import codecs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
import os
import math
from pyecharts import Bar


goodsSearchName = '三只松鼠'
excel_dir  = r"总体.xlsx"
col_index = [0,1,2,3,4,5]
product_name = 0

def log(str):
    #日志函数
    time_stamp = time.time()
    local_time = time.localtime(time_stamp)
    str_time = time.strftime('%Y-%m-%d %H:%M:%S',local_time)
    print(str_time)
    with open('log.txt','a+',encoding="UTF-8") as f:
        logInfo = str_time +  "   " + str
        print(logInfo)
        f.write(logInfo +"\n")

def getData(excel_dir,col_index):
    excel_file = pd.read_excel(excel_dir,usecols=col_index)
    print(type(excel_file))
    excel_list = excel_file.values
    log('获取到excel数据列表')
    log('读取到{}条数据'.format(len(excel_list)))
    return excel_list

def getWordList(excel_list):
    word_list =  []
    stop_words = ['，','。',"!"," ","、","三只","松鼠","因为","所以","就","的",'还是','【','】']
    for item in excel_list:
        split_list =  jieba.lcut(str(item[0]))
        print(split_list)
        for word in split_list:
            if(word not in stop_words):
                print(word)
                word_list.append(word)
    with open("word.txt",'w',encoding="UTF-8") as f:
        for item in word_list:
            f.write(str(item)+' ')
    log('得到分词文件')

def getWordCloud():

    mask = np.array(Image.open("timg2.jpg"))
    with open("word.txt","r",encoding="UTF-8") as f:
        txt=f.read()
    word=WordCloud(background_color="white",\
                    width=500,\
                   height=800,
                    collocations=False,
                   font_path='微软雅黑粗体.ttf',
                   mask=mask,
                   ).generate(txt)
    word.to_file('wordCloud.png')
    log("词云图片已保存")
    plt.imshow(word,interpolation='bilinear')    #使用plt库显示图片
    plt.axis("off")
    plt.show()

def merge_image():
    # 获取指定路径下的文件列表
    all_image=os.listdir('photo_image')
    print(all_image)
    # 设定每个头像的大小
    each_size=int(math.sqrt(float(1024*1024)/len(all_image)))
    # 照片墙的行数
    lines=int(1024/each_size)
    print(lines)
    # 创建Image对象，初始化大小
    image=Image.new('RGBA',(1024,1024))
    x,y=0,0
    for i in all_image:
        print(i)
        img = Image.open('photo_image/'+str(i))      
        # 重新设置图像大小
        img = img.resize((each_size, each_size), Image.ANTIALIAS)
        print(image.size)
        # 根据x,y坐标位置拼接图像
        image.paste(img, (x * each_size, y * each_size))
        # 更新下一张图像位置
        x += 1

        # 一行一行拼接
        if x == lines:
            x = 0
            y += 1

    # 保存生成的照片墙
    # RGBA意思是红色，绿色，蓝色，Alpha的色彩空间，Alpha指透明度。而JPG不支持透明度，所以要么丢弃Alpha,要么保存为.png文件
    image.save('photo_wall.png')

excel_list = getData(excel_dir,col_index)
# getWordList(excel_list)
# getWordCloud()
def down_image(excel_list):
    for index,item in enumerate(excel_list):
        print(item[2])
        if(item[2]=='https://assets.alicdn.com/s.gif'):
            continue
        r = requests.get(item[2])
        with open('./photo_image/image{}.png'.format(index),'wb')as f:
            f.write(r.content)
    log('图片下载已经完成')

def getDescribe():
    excel_file = pd.read_excel(excel_dir,usecols=col_index)
    price = excel_file['c-price']
    sale  = excel_file['总销量']
    comment  = excel_file['评价']
    price_describe = price.describe()
    sale_describe = sale.describe()
    comment_describe = comment.describe()

    print(price_describe)
    print(sale_describe)
    print(comment_describe)
    








