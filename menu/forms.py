from django import forms
from .models import Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        # Fields that will render in the forms from Category models
        fields = ['category_name','description']