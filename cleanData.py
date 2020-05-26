import numpy as np
import pandas as pd
from sklearn.metrics import classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from cleanFunctions import CleanFunctions
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
import math  


cf = CleanFunctions()

with open("./IMDB_MOVIES.csv") as csvfile:
    data = pd.read_csv(csvfile, delimiter=',')


data['writers'].fillna('iamnotaperson', inplace=True)

data.dropna(inplace=True)
data.reset_index(inplace=True)

company_data = data['company']
date_data = data['year']
stars_data = data['stars']

print('data total:',len(data))
print(50*'=')
print('Lengths of features AFTER NAN drop:')
print('company_data length:',len(company_data))
print('date_data length:',len(date_data))
print('stars_data length:',len(stars_data))
print(50*'=')

# Target Data ---------------------------------------------------------------------------------------


all_ratings = data["rating"]

all_ratings = all_ratings.sort_values()

sumOfRating = all_ratings.sum()
average = sumOfRating/len(all_ratings)


target = []
bad_count = 0
good_count = 0

for rating in data["rating"]:
    if(rating < 7.1 ):
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

x_train, x_test, y_train, y_test = train_test_split( data, target, test_size=0.20, random_state=142 )

x_train.reset_index(inplace=True)
x_test.reset_index(inplace=True)




# MPAA ----------------------------------------------------------------------------------
# mpaa_categ = ['Approved','G','GP','NC-17','Not Rated','PG','PG-13','Passed','R','Unrated','X']

# ohe = OneHotEncoder(categories = "auto", sparse = False)
# le = preprocessing.LabelEncoder()

# x_train['mpaa'] = le.fit_transform(x_train["mpaa"])

# cols = le.classes_

# temp = ohe.fit_transform(x_train[["mpaa"]])
# x_train_1 = x_train.drop(['mpaa'], axis=1)
# ohe_column = pd.DataFrame(temp, columns = cols)
# x_train = pd.concat([x_train_1, ohe_column],axis = 1)



# x_test['mpaa'] = le.fit_transform(x_test["mpaa"])
# temp_test = ohe.fit_transform(x_test[["mpaa"]])
# x_test_1 = x_test.drop(['mpaa'], axis=1)
# ohe_column_test = pd.DataFrame(temp_test, columns = cols)
# x_test = pd.concat([x_test_1, ohe_column_test],axis=1)

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



# Stars ----------------------------------------------------------------------------------

stars_dict = cf.get_avg_score_dict(x_train, x_train[['stars']], ',')

x_trian_stars_score_sum = cf.summation_of_avg_f(x_train[['stars']], stars_dict)
x_test_stars_score_sum = cf.summation_of_avg_f(x_test[['stars']], stars_dict)

x_train_stars = pd.DataFrame.from_dict(x_trian_stars_score_sum, orient='index', columns=['actors'])
x_test_stars = pd.DataFrame.from_dict(x_test_stars_score_sum, orient='index', columns=['actors'])

x_train = pd.concat([x_train, x_train_stars], axis=1)
x_test = pd.concat([x_test, x_test_stars], axis=1)

# company ----------------------------------------------------------------------------------

company_dict = cf.get_avg_score_dict(x_train, x_train[['company']], ',')

x_trian_company_score_sum = cf.summation_of_avg_f(x_train[['company']], company_dict)
x_test_company_score_sum = cf.summation_of_avg_f(x_test[['company']], company_dict)

x_train_company = pd.DataFrame.from_dict(x_trian_company_score_sum, orient='index', columns=['companys'])
x_test_company = pd.DataFrame.from_dict(x_test_company_score_sum, orient='index', columns=['companys'])

x_train = pd.concat([x_train, x_train_company], axis=1)
x_test = pd.concat([x_test, x_test_company], axis=1)

# Director ----------------------------------------------------------------------------------

# Cleaned writer dataset:
x_train_directors = cf.clean_f(x_train[['directors']])
x_test_directors = cf.clean_f(x_test[['directors']])


# Retrieved dictionary of existing writer average movie scores (Out of our trained data)
directors_score_dictionary = cf.get_avg_score_dict(x_train, x_train_directors, ',')

# # Per movie, retrieved and summed writers scores
x_trian_director_score_sum = cf.summation_of_avg_f(x_train_directors, directors_score_dictionary)
x_test_director_score_sum = cf.summation_of_avg_f(x_test_directors, directors_score_dictionary)

# # Converting our director dictionaries into dataframe columns
x_train_directors = pd.DataFrame.from_dict(x_trian_director_score_sum, orient='index', columns=['director'])
x_test_directors = pd.DataFrame.from_dict(x_test_director_score_sum, orient='index', columns=['director'])

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
writers_score_dictionary = cf.get_avg_score_dict(x_train, x_train_writers, ',')
# Replace NAN writers with a fair score. (We net 100+ new data points this way)
writers_score_dictionary['iamnotaperson'] = 5
# print('i am not a person:', writers_score_dictionary['iamnotaperson'])

# Per movie, retrieved and summed writers scores
x_trian_writer_score_sum = cf.summation_of_avg_f(x_train_writers, writers_score_dictionary)
x_test_writer_score_sum = cf.summation_of_avg_f(x_test_writers, writers_score_dictionary)

# Converting our writer dictionaries into dataframe columns
x_train_writers = pd.DataFrame.from_dict(x_trian_writer_score_sum, orient='index', columns=['writer'])
x_test_writers = pd.DataFrame.from_dict(x_test_writer_score_sum, orient='index', columns=['writer'])

# Concatinating our writer dataframe columns to their respective dataframes
x_train = pd.concat([x_train, x_train_writers], axis=1)
x_test = pd.concat([x_test, x_test_writers], axis=1)


dropList = ['genre','writers','directors','title','rating','level_0','index','stars','company','mpaa']
x_train = cf.drop_batch_data(x_train, dropList)
x_test = cf.drop_batch_data(x_test, dropList)


# KNN ----------------------------------------------------------------------------------

print(x_train.shape)
print(x_test.shape)
print(x_test.columns)


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





# PCA ----------------------------------------------------------------------------------

from sklearn.decomposition import PCA

n = 3
pca = PCA(n_components=n)
pca.fit(x_train)
x_train_proj = pca.transform(x_train)
x_test_proj = pca.transform(x_test)


print("\nExplained variance ratio (for ",n,"components):")
print(pca.explained_variance_ratio_, "\n")


k = 5
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(x_train_proj, y_train)
prediction = knn.predict(x_test_proj)
report = classification_report(y_test, prediction)

print(70*"=","\n")
print(" --- PCA ---")
print(report)
print(70*"=")



# Logistic Regression ----------------------------------------------------------------------------------

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

clf = LogisticRegression(random_state=142)
clf.fit(x_train, y_train)
predicted = clf.predict(x_test)

accuracy = (accuracy_score(y_test, predicted))

print(70*"=")
print("Logistic Regression Data Accuracy: ",accuracy,'\n')



# Logistic Regression w/ PCA ----------------------------------------------------------------------------------

clf2 = LogisticRegression(random_state=142)
clf2.fit(x_train_proj, y_train)
predicted2 = clf2.predict(x_test_proj)

print(70*"=")
print("Logistic Regression w/PCA Data Accuracy: ",accuracy,'\n')
