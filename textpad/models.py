from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.conf import settings
# from .models import Documents
import uuid

User = get_user_model()

class Documents(models.Model):
    title = models.CharField(max_length=255)  # Document title
    content = RichTextField()   # Main text content of the document
    created_at = models.DateTimeField(auto_now_add=True)  # Date created
    updated_at = models.DateTimeField(auto_now=True)  # Date last updated
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_documents')
    collaborators = models.ManyToManyField(User, related_name='collaborating_documents', blank=True)  # Users with access to edit

    def __str__(self):
        return self.title

class DocumentHistory(models.Model):
    documents = models.ForeignKey(Documents, related_name="history", on_delete=models.CASCADE)
    content = models.TextField()  # Full snapshot or delta
    is_snapshot = models.BooleanField(default=False)  # True if it’s a full snapshot
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Snapshot(models.Model):
    snapshot_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='snapshots')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    version_number = models.IntegerField()

    def _str_(self):
        return f"Snapshot {self.version_number} of Document {self.document.title}"

class Delta(models.Model):
    DELTA_TYPES = [
        ('INSERT', 'Insert'),
        ('DELETE', 'Delete'),
        ('UPDATE', 'Update'),
    ]

    delta_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    document = models.ForeignKey(Documents, on_delete=models.CASCADE, related_name='deltas')
    snapshot = models.ForeignKey(Snapshot, on_delete=models.CASCADE, related_name='deltas')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deltas')
    operation_type = models.CharField(max_length=10, choices=DELTA_TYPES)
    position = models.IntegerField()
    length = models.IntegerField(null=True, blank=True)  # Only for delete operations
    content = models.TextField(null=True, blank=True)  # Only for insert/update operations
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Delta {self.delta_id} on Document {self.document.title}"