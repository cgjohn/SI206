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

# List of all keys in a Movie
#Year, Title, Metascore, Poster, Language, Genre, Country, Ratings, Response, Awards, Plot, DVD, Production, Runtime, Type, Rated, Released, Website, Actors, imdbRating, Writer, imdbVotes, Director, BoxOffice, imdbID


class Movie(object):
	movieID = 0
	title = ""
	director = ""
	rating = 0.0
	actors = []
	numLangs = 0
	year = 0

	def __init__(self, movieDict):
		self.movieID = movieDict['imdbID']
		self.title = movieDict['Title']
		self.director = movieDict['Director']
		self.rating = movieDict['imdbRating']
		self.actors = movieDict['Actors'].split(", ")
		self.numLangs = len(movieDict['Language'].split(','))
		self.year = movieDict['Year']

	def __str__(self):
		return "{} by {} made in {}".format(self.title,self.director,self.year)



## creating the user, tweet, and ombd databases and starting the db connection

conn = sqlite3.connect('final.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('CREATE TABLE Tweets(tweet_id TEXT PRIMARY KEY, text TEXT, user_id TEXT, time_posted TIMESTAMP, retweets INTEGER)')

cur.execute('DROP TABLE IF EXISTS Users')
cur.execute('CREATE TABLE Users(user_id TEXT PRIMARY KEY, screen_name TEXT, num_favs INTEGER)')

cur.execute('DROP TABLE IF EXISTS Movies')
cur.execute('CREATE TABLE Movies(movie_id TEXT PRIMARY KEY, title TEXT, director TEXT, num_langs INTEGER, imdb_rating REAL, actor TEXT, year INTEGER)')



# Defining the get functions for both API's here:

# Sends a request to twitter for tweets containing a given key word
def get_tweets(key):
	formatted_key = "twitter_{}".format(key)
	if formatted_key in CACHE_DICTION:
		response_list = CACHE_DICTION[formatted_key]
	else:
		response =  api.search(q=key, include_rts=True, count=5)['statuses']
		CACHE_DICTION[formatted_key] = response
		cache_file = open(CACHE_FNAME, 'w', encoding = 'utf-8')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
		response_list = []
		for r in response:
			response_list.append(r)

	return response_list

# Returns the twitter user from given username
def get_user(name):
	formatted_key = "twitter_user_{}".format(name)
	if formatted_key in CACHE_DICTION:
		response = CACHE_DICTION[formatted_key]
	else:
		response =  api.get_user(screen_name = name)
		CACHE_DICTION[formatted_key] = response
		cache_file = open(CACHE_FNAME, 'w', encoding = 'utf-8')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()
	return response

#returns a movie object from the OMDB database when passed in a movie name
def get_movie(title):
	if title in CACHE_DICTION:
		response = CACHE_DICTION[title]
	else:
		res = omdb.request(t=title)
		response = res.content.decode('ascii')
		CACHE_DICTION[title] = response
		cache_file = open(CACHE_FNAME, 'w', encoding = 'utf-8')
		cache_file.write(json.dumps(CACHE_DICTION))
		cache_file.close()

	response = json.loads(response)
	return response



#Create a list of dictionaries of three chosen movies

movieNames = ["Star Wars", "Avatar", "Get Out"]
movieList = []

for movie in movieNames:
	movieList.append(get_movie(movie))

# Making an instance for each movie and storing each into a list called movieInstances

movieInstances = []
for i in range(len(movieList)):
	temp = Movie(movieList[i])
	movieInstances.append(temp)

## Searching twitter for 5 tweets that mention one actor from each movie and finding all mentioned users in the tweets

#allTweets = a list of lists of dictionaries
allTweets = []
usernames = []
tupsList = []#list to be commited to DB
for each in movieInstances:
	#creating a tup to commit each movie instance to the DB
	tup = (each.movieID, each.title, each.director, each.numLangs, each.rating, each.actors[0], each.year)
	tupsList.append(tup)
	print("Searching for tweets about " + each.actors[0])
	tweets = get_tweets(each.actors[0])

	# print(tweets)
	# print('\n')
	allTweets.append(tweets)
	# print (usernames)
	screenNames = [tweet['user']['screen_name'] for tweet in tweets]
	print(screenNames)
	mentions = [tweet['entities']['user_mentions'] for tweet in tweets]
	for each in screenNames:
		usernames.append(each)
	for mention in mentions:
		for m in mention:
			usernames.append(m['screen_name'])

#Inserting the unique users into the database

userEx = 'INSERT INTO Users VALUES (?, ?, ?)'

userIds = []
uniqueUsers = []
for user in usernames:
	inputs = get_user(user)
	userIds.append(inputs['id'])
	if user not in uniqueUsers:
		userTup = (inputs['id'], inputs['screen_name'], inputs['favourites_count'])
		cur.execute(userEx, userTup)
		uniqueUsers.append(user)

#Inserting each tweet into the Database

ex = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'

for i in range(len(umich_tweets)):
	tup = (umich_tweets[i]['id'], umich_tweets[i]['text'], umich_tweets[i]['user']['id'], umich_tweets[i]['created_at'], umich_tweets[i]['retweet_count'])
	cur.execute(ex, tup)

conn.commit()


#Inserting each movie instance into the Database

movieEx = 'INSERT INTO Movies VALUES (?,?,?,?,?,?,?)'

for each in tupsList:
	cur.execute(movieEx, each)


conn.commit()

# Creating a list of movies and then making a call to the omdb database to store the results in a movie dictionary with the title being the dictionary key
# Creating a tweet dictionary that contains the object returned from tweepy when searhing the movie titles from the list made above.



movieTweets = {}



# for each in movieList:
# 	actor = each['Actors'].split(",")[0]
# 	movieTweets[each] = get_tweets(actor)

# print('############')
# for each in movieTweets:
# 	print(movieTweets[each][0]['text'])
# 	print('###########')


# for each in movieList:
# 	print(each)
# 	for data in movieList[each]:
# 		print(data)

# 	print("##################")
	

# List of all keys in tweet
# favorite_count, in_reply_to_user_id, id_str, coordinates, lang, geo, in_reply_to_status_id, in_reply_to_user_id_str, place, retweet_count, is_quote_status, retweeted, user, text, created_at, in_reply_to_status_id_str, source, entities, metadata, in_reply_to_screen_name, favorited, contributors, truncated, id, 





##insert into the databases

## Will change to a function that accepts a list to make the code more modular

# ex = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?)'

# for i in range(len(umich_tweets)):
# 	tup = (umich_tweets[i]['id'], umich_tweets[i]['text'], umich_tweets[i]['user']['id'], umich_tweets[i]['created_at'], umich_tweets[i]['retweet_count'])
# 	cur.execute(ex, tup)

# conn.commit()

##test cases (not a complete list of all tests)
conn.close()

## Most test cases are not going to currently run because the code has not been built out.
class Tests(unittest.TestCase):
	def test_users_4(self):
			conn = sqlite3.connect('movies.db')
			cur = conn.cursor()
			cur.execute('SELECT * FROM Movies');
			result = cur.fetchall()
			self.assertTrue(len(result)==len(movieNames),"Testing that there are same number of movies as passed in")
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