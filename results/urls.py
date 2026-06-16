from django.urls import path

from . import views



urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
    'news/<int:news_id>/',
    views.news_detail,
    name='news_detail'
),

    path(
        'constituency/<int:constituency_id>/',
        views.constituency_detail,
        name='constituency_detail'
    ),
    path('dashboard/', views.results_dashboard, name='results_dashboard'),
    path(
    'news/',
    views.news_list,
    name='news_list'
),
    path(
    'constituencies/',
    views.constituencies,
    name='constituencies'
),

]