import re
import requests
import xlwt
import os
import time
import threading
import random
from fake_useragent import UserAgent


class job51():
    def getdata(self,url):
        ua = UserAgent()
        headers = {'user_agrent': ua.random}
        # time.sleep(random.random() * 3)   #增加成功率，但会影响速度
        try:
            r = requests.get(url,timeout=30,headers=headers)
            r.encoding = 'utf-8'
            r.raise_for_status()
        except:
            r = requests.get(url, timeout=30, headers=headers)
        return r.text
    def run(self,x):
        print(time.ctime()+'开始下载')
        url1 = 'https://search.bilibili.com/all?keyword='+x
        # 写入表格
        Excel = xlwt.Workbook(encoding='utf-8',style_compression=0)
        table = Excel.add_sheet('bilibili',cell_overwrite_ok=True)
        table.write(0,0,'搜索词')
        table.write(0,1,'排名')
        table.write(0,2,'id')
        table.write(0,3,'up主')
        table.write(0,4,'关注数')
        table.write(0,5,'视频链接')
        table.write(0,6,'视频名称')
        table.write(0,7,'发布时间')
        table.write(0,8,'播放量')
        table.write(0,9,'弹幕量')
        table.write(0,10,'点赞量')
        table.write(0,11,'投币量')
        table.write(0,12,'收藏量')
        table.write(0,13,'转发量')
        table.write(0,14,'分区1')
        table.write(0,15,'分区2')
        table.write(0,16,'爬取时间')
        # 获取数据
        data1 = self.getdata(url1)
        # 提取信息
        age = self.re_list_re(data1,'</button></li><strong>...</strong><li class="page-item last"><button class="pagination-btn">(.*?)</button>')[0]
        print(x+'共有' + age + '页')
        age = int(age)

        n=1
        for h in range(1,age+1):
            p = str(h)
            url = 'https://search.bilibili.com/all?keyword='+x+'&page='+p
            data = self.getdata(url)
            url_video =self.re_list(data,r'<li class="video-item matrix"><a href="(.*?)"')
            print('开始下载'+x+'第'+p+'页')
            for a in url_video:
                a='http:'+a
                video_data = self.getdata(a)
                search_terms = x    #搜索词
                search_rank = n     #排名
                up_username = self.re_list(video_data, 'itemprop="author" name="author" content="(.*?)"><meta data-vue-meta')[0]    #用户名
                up_id = self.re_list(video_data,'<a href="//space.bilibili.com/(.*?)" target="_blank"')[0]  #id
                # up_follow_num = self.re_list(video_data,'attention":(.*?),"')[0]    #关注数
                up_follow_num = self.re_list(video_data,'"fans":(.*?),"')[0] #粉丝数
                video_url = self.re_list(video_data,'itemprop="url" content="(.*?)/">')[0]  #视频链接
                video_name = self.re_list(video_data,'"title":"(.*?)",')[0]     #视频名称
                video_published_at = self.re_list(video_data,'itemprop="uploadDate" content="(.*?)">')[0]   #发布时间
                video_playback_num = self.re_list(video_data,'"viewseo":(.*?)}')[0] #播放量
                av = video_url.split('v')[-1:][0]
                js_url ="https://api.bilibili.com/x/web-interface/view?aid="+av
                js_data =self.getdata(js_url)
                video_barrage_num=self.re_list(js_data,'"danmaku":(.*?),')[0]   #弹幕
                video_like_num = self.re_list(js_data,'"like":(.*?),')[0]   #点赞量
                video_coin_num = self.re_list(js_data,'"coin":(.*?),')[0]   #投币量
                video_favorite_num = self.re_list(js_data, '"favorite":(.*?),')[0]  #收藏量
                video_share_num = self.re_list(js_data, '"share":(.*?),')[0]    #转发量
                category_1 =self.re_list(video_data,'<a target="_blank" href="//.*?">(.*?)</a><i class="van-icon-general_enter_s">')[0]    #分区1
                category_2 =self.re_list(js_data,'"tname":"(.*?)",')[0]    #分区2
                created_at = time.ctime()
                table.write(n, 0, search_terms)
                table.write(n, 1, search_rank)
                table.write(n, 2, up_id)
                table.write(n, 3, up_username)
                table.write(n, 4, up_follow_num)
                table.write(n, 5, video_url)
                table.write(n, 6, video_name)
                table.write(n, 7, video_published_at)
                table.write(n, 8, video_playback_num)
                table.write(n, 9, video_barrage_num)
                table.write(n, 10, video_like_num)
                table.write(n, 11, video_coin_num)
                table.write(n, 12, video_favorite_num)
                table.write(n, 13, video_share_num)
                table.write(n, 14, category_1)
                table.write(n, 15, category_2)
                table.write(n, 16, created_at)
                n = n + 1
                Excel.save(r'D://哔哩哔哩/'+x+'.xls')


    def re_list(self,data,a):
        r = re.findall(a,data,re.S)
        return r
    def re_list_re(self,data,a):
        r = re.findall(a,data,re.S)
        n=0
        for a in r:
            r[n] = a.strip().replace("\n", "")
            n=n+1
        return r



if __name__ == '__main__':

    zhiye = ['简历','简历模板','面试','实习','找工作','笔试','职场']
    abc = job51()
    if not os.path.exists('D://哔哩哔哩'):
        os.mkdir('D://哔哩哔哩')
    t1 = threading.Thread(target=abc.run, args=(zhiye[0],))
    t2 = threading.Thread(target=abc.run, args=(zhiye[1],))
    t3 = threading.Thread(target=abc.run, args=(zhiye[2],))
    t4 = threading.Thread(target=abc.run, args=(zhiye[3],))
    t5 = threading.Thread(target=abc.run, args=(zhiye[4],))
    t6 = threading.Thread(target=abc.run, args=(zhiye[5],))
    t7 = threading.Thread(target=abc.run, args=(zhiye[6],))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    t5.join()
    t6.join()
    t7.join()
    print("导入完毕")