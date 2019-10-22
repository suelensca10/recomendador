from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    ##path('login/', 'django.contrib.auth.views.login', {'template_name': 'app/login.html'}),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
]