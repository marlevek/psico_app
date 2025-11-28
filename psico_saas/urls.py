from rest_framework.routers import DefaultRouter 
from .views import PlanoTratamentoViewSet 
from django.urls import path, include


router = DefaultRouter()
router.register(r'planos', PlanoTratamentoViewSet, basename='plano')

urlpatterns = router.urls 

#urlpatterns = [
    #path('', include(router.urls)),
#]



