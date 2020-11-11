import pandas as pd 
import tweepy
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

def fetch_tw(ids,output_file):
    list_of_tw_status = api.statuses_lookup(ids, tweet_mode= "extended")
    empty_data = pd.DataFrame()
    for status in list_of_tw_status:
            tweet_elem = {"tweet_id": status.id,
                     "screen_name": status.user.screen_name,
                     "tweet":status.full_text,
                     "date":status.created_at,
                     "likes":status._json['favorite_count'],
                     "retweets":status._json['retweet_count'],
                     "location":status.user.location,
                     "coordinates":status.coordinates,
                     }
            empty_data = empty_data.append(tweet_elem, ignore_index = True)
    empty_data.to_csv(output_file, mode="a")

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

tweet_url = pd.read_csv(input_file, index_col= None, header = None, names = ["links"])
af = lambda x: x["links"].split("/")[-1]
tweet_url['id'] = tweet_url.apply(af, axis=1)
ids = tweet_url['id'].tolist()
total_count = len(ids)
chunks = (total_count - 1) // 50 + 1
print(tweet_url.head())
for i in range(chunks):
        batch = ids[i*50:(i+1)*50]
        result = fetch_tw(batch,output_file)
