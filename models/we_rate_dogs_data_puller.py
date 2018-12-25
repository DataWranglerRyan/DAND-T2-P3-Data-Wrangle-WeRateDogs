import pandas as pd
import requests, io
import json
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

    def get_twitter_data_as_df(self):
        try:
            with open(self.twitter_data_filename) as f:
                return pd.DataFrame([json.loads(row) for row in f])[['id','retweet_count', 'favorite_count']]
            f.close()
        except FileNotFoundError as e:
            print('May need to run write_twitter_data_to_file() to pull data from API.')
            raise e

    def get_combined_data(self):
        archive_and_twitter = pd.merge(self.archive_data, self.get_twitter_data_as_df(),
                                       how='left', left_on='tweet_id', right_on='id')
        return pd.merge(archive_and_twitter, self.images_df, how='left',  on='tweet_id')

    def export_combined_data(self):
        self.get_combined_data().to_csv('../data/combined_data.csv')
