import re
import csv



#start replaceTwoOrMore
def replaceTwoOrMore(s):
    #look for 2 or more repetitions of character and replace with the character itself
    pattern = re.compile(r"(.)\1{1,}", re.DOTALL)
    return pattern.sub(r"\1\1", s)
#end

def getStopWordList(stopWordFile):
	stopwords = []
	stopwords.append("AT_USER")
	stopwords.append("URL")

	with open(stopWordFile, 'r') as f:
		reader = csv.reader(f)
		for w in reader:

			stopwords.append(w[0])

	return stopwords
#end
	

def getFeatureVector(tweet, stopWordFile):
	features = []

	stop_words = getStopWordList(stopWordFile)

	words = tweet.split()
	for w in words:

		w = replaceTwoOrMore(w)

		#strip digits
		w = w.strip('0123456789')

		#strip punctuation
		w = w.strip('\'"!?,.')

		if (w == ""):
			continue
		elif(w in stop_words):
			#print w
			continue
		else:
			features.append(w.lower())

	return features
#end






