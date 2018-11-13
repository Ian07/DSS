from django.shortcuts import render
import numpy as np
import pandas as pd
from collections import OrderedDict
import math 
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
import operator
from django import template
from bs4 import BeautifulSoup
from urllib.request import urlopen
import imdb

def get_list_urls(df):
    
    pelis = []

    for index, row in df.iterrows():
        # Creamos el objeto que se usa para 
        ia = imdb.IMDb() # by default access the web.
        # Buscamos un peli por su nombre
        movie = ia.get_movie(row['imdbId'])
        # para cada peli vamos imprimir la URL de su poster
        page = urlopen(ia.get_imdbURL(movie))
        soup = BeautifulSoup(page, features='lxml')
        cover_div = soup.find(attrs={"class" : "poster"})
        url = (cover_div.find('img'))['src']
        peli = [row['title'],url]
        pelis.append(peli)
    return pelis

def cosine_measure(v1, v2): 
    return cosine_similarity(np.asmatrix(v1),np.asmatrix(v2))

def get_movie_score(movie_features, peli_features):
    return cosine_measure(movie_features, peli_features)[0][0]

def get_movie_recommendations_content(categorias, df_movies, peli_features, n_recommendations):
    #metemos una columna al dataset movies_df con la puntuacion calculada para el usuario
    for i in range(len(df_movies.index)):
        df_movies.loc[i,'score'] = get_movie_score(df_movies.loc[i][categorias].values,peli_features.values)
    df_rankeado = df_movies.sort_values(by=['score'], ascending=False)
    df_links = pd.read_csv("static/ml-latest-small/links.csv",sep=",")
    df_recomendacion = pd.merge(df_rankeado, df_links, on='movieId')[['title', 'imdbId']]
    return df_recomendacion[:n_recommendations]
    

#Recomendacion por modelo por conenido (similitud de coseno)
def por_contenido(pelicula):
    df_movies = pd.read_csv("static/ml-latest-small/movies.csv",sep=",")
    df_movies = pd.concat([df_movies, df_movies.genres.str.get_dummies(sep='|')], axis=1)
    categorias = df_movies.columns[3:]

    #peli_features = df_movies.loc[df_movies['title'].str.contains('Toy Story (1995)')][:1][categorias]
    peli_features = df_movies.loc[1][categorias]

    pelis_recomendadas = get_movie_recommendations_content(categorias, df_movies, peli_features, 1)

    return get_list_urls(pelis_recomendadas)

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
    #Recomendacion para el usuario
    sample_user = usuario #Numero de user 
    recomendacion_usuario = df_ratings[df_ratings.userId==sample_user].sort_values(by=['rating'], ascending=False)
    
    #return recomendacion_usuario[:10]

    df_links = pd.read_csv("static/ml-latest-small/links.csv",sep=",")

    df_recomendacion = pd.merge(recomendacion_usuario, df_links, on='movieId')[['title', 'imdbId']]

    return get_list_urls(df_recomendacion[:1])

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
            print("ENTRE2")
            pelis = por_contenido(str(peli_idUser))
            print(pelis)
        elif modelo == 2:
            print("ENTRE")
            pelis = colaborativo(int(peli_idUser))
            print(pelis)
        else:
            pass

    else:
        pelis = []
    return render(request, 'index.html', {'pelis': pelis})
