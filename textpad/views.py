from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Documents, Snapshot
from django.contrib.auth import get_user_model
from .models import Documents, Delta, Snapshot


User = get_user_model()

class SaveText(APIView):
    def post(self, request):
        title = request.data.get("title")
        content = request.data.get("content")
        user = request.user

        if title and content:
            document = Documents.objects.create(
                title=title,
                content=content,
                created_by=user
            )
            snapshot = Snapshot.objects.create(
                document=document,
                content=content,
                version_number=1
            )

            return Response({
                "message": "Document created successfully",
                "document_id": document.id,
                "snapshot_id": snapshot.snapshot_id,
                "title": document.title,
                "content": document.content
            }, status=status.HTTP_201_CREATED)
        
        return Response({"error": "Title and content are required"}, status=status.HTTP_400_BAD_REQUEST)

class UpdateText(APIView):
    def post(self, request, document_id):
        content = request.data.get("content")
        position = request.data.get("position", 0)  # Position of change
        operation_type = request.data.get("operation_type")  # INSERT, DELETE, or UPDATE
        length = request.data.get("length", 0)
        user = request.user

        try:
            document = Documents.objects.get(id=document_id)
            latest_snapshot = Snapshot.objects.filter(document=document).order_by('-created_at').first()
            
            delta = Delta.objects.create(
                document=document,
                snapshot=latest_snapshot,
                user=user,
                operation_type=operation_type,
                position=position,
                length=length,
                content=content
            )

            # Update the document’s current content based on the delta operation
            if operation_type == 'INSERT':
                document.content = document.content[:position] + content + document.content[position:]
            elif operation_type == 'DELETE':
                document.content = document.content[:position] + document.content[position + length:]
            elif operation_type == 'UPDATE':
                document.content = document.content[:position] + content + document.content[position + length:]

            document.save()

            return Response({
                "message": "Document updated successfully",
                "document_id": document.id,
                "new_content": document.content
            }, status=status.HTTP_200_OK)

        except Documents.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        
class RevertToVersion(APIView):
    def post(self, request, document_id, version_number):
        try:
            document = Documents.objects.get(id=document_id)
            target_snapshot = Snapshot.objects.get(document=document, version_number=version_number)

            # Set the document's content to the snapshot's content
            document.content = target_snapshot.content
            document.save()

            # Optionally delete later snapshots and deltas after the target version
            Snapshot.objects.filter(document=document, version_number__gt=version_number).delete()
            Delta.objects.filter(document=document, created_at__gt=target_snapshot.created_at).delete()

            return Response({
                "message": "Document reverted successfully",
                "document_id": document.id,
                "reverted_content": document.content,
                "version_number": version_number
            }, status=status.HTTP_200_OK)

        except Documents.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
        except Snapshot.DoesNotExist:
            return Response({"error": "Version not found"}, status=status.HTTP_404_NOT_FOUND)