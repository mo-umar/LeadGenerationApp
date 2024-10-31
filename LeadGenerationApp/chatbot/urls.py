from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Ensure this is set for the root URL
    path('chatbot_interaction/', views.chatbot_interaction, name='chatbot'),
]
