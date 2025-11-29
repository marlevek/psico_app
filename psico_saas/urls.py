from rest_framework.routers import DefaultRouter 
from .views import PlanoTratamentoViewSet, plano_form_view, listar_planos_view, excluir_plano, dashboard_view, documentacao_form_view, tarefas_form_view, listar_tarefas_view, tarefas_detail_view
from django.urls import path, include



# Roteamento da API (existente)
router = DefaultRouter()
router.register(r'planos', PlanoTratamentoViewSet, basename='plano')

#urlpatterns = router.urls 

urlpatterns = [
# 1. Dashboard
   path('', dashboard_view, name='dashboard'),
   
# 2. URL para o Formulário Frontend
   path('plano/novo/', plano_form_view, name='criar_plano'),
   
# 3. URLs da API
   path('api/', include(router.urls)),
   
# 4. URLs Para a lista/histórico de planos
   path('plano/editar/<int:pk>/', plano_form_view, name='editar_plano'),
   path('historico/', listar_planos_view, name='listar_planos'),
   path('plano/excluir/<int:pk>/', excluir_plano, name='excluir_plano'),
   
   
# 5. Assistente de Documentação/Sessão ⬅️ NOVAS ROTAS
    path('documentacao/', documentacao_form_view, name='documentacao_form'),
    path('documentacao/<int:pk>/', documentacao_form_view, name='documentacao_form_detail'), # Para exibir o resultado após salvar
    
# 6. Gerador de Exercícios/Tarefas ⬅️ ESTA LINHA DEVE SER VERIFICADA!
    path('tarefas/', tarefas_form_view, name='tarefas_form'),
    path('tarefas/historico/', listar_tarefas_view, name='listar_tarefas'),
   path('tarefas/detalhe/<int:pk>/', tarefas_detail_view, name='tarefas_detail'),
]



