from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_NEW_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUuserApi(TestCase):
    #prueba la API publica de ususario 
    def setUp(self):
        self.client=APIClient()

    def test_create_valid_user_success(self):
        #crea un usuario con un payload exitoso 
        payload = {
            'email': 'test@prueba.com',
            'password': 'prueba123',
            'name': 'prueba'

        }
        res = self.client.post(CREATE_NEW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user=get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        #crear un usuario que ya existe
        payload = {
            'email': 'test@prueba.com',
            'password': 'prueba123',
            'name': 'prueba'

        }
        create_user(**payload)

        res = self.client.post(CREATE_NEW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        #la constraseña es demasiado corta
        payload = {
            'email': 'prueba@prueba.com',
            'password': 'pr',
            'name': 'prueba'
        }
        res = self.client.post(CREATE_NEW_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        use_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(use_exists)

    def test_create_token_for_user(self):
        #probar que el token sea creado por el usuario 
        payload = {
            'email': 'prueba@prueba.com',
            'password': 'prueba123',
            'name': 'prueba'
        }
        create_user(**payload)
        res= self.client.post(TOKEN_URL, payload)
    
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    
    def test_create_token_invalid_credentials(self):
        #rpobar que el token no es creado con credenciales invalidas
        create_user(email='prueba@prueba.com', password='prueba')
        payload = {'email': 'prueba@prueba.com', 'password':'fallas'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        #prueba que no se crea un token si no se crea un usuario 
        payload={
            'email': 'prueba@prueba.com',
            'password': 'prueba123',
            'name': 'prueba'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def teset_create_token_missing_field(self):
        #probar que el emial y contraseña requeridos 
        res = self.client.post(TOKEN_URL, {'email'})
        
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)