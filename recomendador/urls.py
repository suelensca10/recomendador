from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]