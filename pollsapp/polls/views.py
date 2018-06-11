from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
import datetime
from .models import Choice, Question
from django.template import loader
from django.urls import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('id')[:20]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def template(request):
    return render(request, 'polls/template.html', {})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#
#def today_is(request):

#    now = datetime.datetime.now()

#    t = template.loader.get_template('polls/datetime.html')

#    c = template.Context({'now': now})

#    html = t.render(c)

#    return HttpResponse(html)