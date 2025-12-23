from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('app/', views.upload_pdf, name='upload_pdf'),
    path('ask_question/', views.ask_question, name='ask_question'), # Matches fetch('/ask_question/...')
    path('delete/<int:pdf_id>/', views.delete_pdf, name='delete_pdf'),
    path('download_transcript/<int:pdf_id>/', views.download_transcript, name='download_transcript'),
]