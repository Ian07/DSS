from django.core.management.base import BaseCommand, CommandError
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
import imdb

class Command(BaseCommand):
    help = 'Busca todas las pelis de una foto'

    def handle(self, *args, **options):
        ia = imdb.IMDb() # by default access the web.
        
        df_movies = pd.read_csv("static/ml-latest-small/links.csv",sep=",")
        for index, row in df_movies.iterrows():
            try:
                imdbId = row['imdbId']
                movie = ia.get_movie(imdbId)
                # para cada peli vamos imprimir la URL de su poster
                page = urlopen(ia.get_imdbURL(movie))
                soup = BeautifulSoup(page, features='lxml')
                cover_div = soup.find(attrs={"class" : "poster"})
                url = (cover_div.find('img'))['src']
                urlretrieve(url, "static/posters/{}.jpg".format(imdbId))
            except:
                pass