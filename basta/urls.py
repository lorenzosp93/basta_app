from django.urls import path
from .views import (
    PlayView, RoundView, SessionView, SessionListView,
    session_create, session_close,
)

app_name = 'basta'

urlpatterns = [
    path('play/', SessionListView.as_view(), name="home"),
    path('play/session/<slug:slug>/', SessionView.as_view(), name="session"),
    path(
        'play/session/<slug:slug>/round/<int:number>/',
        RoundView.as_view(),
        name="round",
    ),
    path(
        'play/session/<slug:slug>/round/<int:number>/play',
        PlayView.as_view(),
        name="play",
    ),
    path(
        'play/create/',
        session_create,
        name="sessioncreate",
    ),
    path(
        'play/session/<slug:slug>/close/',
        session_close,
        name="sessionclose",
    )
]
