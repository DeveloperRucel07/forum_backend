from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from forum_app.api.serializers import LikeSerializer
from forum_app.models import Like, Question


class LikeTest(APITestCase):
    
    def setUp(self):
        self.user, _ = User.objects.get_or_create(username='dave', password='asdasd')
        self.user_staff, _ = User.objects.get_or_create(username='alice', password='asdasd')
        self.question = Question.objects.create(title ='Test Question', content = 'this is a test content', author = self.user_staff, category = 'frontend')
        self.question2 = Question.objects.create(title ='Test Question', content = 'this is a test content', author = self.user, category = 'frontend')
        self.like = Like.objects.create( user=self.user_staff, question=self.question)
        self.token = Token.objects.create(user = self.user_staff)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        
    def test_get_all_like(self):
        url = reverse('like-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_post_like(self):
        url = reverse('like-list')
        data = {
                'user':self.user_staff.id,
                'question': self.question2.id
            }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def test_detail_like(self):
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.get(url)
        expected_data = LikeSerializer(self.like).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertDictEqual(response.data, expected_data)
        self.assertJSONEqual(response.content, expected_data)
        
    def test_delete_like(self):
        url = reverse('like-detail', kwargs={'pk': self.like.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 