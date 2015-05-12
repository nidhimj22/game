from django.db import models

# Create your models here.

class Player(models.Model):
	age= models.IntegerField()
	email= models.EmailField()
	country=models.CharField(max_length=60)
	gender = models.CharField(max_length=20)
	education=models.CharField(max_length=50)
	majorstudy = models.CharField(max_length=100)
	occupation = models.CharField(max_length=100)

"""

class Game(models.Model):
	gametype=models.IntegerField()
	player=models.ForeignKey(Player)
	humanmoves=[]
	playermoves=[]
	winner=models.CharField(max_length=60)
	hackerscore=  models.IntegerField()
	analystscore=models.IntegerField() #scores in the end
	human=models.CharField(max_length=60)  #profile set


"""
class Feedback(models.Model):
	player=models.ForeignKey(Player,null=True)	
	ownstrategy=models.CharField(max_length=1000)
	oppstrategy=models.CharField(max_length=1000)
	influence=models.CharField(max_length=100)
	
 
	
