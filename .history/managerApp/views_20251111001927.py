from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from managerApp.forms import AdminLoginForm
from django.shortcuts import redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from loanApp.models import loanCategory, loanRequest, CustomerLoan, loanTransaction
from .forms import LoanCategoryForm
from loginApp.models import CustomerSignUp
from django.contrib.auth.models import User
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Sum
# Create your views here.
# Create your views here.
from decimal import Decimal



def superuser_login_view(request):
    form = AdminLoginForm()
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        if request.method == 'POST':
            form = AdminLoginForm(data=request.POST)

            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                user = authenticate(
                    request, username=username, password=password)

                if user is not None:

                    if user.is_superuser:
                        login(request, user)
                        return HttpResponseRedirect(reverse('managerApp:dashboard'))
                    else:
                        return render(request, 'admin/adminLogin.html', context={'form': form, 'error': "You are not Super User"})

            else:

                return render(request, 'admin/adminLogin.html', context={'form': form, 'error': "Invalid Username or Password "})
    return render(request, 'admin/adminLogin.html', context={'form': form, 'user': "Admin Login"})


# @user_passes_test(lambda u: u.is_superuser)
@staff_member_required(login_url='/manager/admin-login')
def dashboard(request):

    totalCustomer = CustomerSignUp.objects.all().count(),
    requestLoan = loanRequest.objects.all().filter(status='pending').count(),
    approved = loanRequest.objects.all().filter(status='approved').count(),
    rejected = loanRequest.objects.all().filter(status='rejected').count(),
    totalLoan = CustomerLoan.objects.aggregate(Sum('total_loan'))[
        'total_loan__sum'],
    totalPayable = CustomerLoan.objects.aggregate(
        Sum('payable_loan'))['payable_loan__sum'],
    totalPaid = loanTransaction.objects.aggregate(Sum('payment'))[
        'payment__sum'],

    dict = {
        'totalCustomer': totalCustomer[0],
        'request': requestLoan[0],
        'approved': approved[0],
        'rejected': rejected[0],
        'totalLoan': totalLoan[0],
        'totalPayable': totalPayable[0],
        'totalPaid': totalPaid[0],

    }
    print(dict)

    return render(request, 'admin/dashboard.html', context=dict)


@staff_member_required(login_url='/manager/admin-login')
def add_category(request):
    form = LoanCategoryForm()
    if request.method == 'POST':
        form = LoanCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('managerApp:dashboard')
    return render(request, 'admin/admin_add_category.html', {'form': form})


@staff_member_required(login_url='/manager/admin-login')
def total_users(request):
    users = CustomerSignUp.objects.all()

    return render(request, 'admin/customer.html', context={'users': users})

#user remove function
@staff_member_required(login_url='/manager/admin-login')
def user_remove(request, pk):
    CustomerSignUp.objects.get(id=pk).delete()
    user = User.objects.get(id=pk)
    user.delete()
    return HttpResponseRedirect('/manager/users')
    # return redirect('managerApp:users')


@staff_member_required(login_url='/manager/admin-login')
def loan_request(request):
    loanrequest = loanRequest.objects.filter(status='pending')
    return render(request, 'admin/request_user.html', context={'loanrequest': loanrequest})

@staff_member_required(login_url='/manager/admin-login')
def view_documents(request, id):
    loan = loanRequest.objects.get(id=id)  # Get the loan request
    return render(request, 'admin/view_documents.html', {'loan': loan})


@staff_member_required(login_url='/manager/admin-login')
def approved_request(request, id):
    today = date.today()
    status_date = today.strftime("%B %d, %Y")

    loan_obj = loanRequest.objects.get(id=id)
    loan_obj.status_date = status_date
    loan_obj.save()

    year = Decimal(str(loan_obj.year)) if loan_obj.year else Decimal('1')
    approved_customer = loan_obj.customer

    # ✅ Convert loan amount safely to Decimal
    loan_amount = Decimal(loan_obj.loan_amount)
    # interest_rate = Decimal('0.12')
    interest_rate = Decimal(loan_obj.category.interest_rate) / 100
    payable_amount = loan_amount + (loan_amount * interest_rate * year)

    # ✅ Add or update CustomerLoan entry
    if CustomerLoan.objects.filter(customer=approved_customer).exists():
        existing_loan = CustomerLoan.objects.get(customer=approved_customer)
        existing_loan.total_loan = existing_loan.total_loan + loan_amount
        existing_loan.payable_loan = existing_loan.payable_loan + payable_amount
        existing_loan.save()
    else:
        save_loan = CustomerLoan(
            customer=approved_customer,
            total_loan=loan_amount,
            payable_loan=payable_amount
        )
        save_loan.save()

    # ✅ Update loan request status
    loanRequest.objects.filter(id=id).update(status='approved')

    # ✅ Send approval email
    subject = "Your Loan Request Has Been Approved"
    message = f"""
Dear {approved_customer.user.username},

Congratulations! Your loan request of ₹{loan_amount} has been approved.

Loan Details:
- Tenure: {year} year(s)
- Payable Amount (with 12% yearly interest): ₹{payable_amount}

Please log in to your account to view full loan details.

Regards,  
Loan Management Team
"""
    recipient = [approved_customer.user.email]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient, fail_silently=False)

    # ✅ Return to the pending requests page
    loan_requests = loanRequest.objects.filter(status='pending')
    return render(request, 'admin/request_user.html', context={'loanrequest': loan_requests})



@staff_member_required(login_url='/manager/admin-login')
def rejected_request(request, id):
    today = date.today()
    status_date = today.strftime("%B %d, %Y")

    # Get loan object
    loan_obj = loanRequest.objects.get(id=id)
    loan_obj.status_date = status_date
    loan_obj.save()

    # Update status to 'rejected'
    loanRequest.objects.filter(id=id).update(status='rejected')

    # ✅ Send rejection email
    rejected_customer = loan_obj.customer
    subject = "Your Loan Request Has Been Rejected"
    message = f"""
    Dear {rejected_customer.user.username},

    We regret to inform you that your loan request of ₹{loan_obj.loan_amount} has been **rejected** after careful review.

    Loan Details:
    - Requested Amount: ₹{loan_obj.loan_amount}
    - Tenure: {loan_obj.year} years
    - Date: {status_date}

    You can log in to your account for more details or to reapply in the future.

    Regards,
    Loan Management Team
    """

    recipient = [rejected_customer.user.email]

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient, fail_silently=False)
        print("📧 Rejection email sent successfully to", rejected_customer.user.email)
    except Exception as e:
        print("❌ Error sending rejection email:", e)

    # ✅ Return to request page
    loanrequest = loanRequest.objects.filter(status='pending')
    return render(request, 'admin/request_user.html', context={'loanrequest': loanrequest})



@staff_member_required(login_url='/manager/admin-login')
def approved_loan(request):
    # print(datetime.now())
    approvedLoan = loanRequest.objects.filter(status='approved')
    return render(request, 'admin/approved_loan.html', context={'approvedLoan': approvedLoan})


@staff_member_required(login_url='/manager/admin-login')
def rejected_loan(request):
    rejectedLoan = loanRequest.objects.filter(status='rejected')
    return render(request, 'admin/rejected_loan.html', context={'rejectedLoan': rejectedLoan})


@staff_member_required(login_url='/manager/admin-login')
def transaction_loan(request):
    transactions = loanTransaction.objects.all()
    return render(request, 'admin/transaction.html', context={'transactions': transactions})
