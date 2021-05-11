from django.urls import path
from .views import ContactView,ContactUpdateView,ContactSearchView

urlpatterns = [
    path('',ContactView.as_view()),
    
]
