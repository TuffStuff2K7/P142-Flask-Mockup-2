import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

share_df = pd.read_csv("shared_articles.csv")
users_df = pd.read_csv("users_interactions.csv")

def lowerTitles(row):
  return row['title'].lower().notna()

share_df['title'] = share_df.apply(lowerTitles, axis = 1)

count = CountVectorizer(stop_words = 'english')
count_matrix = count.fit_transform(share_df['title'])

cosine_sim_ = cosine_similarity(count_matrix, count_matrix)

share_df = share_df.reset_index()
indices = pd.Series(share_df.index, index=share_df['title'])

def get_recommendations(title, cosine_sim):
   idx = indices[title]
   sim_scores = list(enumerate(cosine_sim[idx]))
   sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
   sim_scores = sim_scores[1:11]
   article_indices = [i[0] for i in sim_scores]
   return share_df[['contentId','url','title','text','lang','totalEvents']].iloc[article_indices].values.tolist()
