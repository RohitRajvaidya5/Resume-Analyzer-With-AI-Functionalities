import os
import PyPDF2
import docx2txt
from .utils import analyze_resume, analyze_resume_with_fallback
import time
from google.api_core.exceptions import ResourceExhausted

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import TextDocumentForm
from .models import TextDocument
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os



@csrf_exempt
def analyze_resume(request, doc_id):
    if request.method == "POST":
        try:
            doc = TextDocument.objects.get(id=doc_id)

            # Read resume and job description
            resume_text = doc.file.read().decode("utf-8", errors="ignore")
            job_desc = doc.job_description

            # Run your analyzer
            result = analyze_resume_with_fallback(resume_text, job_desc)

            if not result:
                return JsonResponse({"status": "error", "message": "No result from analyzer"})

            # Map backend result → frontend format
            formatted_result = {
                "ats_score": int(result.get("match_score", 0) * 10),  # convert 0–10 → %
                "suggestions": (
                    result.get("improvement_tips", [])
                    + [f"Missing keyword: {kw}" for kw in result.get("missing_keywords", [])]
                )
            }

            return JsonResponse({"status": "success", "result": formatted_result})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})

    return JsonResponse({"status": "error", "message": "Invalid request"})


def home(request):
    return HttpResponse("Hello World")


def upload_text(request):
    if request.method == 'POST':
        form = TextDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save()
            messages.success(request, 'Upload successful.')
            return redirect('detail',pk=doc.pk)
        else:
            messages.error(request, "Something went wrong. Please check your input.")
    else:
        form = TextDocumentForm()

    return render(request, 'analyzer/upload.html', {'form': form})


def detail(request, pk):

    doc = get_object_or_404(TextDocument, pk=pk)
    file_name = os.path.basename(doc.file.name)
    file_path = doc.file.path
    ext = os.path.splitext(file_path)[1].lower()
    content = ""

    try:
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
            content = f"⚠️ Preview not supported for {ext} files."

    except Exception as e:
        content = f"⚠️ Error reading file: {str(e)}"

    return render(request, 'analyzer/detail.html', {
        'doc': doc,
        'content': content,
        'file_name': file_name,  # pass just the file name
    })


def all_files(request):
    files = TextDocument.objects.order_by('-uploaded_at')
    return render(request, 'analyzer/all_files.html', {'files': files})
