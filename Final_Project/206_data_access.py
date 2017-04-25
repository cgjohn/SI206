import unittest 
import itertools 
import collections 
import tweepy 
import twitter_info
import json
import requests
import collections
import sqlite3 
import omdb #pip install omdb
import re 
from emoji import UNICODE_EMOJI #pip install emoji



# Connor Johnston - Final SI 206 Project


##### TWEEPY SETUP CODE: # Authentication information is in a twitter_info file 
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
 
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


	def main_actor(self):
		return self.actors[0]

	def __str__(self):
		return "{} by {} made in {}".format(self.title,self.director,self.year)



## creating the user, tweet, and ombd databases and starting the db connection

conn = sqlite3.connect('final.db')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Tweets')
cur.execute('CREATE TABLE Tweets(tweet_id TEXT PRIMARY KEY, text TEXT, user_id TEXT, time_posted TIMESTAMP, retweets INTEGER, movie_id INTEGER)')

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
		response =  api.search(q=key, include_rts=True, count=30)['statuses']
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

# decide if a char is an emoji
def is_emoji(s):
    return s in UNICODE_EMOJI

#Create a list of dictionaries of three chosen movies

movieNames = ["Avengers", "Date Night", "Inception"]
movieList = []

for movie in movieNames:
	movieList.append(get_movie(movie))

# Making an instance for each movie and storing each instance into a list called movieInstances

movieInstances = []
for i in range(len(movieList)):
	temp = Movie(movieList[i])
	movieInstances.append(temp)

## Searching twitter for 5 tweets that mention one actor from each movie and finding all mentioned users in the tweets

allTweets = [] #allTweets is a list of lists of dictionaries
usernames = []
tupsList = [] #list to be commited to DB
for each in movieInstances:
	#creating a tup to commit each movie instance to the DB
	tup = (each.movieID, each.title, each.director, each.numLangs, each.rating, each.main_actor(), each.year)
	tupsList.append(tup)
	# print("Searching for tweets about " + each.main_actor())
	tweets = get_tweets(each.main_actor())

	# print(tweets)
	# print('\n')
	allTweets.append(tweets)
	# print (usernames)
	screenNames = [tweet['user']['screen_name'] for tweet in tweets]
	# print(screenNames)
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

ex = 'INSERT INTO Tweets VALUES (?, ?, ?, ?, ?, ?)'

IDTag = 0
count = 0
for tweets in allTweets:
	IDTag = movieInstances[count].movieID
	for i in range(len(tweets)):
		tup = (tweets[i]['id'], tweets[i]['text'], tweets[i]['user']['id'], tweets[i]['created_at'], tweets[i]['retweet_count'], IDTag)
		cur.execute(ex, tup)
	count += 1


#Inserting each movie instance into the Database

movieEx = 'INSERT INTO Movies VALUES (?,?,?,?,?,?,?)'

for each in tupsList:
	cur.execute(movieEx, each)


conn.commit()

## Creating a set comprehension of all the words in the gathered tweets
cur.execute('SELECT text FROM Tweets')
allText = cur.fetchall()

allWords = []
for each in allText:
	sentences = each[0].split(" ")
	for word in sentences:
		allWords.append(word)

setCompWords = {word for sentence in allText for word in sentence[0].split(" ")}


print("There are " + str(len(setCompWords)) + " total different words in the {} tweets found".format(str(len(allText))) )
print('\n')
## using regex to find how many lings are shared and thus being able to give a % of tweets that share links


links = []
for word in allWords:
	link = re.findall('^http\S+', word);
	if link:
		links.append(link)


percentLinks = len(links) / len(allText) * 100

print("roughly {0:.2f}".format(percentLinks) + "%" + " of all tweets contained a link (num links / num tweets)")
print('\n')
##Finds how many emojis are used using the collections counter

count = collections.Counter()

for word in allWords:
	count.update(word)

numEmoji = 0
numChars = 0

for each in count:
	numChars += count[each] 
	if is_emoji(each):
		numEmoji += count[each]

emojiPerc = numEmoji / numChars 

print( str(numEmoji)+" emojis are used which is {0:.6f}% of all characters".format(emojiPerc))
print('\n')


## using the db to get all tweets associated with a movie title
cur.execute('SELECT Movies.title, Tweets.text FROM Movies INNER JOIN Tweets ON Movies.movie_id = Tweets.movie_id')
result = cur.fetchall()

#creating a dictionary of movie title as key and tweet as text
diction = collections.defaultdict(list)

for tweet in result:
	diction[tweet[0]].append(tweet[1])

movieTweetDict = dict(diction)

movieTweetList = []


for movie in movieInstances:
	movieTweetList.append(movieTweetDict[movie.title])

avgTweetLength = []
for movie in movieTweetList:
	total = 0
	for each in movie:
		total += len(each)
	avgTweetLength.append(total / len(movie))

longestTweetsIndex = [i for i,x in enumerate(avgTweetLength) if x == max(avgTweetLength)][0]

longestTweets = movieInstances[longestTweetsIndex].title

print("{} has the longest tweets with an average length of {} characters".format(longestTweets, max(avgTweetLength)))
print('\n')

## Finds the tweet with the most retweets and  returns movie, actor, and tweet
cur.execute('SELECT Tweets.text, Movies.actor, Movies.title, MAX(Tweets.retweets)  FROM Movies INNER JOIN Tweets ON Movies.movie_id = Tweets.movie_id')
mostPopTweet = cur.fetchall()[0]

print('The most popular tweet was "{}" with {} retweets mentioning {} who was in the movie {}'.format(mostPopTweet[0], mostPopTweet[3], mostPopTweet[1], mostPopTweet[2]))


conn.close()

##Test cases
class Tests(unittest.TestCase):
	def test_movie_entries(self):
			conn = sqlite3.connect('final.db')
			cur = conn.cursor()
			cur.execute('SELECT Movies.title FROM Movies');
			result = cur.fetchall()
			print(len(result))
			self.assertTrue(len(result)==len(movieNames),"Testing that there are same number of movies as passed in")
			conn.close()

	def test_caching(self):
			fstr = open("final_cache.json","r")
			self.assertTrue(movieInstances[0].title in fstr.read())
			fstr.close()

	def test_num_tweets(self):
		conn = sqlite3.connect('final.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Tweets');
		result = cur.fetchall()
		self.assertTrue(len(result)>=2, "Testing there are at least 2 records in the Tweets database")
		conn.close()

	def test_nume_users(self):
		conn = sqlite3.connect('final.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Users');
		result = cur.fetchall()
		self.assertTrue(len(result)>=2,"Testing that there are at least 2 distinct users in the Users table")
		conn.close()

	def test_mov_cols(self):
		conn = sqlite3.connect('final.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM Movies');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==7,"Testing that there are 7 columns in the movies database")
		conn.close()

	def test_user_cols(self):
		conn = sqlite3.connect('final.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM users');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==3,"Testing that there are 3 columns in the Users database")
		conn.close()

	def test_tweet_cols(self):
		conn = sqlite3.connect('final.db')
		cur = conn.cursor()
		cur.execute('SELECT * FROM tweets');
		result = cur.fetchall()
		self.assertTrue(len(result[0])==6,"Testing that there are 6 columns in the Tweets database")
		conn.close()

	def test_main_actor(self):
		self.assertTrue(movieInstances[0].main_actor() == movieInstances[0].actors[0])

	def test_main_actor2(self):
		self.assertTrue(movieInstances[0].main_actor() != movieInstances[1].actors[0])

	def test__str__(self):
		self.assertTrue(movieInstances[0].__str__(), "The Avengers by Josh Whedon made in 2012")

	def test__str__2(self):
		self.assertTrue(type(movieInstances[0].__str__()), "")
if __name__ == "__main__":
	unittest.main(verbosity=2)