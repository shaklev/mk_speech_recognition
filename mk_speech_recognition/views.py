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
        # audio_blob = request.FILES['audio'].read(1024)
        # audio_blob = request.FILES['audio']
        current_dir = os.path.dirname(os.path.realpath(__file__))

        # SpeechDetector object
        decoder = SpeechDetector();

        sentence = decoder.run(os.path.join(current_dir, 'test.wav'))
        print 'The input sentence is:'
        decoded_sentence = (' ').join(sentence)
        print(decoded_sentence)
       
        wiki = WikiApi({'locale':'mk'})
        decoded_sentence = 'decoded_sentence'
        print 'Searching for results'
        results = wiki.find(decoded_sentence)
        print 'Done searching'
        if results:
            response = wiki.get_article(results[0]).summary
            print 'The search returned the following article:'
            print response
        else:
            print 'No results were found for the sentence %s' %decoded_sentence
        data = {'status':200}
        return JsonResponse(data)