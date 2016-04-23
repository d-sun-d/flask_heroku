# -*- coding: utf-8 -*-
import requests
import time
import json

YANDEX_API_KEY="trnsl.1.1.20160423T081552Z.391c7bf6d2b74e3b.d83e1c1fa045228689a2328a5214cff12b66e73f"

YANDEX_API_ERROR_CODES={
    401:"Неправильный API-ключ",
    402:"API-ключ заблокирован",
    404:"Превышено суточное ограничение на объем переведенного текста",
    413:"Превышен максимально допустимый размер текста",
    422:"Текст не может быть переведен",
    501:"Заданное направление перевода не поддерживается"}

def retry_request(
        method="POST",
        url="https://translate.yandex.net/api/v1.5/tr.json/translate",
        data={},
        headers="",
        retry_count=0,
        retry_timeout=0.1,
        skip_codes_dict=YANDEX_API_ERROR_CODES,
        debug=True):
    if debug:
        print "start: "+method+" "+url.encode("utf-8")
    if method == "POST":
        response = requests.post(url,
                             headers=headers,
                             data=data,
                             timeout=120,
                             verify=False)
    elif method == "GET":
        response = requests.get(url,
                             headers=headers,
                             timeout=120,)
                             #verify=False)
    elif method == "DELETE":
        response = requests.delete(url,
                             headers=headers,
                             timeout=120,
                             verify=False)
    elif method == "PUT":
        response = requests.put(url,
                             headers=headers,
                             data=data,
                             timeout=120,
                             verify=False)
    if debug:
        print("Result: "+str(response))
    #print("Result_body: "+response.text)
    if response.status_code in skip_codes_dict:
        raise RuntimeError(skip_codes_dict[response.status_code])
    elif response.status_code != 200:
        print response.text
        if retry_count == 0:
            raise RuntimeError("Failed upload to stat uri="+
                               url+"\n\tresponse_headers="+str(response.headers))
        else:
            time.sleep(retry_timeout)
            response = retry_request(method, url, headers, data, retry_count - 1)
    return response


def translate_by_yandex(text, lang="en-ru"):
    #https://tech.yandex.ru/translate/doc/dg/reference/translate-docpage/#JSON
    response = retry_request(
        "POST",
        "https://translate.yandex.net/api/v1.5/tr.json/translate?lang="+lang+"&key="+YANDEX_API_KEY,
        data={"text":text}
    )
    text = json.loads(response.text)
    return text["text"]


if __name__ == "__main__":
    print translate_by_yandex("Clean up my room!")

