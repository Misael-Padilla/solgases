from django import template

register = template.Library()


@register.filter
def with_aria_required(campo):
    if campo.field.required:
        return campo.as_widget(attrs={'aria-required': 'true'})
    return campo.as_widget()
