# -*- coding: utf-8 -*-
import sys
import importlib

import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import urllib.request
from urllib import request
import json
import re
import ssl
from bs4 import BeautifulSoup



'''
def getHtml(url):
    ssl._create_default_https_context = ssl._create_unverified_context
    page = urllib.request.urlopen(url)  ##打开页面
    html = page.read()  ##获取目标页面的源码
    return html

html = getHtml('https://librivox.org/aquis-submersus-by-theodor-storm/')
#print(html)
'''

def write_txt(content, filename):
    """
    将响应返回的信息，写入文件保存
    :param response:服务器返回的响应信息
    :param filename:保存的文件名
    :return:
    """
    with open(filename, 'w') as f:
        f.writelines(content)
        f.close()



# 全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context

def get_headers():
    """
    返回请求头信息
    :return:
    """
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/65.0.3325.181 Safari/537.36"
    }
    return headers


def get_url_content(url):
    """
    获取指定url的请求内容
    :param url:
    :return:
    """
    content = ''
    headers = get_headers()
    res = request.Request(url, headers=headers)
    try:
        resp = request.urlopen(res, timeout=10)
        content = resp.read()
    except Exception as e:
        print('exception: %s' % e)
    return content

'''
# Test
url = 'https://librivox.org/aquis-submersus-by-theodor-storm/'
content = get_url_content(url)
'''


def get_transcripts_original_links(content):
    """
    :return: original web page links of transcripts
    """
    soup = BeautifulSoup(content, 'lxml')
    # 下面的方法找出了所有class为hello的span标签
    # 并将所有的结果都放入一个list返回

    page_sidebar = soup.find_all('div', {'class': 'book-page-sidebar'})
    #print(page_sidebar)

    download_links = soup.find_all('p')
    #print(download_links)

    links = {}
    for i in download_links:
        try:
            # 提取新闻标题
            describe = i.find('a').get_text().strip()
            #print('describe',describe)

            # 提取新闻来源
            link = i.find('a').get('href').strip()
            #print(link)

            # 存储爬取结果
            links[describe] = link
        except AttributeError as e:
            pass

    return links['Online text']

'''
# Test
url = 'https://librivox.org/das-nibelungenlied-by-karl-joseph-simrock/'
content = get_url_content(url)
links = get_transcripts_original_links(content)
print('links',links)
'''



def get_transcripts_original_html(url):
    """
    :return: original web page links of transcripts
    """
    #url = get_transcripts_original_links(content)
    original_tanscripts_html = get_url_content(url)

    return original_tanscripts_html



# Only for 'Spiegel Online' website
def crawl_transcripts_spiegel(transcripts_html_content):
    """

    :return: original web page links of transcripts
    """
    #transcripts_html_content = get_url_content(url_transcripts)

    soup = BeautifulSoup(transcripts_html_content, 'html.parser')

    paragraph = []

    try:
        if soup.find('div', {'id': 'gutenb'}).find('h3'):
            title_h3 = soup.find('div', {'id': 'gutenb'}).find('h3')
            paragraph.append(title_h3.get_text().strip('\r\n\t'))
            paragraph.append('.')
    except AttributeError as e:
        pass

    try:
        if soup.find('div', {'id': 'gutenb'}).find_all('h3'):
            title_h3 = soup.find('div', {'id': 'gutenb'}).find_all('h3')
            paragraph.append(title_h3.get_text().strip('\r\n\t'))
            paragraph.append('.')
    except AttributeError as e:
        pass


    try:
        if soup.find('div', {'id': 'gutenb'}).find('h2'):
            title_h2 = soup.find('div', {'id': 'gutenb'}).find('h2')
            paragraph.append(title_h2.get_text().strip('\r\n\t'))
            paragraph.append('.')
    except AttributeError as e:
        pass

    try:
        if soup.find('div', {'id': 'gutenb'}).find_all('h2'):
            title_h2 = soup.find('div', {'id': 'gutenb'}).find_all('h2')
            paragraph.append(title_h2.get_text().strip('\r\n\t'))
            paragraph.append('.')
    except AttributeError as e:
        pass


    try:
        if soup.find('div', {'id': 'gutenb'}).find('h4'):
            title_h4 = soup.find('div', {'id': 'gutenb'}).find('h4')
            paragraph.append(title_h4.get_text().strip('\r\n\t'))
            paragraph.append('.')
    except AttributeError as e:
        pass

    try:
        if soup.find('div', {'id': 'gutenb'}).find_all('h4'):
            title_h4 = soup.find('div', {'id': 'gutenb'}).find_all('h4')
            paragraph.append(title_h4.get_text().strip('\r\n\t'))
            paragraph.append('.')
    except AttributeError as e:
        pass

    try:
        if soup.find('div', {'id': 'gutenb'}).find('h5'):
            title_h5 = soup.find('div', {'id': 'gutenb'}).find('h5')
            paragraph.append(title_h5.get_text().strip('\r\n\t'))
            paragraph.append('.')
    except AttributeError as e:
        pass

    try:
        if soup.find('div', {'id': 'gutenb'}).find_all('h5'):
            title_h5 = soup.find('div', {'id': 'gutenb'}).find_all('h5')
            paragraph.append(title_h5.get_text().strip('\r\n\t'))
            paragraph.append('.')
    except AttributeError as e:
        pass


    try:
        if soup.find('div', {'id': 'gutenb'}).find_all('td'):
            text_td = soup.find('div', {'id': 'gutenb'}).find_all('td')
            for i in text_td:
               paragraph.append(i.get_text().strip('\r\n\t'.strip(' ').strip('.')))
               paragraph.append('.')
    except AttributeError as e:
        pass


    if soup.find('div', {'id': 'gutenb'}).find_all('p'):
        text_p = soup.find('div', {'id': 'gutenb'}).find_all('p')
        for i in text_p:
            paragraph.append(i.get_text().strip('\r\n\t ').strip('\r\n\t').strip(' ').strip('.'))
            paragraph.append('.')

    file_name = soup.find('b').get_text()
    print(file_name)
    filename = str(file_name).replace('.','').replace('/','_').replace('?','').replace('？','') + '.txt'


    write_txt(paragraph, filename)

    return paragraph



'''
# Test
url_transcripts = 'http://gutenberg.spiegel.de/buch/ein-alter-afrikaner-856/1'
crawl_transcripts_spiegel(url_transcripts)
'''



# Only for 'Zeno.org' website
def crawl_transcripts_zeno_second_links(url_transcripts):
    """
    :return: original web page links of transcripts
    """
    transcripts_html_content = get_url_content(url_transcripts)
    #print(transcripts_html_content )


    soup = BeautifulSoup(transcripts_html_content, 'lxml') #'html.parser'
    #print(soup)

    parts = soup.find('div', {'class': 'zenoTRNavBottom'}).find('ul')
    #print(parts)
    
    chapter = parts.find_all('li')

    web_links = 'http://www.zeno.org/'

    links = {}

    '''
    for i in chapter:
        #print(i)
        describe = i.find('a').get_text().strip()
        #print('describe', describe)

        link = i.find('a').get('href').strip()
        link = web_links + link
        #print('link', link)

        links[describe] = link

    return links
    '''

    for i in chapter:
        # print(i)
        describe = i.find('a').get('href').strip()
        describe = describe[70:]
        #print('describe', describe)

        link = i.find('a').get('href').strip()
        link = web_links + link
        #print('link', link)

        links[describe] = link

    return links



'''
# Test
url_transcripts = 'http://www.zeno.org/Literatur/M/Goethe,+Johann+Wolfgang/Autobiographisches/Aus+meinem+Leben.+Dichtung+und+Wahrheit'
zeno_transcripts_links = crawl_transcripts_zeno_second_links(url_transcripts)
'''


def crawl_transcripts_zeno_text(zeno_transcripts_links):

    for i in zeno_transcripts_links:

        url_transcripts = zeno_transcripts_links[i]
        #print('url_transcripts',url_transcripts  )

        transcripts_html_content = get_url_content(url_transcripts)

        soup = BeautifulSoup(transcripts_html_content, 'html.parser')

        paragraph = []

        try:
            if soup.find('div', {'class': 'zenoCOMain'}).find('h5'):
                title = soup.find('div', {'class': 'zenoCOMain'}).find_all('h5')
                title = str(title)
                print('title', title)
                title=title.replace('<h5>',''); title=title.replace('</h5>','');
                title=title.replace(',',''); title=title.replace('[','');title=title.replace(']','');
                paragraph.append(title) #paragraph.append('.');
                print('paragraph', paragraph)
        except AttributeError as e:
            pass

        try:
            if soup.find('div', {'class': 'zenoCOMain'}).find('h4'):
                title = soup.find('div', {'class': 'zenoCOMain'}).find('h4')
                title = str(title)
                title=title.replace('<h4>',''); title=title.replace('</h4>','');
                paragraph.append(title);paragraph.append('.');
        except AttributeError as e:
            pass

        try:
            if soup.find('div', {'class': 'zenoCOMain'}).find('h3'):
                title = soup.find('div', {'class': 'zenoCOMain'}).find('h3')
                title = str(title)
                title=title.replace('<h3>',''); title=title.replace('</h3>','');
                paragraph.append(title);paragraph.append('.');
        except AttributeError as e:
            pass

        try:
            if soup.find('div', {'class': 'zenoCOMain'}).find('h2'):
                title = soup.find('div', {'class': 'zenoCOMain'}).find('h2')
                title = str(title)
                title=title.replace('<h2>',''); title=title.replace('</h2>','');
                paragraph.append(title);paragraph.append('.');
        except AttributeError as e:
            pass

        try:
            if soup.find('div', {'class': 'zenoCOMain'}).find_all('p'):
                text = soup.find('div', {'class': 'zenoCOMain'}).find_all('p')
                for j in text:
                    paragraph.append(str(j.get_text()).strip('\r\n\t '))
                    paragraph.append('.')
        except AttributeError as e:
            pass


        try:
            if soup.find('div', {'class': 'zenoCOMain'}).find('p'):
                text = soup.find('div', {'class': 'zenoCOMain'}).find('p')
                for j in text:
                    paragraph.append(str(j.get_text()).strip('\r\n\t '))
                    paragraph.append('.')
        except AttributeError as e:
            pass


        try:
            if soup.find_all('p', {'class': 'zenoPLm4n0'}):
                text = soup.find_all('p', {'class': 'zenoPLm4n0'})
                for j in text:
                    paragraph.append(str(j.get_text()).strip('\r\n\t '))
                    paragraph.append('.')
        except AttributeError as e:
            pass

        #filename = str(i.replace('.','').replace('/','_').replace('?','').replace('？',''))  + '.txt'
        filename = str(i).replace('.','').replace('+','').replace('/',' ') + '.txt'
        print('filename:',filename)

        write_txt(paragraph, filename)



'''
# Test
transcripts_directory = '/Users/xinsun/PycharmProjects/PycharmEnv/venv/transcripts/JohannWolfgangGoethe_AusmeinemLeben_DichtungundWahrheit/'
crawl_transcripts_zeno_text(zeno_transcripts_links)
'''



# Only for Etext download
def crawl_transcripts_Etext_second_links(url_librivox):
    """
    :return:
    """
    content = get_url_content(url_librivox)
    soup = BeautifulSoup(content, 'html.parser')

    all_links = soup.find('table', {'class': 'chapter-download'}).find_all('td')

    transcripts_links = {}
    chapter_name = []
    links = []

    for j in all_links:
        try:
            # get the name of each chapter or book
            name = j.find('a', {'class': 'chapter-name'}).get_text().strip()
            # print(name)
            chapter_name.append(name.replace("'", ''))

        except AttributeError as e:
            continue

    for i in all_links:
        try:
            describe = i.find('a').get_text().strip()
            #print(describe)

            link = i.find('a').get('href').strip()
            #print(link)

            if describe == 'Etext':
                links.append(link)

            else:
                continue

        except AttributeError as e:
            continue

    #print('chapter_name:', len(chapter_name))
    #print('links:', len(links))


    for i,j in enumerate(chapter_name):

        transcripts_links[j] = links[i]

    print(transcripts_links)

    return transcripts_links


'''
# Test
url_librivox = 'https://librivox.org/adventskalender-2017-by-various/'
Etext_links = crawl_transcripts_Etext_second_links(url_librivox)
'''


if __name__ == '__main__':

    # Class 1:
    url = 'https://librivox.org/erdgeist-by-frank-wedekind/'
    librivox_html_content = get_url_content(url)

    # Spiegel网站的译文可能会有很多Kapital, 所以此处可以加循环，得到所有Kapital的网页链接，此
    online_text_link = get_transcripts_original_links(librivox_html_content)
    print('online_text_link', online_text_link )
    #online_text_link = 'http://www.zeno.org/Philosophie/M/Voltaire/Kandid+oder+die+beste+Welt'

    if 'spiegel' in str(online_text_link):
        '''
        Spiegel_Kapital_num = 50
        online_text_link_original = str(online_text_link)[:-1]
        '''

        Spiegel_Kapital_num = 26
        online_text_link_original = 'http://gutenberg.spiegel.de/buch/erdgeist-2612/'

        for i in range(Spiegel_Kapital_num):
            # 此处可以根据上式循环后得到的网页链接字典分别得到各自Kapital的译文
            online_text_link = online_text_link_original + str(i+1)
            #print(online_text_link)

            online_text_website = get_transcripts_original_html(online_text_link)

            # only for Spiegel-online website
            spiegel_transcripts = crawl_transcripts_spiegel(online_text_website)


    elif 'zeno' in str(online_text_link):
        # only for Zeno website

        zeno_second_links = crawl_transcripts_zeno_second_links(online_text_link)
        print('zeno_second_links', zeno_second_links)

        #zeno_second_links = {1:'http://www.zeno.org/Philosophie/M/Seneca,+Lucius+Annaeus/Trostschrift+an+seine+Mutter+Helvia'}

        zeno_transcripts = crawl_transcripts_zeno_text(zeno_second_links)





    '''
    # Class 2:
    # Only for Etext download
    Etext_links = crawl_transcripts_Etext_second_links(url_librivox)
    '''
