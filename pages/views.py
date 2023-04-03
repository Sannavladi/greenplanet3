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
from datetime import datetime #for time Anna
from django.utils.html import format_html



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
   now = datetime.now()
   data= {'page': 'chatbot', 'history': []} 
   current_time = now.strftime("%H:%M:%S") # format d'heure à utiliser
   
   #current_date = now.strftime("%Y-%m-%d")
   current_date = now.strftime("%d.%m.%Y")
   
   data['titre'] = current_date
   
   
   msgBot = {"type" : "bot", "content": "Bonjour je suis Green Bot, comment puis-je vous aidez?", "time": current_time}
   data['history'].append(msgBot) 

#    Le code définit un dictionnaire de données appelé "data" avec deux clés:

# "page": une chaîne de caractères qui indique que la page actuelle est la page du chatbot
# "history": une liste vide qui stockera l'historique des messages échangés entre l'utilisateur et le chatbot.
   
   if request.method == 'POST':
# Le code vérifie si la méthode de requête (request.method) est "POST". 

# Si la méthode de requête est "POST", le code récupère le contenu de
#  l'élément de formulaire nommé "history" en utilisant request.POST['history'] 
# et l'assigne à une variable appelée "texthistory".

      texthistory = request.POST['history']
      current_time = now.strftime("%H:%M:%S") # format d'heure à utiliser
   
   
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
      msgUser = {"type" : "user", "content": message, "time": current_time}
      data['history'].append(msgUser)
      #msgBot = {"type" : "bot", "content": reponse, "time": current_time}
      
      if reponse:
         msgBot = {"type" : "bot", "content": reponse, "time": current_time}
      else:
         msgBot = {"type": "bot", "content": format_html("Veuillez nous contacter à &nbsp;<a href='mailto:{}'> {} </a>", "contact@greenplanet.com", "contact@greenplanet.com"), "time": current_time}
      
      data['history'].append(msgBot) 
 

   return(HttpResponse(template.render(data)))





