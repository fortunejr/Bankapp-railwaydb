from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin3445621/', admin.site.urls),
    path('', include('core.urls')),
    
]
