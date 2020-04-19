from django.urls import path
from .views import (
    PlayView, RoundView, SessionView, SessionListView,
    session_create, session_close, round_create, play_create,
)

app_name = 'basta'

urlpatterns = [
    path('', SessionListView.as_view(), name="home"),
    path('session/<slug:slug>/', SessionView.as_view(), name="session"),
    path(
        'session/<slug:slug>/round/<int:number>/',
        RoundView.as_view(),
        name="round",
    ),
    path(
        'session/<slug:slug>/round/<int:number>/play',
        PlayView.as_view(),
        name="play",
    ),
    path(
        'create/',
        session_create,
        name="sessioncreate",
    ),
    path(
        'session/<slug:slug>/close/',
        session_close,
        name="sessionclose",
    ),
    path(
        'session/<slug:slug>/create/',
        round_create,
        name="roundcreate",
    ),
    path(
        'session/<slug:slug>/round/<int:number>/create',
        play_create,
        name="playcreate",
    )
]
