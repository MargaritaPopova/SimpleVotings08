from django.test import TestCase
from django.test import Client

class TestView(TestCase):
  
    def setUp(self):
      self.client = Client()
      self.user = User.objects.create_user(username='testuser', password='12345678qwerty')
      self.response = self.client.get('/')
      
    def test_menu(self):
      self.assertContains(self.response, 'Login')
    
