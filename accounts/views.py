from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages

# Create your views here.
def registerUser(request):
    #return HttpResponse('This is a user registration form')
    # Check the request method is POST or not
    if request.method == 'POST':
        #print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using form
            # password = form.cleaned_data['password'] # First method of setting the password in hash format
            # user = form.save(commit=False) # This means the information is ready to save. This is use if we want to add additional field like role
            # user.set_password(password) # First method of setting the password in hash format
            # user.role = User.CUSTOMER # assign CUSTOMER role to the user
            # user.save()

            # Create the user using create_user method
            # form.cleaned_date is return the cleaed data by clean method
            first_name = form.cleaned_data['first_name'] 
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been registered successfully')
            #messages.error(request, 'Your account has been registered successfully')
            #print('User is created')
            return redirect('registerUser')
            #return redirect(url_for('registerUser'))
        else:
            # This code is added to handle form field error and non field errors
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    # Pass this UserForm inside the registerUser.html
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)
