# AI_News_tracker
crawl news content from website like medium, 科技新報, store in MongoDB, extract information by NLTK

# Getting Started
## Prerequisites(dependency)
MongoDB ([official](https://www.mongodb.com/),[docker](https://hub.docker.com/_/mongo/))

Python package:
  pymongo
  requests
  BeautifulSoup
  nltk

  Some nltk module might be needed, plase modify and insert the script below if neccesary:
  >import nltk
  
  >nltk.download()
  
## Installing
  1.git clone https://github.com/LeeKLTW/AI_News_tracker
  
  2.install mongodb
  
# Running the tests
## 1.Execute MongoDB
mongod
## 2.Crawling

>python crawler.py

## 3.Extracting
>python extracter.py

# Authors
LeeKLTW

# License
MIT
