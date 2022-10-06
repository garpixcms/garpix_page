from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def gx_component(context, component):
    user = context['user']
    component_path = component['admin_edit_url']

    return f'data-gx-component={component_path}' if user.is_authenticated and user.is_staff else ''
