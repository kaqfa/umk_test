from django.contrib import admin
from .models import Transaction

# Register your models here.
class TransactionAdmin(admin.ModelAdmin):

    list_display = ['judul', 'jumlah', 'jenis', 'status', 'user']


admin.site.register(Transaction, TransactionAdmin)