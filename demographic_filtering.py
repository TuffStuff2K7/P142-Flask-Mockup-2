import numpy as np
import pandas as pd

share_df = pd.read_csv("shared_articles.csv")
users_df = pd.read_csv("users_interactions.csv")

eventTypes = list(set(users_df['eventType'].tolist()))
print(eventTypes)

def countEvents(row):
  total_events = 0
  for event in eventTypes:
    total_events = total_events + users_df[(users_df['contentId'] == row['contentId']) & (users_df['eventType'] == event)].shape[0]
  return total_events

share_df['totalEvents'] = share_df.apply(countEvents, axis = 1)

share_df = share_df.sort_values('score', ascending = False)

popular_articles = share_df[['contentId','url','title','text','lang','totalEvents']].head(20).values.tolist()
