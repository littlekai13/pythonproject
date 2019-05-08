import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools
import collections

import tweepy as tw
import nltk
from nltk.corpus import stopwords
import re
import networkx
from itertools import dropwhile
import warnings

warnings.filterwarnings("ignore")

sns.set(font_scale=1.5)
sns.set_style("whitegrid")

nltk.download('stopwords')

def remove_url(txt):
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

def removeExtras(words, term):
	
	stop_words = set(stopwords.words('english'))
	stop_words.add(term)

	clean_tweets = [[word for word in each_words if not word in stop_words] for each_words in words]

	clean_tweets_two = [[word for word in each_words if not len(word)<=2] for each_words in clean_tweets]

	return clean_tweets_two

def getCounter(words):
	# List of all words across tweets
	all_words = list(itertools.chain(*words))
	#print(all_words)

	# Create counter
	all_words_count = collections.Counter(all_words)
	count_list = all_words_count.most_common()
	return count_list

def removeSmall(df):
	return df.drop(df[df['count'] < 4].index) #removes feq=1,2,3

def plotFreq(words, term, twcount):
	count_tweets = pd.DataFrame(words, columns=['words', 'count'])
	count_tweets.head()

	if twcount > 5: #more than 5 tweets
		if count_tweets['count'].max() > 3: #if maxfreq=4,5,...
			count_tweets = removeSmall(count_tweets)
	#print(count_tweets)
	
	if not count_tweets.empty:
		df = count_tweets.sort_values(by='count', ascending=False).plot.barh(x='words', y='count')
		plt.xticks(size = 8)
		plt.yticks(size = 10)
		plt.ylabel('')
		df.set_title(str(count_tweets.shape[0]) +" Words, "+ str(twcount) +" Top Tweets on "+ term )
		plt.tight_layout()
		plt.show()








 





