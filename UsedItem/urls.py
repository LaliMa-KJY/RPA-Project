from django.urls import path

from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('kakaoMSG/', views.kakaoMSG, name='kakaoMSG'),
    path('excelSave/', views.excelSave, name='excelSave'),
    path('myTest/', views.myTest, name='myTest'),
]