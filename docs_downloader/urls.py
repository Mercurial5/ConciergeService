from django.urls import path
from docs_downloader import views

urlpatterns = [
    path('<str:doctype>/<str:name>', views.download)
]
