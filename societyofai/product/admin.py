from django.contrib import admin
from .models import Product, Category, Order
# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'order_date',
                    'status'

                    ]
    list_display_links = [
        'user',

    ]
    list_filter = ['status',
                  ]
    search_fields = [
        'user__email',

    ]
    readonly_fields = ('product',)
    
    def order_date(self, obj):
        if obj:
            return obj.created_at.date()
        return '-'


admin.site.register(Order, OrderAdmin)
admin.site.register(Product)
admin.site.register(Category)
