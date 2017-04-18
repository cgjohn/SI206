import unittest 
import itertools 
import collections 
import tweepy 
# import twitter_info
import json
import requests
import collections
import sqlite3 

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

if __name__ == "__main__":
	unittest.main(verbosity=2)
