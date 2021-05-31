# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path, include
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('dashboard', views.dashboard, name='dashboardPage'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
