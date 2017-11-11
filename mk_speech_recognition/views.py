#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from wikiapi import WikiApi

from core.speech_decoder import SpeechDetector
import os

@method_decorator(csrf_exempt, name='dispatch')
class MainView(View):

    def get(self, request):
        return render_to_response('main.html')
    
    def post(self, request):
        # current_dir = os.path.dirname(os.path.realpath(__file__))
        # audio_blob = os.path.join(current_dir, "test.wav")
        # print(current_dir)
        #import numpy as np
		# import scipy.io.wavfile
		# import math
        # file_name="another.wav"
		# rate=8000
		# data2 = np.asarray(request.data, dtype=np.int16)
        # scipy.io.wavfile.write(file_name,rate,data2)
        audio_blob = request.FILES['audio']
        decoder = SpeechDetector();
        decoder.run(audio_blob)
        wiki = WikiApi({'locale':'mk'})
        results = wiki.find('Гоце Делчев')
        response = wiki.get_article(results[0]).summary
        data = {'status':200}
        return JsonResponse(data)