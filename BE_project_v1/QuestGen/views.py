from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'QuestGen/index.html')

def taketest(request):
    return render(request, 'QuestGen/taketest.html')
