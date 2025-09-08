from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),
    path('agents/', views.property_agent, name='agents'),
    path('listings/', views.propertylist, name='listings'),
    
    
    path('testimonial', views.testimonial, name='testimonial'),
    path("agentprofile", views.agentprofile, name="agentprofile"),
    path("clientlogin", views.clientlogin, name="clientlogin"),
    path("clientsignup", views.clientsignup, name="clientsignup"),
    path("agentsignup", views.agentsignup, name="agentsignup"),
    path("agentregistration", views.agentregistration, name="agentregistration"),
    path("propertyregistration", views.propertyregistration, name="propertyregistration"),
    path("404", views.notfound, name="404"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("properties/<int:pk>/", views.propertydetail, name="propertydetail"),
    path("type/<int:type_id>/", views.properytype, name="type"),
    path("search/", views.search, name="search"),
    
]
