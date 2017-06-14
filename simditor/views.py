"""simditor views."""
from __future__ import absolute_import

import os
from datetime import datetime

from django.conf import settings
from django.core.files.storage import default_storage

from django.http import JsonResponse

from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from . import utils, image_processing


def get_upload_filename(upload_name, user):
    """If SIMDITOR_RESTRICT_BY_USER is True upload file to user specific path."""
    if getattr(settings, 'SIMDITOR_RESTRICT_BY_USER', False):
        user_path = user.get_username()
    else:
        user_path = ''

    # Generate date based path to put uploaded file.
    date_path = datetime.now().strftime('%Y/%m/%d')

    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(
        settings.SIMDITOR_UPLOAD_PATH, user_path, date_path)

    if getattr(settings, 'SIMDITOR_UPLOAD_SLUGIFY_FILENAME', True):
        upload_name = utils.slugify_filename(upload_name)

    return default_storage.get_available_name(os.path.join(upload_path, upload_name))


class ImageUploadView(generic.View):
    """ImageUploadView."""

    http_method_names = ['post']

    @staticmethod
    def _save_file(request, uploaded_file):
        filename = get_upload_filename(uploaded_file.name, request.user)
        saved_path = default_storage.save(filename, uploaded_file)
        return saved_path

    def post(self, request, **kwargs):
        """Post."""
        uploaded_file = request.FILES['upload']

        backend = image_processing.get_backend()

        if not getattr(settings, 'SIMDITOR_ALLOW_NONIMAGE_FILES', True):
            try:
                backend.image_verify(uploaded_file)
            except utils.NotAnImageException:
                retdata = {'file_path': '', 'success': False,
                           'msg': '图片格式错误!'}
                return JsonResponse(retdata)

        saved_path = self._save_file(request, uploaded_file)
        url = utils.get_media_url(saved_path)

        retdata = {'file_path': url, 'success': True,
                   'msg': '上传成功!'}
        return JsonResponse(retdata)


UPLOAD = csrf_exempt(ImageUploadView.as_view())
