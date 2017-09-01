# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from random import randint
from .models import Video

import requests


# Create your views here.
def index(request):
    request.session['score'] = 0
    return redirect('/youtube')

def reset(request):
    request.session['hiscore'] = 0
    request.session['score'] = 0
    return redirect('/youtube')

def youtube(request):
    # reset hiscore
    if 'hiscore' in request.session:
        print "hiscore exists"
    else:
        request.session['hiscore'] = 0
        print "hiscore reset"
    
    # determine two indexes
    index1 = randint(1, 80)
    index2 = randint(1, 80)
    while index1 == index2:
        index2 = randint(1, 80)

    # load videos from db
    videos = Video.objects.all()
    
    # choose two random songs
    song1 = Video.objects.get(pk=index1)
    song2 = Video.objects.get(pk=index2)

    r1 = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&q=' + song1.title + ' by ' + song1.author +'&type=video&fields=items%2Fid&key=AIzaSyCZ3-8TTK_rQNinKI12rQRubjYenemIlVs')
    url1 = "https://www.youtube.com/embed/" + r1.json()['items'][0]['id']['videoId']

    r2 = requests.get('https://www.googleapis.com/youtube/v3/search?part=id&q=' + song2.title + ' by ' + song2.author + '&type=video&fields=items%2Fid&key=AIzaSyCZ3-8TTK_rQNinKI12rQRubjYenemIlVs')
    url2 = "https://www.youtube.com/embed/" + r2.json()['items'][0]['id']['videoId']

    if (song1.views > song2.views):
        answer = song1
    else:
        answer = song2

    request.session['answer_id'] = answer.id

    context = {
        #'list' : videos,
        'song1' : song1,
        'song2' : song2,
        'answer': answer,
        'url1': url1,
        'url2': url2
    }

    return render(request, 'crawl_app/youtube.html', context)

def answer(request):
    if (request.POST.get('song1')):
        print 'you chose song1'
        chosen_id = request.POST.get('song1')
    elif (request.POST.get('song2')):
        print 'you chose song2'
        chosen_id = request.POST.get('song2')

    print request.session['answer_id'], chosen_id

    if int(request.session['answer_id']) == int(chosen_id):
        request.session['score'] += 1
        print 'correct answer'
    else:
        if request.session['score'] > request.session['hiscore']:
            request.session['hiscore'] = request.session['score']
        print 'wrong answer'
        return redirect('/')
    return redirect('/youtube')