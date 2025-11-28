from rest_framework.routers import DefaultRouter 
from .views import PlanoTratamentoViewSet 


router = DefaultRouter()
router.register(r'planos', PlanoTratamentoViewSet)

urlpatterns = router.urls 



