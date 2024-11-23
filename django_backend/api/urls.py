from django.urls import path
from .views import *

urlpatterns = [
    path("scrape/", scrape_and_generate),
    path("scrape_store/", scrape_instagram_post),
]
