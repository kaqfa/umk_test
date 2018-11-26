from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Transaction(models.Model):

    JENIS_CHOICES = [('m', 'Pemasukan'), ('k', 'Pengeluaran')]
    STATUS_CHOICES = [('v', 'Valid'), ('p', 'Pending'), ('i', 'Invalid')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    judul = models.CharField(max_length = 70)
    jumlah = models.IntegerField()
    ket = models.TextField('Keterangan')
    jenis = models.CharField(max_length = 1, choices=JENIS_CHOICES, 
                             default='k')
    status = models.CharField(max_length = 1, choices=STATUS_CHOICES, 
                              default='v')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s [%s]" % (self.judul, self.jumlah)

class TransactionRepo():

    def __init__(self, user=None):
        self.user = user

    def get_saldo(self):
        if self.user is None:
            return 0
        else:
            transs = Transaction.objects.filter(user=self.user)
            saldo = 0
            for trans in transs:
                if trans.jenis == 'k':
                    saldo -= trans.jumlah
                else:
                    saldo += trans.jumlah
            return saldo