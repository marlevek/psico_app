from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Incluir as URLs do app psico_saas
    path('', include('psico_saas.urls')),
    
    # URLs de autenticação
    path('login/', auth_views.LoginView.as_view(template_name='psico_saas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
