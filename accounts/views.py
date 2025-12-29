from django.shortcuts import render,redirect
from django.http import HttpResponse

from accounts.utils import detectUser, send_verification_email
from vendor.forms import VendorForm
from vendor.models import Vendor
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.template.defaultfilters import slugify

# Restric the vandor from accessing customer page
# for that we will custom decorator as follows

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# Restric the customer from accessing vendor page
# # for that we will custom decorator as follows
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('myAccount')
    #return HttpResponse('This is a user registration form')
    # Check the request method is POST or not
    elif request.method == 'POST':
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

            # Send verification email
            print("Sending email...")
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
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

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('myAccount')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES) # since license file will post from vendor form
        if form.is_valid() and v_form.is_valid:
            first_name = form.cleaned_data['first_name'] 
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            vendor.vendor_slug = slugify(vendor_name)+'-'+str(user.id)
            user_profile = UserProfile.objects.get(user=user) # This will hanadle by Signals.py
            vendor.user_profile = user_profile
            vendor.save()  
            # Send verification email
            print("Sending email...")
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request,'Your account has been successfully created. Please wait for the approval')
            return redirect(registerVendor)  
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }
    return render (request, 'accounts/registerVendor.html', context)

def activate(request, uidb64, token):
    # Activate the user by setting the is_activate status to True
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulation! your account is activated')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')

def login(request):
    # Add this statement to check whether the user is already logged in
    # If yes then we should not have any access to other pages like login page, registerUser Page etc
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in!")
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # use django build-in authenticate method to verify whether the user is exist with this email and password
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now loggied in')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render (request, 'accounts/login.html')

def logout(request):
    #return render (request, 'accounts/logout.html')
    auth.logout(request)
    messages.info(request,"You are looged out")
    return redirect('login')

# This function will invoked when user are logged in
# @login_required, this decorator will send the user in login page if the user not logged in
@login_required(login_url='login')
def myAccount(request):
    # To determine which URL to redirect based on user role, 
    # create a helpher method name utils.py insside accounts apps
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)

# def dashboard(request):
#     return render(request, 'accounts/dashboard.html')

# Customer must be logged in to see this dashboard
@login_required(login_url='login')
# User logged in as customer role can see the page
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request, 'accounts/custDashboard.html')

# Customer must be logged in to see this dashboard
@login_required(login_url='login')
# User logged in as vendor role can see the page
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    # user=request.user, because only the logged in user can have access to the page
    # vendor = Vendor.objects.get(user=request.user)
    # context = {
    #     'vendor': vendor,
    # }
    # return render(request, 'accounts/vendorDashboard.html', context)
    # instead of passing context in the return, we call context_processors here 
    return render(request, 'accounts/vendorDashboard.html')

# This section is to handle forgot password

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists:
            user = User.objects.get(email__exact=email)
            # sent password reset link
            mail_subject = 'Reset your password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password rest link has been sent to your email adddress.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')

def reset_password_validate(request, uidb64, token):
    # validate the user by decoding the token and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # uid is stored in request.session['uid'] variable to determine for which useer password will be rest
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('myAccount')
     

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful!')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')
    return render(request, 'accounts/reset_password.html')