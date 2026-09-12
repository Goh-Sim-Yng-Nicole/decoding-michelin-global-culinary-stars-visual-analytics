import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")

reviews = pd.read_csv("restaurant_reviews.csv")

sia = SentimentIntensityAnalyzer()

print("Running sentiment analysis...")

def sentiment_score(text):

    score = sia.polarity_scores(str(text))

    return score["compound"]

reviews["sentiment_score"] = reviews["review_text"].apply(sentiment_score)

reviews.to_csv("reviews_with_sentiment.csv", index=False)

print("Sentiment analysis completed")

print("Saved dataset: reviews_with_sentiment.csv")