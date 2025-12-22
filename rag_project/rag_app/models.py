# rag_app/models.py
from django.db import models
import os

class UploadedPDF(models.Model):
    file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)

    def __str__(self):
        return self.file.name

    @property
    def filename(self):
        return os.path.basename(self.file.name)

class PDFPage(models.Model):
    # Notice we refer to 'UploadedPDF' here, which matches the class above
    pdf = models.ForeignKey(UploadedPDF, on_delete=models.CASCADE, related_name='pages')
    page_number = models.IntegerField()
    image = models.ImageField(upload_to='pdf_pages/')
    
    class Meta:
        ordering = ['page_number']