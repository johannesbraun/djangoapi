import json
from django.shortcuts import render
from django.http import HttpResponse
import requests
import os
from .models import Greeting
import numpy as np
import pandas as pd
import MySQLdb

users1k = pd.read_csv("hello/data/users1k.csv", index_col=0, header =None)
userFeaturesDict = dict(users1k.T)
productFeaturesNumpy = np.array(pd.read_csv("hello/data/items1k.csv", header =None))

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
    stmt = "select * from blasta.item_tastevectors where tid = %d" %tid
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
    #return sim
    return [[productFeaturesNumpy[i][0], sim[i]] for i in np.argsort(-sim)[0:n]]

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

