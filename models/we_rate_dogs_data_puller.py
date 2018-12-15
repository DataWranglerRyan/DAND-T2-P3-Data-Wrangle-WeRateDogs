import pandas as pd
import requests, io
import tweepy
import yaml
from models.tweet import Tweet


class WeRateDogsDataPuller(object):
    def __init__(self):
        self.secrets = self.get_secrets()
        self.api = self.connect_twitter_api()
        self.archive_data = self.get_archive_data()
        self.images_url = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
        self.images_df = self.get_image_data()
        self.twitter_data_filename = '../data/tweet_json.txt'
        self.tweets_with_404 = []

    def get_secrets(self):
        with open('../config/secrets.yaml', 'r') as yml:
            try:
                return yaml.load(yml)
            except yaml.YAMLError as exc:
                print(exc)

    def get_archive_data(self):
        return pd.read_csv('../data/twitter-archive-enhanced.csv')

    def get_image_data(self):
        r = requests.get(self.images_url)
        return pd.read_csv(io.StringIO(r.content.decode('utf-8')), sep='\t')

    def connect_twitter_api(self):
        auth = tweepy.OAuthHandler(self.secrets['consumer_key'], self.secrets['consumer_secret'])
        auth.set_access_token(self.secrets['access_token'], self.secrets['access_secret'])

        return tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    def write_twitter_data_to_file(self):
        # Clear contents of file
        open(self.twitter_data_filename, 'w').close()
        # Write new content to file
        for index, tweet_id in self.archive_data.tweet_id.iteritems():
            try:
                Tweet(self.api.get_status(tweet_id)).write_to_file(self.twitter_data_filename)
            except tweepy.TweepError as e:
                self.tweets_with_404.append(tweet_id)
                print(str(tweet_id) + ': ' + e.reason)
            print(index)
        print(self.tweets_with_404)

wrd = WeRateDogsDataPuller()
print(wrd.get_archive_data().head())
print(wrd.get_image_data().head())
print(wrd.get_secrets())
# wrd.write_twitter_data_to_file()