from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

@method_decorator(csrf_exempt, name='dispatch')
class MainView(View):

    def get(self, request):
        return render_to_response('main.html')
    
    def post(self, request):
        print(request.FILES['audio'].read(1024))
        data = {'status':200}
        return JsonResponse(data)