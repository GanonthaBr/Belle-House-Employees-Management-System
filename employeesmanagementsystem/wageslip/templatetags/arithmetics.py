from decimal import Decimal
from django import template
register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return None
    
def substract(value,arg):
    try:
        return Decimal(value) - Decimal(arg)
    except (ValueError, TypeError):
        return None