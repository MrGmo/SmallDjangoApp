## polls/views.py
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Question, Choice

def get_question(question_id):
  # this is a helper method we've created since we need to find the question in detail(), results(), and vote()
  return Question.objects.get(id=question_id)

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    data = { 'latest_question_list': latest_question_list }
    return render(request, 'polls/index.html', data)

def detail(request, question_id):
    question = get_question(question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_question(question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_question(question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))