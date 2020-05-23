import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from cleanFunctions import CleanFunctions
import math  


cf = CleanFunctions()

with open("./IMDB_MOVIES.csv") as csvfile:
    data = pd.read_csv(csvfile, delimiter=',')

# directors,genre,popularity,rating,runtime,title,writers
# directors,


data['writers'].fillna('iamnotaperson', inplace=True)

data.dropna(inplace=True)
data.reset_index(inplace=True)

print('data total:',len(data))

# Target Data ---------------------------------------------------------------------------------------


all_ratings = data["rating"]

all_ratings = all_ratings.sort_values()

sumOfRating = all_ratings.sum()
average = sumOfRating/len(all_ratings)
# print( "AVG: ", average )


target = []
bad_count = 0
good_count = 0

for rating in data["rating"]:
    if(rating < 7.3 ):
        target.append(0) #Bad
        bad_count += 1
    else:
        target.append(1) #Good
        good_count += 1

print("Good:", good_count, "\nBad: ", bad_count)

# Data Plot ---------------------------------------------------------------------------------------
import matplotlib.pyplot as plt

# ratings_data = data["rating"]
# ratings_data = ratings_data.sort_values()
# ratings_data = ratings_data.reset_index()
# ratings_data.drop('index', axis="columns", inplace=True)
# print(ratings_data)
# plt.plot(ratings_data, 'bo')

# y = [item for item in range(1, 10)] 
# print(y)
# plt.scatter(ratings_data,y)
# plt.show()


# Splitting our data ----------------------------------------------------------------------------------

# TODO: can do this if we have time...
#       np.random.seed, takes care of random

x_train, x_test, y_train, y_test = train_test_split( data, target, test_size=0.20, random_state=42 )

x_train.reset_index(inplace=True)
x_test.reset_index(inplace=True)

# Genres ----------------------------------------------------------------------------------
genres = ["Comedy", "Drama", "Short", "Family", "Romance", "Talk-Show",
          "Animation", "Music", "Adventure", "Fantasy", "Action",
          "Sci-Fi", "News", "Crime", "Game-Show", "Mystery", "Musical",
          "Horror", "Thriller", "Reality-TV", "Documentary", "Sport",
          "History", "Western", "Biography", "War", "Film-Noir", "Adult"]

genres.sort()
blank_genres = pd.DataFrame(columns=genres)

x_train = pd.concat([x_train, blank_genres], axis=1)
x_test = pd.concat([x_test, blank_genres], axis = 1)

x_train.fillna(value=0,inplace=True)
x_test.fillna(value=0,inplace=True)

x_train = cf.vectorize_genre(x_train)
x_test = cf.vectorize_genre(x_test)


# Director ----------------------------------------------------------------------------------

# Cleaned writer dataset:
x_train_directors = cf.clean_f(x_train[['directors']])
x_test_directors = cf.clean_f(x_test[['directors']])


# Retrieved dictionary of existing writer average movie scores (Out of our trained data)
directors_score_dictionary = cf.get_avg_score_dict(x_train, x_train_directors, ',', 'directors')

# # Per movie, retrieved and summed writers scores
x_trian_director_score_sum = cf.summation_of_f(x_train_directors, directors_score_dictionary)
x_test_director_score_sum = cf.summation_of_f(x_test_directors, directors_score_dictionary)

# # Converting our director dictionaries into dataframe columns
x_train_directors = pd.DataFrame.from_dict(x_trian_director_score_sum, orient='index', columns=['directors'])
x_test_directors = pd.DataFrame.from_dict(x_test_director_score_sum, orient='index', columns=['directors'])

# # Concatinating our director dataframe columns to their respective dataframes
# print(x_train_directors)
x_train = pd.concat([x_train, x_train_directors], axis=1)
x_test = pd.concat([x_test, x_test_directors], axis=1)

# print(x_test)

# Writers ----------------------------------------------------------------------------------

# Cleaned writer dataset:
x_train_writers = cf.clean_f(x_train[['writers']])
x_test_writers = cf.clean_f(x_test[['writers']])

# Retrieved dictionary of existing writer average movie scores (Out of our trained data)
writers_score_dictionary = cf.get_avg_score_dict(x_train, x_train_writers, ',', 'writers')
# Replace NAN writers with a fair score. (We net 100+ new data points this way)
writers_score_dictionary['iamnotaperson'] = 5
# print('i am not a person:', writers_score_dictionary['iamnotaperson'])

# Per movie, retrieved and summed writers scores
x_trian_writer_score_sum = cf.summation_of_f(x_train_writers, writers_score_dictionary)
x_test_writer_score_sum = cf.summation_of_f(x_test_writers, writers_score_dictionary)

# Converting our writer dictionaries into dataframe columns
x_train_writers = pd.DataFrame.from_dict(x_trian_writer_score_sum, orient='index', columns=['writers'])
x_test_writers = pd.DataFrame.from_dict(x_test_writer_score_sum, orient='index', columns=['writers'])

# Concatinating our writer dataframe columns to their respective dataframes
x_train = pd.concat([x_train, x_train_writers], axis=1)
x_test = pd.concat([x_test, x_test_writers], axis=1)


x_train = cf.drop_redun_data(x_train)
x_test = cf.drop_redun_data(x_test)


# KNN ----------------------------------------------------------------------------------


from sklearn.metrics import accuracy_score
# we need to do a 5 fold cross validation test now... to really see how good this is...
k_test_score = []
for n in range(1,20):
    knn = KNeighborsClassifier(n_neighbors=n)
    knn.fit(x_train, y_train)
    prediction = knn.predict(x_test)
    k_test_score.append(accuracy_score(y_test,prediction, normalize=True))
    
best_n =  k_test_score.index(max(k_test_score)) + 1
print("Best Score is:", max(k_test_score), "K:", best_n)

knn = KNeighborsClassifier(n_neighbors=best_n)
knn.fit(x_train, y_train)
prediction = knn.predict(x_test)
report = classification_report(y_test, prediction)


print(70*"=","\n")
print(report)
print(70*"=")


# NN ----------------------------------------------------------------------------------

import tensorflow as tf

x_train_list = x_train.values.tolist()
x_test_list = x_test.values.tolist()

y_test = np.array(y_test)
y_train = np.array(y_train)

print("Types:", "\nx_test:",type(x_test_list), '\nx_train:',type(x_train_list), '\ny_test:', type(y_test))

print("number of columns:", len(x_train.columns) )


norm_x_train = tf.keras.utils.normalize(x_train_list, axis = 1)
norm_x_test = tf.keras.utils.normalize(x_test_list, axis = 1)

model_0 = tf.keras.models.Sequential()
model_0.add(tf.keras.layers.Dense(28, activation='relu'))
model_0.add(tf.keras.layers.Dense(128))
model_0.add(tf.keras.layers.Dense(2, activation='softmax'))

model_0.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model_0.fit(norm_x_train, y_train, batch_size=32, epochs=50)


val_loss, val_acc = model_0.evaluate(norm_x_test, y_test)
print(40*"=")
print("activation = relu:")
print("loss:",val_loss, ", acc:",val_acc)
print(40*"=")

