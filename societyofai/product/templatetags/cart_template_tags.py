from django import template
from product.models import Cart

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs = Cart.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs.first().items.count()
    return 0
