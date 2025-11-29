from django.urls import path, include
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Planos de Tratamento
    path('planos/', views.listar_planos_view, name='listar_planos'),
    path('planos/novo/', views.plano_form_view, name='plano_form'),  # ⬅️ ESTA ESTAVA FALTANDO
    path('planos/editar/<int:pk>/', views.plano_form_view, name='editar_plano'),
    path('planos/excluir/<int:pk>/', views.excluir_plano, name='excluir_plano'),
    path('planos/ver/<int:pk>/', views.ver_plano_view, name='ver_plano'),
    
    # Documentação de Sessão
    path('documentacao/', views.documentacao_form_view, name='documentacao_form'),
    
    # Tarefas/Exercícios
    path('tarefas/', views.listar_tarefas_view, name='listar_tarefas'),
    path('tarefas/nova/', views.tarefas_form_view, name='tarefas_form'),
    path('tarefas/<int:pk>/', views.tarefas_detail_view, name='tarefas_detail'),
    
    # Conteúdo Educacional
    path('conteudos-educacionais/', views.listar_conteudos_educacionais_view, name='listar_conteudos_educacionais'),
    path('conteudos-educacionais/novo/', views.conteudo_educacional_form_view, name='conteudo_educacional_form'),
    path('conteudos-educacionais/ver/<int:pk>/', views.ver_conteudo_educacional_view, name='ver_conteudo_educacional'),
    path('conteudos-educacionais/salvar/<int:pk>/', views.salvar_conteudo_educacional_view, name='salvar_conteudo_educacional'),
    
    # API
    path('api/planos/', views.PlanoTratamentoViewSet.as_view({'get': 'list', 'post': 'create'}), name='api_planos'),
]