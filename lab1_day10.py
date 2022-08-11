import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import ast
import chart_studio.plotly as py
from collections import Counter
from wordcloud import WordCloud
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

movies = pd.read_csv('C:/Users/bader/OneDrive/gitlesson/Day10-Lab1-Plotly/dataset/tmdb_5000_movies.csv')
credits = pd.read_csv('C:/Users/bader/OneDrive/gitlesson/Day10-Lab1-Plotly/dataset//tmdb_5000_credits.csv')
# Joining the two datsets
movies = pd.merge(left = movies, right = credits, on='title')
movies = movies.drop(columns=['homepage','tagline','id','overview','status','original_title','movie_id'])

def func(obj):
    List = []
    for i in ast.literal_eval(obj):
        List.append(i['name'])
    return List

movies['genres'] = movies['genres'].apply(func)
movies['production_companies'] = movies['production_companies'].apply(func)
movies['production_countries'] = movies['production_countries'].apply(func)
genres = Counter()
for i in range(movies.shape[0]):
    for j in movies.genres[i]:
        genres[j]+=1
Genres = pd.DataFrame.from_dict(genres, orient='index').reset_index()
Genres = Genres.rename(columns = {'index': 'Genres' ,0: 'Frequency'})
Genres.loc[Genres['Frequency'] < 200, 'Genres'] = 'Others'
#Q1: Use bar chart to draw genres of movies.
fig = px.bar(Genres, x='Genres',y='Frequency',color='Genres',title='Genres of Movies')
fig.show()
#Q2: Use pie chart to draw top 5 languages.
# Top Production Counties
prod_cont = Counter()
for i in range(movies.shape[0]):
    for j in movies.production_countries[i]:
        prod_cont[j]+=1
movie_prod_cont = pd.DataFrame.from_dict(prod_cont, orient='index').reset_index()
movie_prod_cont = movie_prod_cont.rename(columns = {'index': 'Production Country' ,0: 'Frequency'})
movie_prod_cont=movie_prod_cont.sort_values(by = ['Frequency'],ascending=False).reset_index().head(5)

fig = px.pie(movie_prod_cont, values='Frequency', names='Production Country')
fig.show()
#Q3: Use WordCloud to draw genres.
wordcloud = WordCloud(background_color="white").generate(str(Genres['Genres'].values))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()
#Q4: Use scatter to draw the relationship between budget and revenue.
fig = px.scatter(movies,y="budget", x='revenue')
fig.show()
#Q5: Use line chart to draw the relationship between revenue and popularity.
fig = px.line(movies, y="revenue", x="popularity")
fig.show()



