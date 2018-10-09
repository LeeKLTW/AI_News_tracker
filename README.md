# AI_News_tracker
crawl news contents from website like medium(toward data science), 科技新報, store in MongoDB, extract information by NLTK

# Getting Started
## Prerequisites(dependency)
MongoDB ([official](https://www.mongodb.com/),[docker](https://hub.docker.com/_/mongo/))


Python package:
  pymongo

  requests
  
  BeautifulSoup
  
  nltk

  
  Some nltk module might be needed, plase modify and insert the script below if neccesary:
  ```
  import nltk
  nltk.download()
  ```
## Installing
  1.git clone https://github.com/LeeKLTW/AI_News_tracker
  
  2.install mongodb
  
# Running the tests
## 1.Execute MongoDB
in command line 
```
mongod
```
Remember your host,port,account,password

## 2.Crawling
```
python crawler.py
```
```
positional arguments:
  url          string. The URL of tag website or tag of medium. e.g.
               'https://medium.com/tag/machine-learning',
               https://technews.tw/category/cutting-edge/ai/
  layout_type  The layout type of html. e.g. medium, technews
optional arguments:
  -h, --help   show this help message and exit
  --host HOST  The host of MongoDB
  --port PORT  The port of MongoDB
```
Demo 
![](https://imgur.com/dJeAoZs.jpg)

If the file already exists.
![](https://imgur.com/fPFg0Pc.jpg)

The information you will store in MongoDB  shown below:

| layout_type                	| 'title' 	| 'author' 	| 'date' 	| 'content' 	| 'tags' 	|
|----------------------------	|:--------:|:---------:|:-------:|:----------:|:-------:|
| medium(towardsdatascience) 	| Yes     	| Yes      	| Yes    	| Yes       	| Yes    	|
| technews                   	| Yes     	| Yes      	| Yes    	| Yes       	| Yes    	|



## 3.Extracting
```
python extracter.py
```

```
optional arguments:
  -h, --help       show this help message and exit
  --title TITLE    Query for title. Default:None e.g. 'Machine Learning: A
                   Gentle Introduction. – Towards Data Science'
  --author AUTHOR  Query for author. Default:None e.g. 'Nvs Abhishek'
  --date DATE      Query for date. Default:None e.g.'Sep 22'
  --host HOST      The host of MongoDB
  --port PORT      The port of MongoDB
  --show SHOW      Show the title and summary or not.
```
Demo 
Suppose we want to know what this article want to tell us.
[Machine Learning: A Gentle Introduction. – Towards Data Science'](https://towardsdatascience.com/machine-learning-a-gentle-introduction-17e96d8143fc)
![](https://imgur.com/77YTwTx.jpg)
```
Machine Learning: A Gentle Introduction. – Towards Data Science
This AI was developed by Google’s DeepMind.

In 2012 Harvard Business Review called the job of a Data Scientist as “The Sexiest Job of the 21st Century”, and six years hence, it still holds that tag tight and high.

In the past decade or so, Machine Learning and broadly Data Science has taken over the technological front by storm.

It follows the concept of hit and trial method.

Deep learning is a subfield of machine learning which makes use of a certain kind of machine learning algorithm known as Artificial Neural Networks (ANNs), vaguely inspired by the human brain.
```


Judging by this sentence, we can know that:
  2012 HBR “The Sexiest Job of the 21st Century”. Neural Networks is subfield of machine learning, inspired by the human brain. It has taken over the technological front. Google’s DeepMind is notable team in deep learning.


# Work in progress 
- [ ] Update Summary Extracter based on [Seq2Seq](https://arxiv.org/abs/1409.3215) 
- [ ] Add search function on title and content based on tf-idf, cos-similarity
- [x] Check if it's possible to use [doc2vec](https://arxiv.org/abs/1405.4053) on recommendation system
- [x] Check if it's possible to improve the Chineses article POS tagging by Hidden markov.

  Yes.
- [x] Check if it's possible to translate Chineses to English,summarize, and translate it back to Chinese?

  Don't do it.
- [x] Check nltk sinica treebank.
      -> It's not suitable for technews ...

# Authors
LeeKLTW

# License
MIT
