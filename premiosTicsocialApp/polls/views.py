from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from .models import Question,Choice
from django.urls import reverse
from django.views import generic
from django.utils import timezone

# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(request, "polls/index.html",{
#         "latest_question_list": latest_question_list
#     })

# def detail(request, question_id):
#    question = get_object_or_404(Question, pk=question_id )
#    return render(request, "polls/datail.html",{
#        "question":question
#    } )
# def result(request, question_id):
#    question= get_object_or_404(Question, pk=question_id)
#    return render(request, "polls/results.html",{
#        "question": question
#    })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        # escluir todas la preguntas qur todavia no se han publicado todavia 
        
        return Question.objects.filter(pub_data__lte=timezone.now()).order_by("-pub_data")[:5]
    

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/datail.html"
    def get_queryset(self):
        # escluir todas la preguntas qur todavia no se han publicado todavia 
        
        return Question.objects.filter(pub_data__lte=timezone.now())
    
class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
 question = get_object_or_404(Question, pk=question_id)
 try:
    selected_choice= question.choice_set.get(pk=request.POST["choice"])
 except (KeyError, Choice.DoesNotExist):
     return render(request, "polls/datail.html",{
         "question": question,
         "error_message": "No elegiste una respuesta"
     })
 else:
     selected_choice.votes += 1
     selected_choice.save()
     return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))