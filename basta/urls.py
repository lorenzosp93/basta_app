from django.urls import path
from .views import PlayView

app_name = 'basta'

urlpatterns = [
    path('play', PlayView.as_view()),
    path('', PlayView.as_view())
]
