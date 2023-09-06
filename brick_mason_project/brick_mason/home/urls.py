from django.urls import path
#from django.contrib.auth import views
from . import views

app_name = "home"

urlpatterns = [
    #path('', views.main, name='main'),
    path('dashboard/', views.dashboard, name='home'),
    path('import/', views.ImportNewSource, name='import'),
    path('search/', views.search, name='search'),
    path('search/search_results/', views.search_results, name='search_results'),
    path('brick_editor/', views.brick_editor, name='brick_editor'),
    path('profile/', views.profile, name='profile'),
    #path('viewdocx/', views.viewdocx, name='viewdocx'),
]
