# -*- coding: utf-8 -*-
""" 
Extract information from news using Named-entity recognition technique from nltk.
Some nltk module might be needed, plase modify and insert the script below if neccesary:
>>> import nltk
>>> nltk.download()
"""
import pymongo
import nltk
import argparse
import os

FLAGS = None

def __read_from_mongodb__(host,port,query={},show=False):
    """Get the query result from MongoDB.
    Args:
        host: str. The host of MongoDB.
        port: int.The port of MongoDB.
        query: dict. Query for certain collection. Default:all.  e.g. {'title':'Machine Learning: A Gentle Introduction. – Towards Data Science'}
    Returns:
        List of post(document) found.
    """
    client = pymongo.MongoClient(host,port)
    collection = client.get_database('AI_news_tracker').get_collection('article')
    posts = [i for i in collection.find(query)]
    print(f'Read {len(posts)} posts from database.')
    if show:
        _=[print(post['title']) for post in posts]
    return posts

def __summarize__(content,show=False):
    """Summerize the content by counting top 5 sentences that have most NN,NNP in Named-entity recognition.
    Args:
        content: str. The content you want to summerize.
        show: bool. Show the summary or not. Default False.
    Returns:
        List of top 5 sentences.
    """
    results=[]
    for sent_no,sentence in enumerate(nltk.sent_tokenize(content)):
        no_of_tokens=len(nltk.word_tokenize(sentence)) #split the sentence
        tagged=nltk.pos_tag(nltk.word_tokenize(sentence)) #Part-of-Speech tagging
        no_of_nouns=len([word for word,pos in tagged if pos in ["NN","NNP"]])
        ners=nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence)), binary=False) #merge tags for chunking
        no_of_ners= len([chunk for chunk in ners if hasattr(chunk, 'label')]) #check the chunk
        score=(no_of_ners+no_of_nouns)/(float(no_of_tokens)+1)
        results.append((sent_no,no_of_tokens,no_of_ners, no_of_nouns,score,sentence))
        
    summary = []
    for number,sent in enumerate(sorted(results,key=lambda x: x[4],reverse=True)):
        if number < 5:
            if show: 
                print(sent[5]) 
            summary.append(sent[5])
    return summary

def __write_summary_into_db__(post,host,port):
    """write summary into MongoDB
    Args:
        post: dict. document
        host: str. The host of MongoDB.
        port: int.The port of MongoDB.
    Returns:
        None
    """
    client = pymongo.MongoClient(host,port)
    collection = client.get_database('AI_news_tracker').get_collection('article')
    try:
        collection.update_one({'_id':post['_id']}, {'$set': {'summary': post['summary']}})
        print('Write into database successfully.')
    except KeyError:
        print('Warning: No summary was written.')
    return

def main(query,host,port,show=False):
    posts = __read_from_mongodb__(host,port,query,show)
    for post in posts:
        try:
            if show: print(post['title'])
            post['summary'] = __summarize__(post['content'],show)
            __write_summary_into_db__(post,host,port)
        except KeyError:
            print('Warning: No content found in{}'.format(post['_id']))
    print('Done')
    os._exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--title',type=str,default=None,help="Query for title. Default:None e.g. 'Machine Learning: A Gentle Introduction. – Towards Data Science'")
    parser.add_argument('--author',type=str,default=None,help="Query for author. Default:None e.g. 'Nvs Abhishek' ")
    parser.add_argument('--date',type=str,default=None,help="Query for date. Default:None e.g.'Sep 22' ")
    parser.add_argument('--host',type=str,default='127.0.0.1',help="The host of MongoDB")
    parser.add_argument('--port',type=int,default='27017',help="The port of MongoDB")
    parser.add_argument('--show',type=bool,default=False,help="Show the title and summary or not.")
    FLAGS, unparsed = parser.parse_known_args()
    query = {}
    if FLAGS.title is not None: 
        query['title'] = FLAGS.title
    if FLAGS.author is not None:
        query['author'] = FLAGS.author
    if FLAGS.date is not None:
        query['date'] = FLAGS.date
    main(query,FLAGS.host,FLAGS.port,FLAGS.show)