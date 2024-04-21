import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_keyword_sentiment(keyword):
    sid = SentimentIntensityAnalyzer()
    sentiment_score = sid.polarity_scores(keyword)['compound']

    if sentiment_score >= 0.05:
        return "Positive"
    elif sentiment_score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


# Example keywords
# keywords = [
#     "Bhopal Gas tragedy",
#     "Munich Air Disaster",
#     "Battle at Normandy",
#     "NASA Success",
#     "Spain lifts FIFA world cup",
#     "",
#     "Cristiano Ronaldo",
#     "Sachin Tendulkar"
# ]
#
# for keyword in keywords:
#     sentiment = get_keyword_sentiment(keyword)
#     print(f"{keyword} - {sentiment}")