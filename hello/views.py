import json
from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
from .models import Greeting
import numpy as np
import pandas as pd
import MySQLdb
from collections import OrderedDict

users1k = pd.read_csv("hello/data/users1k.csv", index_col=0, header =None)
userFeaturesDict = dict(users1k.T)
productFeaturesNumpy = np.array(pd.read_csv("hello/data/items100k.csv", header =None))

# connect
con = MySQLdb.connect(
    host="blasta.chiim1n4uxwu.eu-central-1.rds.amazonaws.com", 
    user="blasta", 
    passwd="27051980", 
    db="blasta")
cursor = con.cursor()

# Create your views here.
def index(request):
    times = int(os.environ.get('TIMES',3))
    return HttpResponse('Hello!'*times)

    #r = requests.get('http://httpbin.org/status/418')
    #print r.text
    #return HttpResponse('<pre>' + r.text + '</pre>')
    
    #return HttpResponse('Hello from Python!')

def ureco(request, uid):
    recos = recommendProducts(int(uid))
    return HttpResponse(json.dumps(recos), content_type="application/json")


def treco(request, tid):
    stmt = "select * from blasta.item_tastevectors where tid = %d" %(int(tid))
    result = cursor.execute(stmt)
    vector = cursor.fetchall() 
    v = np.array((vector[0][1:]))
    recos = recommendFast(v,productFeaturesNumpy,50)  
    return HttpResponse(json.dumps(recos), content_type="application/json")

def vreco(request, vector):
    v = np.array([np.float64(d) for d in vector.split(", ")])
    recos = recommendFast(v,productFeaturesNumpy,50)    
    return HttpResponse(json.dumps(recos), content_type="application/json")

def recommendFast(tovector, productFeaturesNumpy, n): 
    sim = np.dot(tovector,productFeaturesNumpy[:,1:].T)
    
    #fetch item info
    idx = np.argsort(-sim)[0:10]
    tracks = {}
    for j, i in enumerate(idx):
        tracks[int(productFeaturesNumpy[i][0])]= {"rank": j, "score": sim[i]}

    ids = str(list(tracks.keys())).strip("[,]")

    stmt = "select tid, username, title, likes, plays from blasta.tracks where tid in (%s)" %(ids)
    result = cursor.execute(stmt)
    dbresponse = cursor.fetchall() 
    track_info ={}
    for i, t in enumerate(dbresponse):
        track_info[int(t[0])] = {"username": t[1], "title": t[2],"likes": t[3], "plays": t[4]}   

    recos = [{ "id" : id, "score": tracks[id]['score'], "title": track_info[id]['title'], "username": track_info[id]['username'],"plays": track_info[id]['plays'],"likes": track_info[id]['likes']} for id in track_info]
    recos.sort(key=lambda x: x['score'], reverse=True)
    return recos
    # return [[productFeaturesNumpy[i][0], sim[i]] for i in np.argsort(-sim)[0:n]]

def recommendProducts(user, n=50):
    #print "users in userFeaturesDict", userFeaturesDict.keys() # empty!!!
    #tovector = model.userFeatures().lookup(user)[0] # fetch users' vector 
    tovector = userFeaturesDict[user] # fetch users' vector 
    print tovector
    return recommendFast(tovector,productFeaturesNumpy,n) # find closest product 
    

def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

