from django.db import models
from vendor.models import Vendor

# Create two models one for category and another one for fooditems/product

class Category(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=50, unique=True)
    # slug refer to the url pattern of category_name, like if category is sea food then slug will sea-food
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Thi class is for showing the model name as 'categories' in the admin panel
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    # This function is changing the category_name into capitalize, means first letter capital
    # This is use to check whether the use adding category with the same name 
    def clean(self):
        self.category_name = self.category_name.capitalize()


    def __str__(self):
        return self.category_name
    
class FoodItem(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    food_title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=250, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='foodimages')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.food_title