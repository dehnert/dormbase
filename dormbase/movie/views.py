# Dormbase -- open-source dormitory database system
# Copyright (C) 2012 Alex Chernyakhovsky <achernya@mit.edu>
#                    Drew Dennison       <dennison@mit.edu>
#                    Isaac Evans         <ine@mit.edu>
#                    Luke O'Malley       <omalley1@mit.edu>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

