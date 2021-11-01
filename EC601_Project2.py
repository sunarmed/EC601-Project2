#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import tweepy #https://github.com/tweepy/tweepy
import json
from google.cloud import language_v1
import os, sys
import numpy as np
import time
import matplotlib.pyplot as plt

# In[2]:

#Twitter API credentials
try:
    with open('secret.json','r') as fp:
        a=json.load(fp)
    #    print(a)
        consumer_key = a['consumer_key']
        consumer_secret = a['consumer_secret']
        access_key = a['access_token']
        access_secret = a['access_token_secret']
except:
    print('Read Secret Credential Error')


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


def search_tweets(keyword,filename,max_tweet):
    #search for tweet with 
    #Twitter only allows access to a users most recent 3240 tweets with this method
    print('do',keyword)
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    
    #initialize a list to hold all the tweepy Tweets
    alltweets = []    
    tweet_sentiment_score=[]
    tweet_sentiment_magnitude=[]



    #make initial request for most recent tweets (200 is the maximum allowed count)
    #new_tweets = api.user_timeline(screen_name = screen_name,count=10)
    retry = 0
    retry_limit = 10
    while retry < retry_limit:
        new_tweets = api.search_tweets(keyword,count = 15)
        if(new_tweets):
            break
        retry = retry + 1
        time.sleep(1)
        print(f'retry {retry} on {keyword}')
    if retry >= retry_limit:
        exit(f'No Tweets Found by keyword {keyword}')


    for t in new_tweets:
        if t._json['lang'] !='en':
            continue
        score,magnitude=sample_analyze_sentiment(t._json['text'])
        tweet_sentiment_score.append(score)
        tweet_sentiment_magnitude.append(magnitude)

    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    print( "...%s tweets of %s downloaded so far %s" % (len(alltweets) , keyword , oldest) )
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print('looping')
#    while False:       
        #all subsiquent requests use the max_id param to prevent duplicates
        #new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        retry = 0
        retry_limit = 10
        while retry < retry_limit:
            new_tweets = api.search_tweets(keyword,count = 15,max_id=oldest)
            if(new_tweets):
                break
            retry = retry + 1
            time.sleep(1)
            print(f'retry {retry} on {keyword}')
        if retry >= retry_limit:
            exit(f'No Tweets Found by keyword {keyword}')

        for t in new_tweets:
            if t._json['lang'] !='en':
                continue
            score,magnitude=sample_analyze_sentiment(t._json['text'])
            tweet_sentiment_score.append(score)
            tweet_sentiment_magnitude.append(magnitude)
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) >= max_tweet):
            break
        print( "...%s tweets of %s downloaded so far %s" % (len(alltweets) , keyword , oldest) )
       

    


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


    return np.mean(tweet_sentiment_score),np.std(tweet_sentiment_score)


def show_some_tweet(filename):
    fp = open(filename,'r')
    tweets_from_file=json.load(fp)
    a = json.dumps(tweets_from_file,indent=4)
    fp.close()
    return tweets_from_file


def city_scores(city_names):
    max_tweet_number = 300
    filename = 'tweet-'+city_names+'.json'
    mean, std = search_tweets( city_names , filename , max_tweet_number)
    return mean,std


# In[65]:




city_list =['Boston','Seattle','Chicago','Austin']
usage='python EC601-Test.py <city-name>\n\
if <city-name> is --all, the program will output a list of built-in cities.'

def main():
    print(len(sys.argv))
    if len(sys.argv) < 2:
        print(usage)
        exit(0)
    if sys.argv[1]=='--all':
        print('all citys')
        target_list = city_list
    elif sys.argv[1]=='-h':
        print(usage)
        exit(0)
    else:
        target_list = [sys.argv[1]]            

    if '--graph' in sys.argv:
        graph_on = 1
    else:
        graph_on = 0

    result = {}
    for city_names in target_list:
        mean, std = city_scores(city_names)
        result[city_names] = {'mean':mean,'std':std}

    print(result)
    for city in result:
        print(city,'scores:',result[city]['mean'])

    if graph_on==1:
        fig,ax = plt.subplots()
        x_pos = np.arange(len(target_list))
        scores = [result[c]['mean'] for c in target_list]
        errors = [result[c]['std'] for c in target_list]
        ax.bar(x_pos,scores, yerr=errors,align='center', alpha=0.5, ecolor='black')
        ax.set_ylabel('sentiment score')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(target_list)
        ax.set_title('Sentiment Score of Big Cities')
        ax.yaxis.grid(True)

        plt.tight_layout()
        plt.savefig('cities.png')
        plt.show()



if __name__ == '__main__':
    main()

print('import EC601')