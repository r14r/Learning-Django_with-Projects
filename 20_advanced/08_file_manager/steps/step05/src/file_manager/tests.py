import io
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Folder, UploadedFile


class FileManagerTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user   = User.objects.create_user('alice', password='pass')

    def test_list_requires_login(self):
        resp = self.client.get(reverse('file_manager:list'))
        self.assertNotEqual(resp.status_code, 200)

    def test_list_view(self):
        self.client.login(username='alice', password='pass')
        resp = self.client.get(reverse('file_manager:list'))
        self.assertEqual(resp.status_code, 200)

    def test_upload_file(self):
        self.client.login(username='alice', password='pass')
        f = SimpleUploadedFile('test.txt', b'hello world', content_type='text/plain')
        self.client.post(reverse('file_manager:upload'), {'files': [f]})
        self.assertEqual(UploadedFile.objects.count(), 1)
        self.assertEqual(UploadedFile.objects.first().owner, self.user)

    def test_create_folder(self):
        self.client.login(username='alice', password='pass')
        self.client.post(reverse('file_manager:folder-create'), {'name': 'Docs'})
        self.assertEqual(Folder.objects.count(), 1)

    def test_download_own_file(self):
        self.client.login(username='alice', password='pass')
        f = SimpleUploadedFile('dl.txt', b'content', content_type='text/plain')
        self.client.post(reverse('file_manager:upload'), {'files': [f]})
        uf   = UploadedFile.objects.first()
        resp = self.client.get(reverse('file_manager:download', kwargs={'pk': uf.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_cannot_download_others_file(self):
        other = User.objects.create_user('bob', password='pass')
        f     = SimpleUploadedFile('other.txt', b'secret', content_type='text/plain')
        uf    = UploadedFile.objects.create(
            owner=other, original_name='other.txt', file=f, size=6,
        )
        self.client.login(username='alice', password='pass')
        resp = self.client.get(reverse('file_manager:download', kwargs={'pk': uf.pk}))
        self.assertEqual(resp.status_code, 404)
