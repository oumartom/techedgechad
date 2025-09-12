from django.urls import path
from . import views
from .views import subscribe_newsletter,CustomLoginView,LogoutView,custom_logout
from django.contrib.auth import views as auth_views
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
    path('subscribe/', subscribe_newsletter, name='subscribe'),
    path('blog/', views.blog, name='blog'),
    path('blog/category/<slug:category_slug>/', views.blog_category, name='blog_category'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('blog/<slug:slug>/like/', views.like_blog_post, name='like_blog_post'),
    path('blog/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/register/', views.register, name='register'),
    path('formations/', views.training_list, name='training_list'),
    path('formations/categorie/<slug:category_slug>/', views.training_list, name='training_category'),
    path('formations/<slug:slug>/', views.training_detail, name='training_detail'),
    path('formations/<slug:slug>/inscription/', views.register_for_training, name='register_training'),
    path('mes-formations/', views.my_trainings, name='my_trainings'),
    
]
