from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('about/', views.about, name='about'),  # Page "À propos"
    path('service/', views.service, name='service'),  # Page "Services"
    path('project/', views.project, name='project'),  # Page "Projets"
    path('feature/', views.feature, name='feature'),  # Page "Fonctionnalités"
    path('team/', views.team, name='team'),  # Page "Équipe"
    path('testimonial/', views.testimonial, name='testimonial'),  # Page "Témoignages"
    path('contact/', views.contact, name='contact'),  # Page "Contact"
    path('404/', views.error_404, name='404'),  # Page d'erreur 404
]
