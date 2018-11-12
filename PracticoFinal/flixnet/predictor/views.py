from django.shortcuts import render
import numpy as np
import pandas as pd
from collections import OrderedDict
import math 
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import operator



def dot_product(vector_1, vector_2):
    return sum([ i*j for i,j in zip(vector_1, vector_2)])

def cosine_measure(v1, v2): 
    return cosine_similarity(np.asmatrix(v1),np.asmatrix(v2))

def get_movie_score(movie_features, user_preferences):
    return cosine_measure(movie_features, user_preferences)[0][0]

def get_movie_recommendations(user_preferences, n_recommendations):
    #metemos una columna al dataset movies_df con la puntuacion calculada para el usuario
    for i in range(len(df_movies.index)):
        df_movies.loc[i,'score'] = get_movie_score(df_movies.loc[i][categorias].values,jumanji_features.values)
    return df_movies.sort_values(by=['score'], ascending=False)['title'][:n_recommendations]
    


#Recomendacion por modelo por conenido (similitud de coseno)
def por_contenido():
    df_movies = pd.read_csv("static/ml-latest-small/movies.csv",sep=",")
    df_movies = pd.concat([df_movies, df_movies.genres.str.get_dummies(sep='|')], axis=1)
    categorias = df_movies.columns[3:]
    df_movies.loc[1]
    user_preferences = OrderedDict(zip(categorias, []))

    user_preferences['Action'] = 1
    user_preferences['Adventure'] = 1
    user_preferences['Animation'] = 1
    user_preferences["Children's"] = 1
    user_preferences["Comedy"] = 1
    user_preferences['Crime'] = 1
    user_preferences['Documentary'] = 1
    user_preferences['Drama'] = 1
    user_preferences['Fantasy'] = 1
    user_preferences['Film-Noir'] = 1
    user_preferences['Horror'] = 5
    user_preferences['Musical'] = 1
    user_preferences['Mystery'] = 1
    user_preferences['Romance'] = 1
    user_preferences['Sci-Fi'] = 1
    user_preferences['War'] = 1
    user_preferences['Thriller'] = 1
    user_preferences['Western'] = 1

    jumanji_features = df_movies.loc[1][categorias]

    jumanji_features.values


    pelis_recomendadas = get_movie_recommendations(user_preferences, 20)

    return pelis_recomendadas

#--------------------------------------------------------------------------------------------#

def get_movie_similarity(movie_title):
    '''Devuelve el vector de correlación para una película'''
    movie_idx = list(movie_index).index(movie_title)
    return corr_matrix[movie_idx]

def get_movie_recommendations(user_movies):
    '''Dado un grupo de películas, devolver las mas similares'''
    movie_similarities = np.zeros(corr_matrix.shape[0])
    for movie_id in user_movies:
        movie_similarities = movie_similarities + get_movie_similarity(movie_id)
    similarities_df = pd.DataFrame({
        'movie_title': movie_index,
        'sum_similarity': movie_similarities
        })
    similarities_df = similarities_df[~(similarities_df.movie_title.isin(user_movies))]
    similarities_df = similarities_df.sort_values(by=['sum_similarity'], ascending=False)
    return similarities_df


#Recomendacion por modelo colaborativo (Pearson)
def colaborativo(usuario):
    #leemos los CSV
    df_ratings = pd.read_csv("static/ml-latest-small/ratings.csv",sep=",")
    df_movies = pd.read_csv("static/ml-latest-small/movies.csv",sep=",")
    #borramos la columna
    del df_ratings['timestamp']
    #Mergeamos los CSV
    df_ratings = pd.merge(df_ratings, df_movies, on='movieId')[['userId', 'title', 'movieId','rating']]
    #Creamos la tabla
    ratings_mtx_df = df_ratings.pivot_table(values='rating', index='userId', columns='title')
    ratings_mtx_df.fillna(0, inplace=True)
    movie_index = ratings_mtx_df.columns
    #correlación de Pearson(PMCC) 
    corr_matrix = np.corrcoef(ratings_mtx_df.T)
    corr_matrix.shape
    """
    favoured_movie_title = 'Batman Forever (1995)'
    favoured_movie_index = list(movie_index).index(favoured_movie_title)
    P = corr_matrix[favoured_movie_index]
    list(movie_index[(P>0.4) & (P<1.0)])
    """
    #Recomendacion para el usuario
    sample_user = usuario #Numero de user 
    recomendacion_usuario = df_ratings[df_ratings.userId==sample_user].sort_values(by=['rating'], ascending=False)
    
    #return recomendacion_usuario[:10]

    df_links = pd.read_csv("static/ml-latest-small/links.csv",sep=",")

    df_recomendacion = pd.merge(recomendacion_usuario, df_links, on='movieId')[['title', 'imdbId']]


 #--------------------------------------------------------------------------------------------#

#Recomendacion por red neuronal
def red_neuronal():
    pass


def vista(request):

    if request.method == 'POST':
        print("-------------------------------------")
        print(request.POST)
        print("-------------------------------------")
        peli_idUser = request.POST.get('entrada', False)
        modelo = int(request.POST.get('contenido', False))
        if modelo == 1:
            pass
        elif modelo == 2:
            print("ENTRE")
            pelis = colaborativo(int(peli_idUser))
            print(pelis)
        else:
            pass

    else:
        pass
    return render(request, 'index.html', {'pelis': pelis})
