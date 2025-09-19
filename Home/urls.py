from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
# from .views import  CustomLogoutView
from .views import CustomLoginView, CustomLogoutView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about_us, name='about'),
    path('contact/', views.contact, name='contact'),
    path('agents/', views.property_agent, name='agents'),
    path('listings/', views.propertylist, name='listings'),
    
    
    
    # path("agentprofile", views.agentprofile, name="agentprofile"),
    # path("clientlogin", views.clientlogin, name="clientlogin"),
    path("clientsignup", views.clientsignup, name="clientsignup"),
    path("agentsignup", views.agentsignup, name="agentsignup"),
    path("agentregistration", views.agentregistration, name="agentregistration"),
    path("propertyregistration", views.propertyregistration, name="propertyregistration"),
    path("404", views.notfound, name="404"),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("properties/<int:pk>/", views.propertydetail, name="propertydetail"),
    path("type/<int:type_id>/", views.properytype, name="type"),
    path("search/", views.search, name="search"),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),

    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path("agentdb", views.agentdb, name="agentdb"),
    path('agent/<int:agent_id>/', views.agent_profile, name='agentprofile'),
    path('agent/properties/', views.manage, name='manage'),
    path('property/edit/<int:pk>/', views.edit_property, name='edit_property'),
    path('property/delete/<int:pk>/', views.delete_property, name='delete_property'),
    path("agent/<int:pk>/edit/", views.edit_agent, name="edit_agent"),
    path('property/<int:property_id>/add-image/', views.add_property_image, name='add_property_image'),
    path('album-image/<int:image_id>/delete/', views.delete_album_image, name='delete_album_image'),



    
]
