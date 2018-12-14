import pandas as pd
import requests, io

class WeRateDogsDataPuller(object):
    def __init__(self):
        pass

    def get_archive_data(self):
        print("hello world")
        return pd.read_csv('../data/twitter-archive-enhanced.csv')

    def get_request(self):
        r = requests.get('https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv')
        data = io.StringIO(r.content.decode('utf-8'))
        return pd.read_csv(data, sep='\t')

print(WeRateDogsDataPuller().get_archive_data().head())
print(WeRateDogsDataPuller().get_request().head())