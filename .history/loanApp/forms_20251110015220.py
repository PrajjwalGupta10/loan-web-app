from django import forms
from .models import loanRequest, loanTransaction

OCCUPATION_CHOICES = [
        ('salaried', 'Salaried'),
        ('self_employed', 'Self-Employed'),
        ('student', 'Student'),
        ('retired', 'Retired'),
        ('business_owner', 'Business Owner'),
        ('government_employee', 'Government Employee'),
        ('unemployed', 'Unemployed'),
    ]


class LoanRequestForm(forms.ModelForm):

    class Meta:
        model = loanRequest
        fields = ('category', 'reason')
        # fields = ['loan_amount', 'year', 'property_address', 'property_value', 'property_documents', 'occupation_type', 'identity_proof', 'income_proof', 'bank_statement']
        

        
class LoanApplicationDetailsForm(forms.ModelForm):
    occupation_type = forms.ChoiceField(choices=OCCUPATION_CHOICES, required=True)

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

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # ✅ Make all file fields optional
            self.fields['property_documents'].required = False
            self.fields['identity_proof'].required = False
            self.fields['income_proof'].required = False
            self.fields['bank_statement'].required = False

class LoanTransactionForm(forms.ModelForm):
    class Meta:
        model = loanTransaction
        fields = ('payment',)
