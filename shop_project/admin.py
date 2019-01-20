from .models import *
from django.contrib import admin



@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):

    list_display = ('name', 'description', 'price', 'item_image',)
    readonly_fields = ('item_image',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields =  ('user__username',)