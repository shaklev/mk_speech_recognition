from django.http import HttpResponse
from django.views import View
from django.shortcuts import render_to_response

class MainView(View):

    def get(self, request):
        return render_to_response('main.html')