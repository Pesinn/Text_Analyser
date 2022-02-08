from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

"""
Returns object such as:
{
  "neg": 0.398,
  "neu": 0.602,
  "pos": 0,
  "compound": -0.5106
}
"""
def sentiment_analysis(text):
  sid_obj = SentimentIntensityAnalyzer()
  sentiment_dict = sid_obj.polarity_scores(text)
  return sentiment_dict