from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from Modules import whGenerator
from Modules import clozeGenerator
from django.contrib import messages
import datetime




def index(request):
    return render(request, 'QuestGen/index.html')


def taketest(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    else:
        context = {}
        if request.method == 'POST':
            count = request.POST.get('count')
            uploaded_file = request.FILES['myDocument']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            if not filename.endswith('.txt'):
                messages.error(request,'Not a Valid File Type')
                return redirect('taketest')
            if count == '':
                messages.error(request,'Enter a valid number of questions')
                return redirect('taketest')
            fileurl = fs.path(filename)
            context['fileurl'] = fileurl
            context['count'] = count
            context['filename'] = filename
            global getContext
            def getContext():
                return context
            return redirect('quiz')
        else:
            return render(request, 'QuestGen/taketest.html')

def quiz(request):
    context = {}
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        post_data = getContext()
        count = int(post_data['count'])
        fileurl = post_data['fileurl']
        curr_datetime = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        filename = post_data['filename']
        wh_questions = whGenerator.sentensify(fileurl)
        wh_questions = wh_questions[:count]
        cloze_questions = clozeGenerator.generateQuestions(fileurl, count)
        context['wh_questions'] = wh_questions
        context['cloze_questions'] = cloze_questions
        context['curr_datetime'] = curr_datetime
        context['filename'] = filename
        return render(request, 'QuestGen/quiz.html', context)
