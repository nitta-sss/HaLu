from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # ←これを戻す！
    path('', include('main.urls')),
]
