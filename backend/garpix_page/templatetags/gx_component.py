from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def gx_component(context, component):
    user = context['user']
    if not user.is_authenticated or not user.is_staff:
        return ''

    component_path = None
    if isinstance(component, dict):
        component_path = component.get('admin_edit_url')
    elif hasattr(component, 'admin_edit_url'):
        component_path = getattr(component, 'admin_edit_url')

    if component_path:
        return f'data-gx-component={component_path}'
    else:
        return ''
