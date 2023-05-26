import pandas as pd
movies=pd.read_csv('data_handling/dataset.csv')

# movies.head(10)
# movies.describe()
# movies.info()
# movies.isnull().sum()
# movies.columns

movies=movies[['id', 'title', 'overview', 'genre']]
# movies

movies_ids=movies[['id', 'title']]
# movies_ids

movies['tags'] = movies['overview']+movies['genre']
# movies

new_data  = movies.drop(columns=['overview', 'genre'])
# new_data

from sklearn.feature_extraction.text import CountVectorizer
cv=CountVectorizer(max_features=10000, stop_words='english')
# cv

vector=cv.fit_transform(new_data['tags'].values.astype('U')).toarray()
vector.shape

from sklearn.metrics.pairwise import cosine_similarity
similarity=cosine_similarity(vector)

# similarity

# new_data[new_data['title']=="The Godfather"].index[0]

# distance = sorted(list(enumerate(similarity[2])), reverse=True, key=lambda vector:vector[1])
# for i in distance[0:5]:
#     print(new_data.iloc[i[0]].title)

def recommand(movies):
    index=new_data[new_data['title']==movies].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    for i in distance[0:5]:
        print(new_data.iloc[i[0]].title)

recommand("Iron Man")


import pickle
pickle.dump(new_data, open('movies_list.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))
pickle.dump(movies_ids, open("movies_ids.pkl", "wb"))

# pickle.load(open('movies_list.pkl', 'rb'))


    # Explination
    # import pandas as pd: This line imports the pandas library, which is commonly used for data manipulation and analysis in Python.

    # movies=pd.read_csv('dataset.csv'): This line reads a CSV file named 'dataset.csv' and stores its contents in a pandas DataFrame called 'movies'. The DataFrame is a tabular data structure used for organizing and analyzing data.

    # # movies.head(10): This line is a commented-out code, so it is not executed. It likely displays the first 10 rows of the 'movies' DataFrame, allowing you to inspect the data.

    # # movies.describe(): Another commented-out code. It would display summary statistics of the numerical columns in the 'movies' DataFrame, such as count, mean, standard deviation, etc.

    # # movies.info(): Another commented-out code. It would provide information about the 'movies' DataFrame, including the number of rows, column names, data types, and memory usage.

    # # movies.isnull().sum(): Another commented-out code. It would count the number of missing values (null values) in each column of the 'movies' DataFrame.

    # # movies.columns: Another commented-out code. It would display the column names of the 'movies' DataFrame.

    # movies=movies[['id', 'title', 'overview', 'genre']]: This line creates a new DataFrame named 'movies' by selecting only the columns 'id', 'title', 'overview', and 'genre' from the original 'movies' DataFrame. The double square brackets [['...']] are used to select multiple columns.

    # # movies: This line is commented out. If executed, it would display the updated 'movies' DataFrame with only the selected columns.

    # movies['tags'] = movies['overview']+movies['genre']: This line creates a new column named 'tags' in the 'movies' DataFrame by concatenating the 'overview' and 'genre' columns. The + operator is used for string concatenation.

    # # movies: Another commented-out line. If executed, it would display the 'movies' DataFrame with the newly added 'tags' column.

    # new_data = movies.drop(columns=['overview', 'genre']): This line creates a new DataFrame named 'new_data' by dropping the 'overview' and 'genre' columns from the 'movies' DataFrame using the drop() function. The columns parameter specifies the columns to be dropped.

    # # new_data: Another commented-out line. If executed, it would display the 'new_data' DataFrame without the 'overview' and 'genre' columns.

    # from sklearn.feature_extraction.text import CountVectorizer: This line imports the CountVectorizer class from the sklearn.feature_extraction.text module. CountVectorizer is used to convert text data into numerical feature vectors.

    # cv=CountVectorizer(max_features=10000, stop_words='english'): This line creates an instance of the CountVectorizer class and assigns it to the variable 'cv'. The 'max_features' parameter specifies the maximum number of features (words) to be extracted, and the 'stop_words' parameter specifies that common English words should be excluded from the feature set.

    # # cv: Another commented-out line. If executed, it would display the CountVectorizer object with its current settings.

    # vector=cv.fit_transform(new_data['tags'].values.astype('U')).toarray(): This line applies the CountVectorizer to the 'tags' column of the 'new_data' DataFrame. It converts the text data into a numerical matrix representation. The resulting
