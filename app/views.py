# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from . import eclass

init = 0
lectures = []
lectureSize = 0
codeList = []

inCompleteList = []
completeList = []

# 0 : title
# 1 : 차수
# 4 : 제출기간
# 6 : 제출유무

def checkProject(tempList) : 
    if (tempList[6] == '제출하기') : 
        print(tempList, "save!!")
        inCompleteList.append(tempList)
    elif (tempList[6] == '기간내제출') : 
        completeList.append(tempList)



@login_required(login_url="/login/")
def index(request):
    global init
    global lectureSize
    global codeList
    global lectures
    
    
    if (init == 0) : 

        lectures = eclass.projectList
        lectureSize = len(lectures)
        codeList = eclass.codeList

        for lecture in lectures : 
            fileRoute = open("app/lectures/"+lecture, 'r')
            while True : 
                line = fileRoute.readline()
                
                if not line : break
                
                print(lecture,line)
            
                
                
                temp = lecture + " "+ line
                tempList = temp.split()
                
                checkProject(tempList)
                line = ""
            fileRoute.close()
        
        init = 1        
                
                

    context = {
        'lectures' : lectures,
        'inCompleteList' : inCompleteList,
    }
    context['segment'] = 'index'

    html_template = loader.get_template( 'index.html', )
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:
        
        load_template      = request.path.split('/')[-1]
        context['segment'] = load_template
        
        html_template = loader.get_template( load_template )
        return HttpResponse(html_template.render(context, request))
        
    except template.TemplateDoesNotExist:

        html_template = loader.get_template( 'page-404.html' )
        return HttpResponse(html_template.render(context, request))

    except:
    
        html_template = loader.get_template( 'page-500.html' )
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def dashboard(request) : 
    
    context = {
        'lectures' : lectures,
        'inCompleteList' : inCompleteList,
    }

    html_template = loader.get_template( 'dashboard.html', )
    return HttpResponse(html_template.render(context, request))
    


