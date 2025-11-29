from django import template

register = template.Library()

@register.filter(name='get')
def get_item(dictionary, key):
    """Permite acessar um item de um dicionário (como request.POST ou form.errors) usando uma chave no template. Isso é necessário porque a sintaxe de ponto (dict.key) falha em alguns casos específicos do Django."""
    # Garante que funciona apenas em dicionários ou objetos com método .get()
    if hasattr(dictionary, 'get'):
        return dictionary.get(key)
    return None