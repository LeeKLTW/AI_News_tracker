# -*- coding: utf-8 -*-
""" 
Crawling news from website. Now support medium and technews.
"""
import os
import argparse
import requests
from bs4 import BeautifulSoup
import pymongo
import nltk
import datetime

FLAG = None

def __get_links__(url,layout_type):
    """This function get the links from homepage.
    Args:
        url: string. The URL of website. e.g. 'https://towardsdatascience.com/', 
        layout_type: string. The layout type of html. e.g. medium, technews
    Returns:
        List of links found.
    """
    assert layout_type.lower() in ['medium','technews'],'The layout type {} is not available yet.'.format(layout_type)
    try:
        if layout_type.lower() == 'medium':
            # if not url.starts_with('https'): #tag method
            #     url = 'https://medium.com/tag/'+url.lower().replace(' ','-')
            #     __get_links__(url,layout_type)
            print('Crawling ',url,'from',layout_type)
            html = requests.get(url).text
            soup = BeautifulSoup(html,'html.parser')
            links = [i['href'] for i in soup.find_all('a',{'class':"link link--darken",'data-action':"open-post"})]
        elif layout_type.lower() == 'technews':
            print('Crawling ',url,'from',layout_type)
            html = requests.get('https://technews.tw/category/cutting-edge/ai/').text
            soup = BeautifulSoup(html,'html.parser')
            links = [i['href'] for i in soup.select('tr td h1 a')]
    except:
        pass
    return links

def __get_article_info__(url,layout_type):
    """Get information of article
    Args:
        url: string. The URL of article. e.g. 'https://towardsdatascience.com/wikipedia-data-science-working-with-the-worlds-largest-encyclopedia-c08efbac5f5c', 'https://technews.tw/2018/09/27/minimal-turing-test-the-single-word-can-prove-youre-a-human/'
        layout_type: string. The layout type of html. e.g. medium, technews
    Returns:
        title date content tags
    """
    html = requests.get(url)
    soup = BeautifulSoup(html.text,'html.parser')
    print('get article info from ',url)
    if layout_type.lower() == 'medium':
        title = soup.select('title')[0].text
        author = soup.select('header div div div div div a')[0].text
        date = soup.select('time')[0].text
        content = '  '.join([i.text.replace('\u200a','').replace('\xa0','') for i in soup.select('div.section-inner p')])
        tags = [i.text for i in soup.select('ul li a[data-action-source="post"]')]

        keys = ['title','author','date','content','tags']
        article_info=dict(zip(keys,[title,author, date, content, tags]))
        print('Article found:',article_info['title'])

    elif layout_type.lower() == 'technews':
        title = soup.select('h1 a')[0].text
        author = soup.select('table span a')[0].text
        date = soup.select('table span.body')[1].text
        content = '  '.join([i.text.replace('\xa0','') for i in soup.select('#content div p')])
        tags = [i.text for i in soup.select('header table a')[2:-2]]

        keys = ['title','author','date','content','tags']
        article_info=dict(zip(keys,[title,author, date, content, tags]))
        print('Article found:',article_info['title'])
    
    return article_info

def __write_into_mongodb__(posts,host,port):
    """Write the information of article into MongoDB.
    Args:
        posts: dict. The information of article.
        host: str. The host of MongoDB.
        port: int.The port of MongoDB.
    Returns:
        None
    """
    client = pymongo.MongoClient(host,int(port))
    collection = client.get_database('AI_news_tracker').get_collection('article')
    collection_set = set([i['title'] for i in collection.find({})])
    count = 0
    for post in posts:
        if post['title'] not in collection_set:
            collection.insert_one(post)
            count+=1
        else:
            print('This article already exists in database:  ',post['title'])
    print('Inserted',count,'articles')
    print('The number of documnets in database now is:',collection.estimated_document_count())
    client.close()
    return

def main(url,layout_type,host,port):
    """
    Args:
        url:str. The URL of tag website. e.g. 'https://medium.com/tag/machine-learning', https://technews.tw/category/cutting-edge/ai/
        layout_type:str.The layout type of html. e.g. medium, technews
        host: str. The host of MongoDB, default='127.0.0.1'
        port: int. The port of MongoDB, default='27017'
    Returns:
        None
    """
    links = __get_links__(url,layout_type)
    article_info = [__get_article_info__(link,layout_type) for link in links]
    __write_into_mongodb__(article_info,host,port)
    print('Done')
    os._exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url',type=str,help="string. The URL of tag website or tag of medium. e.g. 'https://medium.com/tag/machine-learning', https://technews.tw/category/cutting-edge/ai/")
    parser.add_argument('layout_type',type=str,help="The layout type of html. e.g. medium, technews ")
    parser.add_argument('--host',type=str,default='127.0.0.1',help="The host of MongoDB")
    parser.add_argument('--port',type=int,default='27017',help="The port of MongoDB")
    FLAGS, unparsed = parser.parse_known_args()
    main(FLAGS.url,FLAGS.layout_type,FLAGS.host,FLAGS.port)