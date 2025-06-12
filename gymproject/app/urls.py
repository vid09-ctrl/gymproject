from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static 
urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('facilities/', views.facilities, name='facilities'),
    path('free-trial/', views.free_trial, name='free_trial'),




]