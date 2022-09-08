from django.test import TestCase
from authuser.models import User, user_directory_path

# Create your tests here.
class TestCustomUser(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user11',
                                     password='user11', 
                                     first_name='User',
                                     last_name='Min')
        return super().setUpTestData()

    def test_user_directory_path(self):
        file = 'file.jpg'
        user_path = 'avatars/user11/file.jpg'
        user_path_2 = user_directory_path(self.user, file)
        self.assertEqual(user_path, user_path_2)