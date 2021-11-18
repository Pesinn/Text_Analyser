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
def sentiment_scores(sentence):
  # Create a SentimentIntensityAnalyzer object.
  sid_obj = SentimentIntensityAnalyzer()

  # polarity_scores method of SentimentIntensityAnalyzer
  # object gives a sentiment dictionary.
  # which contains pos, neg, neu, and compound scores.
  sentiment_dict = sid_obj.polarity_scores(sentence)
  
  """
  print("=====================")
  print("Sentence:", sentence)
  print("Overall sentiment dictionary is : ", sentiment_dict)
  print("sentence was rated as ", sentiment_dict['neg']*100, "% Negative")
  print("sentence was rated as ", sentiment_dict['neu']*100, "% Neutral")
  print("sentence was rated as ", sentiment_dict['pos']*100, "% Positive")

  print("Sentence Overall Rated As", end = " ")

  # decide sentiment as positive, negative and neutral
  if sentiment_dict['compound'] >= 0.05 :
    print("Positive")

  elif sentiment_dict['compound'] <= - 0.05 :
    print("Negative")

  else :
    print("Neutral")
  """  
  return sentiment_dict

def sentiment_analysis(data):
  return sentiment_scores(data)

def combine_sentiment_scores(score1, score2):
  combined = {}
  for i in score1:
    score = (score1[i] + score2[i])/2.0
    combined[i] = score
  return combined