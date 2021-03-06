from django.urls import path
from .views import (
    PlayView, RoundView, SessionView, SessionListView, 
    session_close,
    round_create, play_create, play_score,
    poll_session_refresh_view,
)

app_name = 'basta'

urlpatterns = [
    path('', SessionListView.as_view(), name="home"),
    path('session/<slug:slug>/', SessionView.as_view(), name="session"),
    path('session/<slug:slug>/poll-refresh/', poll_session_refresh_view),
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
    ),
    path(
        'session/<slug:slug>/round/<int:number>/score',
        play_score,
        name="playscore",
    )
]
