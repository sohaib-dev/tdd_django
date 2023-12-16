from django.test import TestCase
from .models import Entry


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
