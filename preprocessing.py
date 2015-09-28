import re
import csv
from sys import argv

#script, file_ = argv

def processRow(row):
	
	
	tweet = row[2]
	#Lower case
	tweet.lower()
	#convert any url to URL
	tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
	#Convert any @Username to "AT_USER"
	tweet = re.sub('@[^\s]+','AT_USER',tweet)
	#Remove additional white spaces
	tweet = re.sub('[\s]+', ' ', tweet)
	tweet = re.sub('[\n]+', ' ', tweet)
	#Remove not alphanumeric symbols white spaces
	tweet = re.sub(r'[^\w]', ' ', tweet)
	#Replace #word with word
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
	#Remove :( or :)
	tweet = tweet.replace(':)','')
	tweet = tweet.replace(':(','')
	#trim
	tweet = tweet.strip('\'"')

	row[2] = tweet

	return row

# end processTweet

if __name__ == '__main__':
	#Read the tweets one by one and process it
	clnfile = open("CLN-"+file_,'wb')
	filewriter = csv.DictWriter(clnfile, fieldnames=["TweetID", "User_ID", "Text", "Sentiment"])

	with open(file_, "rb") as csvfile:
		filereader = csv.reader(csvfile)
		for row in filereader:
			new_row = processRow(row)
			filewriter.writerow({
					"TweetID" : new_row[0],
			 		"User_ID" : new_row[1],
			 		"Text"	: new_row[2],
			 		"Sentiment" : new_row[3]
			 		})
	clnfile.close()



