from django.urls import path
from . import views

urlpatterns = [
    path("predict", views.predictDisease, name="predict-disease"),
    path("plot/", views.plotGraph, name="plot-graph"),
]
