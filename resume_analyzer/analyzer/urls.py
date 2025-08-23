from django.urls import path
from . import views


urlpatterns = [
    path('home/', views.home, name='home'),
    path('', views.upload_text, name='upload'),
    path('doc/<int:pk>/', views.detail, name='detail'),
    path('files/', views.all_files, name='all_files'),
    path('analyze/<int:doc_id>/', views.analyze_resume, name='analyze_resume'),
]
