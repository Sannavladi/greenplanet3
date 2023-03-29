from django.db import models

# Create your models here.
class QuestionReponse(models.Model) :
    question = models.TextField()
    reponses = models.TextField()