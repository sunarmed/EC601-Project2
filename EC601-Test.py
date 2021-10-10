#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import tweepy #https://github.com/tweepy/tweepy
import json
from google.cloud import language_v1
import os


# In[2]:


with open('secret.json','r') as fp:
    a=json.load(fp)
#    print(a)
#Twitter API credentials
    consumer_key = a['consumer_key']
    consumer_secret = a['consumer_secret']
    access_key = a['access_token']
    access_secret = a['access_token_secret']


# In[64]:



def sample_analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}
    document = {"content": text_content, "type_": type_}



    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document

    return response.document_sentiment.score, response.document_sentiment.magnitude
#    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
#    print(
#        u"Document sentiment magnitude: {}".format(
#            response.document_sentiment.magnitude
#        )
#    )
    # Get sentiment for all sentences in the document
#    for sentence in response.sentences:
#        print(u"Sentence text: {}".format(sentence.text.content))
#        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
#        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
#    print(u"Language of the text: {}".format(response.language))


def search_tweets(keyword,filename):
    #search for tweet with 
    #Twitter only allows access to a users most recent 3240 tweets with this method
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    
    #make initial request for most recent tweets (200 is the maximum allowed count)
    #new_tweets = api.user_timeline(screen_name = screen_name,count=10)
    new_tweets = api.search_tweets(keyword,count = 1)
    
    print(sample_analyze_sentiment(new_tweets[0]._json['text']))

    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
#    while False:       
        #all subsiquent requests use the max_id param to prevent duplicates
        #new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        new_tweets = api.search_tweets(keyword,count = 1,max_id=oldest)
        print(sample_analyze_sentiment(new_tweets[0]._json['text']))

        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 10):
            break
#        print( "...%s tweets downloaded so far" % (len(alltweets)) )
       
    #write tweet objects to JSON
    file = open(filename, 'w') 
    print( "Writing tweet objects to JSON please wait...")
    file.write('[\n')
    for status in alltweets:
        json.dump(status._json,file,sort_keys = True,indent = 4)
        file.write(',\n')
    #    json.dumps(status._json,indent=4)
    #close the file
    file.write('{}\n]')
    print( "Done")
    file.close()



def show_some_tweet(filename):
    fp = open(filename,'r')
    tweets_from_file=json.load(fp)
    a = json.dumps(tweets_from_file,indent=4)
    fp.close()
    return tweets_from_file


# In[65]:

if __name__ == '__main__':
    filename = 'tweet-boston.json'
    tweet_text_keyword = 'boston'
    col = os.get_terminal_size()[0]
    search_tweets(tweet_text_keyword,filename)
    tweet_list = show_some_tweet(filename)
    print(len(tweet_list),'tweets are found')
#
#    for count,t in enumerate(tweet_list):
#        print('-'*col)
#        print(count)
#        twt = t.get('text','')
#        print(twt)
#        print(sample_analyze_sentiment(twt))
#        print('-'*col)



