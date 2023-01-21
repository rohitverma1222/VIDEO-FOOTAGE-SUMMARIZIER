from django.urls import path,include
from . views import *
urlpatterns = [
    path('',home,name="home"),
    path('dashboard',dashBoard,name="dashBoard"),
    path('setting',setting,name="setting"),
    path('access',access,name="access"),
    path('previousClip',previous,name="previous"),
    path('dashboard/<int:id>/',dashboard,name="dashBoard"),

]
