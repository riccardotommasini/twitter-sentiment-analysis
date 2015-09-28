from sys import argv, exit
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream 

import json
import csv
import re


script, sentiment_label, campain, keywords = argv

DEBUG = False

keywords = keywords.split(",")

if "positive"==sentiment_label:
	emoticon = ":)"
elif "negative"==sentiment_label:
	emoticon =":("

regex = re.compile('|'.join(keywords).lower())
linenum_re = re.compile(r'([A-Z][A-Z]\d+)')
retweets_re = re.compile(r'^RT\s')

enc = lambda x: x.encode('latin1', errors='ignore')


def fold(f,l,a):
	"""
		f: the function to apply
		l: the list to apply the function on
		a: the initial value
	"""
	return a if(len(l)==0) else fold(f,l[1:],f(a, l[0]))
	

def print_debug(er,msg):
	if DEBUG:
		print "Error: ", er
		print "Message: < %s >" % msg


class SimpleListener(StreamListener):

	def on_data(self,data):
		tweet = json.loads(data, encoding='utf-8')
		print "-" * 10

		tweet_id = tweet['id']
		user_id = enc(tweet['user']['name'])
		text 	 = enc(tweet['text'])
		lang 	 = enc(tweet['lang'])
		
		if not (fold(lambda x, y: x or y, [k.lower() in text.lower() for k in keywords], False)):	
			print tweet
		
		print "ID:", tweet_id
		print "USER:", user_id
		print "TEXT:", text
		print "LANG: ", lang
		print "Contains :)", (':)' in text)
		print "Contains :(", (':(' in text)


		for k in keywords:
			contained = k.lower() in text.lower()
			print "Contains %s: %r" % (k, contained)



	def on_error(self, status):	
		print('status: %s' % status)




class EmoticonListener(StreamListener):

	def __init__(self):
		self.count = 0

	def on_data(self, data):

		if(self.count > 500):
			exit(0)

		tweet = json.loads(data, encoding='utf-8')

		if not tweet.has_key('id'):
			print_debug("No Id, skip the tweet","")
			return True
		elif not tweet.has_key('user'):
			print_debug("No user, skip the tweet", "")
			return True
		elif not tweet.has_key("text"):
			print_debug("not text, skip the tweet", "")
			return True
		elif not tweet.has_key("lang") or tweet['lang'] != "en":
			print_debug("Not english", "")
			return True 
		
		tweet_id = tweet['id']
		user_id = enc(tweet['user']['name'])
		text 	 = enc(tweet['text'])
		
		matches = re.search(regex, text.lower())
		rt_matches = re.search(retweets_re, text)

		if not matches:
		 	print "No Keyword in text, skip the tweet"
		 	print "< %s >" % text
		 	return True
		if not (emoticon in text):
			print_debug("No Emoticon, skip the tweet", text)
			return True
		elif rt_matches:
			print_debug("Is a retweet, skip", text)
			return True
		else:
			print_debug("This is good", text)
			
		writer.writerow({
				"TweetID" : tweet_id,
		 		"User_ID" : user_id,
		 		"Text"    : text,
		 		"Sentiment" : sentiment_label
		 		})

		self.count = self.count + 1

		print "-" * 10 + "Count", self.count

		print "ID:", tweet_id
		print "USER:", user_id
		print "TEXT:", text
		print "Sentiment", sentiment_label


	def on_error(self, status):
		print('status: %s' % status)
#end EmoticonListener

if __name__ == '__main__':
	
	config = json.load(open('config.json','r'))
	auth = OAuthHandler(config['consumer_key'], config['consumer_secret'])
	auth.set_access_token(config['access_token'], config['access_token_secret'])
	

	print "Start collecting tweets"
	print "Campaign name: ", campain
	print "Sentiment: ", sentiment_label
	print "Keywords: ", [k + " " + emoticon for k in keywords]
	print 'Authenticated'



	with open(campain+"-"+sentiment_label+".csv", "w") as f:
			writer = csv.DictWriter(f, fieldnames=["TweetID", "User_ID", "Text", "Sentiment"])
			writer.writeheader()
			l = EmoticonListener()
			s = SimpleListener()
			stream = Stream(auth, l)
			print "Stream created"
			stream.filter(track=[k + " " + emoticon for k in keywords], languages=['en'])
			print 'End'




