from django.urls import path
from .views import PlayView, RoundView, SessionView

app_name = 'basta'

urlpatterns = [
    path('', PlayView.as_view()),
    path('play/<session:pk>/<round:pk>', RoundView.as_view())
    path('play/<session:pk>/<round:pk>/<play:pk>', PlayView.as_view()),

]
