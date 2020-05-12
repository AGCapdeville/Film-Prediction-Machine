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


x_train, x_test, y_train, y_test = train_test_split( data, target, test_size=0.20 )

x_train.reset_index(inplace=True)
x_test.reset_index(inplace=True)


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


def clean_writers(writers):
    for e in range(len(writers)):
        series = writers.iloc[e]
        s = series.to_string(index=False)
        list_s = s.split(',')

        if (len(list_s) >= 3):
            list_s.pop(-1)

        writers.iloc[e] = ','.join(list_s)
    return writers

clean_x_train_writers = clean_writers(x_train[['writers']])
clean_x_test_writers = clean_writers(x_test[['writers']])

x_train_writers_score_dict = get_avg_score_dict(x_train, clean_x_train_writers, ',', 'writers')
# x_test_writers_score_dict = get_avg_score_dict(x_test, clean_x_test_writers, ',', 'writers')



def summation_of_writers(clean_writers, writers_score_dict):
    writers_score_sumation = {}
    for index in range(len(clean_writers)):      
        total_score = 0     
        length = 0
        for item in clean_writers.iloc[index].to_string(index=False).split(','):
            item = item.strip()
            if item in writers_score_dict:
                # print("writer is in the score dictionary")
                total_score += writers_score_dict[item]
                length += 1
            else:
                total_score += 5
                length += 1
                # print("writer is not in score dictionary")
                
        writers_score_sumation[index] = total_score / length
    return writers_score_sumation

# TODO: exclude test writer score data from test, only use what is in trained
# Thats why these are the same: x_train_writers_score_dict
x_trian_writer_score_sum = summation_of_writers(clean_x_train_writers, x_train_writers_score_dict)
x_test_writer_score_sum = summation_of_writers(clean_x_test_writers, x_train_writers_score_dict)

new_x_train_writers_scores = pd.DataFrame.from_dict(x_trian_writer_score_sum, orient='index', columns=['writers'])
new_x_test_writers_scores = pd.DataFrame.from_dict(x_test_writer_score_sum, orient='index', columns=['writers'])


x_train.drop('writers', axis='columns', inplace=True)
x_test.drop('writers', axis='columns', inplace=True)

x_train = pd.concat([x_train, new_x_train_writers_scores], axis=1)
x_train.drop("index", axis='columns', inplace=True)

x_test = pd.concat([x_test, new_x_test_writers_scores], axis=1)
x_test.drop("index", axis='columns', inplace=True)


def drop_data(data):
    data.drop('genre', axis='columns', inplace=True)
    data.drop('directors', axis='columns', inplace=True)
    data.drop('title', axis='columns', inplace=True)
    data.drop('rating', axis='columns', inplace=True)
    return data

x_train = drop_data(x_train)
x_test = drop_data(x_test)


print(5*"\n")

knn = KNeighborsClassifier(n_neighbors=5)

knn.fit(x_train, y_train)
prediction = knn.predict(x_test)
report = classification_report(y_test, prediction)

print(70*"=","\n")
print(report)
print(70*"=")


# we need to do a 5 fold cross validation test now... to really see how good this is...





























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
