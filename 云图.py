# coding:utf-8
import numpy as np
import jieba
from wordcloud import WordCloud
from os import path
from PIL import Image
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片

d = path.dirname(__file__)
color_mask = np.array(Image.open(path.join(d, "zhoujielun.png")))

def read_comment():
	comment=open('comments.txt',encoding='utf8')
	try:
		text=comment.read()
		text_cut = jieba.cut(text , cut_all=False)
		return text_cut
	finally:
		comment.close()


def word_cloud(text):
	font = r'C:\Windows\Fonts\simsun.ttc'#设置字体
	wordcloud = WordCloud(background_color="white",font_path=font,max_font_size=500,mask=color_mask).generate(' '.join(text))
	plt.imshow(wordcloud, interpolation='bilinear')
	plt.axis("off")
	plt.show()


if __name__=='__main__':
	text=read_comment()
	word_cloud(text)


