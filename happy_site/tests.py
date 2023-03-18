"""ТЕСТИ ДЛЯ HAPPY SITE"""

from django.utils import timezone
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy

from happy_site.models import BDays
from happy_site.forms import AddBDayForm


class RegisterUserTestCase(TestCase):
    def setUp(self):
        """
        The setUp function is run before each test. It creates a new user and logs them in.

        :param self: Represent the instance of the object that is being created
        :return: The user data
        """
        self.url = reverse('register')
        self.user_data = {
            'username': 'test_user',
            'email': 'test_user@example.com',
            'password1': 'test_password',
            'password2': 'test_password',
        }

    def test_register_user_success(self):
        """
        The test_register_user_success function tests the following:
            1. The response status code is 302 (redirect to success url)
            2. A new user was created with the username specified in self.user_data

        :param self: Access the instance of the class
        :return: A status code of 302, which is a redirect
        """
        response = self.client.post(self.url, data=self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect to success url
        self.assertTrue(User.objects.filter(username=self.user_data['username']).exists())

    def test_register_user_failure(self):
        """
        The test_register_user_failure function tests the register view with a POST request.
        It checks that the user is not created and that it returns to the register page.

        :param self: Access the attributes and methods of the class in python
        :return: A status code of 200
        """
        self.user_data['password2'] = 'wrong_password'
        response = self.client.post(self.url, data=self.user_data)
        self.assertEqual(response.status_code, 200)  # Return to register page
        self.assertFalse(User.objects.filter(username=self.user_data['username']).exists())

    def test_register_user_page(self):
        """
        The test_register_user_page function tests the register_user view.
        It checks that the page loads successfully and that it contains a form.

        :param self: Access the attributes and methods of the class in python
        :return: A 200 status code and a form tag
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)  # Page loads successfully
        self.assertContains(response, '<form')  # Form is present on the page


class LoginUserTestCase(TestCase):

    def setUp(self):
        """
        The setUp function is a special function that gets run before each test.
        It's useful for setting up common state. Here, we're creating a new Django
        test client and using it to log in our test user.

        :param self: Access the attributes and methods of a class in python
        :return: A test client, a user and a login url
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        self.login_url = reverse_lazy('login')

    def test_login_page_loads(self):
        """
        The test_login_page_loads function tests that the login page loads.
        It does this by making a GET request to the login URL, and then asserting that the response status code is 200 (OK) and that we used the correct template.

        :param self: Access the class attributes and methods
        :return: A response object
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'happy_site/login.html')

    def test_user_can_login(self):
        """
        The test_user_can_login function tests that a user can login to the site.
        It does this by creating a new user, logging them in, and checking that they are redirected to the home page.

        :param self: Access the attributes and methods of the class in python
        :return: A redirect to the home page
        """
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertRedirects(response, reverse_lazy('home'))

    def test_login_context_data(self):
        """
        The test_login_context_data function tests that the login page returns a response with
        the correct context data. The test_login_context_data function is a method of the LoginRequiredTestCase class,
        which inherits from django.test.TestCase.

        :param self: Represent the instance of the class
        :return: The title of the page
        """
        response = self.client.get(self.login_url)
        self.assertIn('title', response.context)
        self.assertEqual(response.context['title'], 'Авторизація')


class AddBDayTestCase(TestCase):
    def setUp(self):
        """
        The setUp function is run before each test in the class.
        It creates a new user and a new BDay post, which will be used for testing.

        :param self: Make the function a method of the class
        :return: A test client, which is a python class that acts as a dummy web browser, allowing you to test your views and interact with your django-powered application programmatically
        """
        self.url = reverse('add_bday')
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.data = {
            'title': 'Test BDay',
            'content': 'This is a test BDay post.',
            'date': timezone.now().date(),
        }

    def test_add_bday_view(self):
        """
        The test_add_bday_view function tests the add_bday view.
        It checks that a user can create a new BDay post with valid data, and that they are redirected to the correct page.

        :param self: Access the attributes and methods of the class in python
        :return: A 302 status code and redirects to the b_days view
        """
        self.client.login(username='test_user', password='12345')
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('b_days'))

        bday = BDays.objects.get(title='Test BDay')
        self.assertEqual(bday.content, 'This is a test BDay post.')
        self.assertEqual(bday.user, self.user)

    def test_add_bday_form(self):
        """
        The test_add_bday_form function tests the AddBDayForm class.
        It creates a form with data from self.data, which is defined in setUp().
        The test checks that the form is valid and then saves it to bday without committing it to the database yet.
        Then, we assign bday's user attribute to self.user (the user created in setUp()). Finally, we save bday again and check that its title, content and user attributes are equal to what they should be.

        :param self: Refer to the instance of the class
        :return: The form
        """
        form = AddBDayForm(data=self.data)
        self.assertTrue(form.is_valid())

        bday = form.save(commit=False)
        bday.user = self.user
        bday.save()

        self.assertEqual(bday.title, 'Test BDay')
        self.assertEqual(bday.content, 'This is a test BDay post.')
        self.assertEqual(bday.user, self.user)
