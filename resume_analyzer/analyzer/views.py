from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import TextDocumentForm
from .models import TextDocument
import os, PyPDF2


def home():
    return HttpResponse("Hello World")


def upload_text(request):
    if request.method == 'POST':
        form = TextDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Upload successful.')
            return redirect('all_files')
        else:
            print(form.errors)
            messages.error(request, "Something went wrong. Please check your input.")
    else:
        form = TextDocumentForm()
    return render(request, 'analyzer/upload.html', {'form': form})

def detail(request, pk):
    doc = get_object_or_404(TextDocument, pk=pk)

    file_path = doc.file.path
    ext = os.path.splitext(file_path)[1].lower()

    content = ""

    # TXT files
    if ext == ".txt":
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

    # PDF files
    elif ext == ".pdf":
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text_list = [page.extract_text() or "" for page in reader.pages]
            content = "\n".join(text_list)

    # DOCX files
    elif ext == ".docx":
        content = docx2txt.process(file_path)

    else:
        content = f"Preview not supported for {ext} files."

    return render(request, 'analyzer/detail.html', {'doc': doc, 'content': content})

def all_files(request):
    files = TextDocument.objects.order_by('-uploaded_at')
    return render(request, 'analyzer/all_files.html', {'files': files})
