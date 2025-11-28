from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Inclui todas as urls do nosso app sob o prefixo 'api/'
   # path('api/', include('psico_saas.urls')),
]

