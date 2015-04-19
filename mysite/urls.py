from django.conf.urls import patterns, include, url
from django.contrib import admin
from mysite.views import playerfeedback,gameover,welcome, about,initgame, attacker, defender,attack_eval,defend_eval, index, survey, exitgame, startgame, questions

urlpatterns = patterns('',
    url(r'^hacker/$', attacker),
    url(r'^analyst/$', defender),
    url(r'^about/$',about),
    url(r'^playerfeedback/$',playerfeedback),
    url(r'^attack_eval/(\d{1,2})/$', attack_eval),
    url(r'^defend_eval/(\d{1,2})/$', defend_eval),
    url(r'^index/$',index),
    url(r'^questions/$',questions),
    url(r'^welcome/$',welcome),
    url(r'^exitgame/$', exitgame),
    url(r'^$',index),
    url(r'^gameover/$',gameover),
    url(r'^startgame/$',startgame),
    url(r'^initgame/$',initgame),
    url(r'^survey/$', survey),
    )
