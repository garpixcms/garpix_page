from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage


@method_decorator(csrf_exempt, name='dispatch')
class DgjsUpload(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            files = request.FILES.getlist('files[]')
            data = []
            fs = FileSystemStorage()
            for file in files:
                filename = fs.save(file.name, file)
                file_url = fs.url(filename)
                data.append(request.build_absolute_uri(file_url))
            return JsonResponse({'data': data})
        return JsonResponse({'data': []})
