from django import forms
from .models import Transactions

class TransactionForm(forms.ModelForm):
    docfile = forms.FileField(
        label='Select a file',
        help_text='max. 42 megabytes'
    )

    class Meta:
        model = Transactions
        fields='__all__'