from django.db import models
from django.contrib.auth.models import User
from loginApp.models import CustomerSignUp
import uuid
# Create your models here.


class loanCategory(models.Model):
    loan_name = models.CharField(max_length=250)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Enter interest rate (e.g. 8.50 for 8.5%)")
    creation_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.loan_name} ({self.interest_rate}%)"

class loanRequest(models.Model):
    customer = models.ForeignKey(CustomerSignUp, on_delete=models.CASCADE)
    category = models.ForeignKey('loanCategory', on_delete=models.CASCADE)
    reason = models.TextField()

    loan_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    # year = models.IntegerField(blank=True, null=True)   
    year = models.PositiveIntegerField(default=1)
    request_date = models.DateField(auto_now_add=True)   

    property_address = models.TextField(blank=True, null=True)
    property_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    property_documents = models.FileField(upload_to='documents/', blank=True, null=True)
    occupation_type = models.CharField(max_length=100, blank=True, null=True)
    identity_proof = models.FileField(upload_to='documents/', blank=True, null=True)
    income_proof = models.FileField(upload_to='documents/', blank=True, null=True)
    bank_statement = models.FileField(upload_to='documents/', blank=True, null=True)

    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


# class loanRequest(models.Model):
#     customer = models.ForeignKey(
#         CustomerSignUp, on_delete=models.CASCADE, related_name='loan_customer')
#     category = models.ForeignKey(
#         loanCategory, on_delete=models.CASCADE, null=True)
#     request_date = models.DateField(auto_now_add=True)
#     status_date = models.CharField(
#         max_length=150, null=True, blank=True, default=None)
#     reason = models.TextField()
#     status = models.CharField(max_length=100, default='pending')
#     amount = models.PositiveIntegerField(default=0)
#     year = models.PositiveIntegerField(default=1)

#     def __str__(self):
#         return self.customer.user.username


class CustomerLoan(models.Model):
    customer = models.ForeignKey(
        CustomerSignUp, on_delete=models.CASCADE, related_name='loan_user')
    total_loan = models.PositiveIntegerField(default=0)
    payable_loan = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.customer.user.username


class loanTransaction(models.Model):
    customer = models.ForeignKey(
        CustomerSignUp, on_delete=models.CASCADE, related_name='transaction_customer')

    transaction = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.PositiveIntegerField(default=0)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.customer.user.username
