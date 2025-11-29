from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # 1. URL do Admin
    path('admin/', admin.site.urls),
    
    # ⬅️ ESSA LINHA É CRÍTICA! Ela inclui o login/logout padrão do Django.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Inclui todas as urls do nosso app sob o prefixo 'api/'
    path('', include('psico_saas.urls')),
]

