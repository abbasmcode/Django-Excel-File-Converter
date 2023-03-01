from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import ExcelFile, ConvertedFile
from .forms import ExcelFileForm
import os

def upload_file(request):
    if request.method == 'POST':
        form = ExcelFileForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = form.save()
            return redirect('converter:download_file', pk=excel_file.convertedfile.pk)
    else:
        form = ExcelFileForm()
    return render(request, 'converter/upload_file.html', {'form': form})

def download_file(request, pk):
    converted_file = get_object_or_404(ConvertedFile, pk=pk)
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={os.path.basename(converted_file.zip_file.name)}'
    response['Content-Length'] = converted_file.zip_file.size
    response.write(converted_file.zip_file.read())
    return response
