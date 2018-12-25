import json


class Tweet(object):
    def __init__(self, tweet):
        self.tweet = tweet
        self.data = tweet._json

    def get_clean_data(self):
        return {
            "id": self.data['id'],
            "retweet_count": self.data['retweet_count'],
            "favorite_count": self.data['favorite_count']
        }

    def write_to_file(self, filename):
        f = open(filename, "a+")
        f.write(json.dumps(self.get_clean_data())+"\n")
        f.close()
