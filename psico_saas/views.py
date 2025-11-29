from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .models import PlanoTratamento, DocumentacaoSessao, TarefaExercicios, Paciente, ConteudoEducacional
from .serializers import PlanoTratamentoSerializer, DocumentacaoSessaoSerializer, TarefaExerciciosSerializer, ConteudoEducacionalSerializer
from django.db.models import Count
from .ia_service import generate_task_exercise
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import re  # Importação necessária para verificar se a string é um número


# ------------------------------------------------------------------
# FUNÇÃO AUXILIAR PARA PEGAR PACIENTES
# ------------------------------------------------------------------

def get_user_pacientes(user):
    """Retorna todos os pacientes associados ao usuário logado."""
    return Paciente.objects.filter(usuario=user).order_by('nome_completo')


# ------------------------------------------------------------------
# 1. VIEW DA API (EXISTENTE E PROTEGIDA)
# ------------------------------------------------------------------
class PlanoTratamentoViewSet(viewsets.ModelViewSet):
    '''
    Endpoint da API que permite criar, visualizar, atualizar e deletar planos de tratamento
    '''
    authentication_classes = [TokenAuthentication]

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Método opcional para customizações
        return PlanoTratamento.objects.filter(usuario=self.request.user).order_by('-data_criacao')

    serializer_class = PlanoTratamentoSerializer


# ------------------------------------------------------------------
# 2. VIEW DO FORMULÁRIO (FRONTEND)
# ------------------------------------------------------------------
@login_required
def plano_form_view(request, pk=None):
    plano_instance = None
    feedback_ia = None
    error_message = None
    form_errors = {}
    is_editing = False
    request_post_data = {}  # ⬅️ MUDAR PARA DICT VAZIO em vez de None

    # 1. Carregar Plano Existente (Edição)
    if pk:
        plano_instance = get_object_or_404(
            PlanoTratamento, pk=pk, usuario=request.user)
        is_editing = True

    # 2. Lógica POST (Submissão do Formulário)
    if request.method == 'POST':
        data = request.POST.copy()
        request_post_data = data  # Agora sempre será um dict, nunca None

        # 🛑 VALIDAÇÃO ROBUSTA DO CAMPO PACIENTE
        paciente_value = data.get('paciente', '')
        if paciente_value and not re.match(r'^\d+$', str(paciente_value)):
            data['paciente'] = ""

        # 🛑 VALIDAÇÃO DA DATA DE INÍCIO PREVISTA
        data_inicio_value = data.get('data_inicio_prevista', '')
        if not data_inicio_value:
            # Se não foi preenchida, podemos definir uma data padrão ou deixar o validation error ocorrer
            # Por exemplo, definir como hoje:
            # from datetime import date
            # data['data_inicio_prevista'] = date.today().isoformat()
            # Ou deixar o serializer capturar o erro
            pass

        # O serializer usa 'plano_instance' para atualizar (PUT/PATCH) ou None para criar
        serializer = PlanoTratamentoSerializer(
            instance=plano_instance,
            data=data,
            context={'request': request}
        )

        if serializer.is_valid():
            try:
                # Associa o usuário antes de salvar
                plano_salvo = serializer.save(usuario=request.user)
                return redirect('listar_planos')

            except Exception as e:
                error_message = f"Erro ao salvar no banco de dados: {str(e)}"
                # Log mais detalhado para debugging
                print(f"Erro detalhado: {e}")
        else:
            form_errors = serializer.errors
            error_message = "Erro de validação. Por favor, verifique os campos em vermelho."

    # 3. Contexto para Renderização do Template
    pacientes = Paciente.objects.filter(usuario=request.user)

    context = {
        'plano': plano_instance,
        'pacientes': pacientes,
        'is_editing': is_editing,
        'error_message': error_message,
        'form_errors': form_errors,
        'feedback_ia': feedback_ia,
        'request_post': request_post_data,  # ⬅️ Agora sempre será um dict
    }

    return render(request, 'psico_saas/plano_form.html', context)


# ------------------------------------------------------------------
# 3. VIEW DA LISTA DE PLANOS (FRONTEND)
# ------------------------------------------------------------------
@login_required
def listar_planos_view(request):
    """
    Busca e exibe todos os planos criados pelo usuário logado.
    """
    # Filtra todos os planos associados ao usuário que está a fazer a requisição
    planos = PlanoTratamento.objects.filter(
        usuario=request.user).order_by('-data_criacao')

    context = {
        'planos': planos
    }

    return render(request, 'psico_saas/plano_lista.html', context)


# ------------------------------------------------------------------
# VIEW PARA VER DETALHES DO PLANO
# ------------------------------------------------------------------
@login_required
def ver_plano_view(request, pk):
    """
    Exibe os detalhes completos de um plano de tratamento.
    """
    plano = get_object_or_404(PlanoTratamento, pk=pk, usuario=request.user)

    context = {
        'plano': plano,
    }

    return render(request, 'psico_saas/ver_plano.html', context)

# ------------------------------------------------------------------
# 4. VIEW DE EXCLUSÃO
# ------------------------------------------------------------------


@login_required
@require_POST  # Apenas permite requisições POST para exclusão (mais seguro)
def excluir_plano(request, pk):
    plano = get_object_or_404(PlanoTratamento, pk=pk, usuario=request.user)
    plano.delete()
    return redirect('listar_planos')


# ------------------------------------------------------------------
# 5. VIEW DO DASHBOARD
# ------------------------------------------------------------------
@login_required
def dashboard_view(request):
    user = request.user

    # 1. Métricas Totais
    total_planos = PlanoTratamento.objects.filter(usuario=user).count()
    total_documentacao = DocumentacaoSessao.objects.filter(
        usuario=user).count()
    total_tarefas = TarefaExercicios.objects.filter(usuario=user).count()

    # 2. Itens Recentes
    ultimos_planos = PlanoTratamento.objects.filter(
        usuario=user).order_by('-data_criacao')[:3]
    ultimas_documentacoes = DocumentacaoSessao.objects.filter(
        usuario=user).order_by('-data_criacao')[:3]
    ultimas_tarefas = TarefaExercicios.objects.filter(
        usuario=user).order_by('-data_criacao')[:3]

    context = {
        'total_planos': total_planos,
        'total_documentacao': total_documentacao,
        'total_tarefas': total_tarefas,
        'ultimos_planos': ultimos_planos,
        'ultimas_documentacoes': ultimas_documentacoes,
        'ultimas_tarefas': ultimas_tarefas,
    }

    return render(request, 'psico_saas/dashboard.html', context)


# ------------------------------------------------------------------
# 6. VIEW DO FORMULÁRIO DE DOCUMENTAÇÃO DE SESSÃO
# ------------------------------------------------------------------
@login_required
def documentacao_form_view(request):
    """
    Lida com o formulário de entrada para documentação de sessão e processa a IA.
    """
    resumo_ia = None
    sugestao_diagnostico = None
    padroes_linguagem = None
    error_message = None

    if request.method == 'POST':
        data = request.POST.copy()
        # Garante que o usuário logado é enviado
        data['usuario'] = request.user.pk

        serializer = DocumentacaoSessaoSerializer(
            data=data,
            context={'request': request}
        )

        if serializer.is_valid():
            try:
                doc_salva = serializer.save(usuario=request.user)

                # Armazena os resultados para exibição
                resumo_ia = doc_salva.resumo_ia
                sugestao_diagnostico = doc_salva.sugestao_diagnostico
                padroes_linguagem = doc_salva.padroes_linguagem

                # Redireciona para evitar reenvio do formulário
                return redirect('documentacao_form', pk=doc_salva.pk)

            except Exception as e:
                # O Serializer levanta um ValidationError se a IA falhar
                error_message = str(e)
        else:
            error_message = f"Erro de validação: {serializer.errors}"

    context = {
        'resumo_ia': resumo_ia,
        'sugestao_diagnostico': sugestao_diagnostico,
        'padroes_linguagem': padroes_linguagem,
        'error_message': error_message,
        'pacientes': get_user_pacientes(request.user)
    }

    return render(request, 'psico_saas/documentacao_form.html', context)


# ------------------------------------------------------------------
# 7. VIEW DO FORMULÁRIO DE EXERCÍCIOS/TAREFAS
# ------------------------------------------------------------------
@login_required
def tarefas_form_view(request):
    """
    Lida com o formulário de entrada para gerar exercícios e processa a IA.
    """
    exercicio_ia = None
    error_message = None
    # Adicionamos 'data_form' para repopular os campos após um erro de validação
    data_form = request.POST.copy() if request.method == 'POST' else None

    if request.method == 'POST':
        data = request.POST.copy()

        # 1. Validação Simples (Obriga campos a serem preenchidos)
        serializer = TarefaExerciciosSerializer(
            data=data,
            context={'request': request}
        )

        if serializer.is_valid():
            try:
                # 2. EXTRAI OS DADOS NECESSÁRIOS PARA A IA
                dados_ia = serializer.validated_data

                abordagem_teorica = dados_ia.get('abordagem_teorica')
                tema_principal = dados_ia.get('tema_principal')
                detalhes_personalizacao = dados_ia.get(
                    'detalhes_personalizacao')

                # 3. CHAMA O SERVIÇO DE IA CORRIGIDO
                exercicio_ia_content = generate_task_exercise(
                    abordagem_teorica,
                    tema_principal,
                    detalhes_personalizacao
                )

                # 4. TRATAMENTO DO RETORNO DA IA
                if exercicio_ia_content.startswith("Erro na API:"):
                    error_message = exercicio_ia_content
                else:
                    # 5. ATUALIZA OS DADOS VALIDADOS COM O CONTEÚDO DA IA
                    dados_ia['exercicio_ia'] = exercicio_ia_content

                    # 6. SALVA NO BANCO (com o conteúdo da IA e o usuário correto)
                    tarefa_salva = serializer.save(usuario=request.user)
                    exercicio_ia = tarefa_salva.exercicio_ia

                    # Opcional: Redirecionar para a página de detalhes/listagem após o sucesso
                    # return redirect('tarefas_detail', pk=tarefa_salva.pk)

            except Exception as e:
                # Captura erros inesperados (não API)
                error_message = f"Erro de processamento: {e}"

        else:
            # Lógica de formatação de erros (mantida e melhorada)
            formatted_errors = []
            for field, errors in serializer.errors.items():
                field_name = field.replace('_', ' ').capitalize()
                error_list = [str(e) for e in errors]
                formatted_errors.append(
                    f"**{field_name}**: {', '.join(error_list)}")

            error_message = f"**Erro de validação:** Por favor, corrija os seguintes campos:\n- {'\n- '.join(formatted_errors)}"

    context = {
        'exercicio_ia': exercicio_ia,
        'error_message': error_message,
        'abordagens': TarefaExercicios.ABORDAGENS,
        'pacientes': get_user_pacientes(request.user),
        # Passa os dados do POST de volta para o template repopular
        'data_form': data_form,
    }

    return render(request, 'psico_saas/tarefas_form.html', context)


# ------------------------------------------------------------------
# 8. VIEW DE LISTAGEM DE TAREFAS/EXERCÍCIOS
# ------------------------------------------------------------------
@login_required
def listar_tarefas_view(request):
    """
    Exibe a lista de todos os exercícios/tarefas criadas pelo usuário.
    """
    tarefas = TarefaExercicios.objects.filter(
        usuario=request.user).order_by('-data_criacao')
    context = {'tarefas': tarefas}
    return render(request, 'psico_saas/tarefas_lista.html', context)


# ------------------------------------------------------------------
# 9. VIEW DE DETALHE E IMPRESSÃO DE TAREFA
# ------------------------------------------------------------------
@login_required
def tarefas_detail_view(request, pk):
    """
    Exibe uma única tarefa. Usado como base para a impressão.
    """
    tarefa = get_object_or_404(TarefaExercicios, pk=pk, usuario=request.user)
    context = {'tarefa': tarefa}
    return render(request, 'psico_saas/tarefas_detail.html', context)


# ------------------------------------------------------------------
# VIEWS PARA CONTEÚDO EDUCACIONAL
# ------------------------------------------------------------------
@login_required
def conteudo_educacional_form_view(request):
    """
    View para criar novo conteúdo educacional com IA.
    """
    if request.method == 'POST':
        data = request.POST.copy()
        
        serializer = ConteudoEducacionalSerializer(
            data=data, 
            context={'request': request}
        )

        if serializer.is_valid():
            try:
                conteudo_salvo = serializer.save(usuario=request.user)
                
                print("=== DEBUG VIEW ANTES DE RETORNAR JSON ===")
                print("SUGESTÕES DE IMAGENS NO OBJETO SALVO:", repr(conteudo_salvo.sugestoes_imagens))  # Usar repr para ver caracteres especiais
                print("=======================")
                
                # Se for requisição AJAX, retorne JSON
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    response_data = {
                        'success': True,
                        'id': conteudo_salvo.id,
                        'conteudo_gerado': conteudo_salvo.conteudo_gerado or '',
                        'sugestoes_titulos': conteudo_salvo.sugestoes_titulos or '',
                        'hashtags': conteudo_salvo.hashtags or '',
                        'sugestoes_imagens': conteudo_salvo.sugestoes_imagens or '',
                    }
                    print("=== DEBUG JSON RESPONSE ===")
                    print("RESPONSE DATA:", response_data)
                    print("SUGESTÕES DE IMAGENS NO RESPONSE:", repr(response_data['sugestoes_imagens']))
                    print("=======================")
                    
                    return JsonResponse(response_data)
                else:
                    return redirect('listar_conteudos_educacionais')
                
            except Exception as e:
                error_msg = f"Erro ao gerar conteúdo: {str(e)}"
                print("ERRO NA VIEW:", error_msg)
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': error_msg})
        else:
            error_msg = f"Erro de validação: {serializer.errors}"
            print("ERRO DE VALIDAÇÃO:", error_msg)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_msg})

    context = {
        'tipos_conteudo': ConteudoEducacional.TIPOS_CONTEUDO,
    }
    
    return render(request, 'psico_saas/conteudo_educacional_form.html', context)

@login_required
def listar_conteudos_educacionais_view(request):
    """
    Lista todos os conteúdos educacionais do usuário.
    """
    conteudos = ConteudoEducacional.objects.filter(
        usuario=request.user).order_by('-data_criacao')

    context = {
        'conteudos': conteudos
    }

    return render(request, 'psico_saas/conteudo_educacional_lista.html', context)


@login_required
def ver_conteudo_educacional_view(request, pk):
    """
    Exibe os detalhes de um conteúdo educacional.
    """
    conteudo = get_object_or_404(
        ConteudoEducacional, pk=pk, usuario=request.user)

    context = {
        'conteudo': conteudo
    }

    return render(request, 'psico_saas/ver_conteudo_educacional.html', context)


@login_required
def salvar_conteudo_educacional_view(request, pk):
    """
    View para salvar/atualizar um conteúdo educacional existente.
    """
    if request.method == 'POST':
        try:
            print("=== 🚀 INICIANDO SALVAMENTO ===")
            print("ID do conteúdo:", pk)
            print("Usuário:", request.user)
            print("Dados POST recebidos:", dict(request.POST))
            
            conteudo = get_object_or_404(ConteudoEducacional, pk=pk, usuario=request.user)
            
            # Log dos valores atuais
            print("Valores atuais no BD:")
            print(f"  Título: {conteudo.titulo}")
            print(f"  Conteúdo: {len(conteudo.conteudo_gerado or '')} chars")
            print(f"  Imagens: {len(conteudo.sugestoes_imagens or '')} chars")
            
            # Atualizar os campos
            novo_titulo = request.POST.get('titulo')
            novo_conteudo = request.POST.get('conteudo_gerado')
            novas_imagens = request.POST.get('sugestoes_imagens')
            
            print("Novos valores recebidos:")
            print(f"  Título: {novo_titulo}")
            print(f"  Conteúdo: {len(novo_conteudo or '')} chars")
            print(f"  Imagens: {len(novas_imagens or '')} chars")
            
            if novo_titulo:
                conteudo.titulo = novo_titulo
            if novo_conteudo:
                conteudo.conteudo_gerado = novo_conteudo
            if request.POST.get('sugestoes_titulos'):
                conteudo.sugestoes_titulos = request.POST.get('sugestoes_titulos')
            if request.POST.get('hashtags'):
                conteudo.hashtags = request.POST.get('hashtags')
            if novas_imagens is not None:  # Permite string vazia
                conteudo.sugestoes_imagens = novas_imagens
            
            # SALVAR EFETIVAMENTE
            conteudo.save()
            
            # Verificar se salvou
            conteudo.refresh_from_db()
            print("Valores após salvamento:")
            print(f"  Título: {conteudo.titulo}")
            print(f"  Conteúdo: {len(conteudo.conteudo_gerado or '')} chars")
            print(f"  Imagens: {len(conteudo.sugestoes_imagens or '')} chars")
            print("=== ✅ SALVAMENTO CONCLUÍDO ===")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Conteúdo salvo com sucesso!'})
            else:
                return redirect('listar_conteudos_educacionais')
                
        except Exception as e:
            print(f"=== ❌ ERRO NO SALVAMENTO: {str(e)} ===")
            import traceback
            traceback.print_exc()
            
            error_msg = f"Erro ao salvar conteúdo: {str(e)}"
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': error_msg})
    
    return JsonResponse({'success': False, 'error': 'Método não permitido'})