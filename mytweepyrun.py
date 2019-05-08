from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tweepy
import tweepyconstants
import json
from pprint import pprint


class mytweepy: 
	def __init__(self):
		## tweepy authentication 
		consumer_key = tweepyconstants.CONSUMER_KEY 
		consumer_secret = tweepyconstants.CONSUMER_SECRET
		access_token = tweepyconstants.ACCESS_TOKEN
		access_token_secret = tweepyconstants.ACCESS_TOKEN_SECRET

		auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
		auth.set_access_token(access_token, access_token_secret)
		self.api = tweepy.API(auth)


	## tweepy GET location
	def getWOEID(self, city='', country='Worldwide'): 
		jsonA = self.api.trends_available()
		for i in jsonA: 
			if i['name'] == city and i['country'] == country : 
				return i["woeid"]

	## tweepy GET list searchResults, text
	def getSearch(self, language, query, counts, rtype):
		return self.api.search(lang=language, q=query, count=counts, result_type=rtype)

	## tweepy GET list searchResults with Cursor, full_text
	def getfullSearch(self, language, query, counts, rtype):
		return tweepy.Cursor(self.api.search, q=query, tweet_mode='extended', lang=language, result_type=rtype).items(counts)

	## tweepy GET home newsfeed tweets top 20 
	def getHometweet(self): 
		public_tweets = self.api.home_timeline()
		for tweet in public_tweets:
			print()
			print(tweet.text)
		return public_tweets

	## tweepy GET user object 
	def getUserinfo(self):
		user = self.api.get_user('twitter')
		print(user.screen_name)
		print(user.followers_count)
		for friend in user.friends():
		   print(friend.screen_name)
		return user

	## tweepy GET media info
	def getMediainfo(self, tweets):
		for tweet in tweets:
			#print(tweet.entities['media'])
			for image in tweet.entities['media']:
				return image['media_url']

















