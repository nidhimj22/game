from django.http import HttpResponse
from django.template.loader import get_template
from newapp.models import Player
from newapp.models import Feedback
from newapp.models import Game
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

def playerfeedback(request):
    return render_to_response('playerfeedback.html')


def startgame(request):
    newplayer = Player()
    newplayer.age=request.POST.get("age", "")    
    newplayer.email=request.POST.get("email", "")    
    newplayer.country=request.POST.get("country", "")    
    newplayer.occupation=request.POST.get("occupation", "")
    newplayer.gender=request.POST.get("gender", "")
    newplayer.education=request.POST.get("education", "")
    newplayer.majorstudy=request.POST.get("majorfield", "")
    newplayer.save()
    request.session['playerid']=newplayer.id
   
    request.session['hackermoves']=[]
    request.session['analystmoves']=[]
   # flag=random.randint(1,2)
   # if flag is 1:
    request.session["profile"] = "Hacker"
   # else:
    #    request.session["profile"] = "Analyst"

   
    request.session['gamematrix'] = 1  #random.randint(1,3)
    if request.session['gamematrix'] is 2:
        request.session['trials'] = research.trials2
        attack_mat=research.attack_mat2
        defence_mat=research.defence_mat2
        request.session['base']=research.base2
        request.session['p']= research.p2
        request.session['q'] = research.q2
     
    elif request.session['gamematrix'] is 3:
        request.session['trials'] = research.trials2
        attack_mat=research.attack_mat2
        request.session['base']=research.base3
        defence_mat=research.defence_mat2
        request.session['p']= research.p2
        request.session['q'] = research.q2
     
    else:
        request.session['trials'] = research.trials1
        attack_mat=research.attack_mat1
        request.session['base']=research.base1
        defence_mat=research.defence_mat1
        request.session['p']= research.p1
        request.session['q'] = research.q1

   
    request.session['h1']=attack_mat[0][0]
    request.session['h2']=attack_mat[0][1]
    request.session['h3']=attack_mat[1][0]
    request.session['h4']=attack_mat[1][1]

    request.session['a1']=defence_mat[0][0]
    request.session['a2']=defence_mat[0][1]
    request.session['a3']=defence_mat[1][0]
    request.session['a4']=defence_mat[1][1]

    request.session['trialnumber']=1
    request.session["extra_h"]=0 #extra hacker score
    request.session["extra_a"]=0 #extra analyst score
    request.session["score_h"]=request.session['base'] #hacker score
    request.session["score_a"]=request.session['base'] #analyst score
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

    newgame = Game()
    newgame.player=Player.objects.get(id=request.session['playerid'])
    newgame.gametype=request.session['gamematrix']
    newgame.hackermoves=request.session['hackermoves']
    newgame.analystmoves=request.session['analystmoves']
    newgame.winner=request.session["winner"]
    newgame.analystscore=request.session['score_a']
    newgame.hackerscore=request.session['score_h']
    newgame.human=request.session["profile"] 
    newgame.save()

    pageTemplate = get_template("gameover.html")
    c = template.Context(request.session)
    return HttpResponse(pageTemplate.render(c))
         
    
def attacker(request):
    if request.session['trials']>0:
        pageTemplate= get_template("hacker.html")
        c = template.Context(request.session)
        return HttpResponse(pageTemplate.render(c))
    else:
        request.session['trialnumber']=request.session['trialnumber']-1
        return HttpResponseRedirect("/gameover")


def defender(request):
    if request.session['trials']>0:
        pageTemplate= get_template("analyst.html")
    	c = template.Context(request.session)
    	return HttpResponse(pageTemplate.render(c))
    else:
        request.session['trialnumber']=request.session['trialnumber']-1
	return HttpResponseRedirect("/gameover")


def defend_eval(request, action):
    request.session['trials']=int(request.session['trials'])-1
    request.session['trialnumber']=int(request.session['trialnumber'])+1

    action=int(action)
    temp = round(random.random()*100,2) 
    print temp
    if temp<=request.session['p']:
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

    if auto_mov ==0 and action == 0:
        request.session["extra_h"]=request.session["h1"]
        request.session["extra_a"]=request.session["a1"]
        request.session["score_h"]+=request.session["h1"]
        request.session["score_a"]+=request.session["a1"]

    if auto_mov ==0 and action == 1:
        request.session["extra_h"]=request.session["h3"]
        request.session["extra_a"]=request.session["a3"]
        request.session["score_h"]+=request.session["h3"]
        request.session["score_a"]+=request.session["a3"]

    if auto_mov ==1 and action == 0:
        request.session["extra_h"]=request.session["h2"]
        request.session["extra_a"]=request.session["a2"]
        request.session["score_h"]+=request.session["h2"]
        request.session["score_a"]+=request.session["a2"]

    if auto_mov ==1 and action == 1:
        request.session["extra_h"]=request.session["h4"]
        request.session["extra_a"]=request.session["a4"]
        request.session["score_h"]+=request.session["h4"]
        request.session["score_a"]+=request.session["a4"]

    sessionlist = request.session['hackermoves']
    sessionlist+=`auto_mov`
    request.session['hackermoves'] = sessionlist
    

    sessionlist = request.session['analystmoves']
    sessionlist+=`action`
    request.session['analystmoves'] = sessionlist
    
    
    return HttpResponseRedirect("/analyst")


def attack_eval(request, action):
    request.session['trials']=int(request.session['trials'])-1
    request.session['trialnumber']=int(request.session['trialnumber'])+1

    action=int(action)
    temp = round(100*random.random(),2)
    print temp
    if temp<=request.session['q']:
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

    
    if auto_mov ==0 and action == 0:
        request.session["extra_h"]=request.session["h1"]
        request.session["extra_a"]=request.session["a1"]
        request.session["score_h"]+=request.session["h1"]
        request.session["score_a"]+=request.session["a1"]

    if auto_mov ==0 and action == 1:
        request.session["extra_h"]=request.session["h2"]
        request.session["extra_a"]=request.session["a2"]
        request.session["score_h"]+=request.session["h2"]
        request.session["score_a"]+=request.session["a2"]

    if auto_mov ==1 and action == 0:
        request.session["extra_h"]=request.session["h3"]
        request.session["extra_a"]=request.session["a3"]
        request.session["score_h"]+=request.session["h3"]
        request.session["score_a"]+=request.session["a3"]

    if auto_mov ==1 and action == 1:
        request.session["extra_h"]=request.session["h4"]
        request.session["extra_a"]=request.session["a4"]
        request.session["score_h"]+=request.session["h4"]
        request.session["score_a"]+=request.session["a4"]

    sessionlist = request.session['hackermoves']
    sessionlist+=`action`
    request.session['hackermoves'] = sessionlist
    

    sessionlist = request.session['analystmoves']
    sessionlist+=`auto_mov`
    request.session['analystmoves'] = sessionlist
    

    return HttpResponseRedirect("/hacker")


def survey(request):
    return render_to_response('survey.html',)


def index(request):
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return render_to_response('index.html',)


def exitgame(request):
    newfeedback = Feedback()
    newfeedback.player=Player.objects.get(id=request.session['playerid'])
    newfeedback.ownstrategy=request.POST.get("ownstrategy",)
    newfeedback.oppstrategy=request.POST.get("oppstrategy","")
    newfeedback.influence=request.POST.get("influence")
    newfeedback.save()
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return render_to_response('exitgame.html',)

