# Sentiment Analysis

## Scenario
It's all about data.  According to Forbes in 2020 there is around 44 zettabytes (1 zettabyte is 1,000,000,000,000,000,000,000 bytes) of data in our digital universe.  They also stated that we'll create 1.7 megabytes of new information every second for every human being on the planet.  That's a lot of data. (this data came from an old article for an interesting <a href="https://www.forbes.com/sites/bernardmarr/2015/09/30/big-data-20-mind-boggling-facts-everyone-must-read/#3b00d97717b1">read</a>)

Data is important to every type of company.  Problem is nearly <a href="https://learn.g2.com/structured-vs-unstructured-data">80% of the world's digital data is unstructured</a> with a large part of this being social media data.  One of the great social media platforms to gather data is Twitter.  Twitter has more than 321 million active users, sending a daily average of 500 million tweets.

There are many ways to use Twitter data to help companies.  This assessment will focus on Sentiment Analysis.

## What is Sentiment Analysis?
<a href="https://en.wikipedia.org/wiki/Sentiment_analysis">Wikipedia</a> defines Sentiment Analysis as the use of natural language processing, text analysis, computational linguistics, and biometrics to systematically identify, extract, quantify, and study effective states and subjective information.  Simply put it is getting how a customer feels about a company or product by looking at what they say or in this case what they Tweet.

## Steps required for Sentiment Analysis:
### 1- Gather Twitter data
### 2- Prepare your data
### 3- Create a Sentiment Analysis Model
### 4- Visualize Your Results

## Before we get started:
In order to accomplish this assessment you will need a Twitter account and a Twitter Developer account.  If you already have a Twitter account you can apply for a Twitter developer account <a href="https://developer.twitter.com/en">Here</a>

### Step 1 Gather Twitter data
Twitter has many API's you can use to gather Tweets.  You can gather them in real time as they happen, or do a history search from 7 days, 30 days, or full archive.  The 30 days and full archive are premium APIs, but you have trial access to them that has limits.  We will be gathering real time Tweets.

There are many open source libraries you can use with Python to capture Twitter data, in this assessment you will be using <a href="http://docs.tweepy.org/en/v3.8.0/getting_started.html">tweepy</a>

When doing Sentiment Analysis you will capture Tweets about a particular subject.  This subject can be current events, sporting events or even a product you are interested in.  For this assessment the user input the search terms, each term should be separated by a comma.

Create a separate module called gathertweets.py in this module use tweepy to setup a stream and capture live Tweets about your topic, save these in a list called tweets in the following format:

{"text": tweet.text, "label": None}

### Step 2 Prepare Your data
In Sentiment Analysis there are a few things that do not help in the analysis so we can remove them, they are punctuation, usernames, URLs, and hashtags.  When we speak we use a lot of stop words.  Stop words are sentence fluff and have no bearing on Sentiment Analysis so to save processing time we should remove them first.  Then we need to get rid of duplicate characters in words so if someone typed caaaaar it would be replaced with car so we do not miss any important words.  Then finally we will break the tweet into words or what is called tokenize the tweet.

#### 1- Use the string library and import punctuation you can use this to strip punctuation from the tweet.
#### 2- Use regex to search for usernames, URLs and hashtags in the Tweet and remove them.
#### 3- Python has a library nltk <a href="https://www.nltk.org/">Natural Language Toolkit</a> that can be used to get rid of stop words and to tokenize the tweets.

### Step 3 Create a Sentiment Analysis Model
This is the fun part or the mind boggling part.  Computers do not understand human language so we need to train our program to know if a Tweet is positive or negative based on the words in the Tweet.  As with any training the more you train the better you become.  We can not just download a bunch of tweets and pass it to our model and have it return positive or negative without training it first.

So how do we train, well first we need a set of training data.  But I just said our model would return nothing if not trained, that is correct.  So to prepare this training data we have to go old school and do it by hand.  So we would have to capture our Tweets, then go through them by hand and classify them as positive or negative so we would be able to train our model.

This is a lot of work, fortunately a guy named Niek Sanders has hand-classified 5000 Tweets so we do not have to.  Unfortunately Twitter does not allow you to store Tweet data on a personal device.  So included in this repo are two files first is corpus.csv this is Niek Sanders' corpus file it is comprised of a keyword(topic of the Tweet), label(pos/neg) and a Tweet ID number.  The next file is retrievetrainingdata.py this uses the library python-twitter to connect to Twitter's API and download the tweets.  However Twitter has limits on how many Tweets you can download in 15 minutes and if you abuse it they will block your app from the API.  You can shorten this corpus file but remember the more data you train your model with the more accurate it will be.  If you do all 5000 it can take up to 6 hours to get all the Tweets, so this will create a file called tweetDataFile.csv (I know we are not supposed to store Tweets, but I am not waiting 6 hours every time I need to test my app.  Just do not add this file to your repo. Lucky for you this module is already tested and working, it took me three trys to accomplish it(18 hours of nothing but Tweets scrolling in my console.))  You can run this by importing it into your sentimentanalysis.py and using this 

    training_data = build_training("corpus.csv", "tweetDataFile.csv")

Hope you got a good nights sleep and have your training data.  Before we can continue to train our model you need to run the training data through step 2 first.  Once data is prepared we can continue.

Now we need a classifier to train our model.  For this we will use Naive Bayes Classifier which is based on Bayes' Theorem.  If you enjoy math and want to dive deep into this here is a starting point https://www.datacamp.com/community/tutorials/naive-bayes-scikit-learn .  I will not be going into this here because for one thing this readme file is getting way too long.

In order to build our model we need to do the following:
#### 1- Build a vocabulary of all words in our training data.
#### 2- Match tweet content against our vocabulary word-by-word
#### 3- Build our word feature vector
#### 4- Plug our feature vector into the Naive Bayes Classifier.

Sounds like a lot of fun doesn't it.  Lets break it down even further (told you this readme is long).

To accomplish step one we need to create a list of all distinct words in the training data and the key will be the frequency of that word in the set.  We can accomplish this using nltk.FreqDist.

For step two we need to create a dictionary that will be formated like

    tweet_features['contains(%s)' % word] = (word in tweet_words)
    
where x is the word from our Tweet and it's value is True if in the dictionary of False if it is not.
