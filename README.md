# twitter-sentiment-analysis
An example of sentiment analysis on Twitter using Emoticons to label the sentiment of the tweet.

To complete the analysis exploits two python libraries:

- [tweepy](http://www.tweepy.org/), which offers the access to twitter API
- [Stanford Natural Language Toolkit](http://www.nltk.org/), which provides the natural languages functionalities to build up classifier

# Collector

The collector scripts allows to define a campaign to collect the tweets we need for the sentiment analysis.

The scripts requires three arguments:  
 - sentiment_label, the kind of emoticons we are looking for in the tweets positive -> :) or negative -> :(
 - campain_name, the name of campaign we are going to define
 - keywords, the keywords we are going to look for in the tweets.

The output of the collector.py execution is a csv file named with the pattern 
[campaign_name]+[sentiment_label].csv (e.g. iphone6-positive.csv). The fields of such a file are TweetID,User_ID,Text,Sentiment.

# Pre Processing

The preprocessing scripts modifies the tweets content in order to make possible the further analysis. 

- Any url is removed and substituted with the word "URL"
- Any @Username is converted to "AT_USER" to make any tweet anonymous 
- Any additional white spaces is removed
- Ant not alphanumeric symbol is removed 
- Hashtags are substituted with the corresponding word
- The emoticon used for the labeling is stripped out from the text

# Feature Extractor

Before building a classifier we need to extract all the features (word) contained in the tweet text.

Moreover, is necessary to remove any stop words. 
We also strip out punctuation, digits, and any symbols that might be still in the tweet text.

The file stopwords.txt contains a list of the most common English stopwords.

# Classifier

The actual analysis happens by the means of the classifier.py script.

It requires as arguments (the order is relevant):

- the file of the positive tweets, 
- the file of the negative tweets,
- the file with the stop words

The analysis follows the following steps:

1) The tweets dataset which are now separated will be merged and divides into a train dataset, which will be used to train the classifier, and a test dataset, used to test it. Respectively there will be the 80% of the tweets for training and the 20% for testing.

2) From each tweet will be extracted a feature-set
3) We use NLTK to describe each tweets in terms of the features it contains. Indeed, we create a list of words ordered by frequency.
4) We trains a NaiveBayesClassifier with such a dataset
5) We test the classifier using the remaining 20% of the tweets and we process in the same way of the training dataset.

# Results

Here the results of the analysis for the example, train dataset of 800 instances, test dataset of 202 instances.

## Most Informative Features:


- contains check =  True  ;  positive : negative  =   200.3 : 1.0
- contains free = True    ;    positive : negative =    200.3 : 1.0
- contains bi =  True     ;       positive : negative =   199.7 : 1.0
- contains thx = True     ;       positive : negative =     199.7 : 1.0 
- contains do =  True    ;       positive : negative =    125.7 : 1.0
- contains hurry =  True ;          positive : negative =      81.7 : 1.0 
- contains hi =  True    ;        positive : negative =     39.9 : 1.0
- contains wanna =  True  ;          positive : negative =      20.8 : 1.0
- contains ios =  True   ;         negative : positive =      12.2 : 1.0
- contains don =  True   ;         negative : positive =     11.7 : 1.0 

## Metrics

- pos precision: 1.0
- pos recall: 0.693069306931
- pos F-measure: 0.818713450292
- neg precision: 0.765151515152
- neg recall: 1.0
- neg F-measure: 0.8669527897

To complete this experiment I followed the guided at [Link1](http://ravikiranj.net/posts/2012/code/how-build-twitter-sentiment-analyzer/#implementation-details) and [Link2](http://www.laurentluce.com/posts/twitter-sentiment-analysis-using-python-and-nltk/)


