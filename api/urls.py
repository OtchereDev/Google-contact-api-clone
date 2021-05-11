from django.urls import path
from .views import ContactView,ContactUpdateView,ContactSearchView

urlpatterns = [
    path('',ContactView.as_view()),
    path('search/<str:full_name>/',ContactSearchView.as_view()),
]
