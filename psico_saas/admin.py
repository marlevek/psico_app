# psico_saas/admin.py
from django.contrib import admin
from .models import PlanoTratamento, DocumentacaoSessao, TarefaExercicios, Paciente # ⬅️ IMPORTAR PACIENTE


# -------------------------------------------------------------
# REGISTRO PADRÃO DOS MODELOS EXISTENTES (Mantenha)
# -------------------------------------------------------------
@admin.register(PlanoTratamento)
class PlanoTratamentoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'paciente', 'diagnostico_base', 'data_criacao')
    search_fields = ('titulo', 'diagnostico_base')
    list_filter = ('paciente', 'data_criacao')
    


# -------------------------------------------------------------
# REGISTRO DO MODELO PACIENTE (Verifique este bloco!)
# -------------------------------------------------------------
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'usuario', 'data_nascimento', 'data_cadastro')
    search_fields = ('nome_completo',)
    list_filter = ('usuario',)
    
    # Garante que o usuário logado seja definido automaticamente
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
    
    # Filtra para que o psicólogo só veja seus próprios pacientes
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)