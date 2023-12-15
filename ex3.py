# 网络爬虫（25”）
# 1. 爬取所有豆瓣电影评分Top250的电影的信息(10”)
# a) 正文链接
# b) 英文名（如有），中文名
# c) 等等
# 2. 获取每部影片的简介和影评(5”)
# 3. 加分项(10”)：
# a) 不限于豆瓣的简介，影评
# b) 是否分析了演员与电影类型的关联关系？
# c) 是否分析了演员与演员的关系？
# d) 是否对简介和影评进行词云分析？
# e) 等等
"""
-*- coding: utf-8 -*-
@Time : 2021/11/6 下午 4:59
@Author : SunGuoqi
@Website : https://sunguoqi.com
@Github: https://github.com/sun0225SUN
"""

# 导入一些模块
"""
-*- coding: utf-8 -*-
@Time : 2021/11/7 下午 4:25
@Author : SunGuoqi
@Website : https://sunguoqi.com
@Github: https://github.com/sun0225SUN
"""

import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 数据存放在列表里
datas = []
# 遍历十页数据
for k in range(1):
    print("正在抓取第{}页数据...".format(k + 1))
    url = 'https://movie.douban.com/top250?start=' + str(k * 25)
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
    }
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    # 查找电影链接
    lists = soup.find_all('div', {'class': 'hd'})

    # 遍历每条电影链接
    for item in lists:
        href = item.a['href']
        # 休息一下，防止被封
        time.sleep(0.1)
        # 请求每条电影，获得详细信息
        response = requests.get(href, headers=headers)
        # 把获取好的电影数据打包成BeautifulSoup对象
        movie_soup = BeautifulSoup(response.text, 'lxml')

        # 解析每条电影数据
        # 片名
        name = movie_soup.find('span', {'property': 'v:itemreviewed'}).text.split(' ')[0]
        # 英文名
        eng_name = ' '.join(movie_soup.find('span', {'property': 'v:itemreviewed'}).text.strip().split(' ')[1:])
        plot_summary_tag = movie_soup.find('span', class_='all hidden')
        if plot_summary_tag:
            plot_summary = plot_summary_tag.get_text(strip=True)
        else:
            plot_summary = '无剧情简介'
        # 上映年份
        year = movie_soup.find('span', {'class': 'year'}).text.replace('(', '').replace(')', '')
        # 评分
        score = movie_soup.find('strong', {'property': 'v:average'}).text
        # 评价人数
        votes = movie_soup.find('span', {'property': 'v:votes'}).text
        infos = movie_soup.find('div', {'id': 'info'}).text.split('\n')[1:11]
        # infos返回的是一个列表，我们只需要索引提取就好了
        # 导演
        director = infos[0].split(': ')[1]
        # 编剧
        scriptwriter = infos[1].split(': ')[1]
        # 主演
        actor = infos[2].split(': ')[1]
        # 类型
        filmtype = infos[3].split(': ')[1]
        # 国家/地区
        area = infos[4].split(': ')[1]

        # 数据清洗一下
        if '.' in area:
            area = infos[5].split(': ')[1].split(' / ')[0]
            # 语言
            language = infos[6].split(': ')[1].split(' / ')[0]
        else:
            area = infos[4].split(': ')[1].split(' / ')[0]
            # 语言
            language = infos[5].split(': ')[1].split(' / ')[0]
        if '大陆' in area or '中国香港' in area or '台湾' in area:
            area = '中国'
        if '戛纳' in area:
            area = '法国'
        # 时长
        times0 = movie_soup.find(attrs={'property': 'v:runtime'}).text
        times = re.findall('\d+', times0)[0]

        # 将数据写入列表
        datas.append({
            '片名': name,
            '英文名':eng_name,
            '上映年份': year,
            '评分': score,
            '评价人数': votes,
            '导演': director,
            '编剧': scriptwriter,
            '主演': actor,
            '类型': filmtype,
            '国家/地区': area,
            '语言': language,
            '时长(分钟)': times,
            '剧情简介': plot_summary
        })
        print("电影《{0}》已爬取完成...".format(name))

# 写入到文件
df = pd.DataFrame(datas)
df.to_csv("豆瓣电影top250.csv", index=False, header=True, encoding='utf_8_sig')