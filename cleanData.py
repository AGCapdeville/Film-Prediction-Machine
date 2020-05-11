import numpy
import pandas as pd
from sklearn.model_selection import train_test_split




with open("./IMDB_MOVIES.csv") as csvfile:
    data = pd.read_csv(csvfile, delimiter=',')

pop = data['popularity']
data.drop('popularity', axis='columns', inplace=True)

pop.dropna(inplace=True)
print("the length of all pop", len(pop))

data.dropna(inplace=True)
data.reset_index(inplace = True)
# print(len(data))
# print(data)


# target_ratings = data["rating"]
# data.drop('rating', axis='columns', inplace=True)
target = []
bad_count = 0
good_count = 0
for rating in data["rating"]:
    if(rating < 7.5):
        target.append("Bad")
        bad_count+=1
    else:
        target.append("Good")
        good_count+=1

print("Good:", good_count, "\nBad: ",bad_count)



# cleaning:

# directors,genre,rating,runtime,title,writers

writers = data["writers"]
data.drop('writers', axis='columns', inplace=True)

genre = data["genre"]
data.drop('genre', axis='columns', inplace=True)

directors = data["directors"]
data.drop('directors', axis='columns', inplace=True)

title = data["title"]
data.drop('title', axis='columns', inplace=True)


#  Cleaning up writers
# print("========================================================")
# print(writers)
for index in range(len(writers)):
    splitUp = writers[index]
    splitUp = splitUp.split(',')
    if len(splitUp) >= 3:
        splitUp.pop(-1)
    writers[index] = str(splitUp)

# print(writers[0])
print("========================================================")
from sklearn.preprocessing import OneHotEncoder

# ohe = OneHotEncoder()
# w = ohe.fit_transform(writers)
# print(w[0])

writer_dict = {}

# for index in range(len(writers)):
#     for w in writers[index].split(','):
#         if not (w in writer_dict):
#             writer_dict[index] = w

from sklearn.feature_extraction.text import CountVectorizer

count_vector = CountVectorizer(binary = True)
count_vector.fit()

# Attempt # 0
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report

knn = KNeighborsClassifier(n_neighbors=3)

x_train, x_test, y_train, y_test = train_test_split(data, target, test_size=0.20)


# strings wont work here.........
# actor names -> need to get actor avg movie score,
# same for: directors, writers, genre, (runtime?)

# ohe = OneHotEncoder(categories = "auto",sparse = False)

# X = dff[['directors','genre','rating','runtime','title','writers']]

# x_train_enc = ohe.fit_transform(x_train)
# x_test_enc = ohe.fit_transform(x_test)



# director_dummy = pd.get_dummies(data['director'])


# knn.fit(x_train, y_train)

# prediction = knn.predict(x_test)
# report = classification_report(y_test, prediction)
# print(report)






# directors,genre,popularity,rating,runtime,title,writers

# titles = data['title']
# directors = data['directors']
# genre = data['genre']
# # popularity = data['popularity']
# rating = data['rating']
# runtime = data['runtime']
# writers = data['writers']

# print("In Title:",titles.isnull().values.any())
# print("In Directors:",directors.isnull().values.any())
# print("In Genre:",genre.isnull().values.any())
# # print("In popularity:",popularity.isnull().values.any())
# print("In rating:",rating.isnull().values.any())
# print("In runtime:",runtime.isnull().values.any())
# print("In writers:",writers.isnull().values.any())

# df1 = data[data.isna().any(axis=1)]
# print(df1)

# print(allTitles)



