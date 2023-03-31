from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader #Anna
from greenchatbot.models import QuestionReponse
from django.views.decorators.csrf import csrf_exempt

import json
import ast

import nltk
from nltk.chat.util import Chat, reflections
import unicodedata



template = loader.get_template('index.html')

def home (request) :
  data= {'page':'home'}
  return(HttpResponse(template.render(data)))


def service (request) :
  data= {'page':'service'}
  return(HttpResponse(template.render(data)))


def about (request) :
  data= {'page':'about'}
  return(HttpResponse(template.render(data)))


def contact (request) :
  data= {'page':'contact'}
  return(HttpResponse(template.render(data)))


@csrf_exempt
def chatbot (request) :
   data= {'page':'chatbot', 'history': []}
   
   if request.method == 'POST':

      texthistory = request.POST['history']
      # si on a un historique dans le champs, il faut le récupérer au format json
      ##### penser à faire un "import json" en début de programme
      if (texthistory):
         json_dat = json.dumps(ast.literal_eval(texthistory))
         data['history'] = json.loads(json_dat)


      pairs = []
      for question_reponse in QuestionReponse.objects.all():
         question = question_reponse.question
         reponse = question_reponse.reponses
         # Création de la paire de question-réponse correspondante
         pair = [r"{}".format(question), reponse.split("|")]
         # Ajout de la paire à la liste des paires
         print (pair)
         pairs.append(pair)

      message = request.POST['question']
      # Normalisation unicode
      texte_normalized = unicodedata.normalize('NFKD', message).encode('ASCII', 'ignore').decode('utf-8')

      chat = Chat(pairs, reflections)
      reponse = chat.respond(texte_normalized)
     
      # on conserve les échange dans l'historique
      msgUser = {"type" : "user", "content": message}
      data['history'].append(msgUser)
      msgBot = {"type" : "bot", "content": reponse}
      data['history'].append(msgBot) 
 

   return(HttpResponse(template.render(data)))





