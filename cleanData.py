from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import OneHotEncoder
import numpy
import pandas as pd
from sklearn.model_selection import train_test_split




with open("./IMDB_MOVIES.csv") as csvfile:
    data = pd.read_csv(csvfile, delimiter=',')

pop = data['popularity']
data.drop('popularity', axis='columns', inplace=True)

pop.dropna(inplace=True)
# print("the length of all pop", len(pop))

data.dropna(inplace=True)
data.reset_index(inplace=True)



target = []
bad_count = 0
good_count = 0
for rating in data["rating"]:
    if(rating < 7.5):
        target.append("Bad")
        bad_count += 1
    else:
        target.append("Good")
        good_count += 1

print("Good:", good_count, "\nBad: ", bad_count)

# Our data split ----------------------------------------------------------------------------------










def get_avg_score_dict(data, data_col, splitby, col_str):
    data_dict = {}
    for index in range(len(data_col)):            
        for item in data_col.iloc[index].to_string(index=False).split(splitby):
            item = item.strip()
            if not (item in data_dict):
                data_dict[item] = [data.iloc[index]["rating"], 1]
            else:
                data_dict[item][1] += 1
                data_dict[item][0] += data.iloc[index]["rating"]

    for e in data_dict:
        data_dict[e] = data_dict[e][0] / data_dict[e][1]

    return data_dict





genres = ["Comedy", "Drama", "Short", "Family", "Romance", "Talk-Show",
          "Animation", "Music", "Adventure", "Fantasy", "Action",
          "Sci-Fi", "News", "Crime", "Game-Show", "Mystery", "Musical",
          "Horror", "Thriller", "Reality-TV", "Documentary", "Sport",
          "History", "Western", "Biography", "War", "Film-Noir", "Adult"]


writers = data[['writers']]

# print("type:", type(writers))
# print("writers[0]:", writers[0])
# print("writers.iloc[0]:", writers.iloc[0])


for e in range(len(writers)):
    series = writers.iloc[e]
    s = series.to_string(index=False)
    list_s = s.split(',')

    if (len(list_s) >= 3):
        list_s.pop(-1)

    writers.iloc[e] = ','.join(list_s)


writers_score_dict = get_avg_score_dict(data, writers, ',', 'writers')
# data.drop('writers', axis='columns', inplace=True)
# print(writers_score_dict)

print("We are here writing about the writers!!!!!!!!!!!!!!!!!!!!!!")

i = 0    
writers_score_sumation = {}

for index in range(len(writers)):      
    total_score = 0      
    length = 0
    for item in writers.iloc[index].to_string(index=False).split(','):
        item = item.strip()
        total_score += writers_score_dict[item]
        length += 1
    writers_score_sumation[index] = total_score / length

newWritersScores = pd.DataFrame.from_dict(writers_score_sumation, orient='index', columns=['writers'])

print("length of newDataframe:", len(newWritersScores))
print("length of data:", len(data))

data.drop('writers', axis='columns', inplace=True)


data = pd.concat([data, newWritersScores], axis=1)
data.drop("index", axis='columns', inplace=True)



# genre_dict = get_avg_score_dict(data,data["genre"], True, ',', 'genre')
data.drop('genre', axis='columns', inplace=True)
# directors_dic = data["directors"]
data.drop('directors', axis='columns', inplace=True)
# title = data["title"]
data.drop('title', axis='columns', inplace=True)

data.drop('rating', axis='columns', inplace=True)








knn = KNeighborsClassifier(n_neighbors=2)
x_train, x_test, y_train, y_test = train_test_split( data, target, test_size=0.20 )

knn.fit(x_train, y_train)
prediction = knn.predict(x_test)
report = classification_report(y_test, prediction)

print(report)

































# knn = KNeighborsClassifier(n_neighbors=3)

# x_train, x_test, y_train, y_test = train_test_split(
#     data, target, test_size=0.20)


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
