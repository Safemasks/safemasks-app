"""safemasks.resources URL Configuration
"""
from django.urls import path, include
from resources.rest.router import ROUTER

app_name = "resources"
urlpatterns = [
    path("", include(ROUTER.urls)),
]
