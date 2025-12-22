from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_pdf, name='upload_pdf'),
    path('ask_question/', views.ask_question, name='ask_question'), # Matches fetch('/ask_question/...')
    path('delete/<int:pdf_id>/', views.delete_pdf, name='delete_pdf'),
]