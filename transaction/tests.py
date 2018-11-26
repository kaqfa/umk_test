from django.test import TestCase
from .models import Transaction, TransactionRepo
from django.contrib.auth.models import User
from django.test import Client, LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class AdminTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    # def tearDown(self):
    #     self.browser.quit()

    def test_admin_site(self):
        self.browser.get(self.live_server_url+'/admin/')
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)


class TransactionModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'pass')
    
    def test_minimal_input(self):
        Transaction.objects.create(user=self.user, 
                                   judul='Transaksi test', 
                                   jumlah=15000)
                                   
        trans = Transaction.objects.filter(judul='Transaksi test')        
        self.assertEquals(trans[0].jumlah, 15000)
        self.assertEquals(trans[0].status, 'v')
        self.assertEquals(trans[0].jenis, 'k')

    def test_all_input(self):
        Transaction.objects.create(user=self.user, 
                                   judul='Transaksi test', 
                                   status='p', jenis='k',
                                   jumlah=20000, 
                                   ket='Keterangan transaksi')
        trans = Transaction.objects.filter(judul='Transaksi test')
        self.assertEquals(trans[0].jumlah, 20000)
        self.assertEquals(trans[0].status, 'p')

    def test_hitung_saldo(self):
        Transaction.objects.create(user=self.user, jenis='p',
                                   judul='Transaksi 1', 
                                   jumlah=2000000)
        Transaction.objects.create(user=self.user,
                                   judul='Transaksi 2', 
                                   jumlah=50000)
        Transaction.objects.create(user=self.user, jenis='k',
                                   judul='Transaksi 3', 
                                   jumlah=100000)

        repo = TransactionRepo(self.user)
        self.assertEquals(repo.get_saldo(), 1850000)
                                   

class TransactionViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'user@test.com', 'pass')
        Transaction.objects.create(user=self.user, jenis='p',
                                   judul='Transaksi 1', 
                                   jumlah=2000000)
        Transaction.objects.create(user=self.user,
                                   judul='Transaksi 2', 
                                   jumlah=50000)
        Transaction.objects.create(user=self.user, jenis='k',
                                   judul='Transaksi 3', 
                                   jumlah=100000)        

    def test_no_login_user(self):
        c = Client()
        response = c.get('')
        self.assertContains(response, 'tidak ada transaksi')
        self.assertNotContains(response, 'Tampilkan semua list keuangan')

    def test_login_user_only_see_theirs(self):
        user2 = User.objects.create_user('user2', 'user2@test.com', 'pass2')
        Transaction.objects.create(user=user2, jenis='p',
                                   judul='Transaksi 4', 
                                   jumlah=1500000)
        
        c = Client()
        c.login(username='user', password='pass')
        response = c.get('')
        self.assertContains(response, 'Transaksi 1')
        self.assertNotContains(response, 'Transaksi 4')