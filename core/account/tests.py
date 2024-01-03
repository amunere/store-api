from django.test import TestCase
from django.urls import reverse
import json
from .models import User


class AccountTestCase(TestCase):    
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            password='test1234',
            email='email@email.com',
            first_name='test',
            last_name='test',            
            middle_name='test',
            phone='+79084657354',
        )
        self.user.save()
    
    def tearDown(self):
        self.user.delete()
        
    """
    Test create user
    """
    def test_user_created(self):
        users = User.objects.all()        
        self.assertEqual(users.count(), 1)


    """
    Test auth with email
    """
    def test_jwt_login_get_token(self):
        url = reverse('token')
        user_data = {
            'email': 'email@email.com',
            'password': 'test1234',
        }
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue('access' in json.loads(response.content))
    
    """
    Test token refresh
    """
    def test_jwt_login_token_refresh(self):
        url = reverse('token')
        r_url = reverse('token_refresh')
        user_data = {
            'email': 'email@email.com',
            'password': 'test1234',
        }
        # Get token, refresh
        response = self.client.post(url, user_data, format='json')
        data = json.loads(response.content)
        refresh = {
            'refresh': data['refresh']
            }
        response = self.client.post(r_url, refresh, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue('access' in json.loads(response.content))

