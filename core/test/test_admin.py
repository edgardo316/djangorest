from core import admin
from django.test import TestCase, client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminSiteTest():
    def setUp(self):
        self.client = client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'admin@prueba.com',
            password = 'pass123'

        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email = 'test@prueba.com',
            password = 'pass123',
            name = 'nombre completo'
        )
    def test_user_list(self):
        #testerar que los usuarios an sido enlistados 
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
    
    def test_user_change_page(self):
        url= reverse('admin:core_user_change', args=[self.user.id])
        res= self.client.get(url)

        set.assertEqual(res.status_code, 200)
    
    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res= self.client.get(url)

        self.assertEqual(res.status_code, 200)