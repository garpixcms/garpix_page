from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings


@method_decorator(csrf_exempt, name='dispatch')
class DgjsUpload(View):
    def post(self, request, *args, **kwargs):
        files = request.FILES.getlist('files[]')
        print(files)
        data = []
        fs = FileSystemStorage() #defaults to   MEDIA_ROOT  
        for file in files:
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            data.append(file_url)
        return JsonResponse({ 'data': data })
