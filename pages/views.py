from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader #Anna
from greenchatbot.models import QuestionReponse
from django.views.decorators.csrf import csrf_exempt


import nltk
from nltk.chat.util import Chat, reflections

# Create your views here.
# def home(request):
#     # Exemple de page HTML, non valide pour que l'exemple soit concis Anna
#     text = "<h1>Bienvenue sur mon blog !</h1>"
#     text = text+ "<p>premier texte de présentation !</p>"
#     return HttpResponse(text)


#Anna start
   #accueil
template = loader.get_template('index.html')

def home (request) :
  data= {'page':'home'}
  return(HttpResponse(template.render(data)))

@csrf_exempt
def chatbot (request) :
   data= {'page':'chatbot'}

   data['reponse'] = ""
   data['question'] = ""
   if request.method == 'POST':

      pairs = []
      for question_reponse in QuestionReponse.objects.all():
         question = question_reponse.question
         reponse = question_reponse.reponses
         # Création de la paire de question-réponse correspondante
         pair = [r"{}".format(question), reponse.split("|")]
         # Ajout de la paire à la liste des paires
         pairs.append(pair)

      message = request.POST['question']

      chat = Chat(pairs, reflections)
      result = chat.respond(message)
 
      data['reponse'] = result
      data['question'] = message

   return(HttpResponse(template.render(data)))

def service (request) :
  data= {'page':'service'}
  return(HttpResponse(template.render(data)))