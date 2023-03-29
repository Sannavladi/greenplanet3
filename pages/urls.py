#start/ Anna
from django.urls import path
from django.views.generic import TemplateView

app_name = 'pages'

urlpatterns = [
   path('', TemplateView.as_view(template_name='templates/index.html'), name='index'),
    
 ]


# des routes pour servir les fichiers html en utilisant la vue TemplateView. 
#end/ Anna (créé tout le fichier) À l'aide de la méthode as_view(), le chemin d'accès au modèle qui sera utilisé comme réponse est défini via le paramètre template_name.
