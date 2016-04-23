# -*- coding: utf-8 -*-
import requests
import time
import simplejson
from util_lib import retry_request


YANDEX_API_KEY="trnsl.1.1.20160423T081552Z.391c7bf6d2b74e3b.d83e1c1fa045228689a2328a5214cff12b66e73f"

YANDEX_API_ERROR_CODES={
    401:"Неправильный API-ключ",
    402:"API-ключ заблокирован",
    404:"Превышено суточное ограничение на объем переведенного текста",
    413:"Превышен максимально допустимый размер текста",
    422:"Текст не может быть переведен",
    501:"Заданное направление перевода не поддерживается"}


def translate(text, lang="en-ru"):
    #https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/#JSON
    response = retry_request(
        "POST",
        "https://translate.yandex.net/api/v1.5/tr.json/translate?lang="+lang+"&key="+YANDEX_API_KEY,
        data={"text":text}
    )
    text = simplejson.loads(response.text)
    return text["text"][0]

def detect_lang(text):
    response = retry_request(
        "POST",
        "https://translate.yandex.net/api/v1.5/tr.json/detect?key="+YANDEX_API_KEY,
        data={"text":text}
    )
    text = simplejson.loads(response.text)
    return text["lang"]

if __name__ == "__main__":
    print translate("Clean up my room!")

