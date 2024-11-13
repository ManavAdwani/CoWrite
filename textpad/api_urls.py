from django.urls import path
from .views import *

urlpatterns = [
    path('save-text/', SaveText.as_view(), name='save_text'),  # For creating a new document
    path('update-text/<int:document_id>/', UpdateText.as_view(), name='update_text'),  # For updating a document
    path('revert-text/<int:document_id>/<int:version_number>/', RevertToVersion.as_view(), name='revert_text'),  # For reverting to a specific version
    # path('delete-text/<int:document_id>/', DeleteDocument.as_view(), name='delete_text'),  # For deleting a document
]
