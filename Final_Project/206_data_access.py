import unittest 
import itertools 
import collections 
import tweepy 
import twitter_info
import json
import requests
import collections
import sqlite3 
import omdb

# Connor Johnston - Final SI 206 Project


##### TWEEPY SETUP CODE: # Authentication information is in a twitter_info file 
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up library to grab stuff from twitter with your authentication, and return
# it in a JSON format  
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## setting up cache file

CACHE_FNAME = "final_cache.json" # Put the rest of your caching setup here:

try:
	cache_file = open(CACHE_FNAME,'r')
	cache_contents = cache_file.read()
	cache_file.close()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}



# Defining the get functions for both API's here:

def get_movie(title):
	if title in CACHE_DICTION:
		response = CACHE_DICTION[title]
	else:
		res = omdb.request(t='title')
		response = res.content.decode('ascii')
		CACHE_DICTION[title] = response
		cache_file = open(CACHE_FNAME, 'w', encoding = 'utf-8')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return response
		
## Movie ID is the key at imdbID

def get_tweets(key):
	formatted_key = "twitter_{}".format(key)
	if formatted_key in CACHE_DICTION:
		response_list = CACHE_DICTION[formatted_key]
	else:
		response =  api.user_timeline(screen_name=key, include_rts=True, count=2)
		CACHE_DICTION[formatted_key] = response
		cache_file = open(CACHE_FNAME, 'w', encoding = 'utf-8')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
		response_list = []
		for r in response:
			response_list.append(r)

	return response_list

umich_tweets = get_tweets('umich')

print(type(umich_tweets))

## creating the user, tweet, and ombd databases

conn = sqlite3.connect('final.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('CREATE TABLE Tweets(tweet_id TEXT PRIMARY KEY, text TEXT, user_id TEXT, time_posted TIMESTAMP, retweets INTEGER)')

cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('CREATE TABLE Users(user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER)')

cur.execute('DROP TABLE IF EXISTS Movies')
cur.execute('CREATE TABLE Movies(movie_id TEXT PRIMARY KEY, title TEXT, director TEXT, num_langs INTEGER, imdb_rating INTEGER, actor TEXT)')


##insert into the databases

## Will change to a function that accepts a list to make the code more modular

ex = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'

for i in range(len(umich_tweets)):
	tup = (umich_tweets[i]['id'], umich_tweets[i]['text'], umich_tweets[i]['user']['id'], umich_tweets[i]['created_at'], umich_tweets[i]['retweet_count'])
	cur.execute(ex, tup)

conn.commit()

##test cases


## Most test cases are not going to currently run because the code has not been built out.
class Tests(unittest.TestCase):
	def test_users_4(self):
			conn = sqlite3.connect('movies.db')
			cur = conn.cursor()
			cur.execute('SELECT * FROM Movies');
			result = cur.fetchall()
			self.assertTrue(len(result)==len(movie_list),"Testing that there are same number of movies as passed in")
			conn.close()

	def test_umich_caching(self):
			fstr = open("final_cache.json","r").read()
			self.assertTrue("movie" in fstr)

	def test_num_tweets(self):
		conn = sqlite3.connect('tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=2, "Testing there are at least 2 records in the Tweets database")
		conn.close()

	def test_nume_users(self):
		conn = sqlite3.connect('project3_tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=2,"Testing that there are at least 2 distinct users in the Users table")
		conn.close()

	def test_mov_cols(self):
		conn = sqlite3.connect('movies.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6,"Testing that there are 6 columns in the movies database")
		conn.close()

	def test_user_cols(self):
		conn = sqlite3.connect('users.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM users');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==3,"Testing that there are 3 columns in the Users database")
		conn.close()

	def test_tweet_cols(self):
		conn = sqlite3.connect('tweets.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6,"Testing that there are 6 columns in the Users database")
		conn.close()

	def test_common_char2(self):
		self.assertTrue(type(most_common_char)=="","Testing that most common word is a string")

# if __name__ == "__main__":
# 	unittest.main(verbosity=2)