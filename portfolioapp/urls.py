from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('Aboutme/', views.Aboutme, name='Aboutme'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),

    # Old project URLs now point at sections of the single Projects page
    path('deeplearning/', RedirectView.as_view(url='/projects/#cv')),
    path('machinelearning/', RedirectView.as_view(url='/projects/#predictive')),
    path('webprojects/', RedirectView.as_view(url='/projects/#dashboards')),
]
