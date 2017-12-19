#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from core.speech_decoder import SpeechDetector
from audio.models import Audio

from wikiapi import WikiApi
import os
import wave
import pyaudio
import time
import re
import urllib2
import requests
from scrapy.selector import Selector

@method_decorator(csrf_exempt, name='dispatch')
class MainView(View):

    def hasNumbers(self, inputString):
        return any(char.isdigit() for char in inputString)

    def get_mk_dict(self, phrase):
        mk_dict = {}
        meaning = []
        session = requests.Session()
        session.headers.update({'User-Agent': 'Custom user agent'})
        url = 'http://www.makedonski.info/search/'
        data = dict(q=phrase,)
        r = session.post(url, data=data, allow_redirects=True)
        try:
            mk_dict['word_type'] = Selector(text=r.content).xpath('//div[re:test(@class,"grammar")]//text()').extract()[1].encode('utf-8')
        except:
            mk_dict['word_type'] = 'Нема резултати'
        word_definition = Selector(text=r.content).xpath('//div[re:test(@class,"meaning")]//text()').extract()
        if word_definition:
            mk_dict['word_definition'] = word_definition
        else:
            mk_dict['word_definition'] = 'Нема резултати'
        return mk_dict

    def get_wiki_data(self, phrase):
        wiki = WikiApi({'locale':'mk'})
        results = wiki.find(phrase)
        if results:
            wiki_response = wiki.get_article(results[0]).summary
        else:
            wiki_response = 'Нема резултати'
        return wiki_response

    def get(self, request):
        return render_to_response('main.html')
    
    def post(self, request):
        data = {}
        audio = request.FILES['audio']
        audio = Audio(audio_file=audio)
        audio.save()
        # Decode audio
        decoder = SpeechDetector()
        sentence = decoder.run(audio.audio_file.url)
        decoded_sentence = (' ').join(sentence)
        data['decoded_phrase'] = re.sub('<[^<]+?>', '', decoded_sentence).strip(' \n\t\r')
        # Wikipedia search
        data['wiki_response'] = self.get_wiki_data(decoded_sentence)
        # MDR search
        mk_dict = self.get_mk_dict(data['decoded_phrase'])
        data['mk_dict_type'] = mk_dict['word_type']
        data['mk_dict_definition'] = mk_dict['word_definition']
        return JsonResponse(data)