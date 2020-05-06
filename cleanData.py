import numpy
import pandas as pd


with open("./IMDB_MOVIES.csv") as csvfile:
    data = pd.read_csv(csvfile, delimiter=',')

pop = data['popularity']
data.drop('popularity', axis='columns', inplace=True)

pop.dropna(inplace=True)
print("the length of all pop", len(pop))

data.dropna(inplace=True)

print(len(data))
print(data)

# directors,genre,popularity,rating,runtime,title,writers

titles = data['title']
directors = data['directors']
genre = data['genre']
# popularity = data['popularity']
rating = data['rating']
runtime = data['runtime']
writers = data['writers']

print("In Title:",titles.isnull().values.any())
print("In Directors:",directors.isnull().values.any())
print("In Genre:",genre.isnull().values.any())
# print("In popularity:",popularity.isnull().values.any())
print("In rating:",rating.isnull().values.any())
print("In runtime:",runtime.isnull().values.any())
print("In writers:",writers.isnull().values.any())

# df1 = data[data.isna().any(axis=1)]
# print(df1)

# print(allTitles)