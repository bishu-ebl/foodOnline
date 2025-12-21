from django.contrib import admin
from .models import Category, FoodItem

# Create this class is for prepopulating slug field and pass it through
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'vendor', 'slug', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name') # since the vendor is a foreign key. so target model's field_name should be used

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title','category', 'vendor', 'price','is_available','updated_at')
    search_fields = ('food_title', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter = ('is_available',) # , is used since it is a Tuple

# Register your models here.

admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodItem, FoodItemAdmin)
