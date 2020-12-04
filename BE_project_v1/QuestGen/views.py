from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    return render(request, 'QuestGen/index.html')


def taketest(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'QuestGen/taketest.html')

def quiz(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    return render(request, 'QuestGen/quiz.html')
