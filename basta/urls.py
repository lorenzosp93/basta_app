from django.urls import path
from .views import PlayView, RoundView, SessionView

app_name = 'basta'

urlpatterns = [
    path('play/', PlayView.as_view()),
    path('play/session/<int:pk>/', SessionView.as_view(), name="session"),
    path(
        'play/session/<int:pk>/round/<int:number>/',
        RoundView.as_view(),
        name="round"
    ),
    path(
        'play/session/<int:pk>/round/<int:number>/play',
        PlayView.as_view(),
        name="play"
    ),
]
