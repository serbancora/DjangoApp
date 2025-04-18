from django.urls import path
from . import views

urlpatterns = [
    # Core pages
    path('', views.index, name='index'),
    path('courses/', views.courses, name='courses'),
    path('about/', views.about, name='about'),
    path('ierarhie/<int:id>/', views.view_rest, name='view_rest'),

    # Flashcards
    path('upload-flashcards/', views.upload_flashcards, name='upload_flashcards'),
    path('ierarhie-json/', views.ierarhie_json, name='ierarhie_json'),

    # Auth
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]