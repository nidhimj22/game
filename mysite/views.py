from django.http import HttpResponse
from django.template.loader import get_template
from newapp.models import Player
from newapp.models import Feedback
from django import template
import os
import time
import datetime
from django.http import HttpResponseRedirect
import random
import re
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template import RequestContext
from django.shortcuts import render_to_response
from mysite import research

attack_mat=research.attack_mat
defence_mat=research.defence_mat
p=research.p
newplayer = Player()
newfeedback=Feedback()

def playerfeedback(request):
    return render_to_response('playerfeedback.html')

def startgame(request):
#    newplayer = Player()
    newplayer.age=request.POST.get("age", "")    
    newplayer.email=request.POST.get("email", "")    
    newplayer.country=request.POST.get("country", "")    
    newplayer.occupation=request.POST.get("occupation", "")
    newplayer.gender=request.POST.get("gender", "")
    newplayer.education=request.POST.get("education", "")
    newplayer.majorstudy=request.POST.get("majorfield", "")
    newplayer.save()

    flag=random.randint(1,2)
    if flag is 1:
        request.session["profile"] = "Hacker"
    else:
        request.session["profile"] = "Analyst"
    request.session['trials']=research.trials
    request.session['h1']=attack_mat[0][0]
    request.session['h2']=attack_mat[0][1]
    request.session['h3']=attack_mat[1][0]
    request.session['h4']=attack_mat[1][1]

    request.session['a1']=defence_mat[0][0]
    request.session['a2']=defence_mat[0][1]
    request.session['a3']=defence_mat[1][0]
    request.session['a4']=defence_mat[1][1]

    request.session['trialnumber']=0
    request.session["extra_h"]=0 #extra hacker score
    request.session["extra_a"]=0 #extra analyst score
    request.session["score_h"]=1000 #hacker score
    request.session["score_a"]=1000 #analyst score
    request.session["choice_h"]="None" #prev_move of hacker
    request.session["choice_a"]="None" #prev move of analsyt

    pageTemplate = get_template("startgame.html")
    c = template.Context(request.session)
    return HttpResponse(pageTemplate.render(c))


def questions(request):
    return render_to_response('questions.html',)


def welcome(request):
    if request.GET.get('validage', 'no')=='no':
        return HttpResponseRedirect('/index')
    if request.GET.get('readInformation', 'no')=='no':
        return HttpResponseRedirect('/index')
    if request.GET.get('participate', 'no')=='no':
        return HttpResponseRedirect('/index')

    return render_to_response('welcome.html',)


def initgame(request):
    if request.session["profile"] == "Hacker":
        return HttpResponseRedirect("/hacker")
    else:
        return HttpResponseRedirect("/analyst")

def gameover(request):
    if request.session['score_h']>request.session['score_a']:
        request.session['winner']="Hacker"
    elif request.session['score_a']>request.session['score_h']:
	request.session['winner']="Analyst"
    else:
        request.session['winner']="None. Game was a tie."
    pageTemplate = get_template("gameover.html")
    c = template.Context(request.session)
    return HttpResponse(pageTemplate.render(c))
         
    
def attacker(request):
    if request.session['trials']>0:
        pageTemplate= get_template("hacker.html")
        c = template.Context(request.session)
        request.session['trials']=int(request.session['trials'])-1
        request.session['trialnumber']=int(request.session['trialnumber'])+1
        return HttpResponse(pageTemplate.render(c))
    else:
        return HttpResponseRedirect("/gameover")

def defender(request):
    if request.session['trials']>0:
        pageTemplate= get_template("analyst.html")
    	c = template.Context(request.session)
        request.session['trials']=int(request.session['trials'])-1
        request.session['trialnumber']=int(request.session['trialnumber'])+1
    	return HttpResponse(pageTemplate.render(c))
    else:
	return HttpResponseRedirect("/gameover")

def defend_eval(request, action):
    action=int(action)
    temp = random.randint(1, 100)
    if temp<p:
        auto_mov=0
    else:
        auto_mov=1

    if auto_mov==1:
        request.session["choice_h"]="Not Attack"
    else:
        request.session["choice_h"]="Attack"
    if action==1:
	request.session["choice_a"]="Not Defend"
    else:
        request.session["choice_a"]="Defend"
    request.session["extra_h"]=attack_mat[auto_mov][action]
    request.session["extra_a"]=defence_mat[auto_mov][action]
    request.session["score_h"]+=attack_mat[auto_mov][action]
    request.session["score_a"]+=defence_mat[auto_mov][action]
    return HttpResponseRedirect("/analyst")


def attack_eval(request, action):
    action=int(action)
    temp = random.randint(1, 100)
    if temp<p:
        auto_mov=0
    else:
        auto_mov=1

    if auto_mov==1:
        request.session["choice_a"]="Not Defend"
    else:
        request.session["choice_a"]="Defend"
    if action==1:
	request.session["choice_h"]="Not Attack"
    else:
        request.session["choice_h"]="Attack"
    request.session["extra_h"]=attack_mat[auto_mov][action]
    request.session["extra_a"]=defence_mat[auto_mov][action]
    request.session["score_h"]+=attack_mat[action][auto_mov]
    request.session["score_a"]+=defence_mat[action][auto_mov]
    return HttpResponseRedirect("/hacker")




def survey(request):
    return render_to_response('survey.html',)

def index(request):
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return render_to_response('index.html',)


def exitgame(request):
    newfeedback.player=newplayer
    newfeedback.ownstartegy=request.POST.get("ownstrategy","")
    newfeedback.oppstrategy=request.POST.get("oppstrategy","")
    newfeedback.influence=request.POST.get("influence","")
    newfeedback.save()
    return render_to_response('exitgame.html',)

