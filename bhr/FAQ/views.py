from django.shortcuts import render
from .models import FAQ
from django.http import Http404
# Create your views here.


def faq(request):
    questions = FAQ.objects.all()
    questions_list = []
    for question in questions:
        questions_list.append((question.question_id,question.title))
    
    question_id = request.GET.get('q')
    if question_id:
        try:
            question = FAQ.objects.get(question_id=question_id)
        except FAQ.DoesNotExist:
            raise Http404("Question does not exist")
    else:
        question = {'title':'FQA',
                    'description':'You can check why do I need to login <a href="?q=1">here</a><br>And if you have any question that is not here please contact me'}
    return render(request, 'FAQ.html',{"questions":questions_list,"question":question})