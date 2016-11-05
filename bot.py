"""
Prep:
1. Make a Twitter account
2. Sign up at https://dev.twitter.com for a developer account
    a. Ensure it has read/write access
3. Make an new app under your development account
4. Generate an access token key pair
5. Rename `twitter_keys_sample.json` to `twitter_keys.json`
6. Copy tokens to their respective fields in `twitter_keys.json`
7. Install tweepy
"""
import json
from datetime import datetime, timedelta
import requests
import tweepy           # python library for sending data to the twitter api

wprdc_api_endpoint = "https://data.wprdc.org/api/3/action/datastore_search_sql"
resource_id = "1797ead8-8262-41cc-9099-cbc8a161924b"

# Get yesterday's date (the current date - 1 day)
yesterday_date = datetime.now() - timedelta(days=1)

# Convert to a string the format the the data center accepts (yyyy-mm-dd)
yesterday_str = yesterday_date.strftime("%Y-%m-%d")

# SQL query we'll use in API call to request data
query = "SELECT count(\"PK\") as count FROM \"{}\" WHERE \"INCIDENTTIME\" >= '{}';".format(resource_id, yesterday_str)

# Make WPRDC API Call
response = requests.get(wprdc_api_endpoint, {'sql': query})

# Parse response JSON into python dictionary
response_data = json.loads(response.text)
count = response_data['result']['records'][0]['count']

# Read twitter keys from file
with open('twitter_keys.json') as f:
    twitter_keys = json.load(f)

consumer_key = twitter_keys['consumer_key']
consumer_secret = twitter_keys['consumer_secret']
access_token_key = twitter_keys['access_token_key']
access_token_secret = twitter_keys['access_token_secret']

# Generate OAth credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

# Create twitter API handler and authorize with credentials
twitter = tweepy.API(auth)

# Tweet our new string
twitter.update_status('Gee willickers! There were {} crime incidents in Pittsburgh yesterday.'.format(count))
