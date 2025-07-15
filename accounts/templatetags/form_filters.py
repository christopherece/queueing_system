from django import template

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def add_class(value, arg):
    """Add CSS classes to form fields"""
    return value.as_widget(attrs={'class': arg})
