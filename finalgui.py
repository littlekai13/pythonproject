from PIL import ImageTk
import PIL.Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tweepy
import tkinter as tk
from tkinter import *
import requests
from io import BytesIO

import tweepyconstants
import mytweepyrun
import termfreq



def go_search():

	lang='en'
	hashtag=""
	term = entry_word.get().strip()
	noRT = " -filter:retweets "
	query = hashtag + term + noRT
	count=100
	rtype='popular' #mixed, recent, popular
	
	if term == '': 
		messagebox.showwarning("Warning","Please type a word.")
	else: 		
		mt = mytweepyrun.mytweepy()
		
		#NOTE:get tweets
		all_tweets = mt.getfullSearch(lang, query, count, rtype='mixed')
		all_tweets = [tweet.full_text for tweet in all_tweets]

		#NOTE:get most popular tweet
		pop_tweet = mt.getfullSearch(lang,query,count, rtype)
		pop_tweet = [tweet.full_text for tweet in pop_tweet]
		
		if all_tweets:
			#NOTE:remove url links
			all_tweets_text = [termfreq.remove_url(tweet) for tweet in all_tweets]
			pop_tweet_text = [termfreq.remove_url(tweet) for tweet in pop_tweet]

			#NOTE:lowercase texts
			all_tweets_text_lower = [tweet.lower().split() for tweet in all_tweets_text]
			pop_tweet_text_lower = [tweet.lower().split() for tweet in pop_tweet_text]

			#NOTE:remove common words
			all_tweets_text_clean = termfreq.removeExtras(all_tweets_text_lower, term)
			pop_tweet_text_clean = termfreq.removeExtras(pop_tweet_text_lower, term)
			
			#NOTE:count frequency of words
			all_word_counter = termfreq.getCounter(all_tweets_text_clean)
			pop_word_counter = termfreq.getCounter(pop_tweet_text_clean)
			
			#NOTE:get most popular photo
			one_tweet = mt.getfullSearch(lang,query+' filter:images',1, rtype)
			image_url = mt.getMediainfo(one_tweet)

			#NOTE:show popular photo and common list
			show_imglist(all_word_counter, image_url, (pop_tweet[0] if pop_tweet else all_tweets[0]))

			#NOTE:plot frequency map of pop list
			termfreq.plotFreq(pop_word_counter,term, len(pop_tweet))
					
		else: 
			messagebox.showwarning("Warning","Oh no! No Results Found in Twitter. Sorry!")


def show_imglist(wordlist, url, poptweet):
	nop = Toplevel()
	scrollbar=Scrollbar(nop, orient=VERTICAL)
	scrollbar.pack(side=RIGHT, fill=Y)
	mylist = Listbox(nop, yscrollcommand=scrollbar.set)
	for tweetcount in wordlist: 
		mylist.insert(END, tweetcount[0] + " ("+ str(tweetcount[1]) + " count)")
	mylist.pack(side=LEFT, fill=BOTH)
	scrollbar.config(command=mylist.yview)

	labelText=StringVar()
	labelText.set(poptweet)
	twlabel = Label(nop, textvariable=labelText, wraplength=480)
	twlabel.pack()

	if url: 
		response = requests.get(url)
		photo = PIL.Image.open(BytesIO(response.content))		
		photo.thumbnail((640,480),PIL.Image.ANTIALIAS)
		img = ImageTk.PhotoImage(photo)
		
		label = Label(nop, image=img)
		label.image=img
		label.pack()


def show_list(wordlist):
	nop = Toplevel()
	scrollbar=Scrollbar(nop, orient=VERTICAL)
	scrollbar.pack(side=RIGHT, fill=Y)
	mylist = Listbox(nop, yscrollcommand=scrollbar.set)
	for tweetcount in wordlist: 
		mylist.insert(END, tweetcount[0] + " ("+ str(tweetcount[1]) + " count)")
	mylist.pack(side=LEFT, fill=BOTH)
	scrollbar.config(command=mylist.yview)


def show_image(path):
	novi = Toplevel()
	canvas = Canvas(novi) #, width=800, height=600)
	canvas.pack(fill="both", expand=True)
	
	gif1 = ImageTk.PhotoImage(file=path)

	canvas.create_image(1,1, anchor=NW, image=gif1)
	canvas.gif1 = gif1

def show_url(url):
	response = requests.get(url)
	photo = PIL.Image.open(BytesIO(response.content))
	#width, height = photo.size
	
	photo.thumbnail((800,600),PIL.Image.ANTIALIAS)
	img = ImageTk.PhotoImage(photo)
	
	novi = Toplevel()
	label = Label(novi, image=img)
	label.image=img
	label.pack()




if __name__ == '__main__':

	app = Tk()
	app.title('Twitter Inferences')

	labelText=StringVar()
	labelText.set("Want to infer about a word? \n Want to see how social media sees it? \n Type a word here to find out: \n Note: based on the first 100 tweets of now.")
	label_intro=Label(app, textvariable=labelText, height=4)
	label_intro.pack()

	userInput=StringVar(None)
	entry_word=Entry(app,textvariable=userInput,width=50)
	entry_word.pack()

	buttonQuit = Button(app, text="Quit", command=quit)
	buttonQuit.pack(side=LEFT)

	buttonGo = Button(app, text="Search", command=go_search)
	buttonGo.pack(side=RIGHT)

	app.mainloop()














