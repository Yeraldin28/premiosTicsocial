import datetime

from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse

def create_question(question_text, days): 
        # se crea una pregunta con question dado en el parametro,
        # y publicada con diferecia del moneto actual
        #numero de nrgativo para preguntas publicas en el pasado y numero positivo para preguntas en el futuro 
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text = question_text, pub_data = time) 
    
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_questions(self):
        # was_published_recently returns False for questions whose pub_date is in the futur
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿quien es el mejor director de proyecto?", pub_data=time)
        self.assertIs(future_question.was_published_recenrly(), False) #se verifica si al hacer la configuracion se realizan los cambios 
        
        
class QuestionAfterTests(TestCase):
    
# al momneto de realizar las preguntas en un pasado revisaremos 
    def test_de_las_preguntas_con_un_tiempo_mayor_a_un_dia(seft):
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(question_text="¿quien es el mejor director de proyecto?", pub_data=time)
        seft.assertIs(future_question.was_published_recenrly(), False)
   
    
        
class QuestionIndexViewTest(TestCase):
    #si no existe alguna pregunta vamos a poner el error apropiado
    
    
    def test_no_question(seft):
        response = seft.client.get(reverse("polls:index"))
        seft.assertEqual(response.status_code, 200)
        seft.assertContains(response, "No tienen ninguna variable ")
        seft.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_mquestion(seft):
        #no publique preguntas que se crearon en el futuro 
        create_question("future question", days=30)
        response = seft.client.get(reverse("polls:index"))
        seft.assertContains(response, "No tienen ninguna variable " )
        seft.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_past_question(seft):
        # cunado la pregunte este en paso de los dias se mire en el index 
        question = create_question("past question", days=-30)
        response = seft.client.get(reverse("polls:index"))
        seft.assertQuerysetEqual(response.context["latest_question_list"], [question])
        
    def test_two_question_past_future(seft):
    # "" cunado se publique una pregunta de manera futura y otra en pasado que se visualizen solo la del pasado
        pass_question = create_question(question_text="past question", days = -12)
        future_question = create_question(question_text="future question", days=30)
        response = seft.client.get(reverse("polls:index"))
        seft.assertQuerysetEqual(
            response.context["latest_question_list"],
            [pass_question]
        )
    def test_two_question_past_past(seft):
    # "" cunado se publique una pregunta de manera futura y otra en pasado que se visualizen solo la del pasado
        past_question1 = create_question(question_text="past question 1", days = -12)
        past_question2 = create_question(question_text="future question 2", days=-30)
        response = seft.client.get(reverse("polls:index"))
        seft.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1,past_question2]
        )
        
    def test_two_question_future_and_future(seft):
        # cuando se crean dos preguntas en el futuro que no se visualizen 
        future_question1 = create_question(question_text="future question 1", days= 12)
        future_question2= create_question(question_text="question future 2", days= 34)
        response = seft.client.get(reverse("polls:index"))
        seft.assertContains(response, "No tienen ninguna variable " )
        seft.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )
        
        
class QuestionDetailViewTest(TestCase) :
   def URL_future_question(seft):
        #si un usuario ingresa desde la URL a una pregunta furutura debe encintrsrse con el error 404
        future_question = create_question(question_text="future question 1", days= 12)
        url = reverse("polls:detail", args=(future_question.id,))
        response = seft.client.get(url)
        seft.assertEqual(response.status_code, 404)

    
   def URL_pass_question(self):
        #si un usuario ingresa desde la url a una pregunta del pasado le debe de mostrar la pregunta 
        past_question = create_question(question_text="future question 1", days= 12)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
    