from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class ModelTest(TestCase):
    def test_create_user_with_email_seccessful(self):
        #crea usuario nuevo correctamente
        email = 'prueba@prueba.com'
        password = 'prueba123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        #normalizar el correo todo sea en minuscula
        email = 'prueba@¨PRUEBA.COM'
        user = get_user_model().objects.create_user(
            email, 'prueba123')

        self.assertEqual(user.email, email.lower())
    
    def test_user_invalid_email(self):
        #email no valido
        with self.assertRaises(ValueError):
            get_user_model().objects.creare_user(None, 'Prueba')

    def test_new_create_superuser(self):
        #crear super user
        email = 'prueba@prueba.com'
        password = 'prueba123'
        user = get_user_model().objects.create_superuser(
            email=email,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
                

