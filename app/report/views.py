from django.shortcuts import render
from .forms import TransactionForm
import pandas as pd
import uuid
from .models import Transactions
from .mail import report as report_mail

# Create your views here.
def report(request):
    if request.method == 'POST':
        df = pd.read_csv(request.FILES['files'])
        uuid_key = uuid.uuid4()
        data = []
        for index, row in df.iterrows():
            tx = Transactions(report_id=row['id'], date=row['date'], report=uuid_key, amount=row['amount'])
            tx.save()
            data.append(tx)
        report_mail(data, df, request.POST.get('email'))

    return render(request, template_name='report/report.html')