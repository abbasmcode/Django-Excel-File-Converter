from django.urls import path
from .views import upload_file, download_file

app_name = 'converter'

urlpatterns = [
    path('', upload_file, name='upload_file'),
    path('download/<int:pk>/', download_file, name='download_file'),
]
