from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def gx_component(context, component):
    if not user.is_authenticated and not user.is_staff:
        return ''

    if not hasattr(context, 'user') or not hasattr(component, 'admin_edit_url'):
        return ''

    user = context['user']
    component_path = component['admin_edit_url']
    return f'data-gx-component={component_path}'
