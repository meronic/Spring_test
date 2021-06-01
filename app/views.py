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

non_attendance = []

not_taken_lectures = []

# 0 : title
# 1 : 차수
# 3 : 제출기간
# 5 : 제출유무

def checkProject(tempList) : 
    if (tempList[5] == '제출하기') : 
        print(tempList, "save!!")
        inCompleteList.append(tempList)
    elif (tempList[5] == '기간내제출') : 
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
            fileRoute = open("app/reports/"+lecture, 'r')
            while True : 
                line = fileRoute.readline()
                
                if not line : break
                
                print(lecture,line)
            
                
                
                temp = lecture + " "+ line
                tempList = temp.split()
                
                checkProject(tempList)
                line = ""
            fileRoute.close()
            
            ### 미수강 강의
        for lecture in lectures : 
            line = ""
            with open("app/lectures/"+lecture, 'r') as f : 
                while True : 
                    line = f.readline()
                    if not line : break
                    temp = lecture + " "+ line
                    tempList = temp.split()
                    
                    not_taken_lectures.append(tempList)
                    
                    line = ""
        
        init = 1        
                
                

    context = {
        'lectures' : lectures,
        'inCompleteList' : inCompleteList,
        'completeList' : completeList,
        'not_taken_lectures' : not_taken_lectures,
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
        'completeList' : completeList,
        'not_taken_lectures' : not_taken_lectures,
    }

    html_template = loader.get_template( 'dashboard.html', )
    return HttpResponse(html_template.render(context, request))
    


@login_required(login_url="/login/")
def lectureboard(request) : 
    
    context = {
        'lectures' : lectures,
        'inCompleteList' : inCompleteList,
        'completeList' : completeList,
        'not_taken_lectures' : not_taken_lectures,
    }

    html_template = loader.get_template( 'lectureboard.html', )
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def board(request) : 
    
    context = {
        'lectures' : lectures,
        'inCompleteList' : inCompleteList,
        'completeList' : completeList,
        'not_taken_lectures' : not_taken_lectures,
    }

    html_template = loader.get_template( 'board.html', )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def kakaotalk(request) : 
    
    context = {
        'lectures' : lectures,
        'inCompleteList' : inCompleteList,
        'completeList' : completeList,
        'not_taken_lectures' : not_taken_lectures,
    }

    html_template = loader.get_template( 'kakaotalk.html', )
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def notice(request) : 
    
    context = {
        'lectures' : lectures,
        'inCompleteList' : inCompleteList,
        'completeList' : completeList,
        'not_taken_lectures' : not_taken_lectures,
    }

    html_template = loader.get_template( 'notice.html', )
    return HttpResponse(html_template.render(context, request))
