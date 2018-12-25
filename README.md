# DAND-Term2-P3-Data-Wrangle-WeRateDogs

Udacity Data Analyst Nano Degree's Term 2 third project: Wrangle WeRateDogs Twitter Data.

The goal of this project is to gather, assess, clean/tidy, analyze, and then visualize data from the
WeRateDogs twitter feed. WeRateDogs is a feed that allows a community of dog lovers to post
pictures of their dogs as well as rate other people's dogs based on their cuteness. Most of the
time people rate on a scale from 1-10, but intentionally exceed the upper limit of 10 (so, 13
out of 10 is a common rating).The whole process will be done using Python's Pandas library as 
well as some other common libraries like requests and Tweepy.

The required data for this project will be wrangled from three different sources:
1. a csv of Archived Twitter data downloaded manually
2. a tsv of Dog Image Predictions programmatically downloaded using the Requests Library
3. Retweet and Favorite information found in JSON format via Twitter's API

The data cleaning and tidying was mainly done using the Pandas library.

The analysis was done by exporting the final cleaned dataframe to a Sqlite database and running
queries off of that database to gain insight about the data.

The final visualizations were created using Tableau Desktop.

## Dependencies
pandas,
sqlalchemy,
numpy,
requests,
io,
json,
tweepy,
yaml

## Resources
* http://docs.tweepy.org/en/v3.2.0/api.html#API
* https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.melt.html
* https://docs.sqlalchemy.org/en/latest/
* http://docs.python-requests.org/en/master/

