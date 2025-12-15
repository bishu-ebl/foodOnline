from django import forms
from .models import User, UserProfile
from .validators import allow_only_image_validator

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
        

class UserProfileForm(forms.ModelForm):
    # profile_picture = forms.ImageField(widget=forms.FileInput(attrs= {'class': 'btn btn-info'}), validators=[allow_only_image_validator])
    # cover_photo = forms.ImageField(widget=forms.FileInput(attrs= {'class': 'btn btn-info'}),validators=[allow_only_image_validator])
    # While using custom validation instead of ImageField, we need to use FileField
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs= {'class': 'btn btn-info'}), validators=[allow_only_image_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs= {'class': 'btn btn-info'}),validators=[allow_only_image_validator])
    # There is two way to make a field ready only
    # first method
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        # fields = ['profile_picture', 'cover_photo', 'addess_line_1','addess_line_2','country','state','city','pin_code','latitude','longitude']
        fields = ['profile_picture', 'cover_photo', 'address','country','state','city','pin_code','latitude','longitude']

    # 2nd metthod to make fields read only by init method
    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'