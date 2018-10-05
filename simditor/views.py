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


def get_upload_filename(upload_name):
    # Generate date based path to put uploaded file.
    date_path = datetime.now().strftime('%Y/%m/%d')

    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(settings.SIMDITOR_UPLOAD_PATH, date_path)

    if getattr(settings, 'SIMDITOR_UPLOAD_SLUGIFY_FILENAME', True):
        upload_name = utils.slugify_filename(upload_name)

    return default_storage.get_available_name(os.path.join(upload_path, upload_name))


def upload_handler(request):
    files = request.FILES

    upload_config = settings.SIMDITOR_CONFIGS.get(
        'upload', {'fileKey': 'upload'})
    filekey = upload_config.get('fileKey', 'upload')

    uploaded_file = files.get(filekey)

    if not uploaded_file:
        retdata = {'file_path': '', 'success': False,
                   'msg': '图片上传失败，无法获取到图片对象!'}
        return JsonResponse(retdata)

    image_size = upload_config.get('image_size')
    if image_size and uploaded_file.size > image_size:
        retdata = {'file_path': '', 'success': False,
                   'msg': '上传失败，已超出图片最大限制!'}
        return JsonResponse(retdata)

    backend = image_processing.get_backend()

    if not getattr(settings, 'SIMDITOR_ALLOW_NONIMAGE_FILES', True):
        try:
            backend.image_verify(uploaded_file)
        except utils.NotAnImageException:
            retdata = {'file_path': '', 'success': False,
                       'msg': '图片格式错误!'}
            return JsonResponse(retdata)

    filename = get_upload_filename(uploaded_file.name)
    saved_path = default_storage.save(filename, uploaded_file)

    url = utils.get_media_url(saved_path)

    is_api = settings.SIMDITOR_CONFIGS.get('is_api', False)
    url = request.META.get('HTTP_ORIGIN') + url if is_api else url

    retdata = {'file_path': url, 'success': True, 'msg': '上传成功!'}

    return JsonResponse(retdata)


class ImageUploadView(generic.View):
    """ImageUploadView."""

    http_method_names = ['post']

    def post(self, request, **kwargs):
        """Post."""
        return upload_handler(request)


UPLOAD = csrf_exempt(ImageUploadView.as_view())
