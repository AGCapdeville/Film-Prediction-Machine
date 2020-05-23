
class CleanFunctions:

    def get_avg_score_dict(self, data, data_col, splitby, col_str):
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

    def clean_f(self, f):
        for e in range(len(f)):
            series = f.iloc[e]
            s = series.to_string(index=False)
            list_s = s.split(',')

            if (len(list_s) >= 3):
                list_s.pop(-1)

            f.at[e] = ','.join(list_s)

        return f
    
    def summation_of_f(self, clean_f, f_score_dict):
        score_sumation = {}
        for index in range(len(clean_f)):      
            total_score = 0     
            length = 0
            for item in clean_f.iloc[index].to_string(index=False).split(','):
                item = item.strip()
                if item in f_score_dict:
                    total_score += f_score_dict[item]
                    length += 1
                else:
                    total_score += 5
                    length += 1
                    
            score_sumation[index] = total_score / length
        return score_sumation

    def drop_redun_data(self, data):
        data.drop('genre', axis='columns', inplace=True)
        data.drop('popularity', axis='columns', inplace=True)
        data.drop('writers', axis='columns', inplace=True)
        data.drop('directors', axis='columns', inplace=True)
        data.drop('title', axis='columns', inplace=True)
        data.drop('rating', axis='columns', inplace=True)
        data.drop('runtime', axis='columns', inplace=True)

        data.drop('level_0', axis="columns", inplace=True)
        data.drop('index', axis="columns", inplace=True)
        return data


    def vectorize_genre(self, df):
        for m in range(len(df)):
            for genres in df.iloc[m][['genre']]:
                list_genre = genres.split(',')
                for g in list_genre:
                    df.at[m, g.strip()] = 1
        return df



# Notes:


# Notes: too many writers for this to be vectoriezed ---------------------------------

# Capture Unique Writers
# dict_unique_writers = []
# for movie in range(len(x_train_writers)):
#     for list_w in x_train_writers.iloc[movie][['writers']]:
#         for w in list_w.split(','):
#             if w not in dict_unique_writers:
#                 dict_unique_writers.append(w.strip())

# print(len(dict_unique_writers))

# writers_set = pd.DataFrame(orient='index', columns=[dict_unique_writers])
# print(writers_set)
# 
# -------------------------------------------------------------------------------------