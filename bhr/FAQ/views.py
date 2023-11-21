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
                    'description':'<p> You can check why do I need to login <a href="?q=1">here</a><br></p><p>If you have any question further question please contact me </p>'}
    return render(request, 'faq.html',{"questions":questions_list,"question":question})
