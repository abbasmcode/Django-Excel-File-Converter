from django.test import TestCase, Client
from django.urls import reverse
from .models import ExcelFile, ConvertedFile

class ConverterTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.excel_file = ExcelFile.objects.create(file='test_files/test_excel.xlsx')

    def test_upload_file(self):
        response = self.client.get(reverse('converter:upload_file'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'converter/upload_file.html')

        with open(self.excel_file.file.path, 'rb') as f:
            response = self.client.post(reverse('converter:upload_file'), {'file': f})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(ConvertedFile.objects.count(), 1)
