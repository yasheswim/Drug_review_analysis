# Drug_review_analysis
The following repository consists of all the python codes used to scrape drug reviews, perform EDA on it and eventually build a text mining modelling algorithm to evaluate
and list out the effectiveness and side effects of the potential drugs. Data has been webscraped from Drugs.com for various drugs pertaining to various conditions. Rating, 
count(number of upvotes), dates and Condition are used as features which have also been extracted from web. Subsequently, topic modelling is performed on the reviews after 
applying appropriate data cleaning techniques like tokenization, stopword removal, lemmetization, POS tagging, etc.
Libraries used- Gensim for topic modelling and visualization of topic modelling
Scrapy, NLTK for text preprocessing and text normalization.
Beautiful_soup and Requests library to acquire content from web using URL authorization and parse though the HTmL tags.
