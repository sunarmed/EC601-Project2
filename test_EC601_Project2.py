from EC601_Project2 import *
import os.path

def test_credential_file_exist():
	"""
	Test whether credential file exists

	"""
	rslt=False
	try:
		with open('secret.json','r') as fp:
			rslt=True
	except:
		pass
	
	assert(rslt)

def test_credential_content():
	"""
	Test whether credential has a correct json format
	"""

	rslt=False
	try:
	    with open('secret.json','r') as fp:
	        a=json.load(fp)
	        consumer_key = a['consumer_key']
	        consumer_secret = a['consumer_secret']
	        access_key = a['access_token']
	        access_secret = a['access_token_secret']
	        rslt = True
	except:
		pass

	assert(rslt)

def test_Twitter_server_response():
	"""
	Test whether TwitterAPI respond to our search requests
	"""
	rslt = False
	keyword = "Love" #This should be a universal keyword.
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	print(api)
	try:
		new_tweets = api.search_tweets(keyword,count = 1)
		rslt = True
	except:
		pass

	assert(rslt)

def test_Google_server_response():
	"""
	Test whether google-api respond to our requests
	"""
	rslt = False
	test_text = 'I love you, no matter what happen.'
	try:
		score , magd = sample_analyze_sentiment(test_text)
		rslt = True
	except:
		pass

	assert(rslt)


def test_Twitter_search_complete():
	"""
	Test if tweet searching is completed
	"""
	max_tweet_number = 30
	test_keyword = "love"
	test_filename = "tweet-unittest-temp.json"
	rslt = False
	try:
		mean, std = search_tweets( test_keyword , test_filename , max_tweet_number)
		rslt = True
	except:
		pass


	assert(rslt)
	assert(os.path.exists(test_filename))

def main():
	test_Twitter_server_response()

if __name__ == "__main__":

	main()