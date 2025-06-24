from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.service, name='service'),
    path('services/<slug:slug>/', views.service_detail, name='service_detail'),
    path('projects/', views.project, name='project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('features/', views.feature, name='feature'),
    path('team/', views.team, name='team'),
    path('testimonials/', views.testimonial, name='testimonial'),
    path('contact/', views.contact, name='contact'),
    path('404/', views.error_404, name='error_404'),
]