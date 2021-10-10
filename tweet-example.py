#!/usr/bin/env python3
# coding: utf-8

# In[1]:


import tweepy #https://github.com/tweepy/tweepy
import json
from google.cloud import language_v1



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




def sample_analyze_entities(text_content):
    """
    Analyzing Entities in a String
    Args:
      text_content The text content to analyze
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'California is a state.'

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})

    # Loop through entitites returned from the API
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))

        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))

        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))

        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{}: {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))

            # Get the mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name)
            )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(u"Language of the text: {}".format(response.language))



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
