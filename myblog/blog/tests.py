from django.test import TestCase
from .models import Entry
from django.contrib.auth import get_user_model


# Create your tests here.
class EntryModelTest(TestCase):

    def test_string_representation(self):
        entry = Entry(title='My First Post')
        self.assertEquals(str(entry), entry.title)

    def test_verbose_name_plural(self):
        self.assertEquals(str(Entry._meta.verbose_name_plural), 'Entries')


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
