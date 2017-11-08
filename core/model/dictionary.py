#!/usr/bin/python
# -- coding: utf-8 --


# Converts an accented vocabulary to dictionary, for example
#
# абстракцион+истов
# абстр+акцию
# абстр+акция
# 
# абстракционистов a0 b s t r a0 k c i0 o0 nj i1 s t o0 v
# абстракцию a0 b s t r a1 k c i0 j u0
# абстракция a0 b s t r a1 k c i0 j a0
#
 
import sys

softletters=set(u"")
startsyl=set(u"")
others = set(["#", "+", "-"])


softhard_cons = {                                                                
    u"б" : u"b",
    u"в" : u"v",
    u"г" : u"g",
    u"д" : u"d",
    u"з" : u"z",
    u"ј" : u"j",
    u"к" : u"k",
    u"л" : u"l",
    u"м" : u"m",
    u"н" : u"n",
    u"п" : u"p",
    u"р" : u"r",
    u"с" : u"s",
    u"т" : u"t",
    u"ф" : u"f",
    u"х" : u"h"
}

other_cons = {
    u"ж" : u"zh",
    u"ц" : u"c",
    u"ч" : u"ch",
    u"ѕ" : u"d z",
    u"ш" : u"sh",
    u"ќ" : u"kj",
    u"ѓ" : u"gj",
    u"љ" : u"lj",
    u"њ" : u"nj",
    u"џ" : u"dj"
}
                                
vowels = {
    u"а" : u"a",
    u"у" : u"u",
    u"о" : u"o",
    u"е" : u"e",
    u"и" : u"i",
}                                

# adds 0 after softheard_cons and other_cons letters
def pallatize(phones):
    for i, phone in enumerate(phones[:-1]):
    	if phone[0] in softhard_cons: 
    	   phones[i] = (softhard_cons[phone[0]], 0)
    	if phone[0] in other_cons:
    	    phones[i] = (other_cons[phone[0]], 0)


# adds 0 after vowels
def convert_vowels(phones):
    new_phones = []
    for phone in phones:
        if phone[0] in vowels:
            new_phones.append(vowels[phone[0]] + str(phone[1]))
        else:
            new_phones.append(phone[0])
    return new_phones


def add_accent(phones):
    counter = 0
    for phone in phones:
        if phone[0] in vowels:
            counter += 1
    # word has 1 vowel
    if counter == 1:
        for phone in phones:
            if phone[0] in vowels:
                phone[1] = 1
    # word has 2 vowels
    elif counter == 2:
        vowel_count = 0;
        for phone in reversed(phones):
            if phone[0] in vowels:
                vowel_count += 1
                if vowel_count == 2:
                    phone[1] = 1
    # word has 3 or more vowels
    elif (counter >= 3):
        # add accent on the second vowel if the word ends with јќи
        letters = []
        for phone in phones:
            letters.append(phone[0])
        first = letters[-4]
        second = letters[-3]
        if (first == 'j' and second == 'kj'):
            vowel_count = 0
            for phone in reversed(phones):
                if phone[0] in vowels:
                    vowel_count += 1
                    if vowel_count == 2:
                        phone[1] = 1
        # add accent on the third vowel 
        else:
            vowel_count = 0    
            for phone in reversed(phones):
                if phone[0] in vowels:
                    vowel_count += 1
                    if vowel_count == 3:
                        phone[1] = 1



def convert(stressword):
    phones = ("#" + stressword + "#").decode('utf-8')

    # Assign stress marks
    stress_phones = []
    stress = 0
    for phone in phones:
        stress_phones.append([phone, stress])
        stress = 0


    # Pallatize
    pallatize(stress_phones)

    # Add accent
    add_accent(stress_phones)

    # Assign stress
    phones = convert_vowels(stress_phones)

    # Filter
    phones = [x for x in phones if x not in others]

    return " ".join(phones).encode("utf-8")

for line in open(sys.argv[1]):
    stressword = line.strip()
    print stressword.replace("+", ""), convert(stressword)