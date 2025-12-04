from django import forms
from .models import User

# This call will inherit Modelform from django forms
# 
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput()) # We need to create this field because model do not have this field
    class Meta:
        model = User # Define user model from where you want to access the fields
        #fields = ['first_name', 'last_name', 'username', 'email', 'phone_number','password']   # Define which are the feild from the model you want to access in the form
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    # This method is design for non- field data validation and error handling
    # django model form by default call this clean method whenever the form is triggered

    def clean(self):
        cleaned_data = super(UserForm, self).clean() # Super method overwrite the clean method
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']

        if password != confirm_password:
            raise forms.ValidationError(
                'Password does not match!'
            )