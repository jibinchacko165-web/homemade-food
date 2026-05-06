from django.contrib import admin
from .models import FoodItem, ChefProfile


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'chef', 'category', 'price', 'is_available', 'created_at')
    list_filter = ('category', 'is_available', 'created_at')
    search_fields = ('name', 'chef__username')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ChefProfile)
class ChefProfileAdmin(admin.ModelAdmin):
    list_display = ('chef', 'specialty', 'years_of_experience', 'average_rating', 'is_verified')
    list_filter = ('is_verified', 'average_rating')
    search_fields = ('chef__username', 'specialty')
    readonly_fields = ('created_at', 'updated_at')
