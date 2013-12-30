#coding=utf-8
import os
import re
import time
import urllib, urllib2
from tempfile import NamedTemporaryFile
from translate import Translator

LANG_CODES = {
        "Afrikaans":"af",
        "Albanian":"sq",
        "Arabic":"ar",
        "Armenian":"hy",
        "Azerbaijani":"az",
        "Basque":"eu",
        "Belarusian":"be",
        "Bengali":"bn",
        "Bosnian":"bs",
        "Bulgarian":"bg",
        "Catalan":"ca",
        "Cebuano":"ceb",
        "Chinese (Simplified)":"zh-CN",
        "Chinese (Traditional)":"zh-TW",
        "Croatian":"hr",
        "Czech":"cs",
        "Danish":"da",
        "Dutch":"nl",
        "English":"en",
        "Esperanto":"eo",
        "Estonian":"et",
        "Filipino":"tl",
        "Finnish":"fi",
        "French":"fr",
        "Galician":"gl",
        "Georgian":"ka",
        "German":"de",
        "Greek":"el",
        "Gujarati":"gu",
        "Haitian Creole":"ht",
        "Hausa":"ha",
        "Hebrew":"iw",
        "Hindi":"hi",
        "Hmong":"hmn",
        "Hungarian":"hu",
        "Icelandic":"is",
        "Igbo":"ig",
        "Indonesian":"id",
        "Irish":"ga",
        "Italian":"it",
        "Japanese":"ja",
        "Javanese":"jw",
        "Kannada":"kn",
        "Khmer":"km",
        "Korean":"ko",
        "Lao":"lo",
        "Latin":"la",
        "Latvian":"lv",
        "Lithuanian":"lt",
        "Macedonian":"mk",
        "Malay":"ms",
        "Maltese":"mt",
        "Maori":"mi",
        "Marathi":"mr",
        "Mongolian":"mn",
        "Nepali":"ne",
        "Norwegian":"no",
        "Persian":"fa",
        "Polish":"pl",
        "Portuguese":"pt",
        "Punjabi":"pa",
        "Romanian":"ro",
        "Russian":"ru",
        "Serbian":"sr",
        "Slovak":"sk",
        "Slovenian":"sl",
        "Somali":"so",
        "Spanish":"es",
        "Swahili":"sw",
        "Swedish":"sv",
        "Tamil":"ta",
        "Telugu":"te",
        "Thai":"th",
        "Turkish":"tr",
        "Ukrainian":"uk",
        "Urdu":"ur",
        "Vietnamese":"vi",
        "Welsh":"cy",
        "Yiddish":"yi",
        "Yoruba":"yo",
        "Zulu":"zu"
        }

def google_tts(text, tl='en'):
    """
    this function is adapted from https://github.com/hungtruong/Google-Translate-TTS, thanks @hungtruong.
    """
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
        mp3url = "http://translate.google.com/translate_tts?tl=%s&q=%s&total=%s&idx=%s" % (tl, urllib.quote(val), len(combined_text), idx)
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
ttsLang = os.environ['POPCLIP_OPTION_TTSLANG']

from translate import Translator
translator= Translator(to_lang=LANG_CODES[destLang])
translation = translator.translate(selectedText)

if ttsLang != 'Disabled':
    google_tts(selectedText, LANG_CODES[ttsLang])

result = translation.encode('utf-8')

print result