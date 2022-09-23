from django.urls import path

from . import views

app_name = 'exchange'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('time/<str:currency>/', views.time_chart, name='time_chart'),
    path('<str:currency>/', views.full_chart, name='full_chart'),
]
