#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import tweepy #https://github.com/tweepy/tweepy
import json


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
    new_tweets = api.search_tweets(keyword)
    
    #save most recent tweets
    alltweets.extend(new_tweets)
    
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        
        #all subsiquent requests use the max_id param to prevent duplicates
        #new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
        new_tweets = api.search_tweets(keyword)
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        if(len(alltweets) > 300):
            break
        print( "...%s tweets downloaded so far" % (len(alltweets)) )
       
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
    search_tweets(tweet_text_keyword,filename)
    tweet_list = show_some_tweet(filename)
    print(len(tweet_list),'tweets are found')

    for count,t in enumerate(tweet_list):
        print(count)
        print(t.get('text',''))
