from django.urls import path
from .views import scrape_and_generate

urlpatterns = [
    path("scrape/", scrape_and_generate),
]
