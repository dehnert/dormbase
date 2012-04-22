from django.shortcuts import render_to_response, RequestContext
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from dormbase.movie.models import Movie, Genre
from random import sample

from django.http import HttpResponse, HttpResponseRedirect, Http404

def movie_detail(request, movieId):
    payload = {'movie': Movie.objects.get(imdbId = movieId)}
    return render_to_response('movie/movieDetail.html', payload, context_instance=RequestContext(request))

def movie_reserve(request):
    if request.method == 'POST':
        id = request.POST['imdbId']
        m = Movie.objects.get(imdbId = id)
        m.available = False
        m.save()
        return movie_detail(request, id)
    raise Http404

def genre_list(request, genreType):
    genresFilter = Genre.objects.filter(name = genreType)
    selectFilms = [(genreType, Movie.objects.filter(genres = genresFilter).order_by('title'))]

    #print selectFilms

    payload = {'selectFilms' : selectFilms}
    #print payload
    return render_to_response('movie/movies.html', payload, context_instance=RequestContext(request))

def genre_random(request):
    genreList = ['Action',
                 'Adventure',
                 'Comedy',
                 'Drama',
                 'Horror',
                 'Sci-Fi',
                 'Romance',
                 'Thriller']

    selectFilms = []

    for i in genreList:
        filmGenre = Movie.objects.filter(genres = Genre.objects.filter(name = i))
        rands = sample(xrange(len(filmGenre)-1), min(5, len(filmGenre)))
        selectFilms.append((i, [filmGenre[x] for x in rands]))

    payload = {'selectFilms' : selectFilms}
    #print payload
    return render_to_response('movie/movies.html', payload, context_instance=RequestContext(request))

