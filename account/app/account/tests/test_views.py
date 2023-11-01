from django.test import TestCase, SimpleTestCase
from rest_framework.test import APIRequestFactory

from ..serializers import AccountSerializer
from ..views import AccountList, AccountCreate, AccountUpdate, \
    AccountDetail, AccountDestroy  # Замените на правильный импорт вашего представления
from ..models import Account, Users  # Замените на правильный импорт вашей модели


class AccountListViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountList.as_view({'get': 'list'})
        self.accounts = [
            Account.objects.create(username='user1', balance=100.0),
            Account.objects.create(username='user2', balance=200.0),
        ]

    def test_list_accounts(self):
        request = self.factory.get('/account5/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_empty_accounts(self):
        Account.objects.all().delete()
        request = self.factory.get('/account5/')
        response = self.view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)


class AccountCreateViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountCreate.as_view({'post': 'create'})

        self.user = Users.objects.create(full_names='John Doe', username='johndoe', email='johndoe@example.com',
                                         password='securepassword')

    def test_create_account(self):
        data = {
            'id': self.user.id,
            'balance': 100.0,
        }

        request = self.factory.post('/account2/', data, format='json')
        response = self.view(request)
        self.assertEqual(response.status_code, 201)

        self.assertTrue(Account.objects.filter(user=self.user).exists())


class AccountUpdateViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountUpdate.as_view()
        self.account = Account.objects.create(id=10, balance=100)

    def test_update_account(self):
        request = self.factory.put(f'/account4/{self.account.id}/', format='json')
        response = self.view(request, pk=self.account.id)

        self.assertEqual(response.status_code, 200)

        updated_account = Account.objects.get(id=self.account.id)
        self.assertEqual(updated_account.balance, 200.0)

    def test_update_nonexistent_account(self):
        request = self.factory.put('/account4/nonexistent_id/', format='json')
        response = self.view(request, pk='nonexistent_id')

        self.assertEqual(response.status_code, 404)


class AccountDetailViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountDetail.as_view()
        self.account = Account.objects.create(balance=100.0, usernameid='user123')

    def test_get_account_detail(self):
        request = self.factory.get(f'/account5/user123/')
        response = self.view(request, usernameid='user123')

        self.assertEqual(response.status_code, 200)

        account = Account.objects.get(usernameid='user123')
        serializer = AccountSerializer(account)

        self.assertEqual(response.data, serializer.data)

    def test_get_nonexistent_account_detail(self):
        request = self.factory.get('/account5/nonexistent_username/')
        response = self.view(request, usernameid='nonexistent_username')

        self.assertEqual(response.status_code, 404)


class AccountDestroyViewTest(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = AccountDestroy.as_view()
        self.account = Account.objects.create(balance=100.0)

    def test_destroy_account(self):
        request = self.factory.delete(f'/account3/{self.account.id}/')
        response = self.view(request, pk=self.account.id)

        self.assertEqual(response.status_code, 204)

        with self.assertRaises(Account.DoesNotExist):
            Account.objects.get(id=self.account.id)

    def test_destroy_nonexistent_account(self):
        request = self.factory.delete('/account3/nonexistent_id/')
        response = self.view(request, pk='nonexistent_id')

        self.assertEqual(response.status_code, 404)
