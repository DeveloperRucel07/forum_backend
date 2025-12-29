from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from forum_app.api.serializers import AnswerSerializer
from forum_app.models import Answer, Question


class AnswerTest(APITestCase):
    
    def setUp(self):
        self.user, _ = User.objects.get_or_create(username='bob', password='asdasd')
        self.question = Question.objects.create(title ='Test Question', content = 'this is a test content', author = self.user, category = 'frontend')
        self.answer = Answer.objects.create(content='You can use React.memo to optimize your component.', author=self.user, question=self.question)
        self.token = Token.objects.create(user = self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        
    def test_get_all_answers(self):
        url = reverse('answer-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_post_answer(self):
        url = reverse('answer-list-create')
        data = {
                'content':'Content1',
                'author':self.user.id,
                'question': self.question.id
            }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def test_detail_answer(self):
        url = reverse('answer-detail', kwargs={'pk': self.answer.id})
        response = self.client.get(url)
        expected_data = AnswerSerializer(self.answer).data
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
        self.assertDictEqual(response.data, expected_data)
        self.assertJSONEqual(response.content, expected_data)
        
    def test_delete_answer(self):
        url = reverse('answer-detail', kwargs={'pk': self.answer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT) 