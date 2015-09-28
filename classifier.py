from sys import argv
from sys import exit

import csv

import preprocessing
import feature_extractor
import nltk

import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
import nltk.metrics
import collections


script,  positive_tweets, negative_tweets, stop_words_file_name = argv

word_features = []

def read_tweets(tweet_file):

	features = []
	tweets = []

	with open(tweet_file,'r') as csv_file:
		csv_reader = csv.reader(csv_file)

		for l in csv_reader:
				
				if l[0] == "TweetID":
					continue

				new_row = preprocessing.processRow(l)
				
				if len(new_row) < 4:
					print "Malformed Data"
					continue
				
				features = feature_extractor.getFeatureVector(new_row[2], stop_words_file_name)

				tweets.append(
			 		( [f.strip("\'") for f in features],
			 		 new_row[3]
			 		))

	return tweets
#End

def extract_features(document):
	document_words = set(document)
	features = {}
	for w in word_features:
		features['contains %s'% w] = (w in document_words)
	return features

if __name__ == '__main__':
	
	neg_tweets = read_tweets(negative_tweets)
	pos_tweets = read_tweets(positive_tweets)

	cutoff = 0

	if(len(neg_tweets) > len(pos_tweets)):
		cutoff = len(pos_tweets)*4/5
	else:
		cutoff = len(neg_tweets)*4/5
 
	tweets = neg_tweets[:cutoff] + pos_tweets[:cutoff]
	test_tweets = neg_tweets[cutoff:] + pos_tweets[cutoff:]
	
	print 'train on %d instances, test on %d instances' % (len(tweets), len(test_tweets))
 
	all_words = []
	words_frequency = []

	#Get all the words
	for (words, sentiment) in tweets:
		all_words.extend(words)

	#extract the features
	wordlist = nltk.FreqDist(all_words)
	word_features = wordlist.keys()

	training_set = nltk.classify.apply_features(extract_features, tweets)
	
	classifier = NaiveBayesClassifier.train(training_set)
	
	refsets  = { 'positive': set([]), 'negative':set([])}
	testsets = { 'positive': set([]), 'negative':set([])}
	
   
	classifier.show_most_informative_features()

	for i, (feats, label) in enumerate(test_tweets):
	 	refsets[label].add(i)
 	  	testsets[classifier.classify(extract_features(feats))].add(i)
    
   

	print 'pos precision:', nltk.metrics.precision(refsets['positive'], testsets['positive'])
	print 'pos recall:', nltk.metrics.recall(refsets['positive'], testsets['positive'])
	print 'pos F-measure:', nltk.metrics.f_measure(refsets['positive'], testsets['positive'])
	print 'neg precision:', nltk.metrics.precision(refsets['negative'], testsets['negative'])
	print 'neg recall:', nltk.metrics.recall(refsets['negative'], testsets['negative'])
	print 'neg F-measure:', nltk.metrics.f_measure(refsets['negative'], testsets['negative'])



#

