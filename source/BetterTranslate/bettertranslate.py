#coding=utf-8
import os
import re
import time
import urllib, urllib2
from tempfile import NamedTemporaryFile
from translate import Translator

def google_tts(text):
	#process text into chunks
    text = text.replace('\n','')
    text_list = re.split('(\,|\.)', text)
    combined_text = []
    for idx, val in enumerate(text_list):
        if idx % 2 == 0:
            combined_text.append(val)
        else:
            joined_text = ''.join((combined_text.pop(),val))
            if len(joined_text) < 100:
                combined_text.append(joined_text)
            else:
                subparts = re.split('( )', joined_text)
                temp_string = ""
                temp_array = []
                for part in subparts:
                    temp_string = temp_string + part
                    if len(temp_string) > 80:
                        temp_array.append(temp_string)
                        temp_string = ""
                #append final part
                temp_array.append(temp_string)
                combined_text.extend(temp_array)
    #download chunks and write them to the output file
    f = NamedTemporaryFile(delete=False)
    for idx, val in enumerate(combined_text):
        mp3url = "http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % ('en', urllib.quote(val), len(combined_text), idx)
        headers = {"Host":"translate.google.com",
          "Referer":"http://www.gstatic.com/translate/sound_player2.swf",
          "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.163 Safari/535.19"}
        req = urllib2.Request(mp3url, '', headers)
        if len(val) > 0:
            try:
                response = urllib2.urlopen(req)
                f.write(response.read())
                time.sleep(.5)
            except urllib2.HTTPError as e:
                print ('%s' % e)
    f.close()
    os.system('afplay {0}'.format(f.name))
    os.unlink(f.name)


selectedText= os.environ['POPCLIP_TEXT']
destLang = os.environ['POPCLIP_OPTION_DESTLANG']
tts = os.environ['POPCLIP_OPTION_TTS']

from translate import Translator
translator= Translator(to_lang=destLang)
translation = translator.translate(selectedText)

if tts == 'system':
	os.system('echo {0} | say'.format(selectedText))
elif tts == 'google':
	google_tts(selectedText)

print translation.encode('utf-8')