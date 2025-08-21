from django import forms
from .models import TextDocument

class TextDocumentForm(forms.ModelForm):
    job_description = forms.CharField(
        widget=forms.Textarea(attrs={
            "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:outline-none",
            "placeholder": "Paste the job description here..."
        })
    )

    class Meta:
        model = TextDocument
        fields = ('file', 'job_description')

    def clean_file(self):
        f = self.cleaned_data['file']

        # 1. Size limit (e.g., 5 MB)
        if f.size > 5 * 1024 * 1024:  # 5 MB
            raise forms.ValidationError('File too large (max 5 MB).')

        # 2. Optional: double-check allowed extensions
        valid_extensions = [
            'txt', 'pdf', 'doc', 'docx', 'rtf',
            'odt', 'tex', 'wps', 'ppt', 'pptx',
            'xls', 'xlsx'
        ]
        ext = f.name.split('.')[-1].lower()
        if ext not in valid_extensions:
            raise forms.ValidationError(f'Unsupported file type: .{ext}')

        return f
