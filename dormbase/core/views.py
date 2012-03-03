from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from django.contrib.auth.models import User
from dormbase.core.models import Resident
from dormbase.core.models import Room

from django.http import HttpResponse, HttpResponseRedirect, Http404
import json
import itertools

def user_to_dict(user):
    try:
        room, year = user.get_profile().room, user.get_profile().year
    except Resident.DoesNotExist:
        room, year = 'n/a', 'n/a'

    return {
        'id' : user.id,
        'username' : user.username,
        'firstname' : user.first_name,
        'lastname' : user.last_name,
        'room' : str(room), # force room to be serialized
        'year' : str(year),
    }

def resident_to_dict(resident):
    return {
        'id' : resident.user.id,
        'username' : resident.user.username,
        'firstname' : resident.user.first_name,
        'lastname' : resident.user.last_name,
        'room' : str(resident.room), # force room to be serialized
        'year' : str(resident.year),
    }

def directory(request):
    return render_to_response('core/directory.html', context_instance = RequestContext(request))

def directory_json(request):
    resident_results = []
    
    def one_not_empty(d, strings):
        return sum(len(d[s]) for s in strings) > 0
    
    if one_not_empty(request.GET, ['title', 'year', 'room', 'firstname', 'lastname', 'username']):
        resident_results = map(resident_to_dict, Resident.objects
                               .select_related()
                               .distinct()
                               .filter(title__icontains = request.GET['title'])
                               .filter(year__contains = request.GET['year'])
                               .filter(room__number__startswith = request.GET['room'])
                               .filter(user__first_name__icontains = request.GET['firstname'])
                               .filter(user__last_name__icontains = request.GET['lastname'])
                               .filter(user__username__icontains = request.GET['username'])
                               .order_by('user__username'))
        
    jsons = json.dumps({'result' : resident_results})
    return HttpResponse(jsons, mimetype='application/json')

def populate_directory(request):
    f = open('core/names.txt')
    import random
    rooms = []    
    MAX_ROOM = 1000
    for i in range(0, MAX_ROOM):
        r = Room(number = str(i), phone = str(random.randint(1111111111, 9999999999)))
        r.save()
        rooms.extend([r])

    for line in f.readlines():
        if '(' in line:
            continue
        line = line.split(' ')
        firstname, lastname = line[0], line[-1]
        if len(firstname) < 3 or len(lastname) < 3:
            continue
        print 'adding ' + firstname + ' ' + lastname
        username = firstname[0:3] + lastname[0:3] + str(random.randint(0, 99))
        u = User(first_name = firstname, last_name = lastname, username = username)
        u.save()
        r = Resident(user = u,
                     room = random.choice(rooms),
                     athena = username,
                     year = random.choice([2012, 2013, 2014, 2015]),
                     livesInDorm = True)
        r.save()
