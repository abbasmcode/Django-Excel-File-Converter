from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
import os
import zipfile
import csv
import json
import pandas as pd

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files')

    def __str__(self):
        return os.path.basename(self.file.name)

class ConvertedFile(models.Model):
    excel_file = models.OneToOneField(ExcelFile, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='converted_files', null=True, blank=True)
    json_file = models.FileField(upload_to='converted_files', null=True, blank=True)
    zip_file = models.FileField(upload_to='converted_files', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Converted files for {os.path.basename(self.excel_file.file.name)}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.convert_files()

    def convert_files(self):
        # Convert Excel to CSV
        csv_file = f'{os.path.splitext(self.excel_file.file.name)[0]}.csv'
        data_xls = pd.read_excel(self.excel_file.file.name, index_col=None)
        data_xls.to_csv(csv_file, encoding='utf-8', index=False)
        self.csv_file.name = csv_file
        self.csv_file.save(csv_file, files.File(open(csv_file, 'rb')))

        # Convert Excel to JSON
        json_file = f'{os.path.splitext(self.excel_file.file.name)[0]}.json'
        data_xls = pd.read_excel(self.excel_file.file.name, index_col=None)
        data_json = json.loads(data_xls.to_json(orient='records'))
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data_json, f, ensure_ascii=False, indent=4)
        self.json_file.name = json_file
        self.json_file.save(json_file, files.File(open(json_file, 'rb')))

        # Create ZIP file of all converted files
        zip_file = f'{os.path.splitext(self.excel_file.file.name)[0]}.zip'
        with zipfile.ZipFile(zip_file, 'w') as f:
            f.write(self.csv_file.path, os.path.basename(self.csv_file.name))
            f.write(self.json_file.path, os.path.basename(self.json_file.name))
        self.zip_file.name = zip_file
        self.zip_file.save(zip_file, files.File(open(zip_file, 'rb')))

    def get_absolute_url(self):
        return reverse('converter:download_file', args=[str(self.pk)])
