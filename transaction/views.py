from django.shortcuts import render
from .models import Transaction


def index(request):
    transactions = None
    if request.user.is_authenticated :
        transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'index.html', context={'transactions': transactions, 'user': request.user})