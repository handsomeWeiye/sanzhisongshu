# encoding=utf-8
import pandas as pd
import time
import jieba
from PIL import Image
import numpy as np
from wordcloud import WordCloud
import codecs
import matplotlib.pyplot as plt

comment_dir  = r"评论.xlsx"
col_index = [2]

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

def getCommentList(comment_dir,col_index):
    #数据函数，把excel列表中的数据转化为了一个列表
    comment_file = pd.read_excel(comment_dir,usecols=col_index)
    comment_list  = comment_file.values
    print("目前的读取到的数据是",comment_file.head())
    log('获取到excel数据，转化为了list')
    log('读取到{}条评论'.format(len(comment_list)))
    print(comment_list)
    return comment_list

def getWordList(comment_list):
    word_list =  []
    stop_words = ['，','。',"!"," ","、","三只","松鼠","因为","所以","就","的",'还是']
    for comment in comment_list:
        split_list =  jieba.lcut(str(comment[0]))
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

    mask = np.array(Image.open("timg4.jpg"))
    with open("word.txt","r",encoding="UTF-8") as f:
        txt=f.read()
    word=WordCloud(background_color="white",\
                    width=2400,\
                   height=3500,
                    collocations=False,
                   font_path='微软雅黑粗体.ttf',
                   mask=mask,
                   ).generate(txt)
    word.to_file('test.png')
    log("词云图片已保存")
    
    plt.imshow(word,interpolation='bilinear')    #使用plt库显示图片
    plt.axis("off")
    plt.show()

   





if __name__ == "__main__":
    comment_list =  getCommentList(comment_dir,col_index)
    getWordList(comment_list)
    getWordCloud()


