from django.urls import path
from . import views

app_name = 'statistic'

urlpatterns = [
    path('', views.index, name='index'),
    path('date_filter/', views.date_filter, name='date_filter'),
    path('done_filter/', views.done_filter, name='done_filter')
]
