# -*- coding: utf-8 -*-
import string
import re

with open('lm_sentences.txt') as oldfile, open('mk_subs_clean.txt', 'w') as newfile:
    for line in oldfile:
		line = re.sub(r'\d+', '', line)
		line = re.sub('[abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ]', '', line)
		if re.search('[абвгдѓежзѕијклљмнњопрстќуфxцчџшАБВГДЃЕЖЗЅИЈКЛЉМНЊОПРСТЌУФХЦЧЏШ]', line):
			line = line.replace("<s>","")
			line = line.replace("</s>","")
			line = line.replace("<>","")
			line = line.replace("</>","")
			newfile.write(line)
