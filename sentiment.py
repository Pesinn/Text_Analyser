import SentimentAnalysis.External.vader as vader

def sentiment_analysis(data):
  return vader.sentiment_analysis(data)

def combine_sentiment_scores(score1, score2):
  combined = {}
  for i in score1:
    score = (score1[i] + score2[i])/2.0
    combined[i] = score
  return combined