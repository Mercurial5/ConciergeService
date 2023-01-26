from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from documents import models


@api_view()
def download(request: Request, doctype: str, *args):
    if doctype == 'docs':
        try:
            file = models.Document.objects.get(document=request.get_full_path()[1:])
        except models.Document.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    file_handle = file.document.open()
    response = FileResponse(file_handle)
    response['Content-Length'] = file.document.size
    response['Content-Disposition'] = f'attachment; filename="{file.document.name}"'

    return response
