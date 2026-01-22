from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("users.txt", views.users_txt, name="users_txt"),
    path('run/', views.run_python_view, name='run_python'),
    
]
