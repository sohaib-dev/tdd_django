from django.test import TestCase
from django_webtest import WebTest
from .models import Entry, Comment
from django.contrib.auth import get_user_model

from .forms import CommentForm


# Create your tests here.
class EntryModelTest(TestCase):

    def test_string_representation(self):
        entry = Entry(title='My First Post')
        self.assertEquals(str(entry), entry.title)

    def test_verbose_name_plural(self):
        self.assertEquals(str(Entry._meta.verbose_name_plural), 'Entries')

    def test_get_absolute_url(self):
        user = get_user_model().objects.create(username='test_user')
        entry = Entry.objects.create(title="My entry title", author=user)
        self.assertIsNotNone(entry.get_absolute_url())


class ProjectTest(TestCase):

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)


class HomePageTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')

    def test_one_entry(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')

    def test_two_entires(self):
        Entry.objects.create(title='1-title', body='1-body', author=self.user)
        Entry.objects.create(title='2-title', body='2-body', author=self.user)
        response = self.client.get('/')
        self.assertContains(response, '1-title')
        self.assertContains(response, '2-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, '2-body')

    def test_no_entries(self):
        response = self.client.get('/')
        self.assertContains(response, 'No blog entries yet.')


class EntryViewTest(WebTest):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.entry = Entry.objects.create(title='1-title', body='1-body', author=self.user)

    def test_basic_view(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertEquals(response.status_code, 200)

    def test_title_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.title)

    def test_body_in_entry(self):
        response = self.client.get(self.entry.get_absolute_url())
        self.assertContains(response, self.entry.body)

    def test_view_page(self):
        page = self.app.get(self.entry.get_absolute_url())
        # self.assertEquals(len(page), 1)

    # def test_form_error(self):
    #     page = self.app.get(self.entry.get_absolute_url())
    #     page = page.form.submit()
    #     self.assertContains(page, 'This field is required.')

    # def test_form_success(self):
    #     page = self.app.get(self.entry.get_absolute_url())
    #     page.form['name'] = "Phillip"
    #     page.form['email'] = "phillip@example.com"
    #     page.form['body'] = "Test comment body."
    #     page = page.form.submit()
    #     self.assertRedirects(page, self.entry.get_absolute_url())

#########################################
# Comment Tests
#########################################


class CommentModelTest(TestCase):

    def test_str_representation(self):
        comment = Comment(body='First Comment')
        self.assertEquals(str(comment), 'First Comment')


class CommentFormTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.entry = Entry.objects.create(title='1-title', body='1-body', author=self.user)

    def test_init(self):
        CommentForm(entry=self.entry)

    def test_init_without_key(self):
        with self.assertRaises(KeyError):
            CommentForm()

    def test_valid_data(self):
        form = CommentForm({
            'name': 'Turanga Leela',
            'email': 'leela@example.com',
            'body': 'Hi there',
        }, entry=self.entry)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEquals(comment.name, 'Turanga Leela')
        self.assertEquals(comment.email, 'leela@example.com')
        self.assertEquals(comment.body, 'Hi there')
        self.assertEquals(comment.entry, self.entry)

    def test_blank_data(self):
        form = CommentForm({}, entry=self.entry)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'email': ['This field is required.'],
            'body': ['This field is required.'],
        })
