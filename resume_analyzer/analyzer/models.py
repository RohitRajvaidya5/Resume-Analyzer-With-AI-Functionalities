from django.db import models
from django.core.validators import FileExtensionValidator

def user_directory_path(instance, filename):
    # Save as: resume_files/YYYYMMDD_HHMMSS_originalfilename
    base, ext = os.path.splitext(filename)
    timestamp = now().strftime("%Y%m%d_%H%M%S")
    return f'resume_files/{timestamp}_{base}{ext}'

class TextDocument(models.Model):
    file = models.FileField(
        upload_to='user_directory_path',
        validators=[FileExtensionValidator(allowed_extensions=[
            'txt', 'pdf', 'doc', 'docx', 'rtf', 'odt', 'tex', 'wps',
            'ppt', 'pptx', 'xls', 'xlsx'
        ])]
    )
    job_description = models.TextField(null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} : {self.job_description}"