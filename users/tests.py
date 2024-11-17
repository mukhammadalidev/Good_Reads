from django.contrib.auth import get_user
from users.models import CustomUser
from django.test import TestCase
# Create your tests here.
from django.urls import reverse


class RegistrationTest(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse('users:register'),
            data = {
                'username':'jakhongir',
                'first_name':'Jakhongir',
                'last_name':'Rakhmonov',
                'email':'jakhongir@gmail.com',
                'password':'somepassword'
            }
        )

        user = CustomUser.objects.get(username='jakhongir')

        self.assertEqual(user.first_name,'Jakhongir')
        self.assertEqual(user.last_name,'Rakhmonov')
        self.assertEqual(user.email,'jakhongir@gmail.com')
        self.assertNotEqual(user.password,'somepassword')
        self.assertTrue(user.check_password('somepassword'))

    def test_required_field(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'email':'qul@mail.ru',
                'first_name':'Mukhammad'
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count,0)
        self.assertFormError(response,'form','username','This field is required.')
        self.assertFormError(response,'form','password','This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'jakhongir',
                'first_name': 'Jakhongir',
                'last_name': 'Rakhmonov',
                'email': 'invalid-email',
                'password': 'somepassword'
            }

        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count,0)
        self.assertFormError(response,'form','email','Enter a valid email address.')

    def test_unique_username(self):

        user = CustomUser.objects.create(username='mukhammadali',first_name='Jakhongir')
        user.set_password('somepassword')
        user.save()

        response = self.client.post(
            reverse('users:register'),
            data={
                'username': 'mukhammadali',
                'first_name': 'Jakhongir',
                'last_name': 'Rakhmonov',
                'email': 'invalid-email@gmail.com',
                'password': 'somepassword'
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count,1)
        self.assertFormError(response,'form','username','A user with that username already exists.')


class LoginTestCase(TestCase):
    def test_user_success(self):
        db_user = CustomUser.objects.create(username='mukhammadali', first_name='Jakhongir')
        db_user.set_password('somepassword')
        db_user.save()

        self.client.post(
            reverse('users:login'),
            data={
                "username":"mukhammadali",
                "password":"somepassword"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_username_and_password_wrong(self):
        db_user = CustomUser.objects.create(username='mukhammadali', first_name='Jakhongir')
        db_user.set_password('somepassword')
        db_user.save()

        self.client.post(
            reverse('users:login'),
            data={
                "username":"ajdar",
                "password":"somepassword"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse('users:login'),
            data={
                "username":"mukhammadali",
                "password":'1234'
            }
        )

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)

    def test_logout_user(self):
        user = CustomUser.objects.create(username='mukhammadali',first_name='Jakhongir')
        user.set_password('somepassword')
        user.save()

        self.client.login(username="mukhammadali",password="somepassword")

        self.client.get(reverse('users:logout'))

        user_date = get_user(self.client)

        self.assertFalse(user_date.is_authenticated)



class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login")+'?next=/users/profile/')

    def test_profile_details(self):
        user = CustomUser.objects.create(
            username="jakhongir", first_name="Jakhongir", last_name="Rakhmonov", email="jrahmonov2@gmail.com"
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username="jakhongir", password="somepass")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user_db = CustomUser.objects.create(username="killer",first_name="Muhammadali",last_name="Shamsidinov",email="muxa@gmail.com")
        user_db.set_password("somepassword")
        user_db.save()

        self.client.login(username="killer",password="somepassword")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username":"killer",
                "first_name":"Ali",
                "last_name":"Shamsidinov",
                "email":"muxa@gmail.com"
            }
        )

        user = CustomUser.objects.get(pk=user_db.pk)

        self.assertEqual(user.first_name,"Ali")
        self.assertEqual(response.url,reverse("users:profile"))


