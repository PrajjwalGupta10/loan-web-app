from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect   # ✅ Added HttpResponse
from django.urls import reverse
from django.conf import settings
from .forms import CustomerSignUpForm, CustomerLoginForm, UpdateCustomerForm  # ✅ Added missing imports
from .models import CustomerSignUp


# -----------------------------
# Customer Sign-up with Email Verification
# -----------------------------
def sign_up_view(request):
    error = ''
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    form = CustomerSignUpForm()
    if request.method == 'POST':
        form = CustomerSignUpForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # user inactive until email verified
            user.save()

            # Create Customer Profile
            CustomerSignUp.objects.create(user=user)

            # --- Email verification ---
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('loginApp/account_verification_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return HttpResponse("✅ Please confirm your email address to complete the registration.")

        else:
            # Collect form validation errors
            error_list = []
            for field, messages in form.errors.items():
                for msg in messages:
                    error_list.append(f"{field.capitalize()}: {msg}")
            error = " | ".join(error_list)

    return render(
        request,
        'loginApp/signup.html',
        context={'form': form, 'user': "Customer Register", 'error': error}
    )


# -----------------------------
# Account Activation (Email Link)
# -----------------------------
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return render(request, 'loginApp/activation_success.html')
        return redirect('account:signup_customer')

    else:
        return render(request, 'loginApp/activation_invalid.html')


# -----------------------------
# Login
# -----------------------------
def login_view(request):
    form = CustomerLoginForm()
    if request.method == 'POST':
        form = CustomerLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))

        return render(
            request,
            'loginApp/login.html',
            context={'form': form, 'user': "Customer Login", 'error': 'Invalid username or password'}
        )

    return render(request, 'loginApp/login.html', context={'form': form, 'user': "Customer Login"})


# -----------------------------
# Logout
# -----------------------------
@login_required()
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


# -----------------------------
# Edit Customer Profile
# -----------------------------
@login_required(login_url='/account/login-customer/')
def edit_customer(request):
    customer = CustomerSignUp.objects.get(user=request.user)
    form = UpdateCustomerForm(instance=customer)
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():  # ✅ added missing parentheses
            form.save()
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'loginApp/edit.html', context={'form': form})
