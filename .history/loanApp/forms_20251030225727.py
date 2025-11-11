from django import forms
from .models import loanRequest, loanTransaction

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = loanRequest
        fields = ('category', 'reason')


class LoanApplicationDetailsForm(forms.ModelForm):
    class Meta:
        model = loanRequest
        fields = (
            'loan_amount', 'year',
            'property_address', 'property_value', 'property_documents',
            'occupation_type', 'identity_proof', 'income_proof', 'bank_statement'
        )
        # widgets = {
        #     'property_documents': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        #     'identity_proof': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        #     'income_proof': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        #     'bank_statement': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        # }


class LoanTransactionForm(forms.ModelForm):
    class Meta:
        model = loanTransaction
        fields = ('payment',)
