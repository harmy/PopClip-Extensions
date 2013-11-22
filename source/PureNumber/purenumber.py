#coding=utf-8
import os

CHINESE_NUMBERS = ['ling', 'yi', 'er', 'san', 'si', 'wu', 'liu', 'qi', 'ba', 'jiu']

selected_text = os.environ.get('POPCLIP_TEXT', '幺两三四五六拐八狗洞')

selected_text = unicode(selected_text, 'utf-8')

pinyin_data = {}
with open('pinyin.dat') as f:
    for line in f:
        key, value = line.strip().split(' ', 1)
        value = value.split(' ', 1)[0][:-1]
        if value in CHINESE_NUMBERS:
            pinyin_data[unicode(key, 'utf-8')] = str(CHINESE_NUMBERS.index(value))

translated_text = [pinyin_data.get(char, char) for char in selected_text]

print ''.join([char for char in translated_text if char.isdigit()])