# EC601-Project2
This is a demonstration of Twitter API and Google NLP API. 

## User Story:

I myself is a newcomer to this city of Boston. I am even a newcomer to this enormous country of the US. From travel booklets or historical stories, I can easily catch the brief overview of this city. However, those are the fact of the material world, but not the real feeling of people. What I care the most, and it might be the most crucial thing, is how people around here feel about their daily lives in this city. I want to know if people here are satisfied with their lives, or have endless complaints toward public affairs. Since Twitter is the most popular social media in the US, it should be a great source to gather people's thoughts and feelings. 

For any newcomer, he or she should have a meaningful source of information of this city. Moreover, we can compare the people's sentiment toward this city with other places. This tool can be a searchlight when I am choosing careers, jobs, or making important decisions. 


## MVP:

With the help of Tweepy (https://www.tweepy.org/) , "an easy-to-use Pythn library for accessing the Twitter API", I can search the collect every tweets containing the keywords of a specified city, e.g. Boston. Every tweet can be analyzed by the Cloud Language Processing API and given a sentiment score of the tweet ranging from -1 to 1, meaning the positiveness of this short text.

At any given time, I can collect at least 300 tweet and calculate the mean and standard deviation of sentiment regarding this city. Those two indicators enable us to have a more holistic view over the sentimental part of this city.

## Usage:


run the following commands:

> python EC601-Test.py <city name>

  It will shows the mean and standard deviation of sentimental score of the city.
 
> python EC601-Test.py --all
  
  It will run the analysis of a built-in list of cities.

>python EC601-Test.py --all --graph
  
  It will also shows a bar graph of sentiment scores.
  
## Result:

  In the figure cities.png, Boston scored 0.09, Seattle scored 0.01, Chicago scored -0.004, and Auston scored 0.018.
  Among the four cities, Boston is the one with the highest sentiment score. It shows that the people here feel more positive. However, Chicago has a negative average score. I guess the lives there wasn't so good recently.  
