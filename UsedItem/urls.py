from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('excelSave/', views.excelSave, name='excelSave'),
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('oauth/', views.kakao_callback, name='kakao_callback'),
]