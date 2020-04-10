import jieba
import wordcloud
import imageio
mk = imageio.imread("D://51job1/123.png")
exclude={'font','color','style','data','normal','size','quot',
         'spark','redi','Hadoop','family','2em','text','shell',
         'indent','Oracle','Spark','and','the','of','and','in',
         'span','with','to','<span style="font-size:16px;line-height:150%">',
         'as','system','Strong','space','Have','13px','line','year','for','san','or','at',
         'test',''}
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        collocations=False,
                        background_color='white',
                        font_path='msyh.ttc',
                        mask=mk,
                        stopwords=exclude,
                        max_words=100,
                        scale=15)
f = open('D://51job1/信息.txt',encoding='utf-8')
txt = f.read()
txtlist = jieba.cut(txt)
string = " ".join(txtlist)
w.generate(string)
w.to_file('D://51job1/词云.png')
print('生成完毕')