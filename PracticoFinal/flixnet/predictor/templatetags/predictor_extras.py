from django import template
from bs4 import BeautifulSoup
from urllib.request import urlopen
import imdb

register = template.Library()


@register.filter
def dame_url(value):
    
    # Creamos el objeto que se usa para 
    ia = imdb.IMDb() # by default access the web.

    # Buscamos un peli por su nombre
    movie = ia.get_movie(value)
    # para cada peli vamos imprimir la URL de su poster
    page = urlopen(ia.get_imdbURL(movie))
    soup = BeautifulSoup(page, features='lxml')
    cover_div = soup.find(attrs={"class" : "poster"})
    cover_url = (cover_div.find('img'))['src']
    return cover_url