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
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # ✅ Ensure all fields are required
    #     for field in self.fields.values():
    #         field.required = True

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

        # Make all fields required by default
        for field in self.fields.values():
            field.required = True

        # ❗ If category is not "Home Loan", make property fields optional
        instance = kwargs.get('instance')
        if instance and getattr(instance.category, 'name', '').lower() != 'home loan':
            self.fields['property_address'].required = False
            self.fields['property_value'].required = False
            self.fields['property_documents'].required = False



class LoanTransactionForm(forms.ModelForm):
    class Meta:
        model = loanTransaction
        fields = ('payment',)

