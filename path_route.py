# -*- coding: utf-8 -*-
import libs.chartfirst_client as c1_client
from libs.util_lib import retry_request
from flask import render_template, jsonify, make_response
from flask import request
import simplejson
import urllib2
import pprint
import traceback

DEFAULT_LOCATIONS_YANDEX_RTEXT = {
    'Афимолл':"55.748070%2C37.536850",
    "Sheremetievo":"55.962870%2C37.405975"
}
IS_DEBUG = True

def get_rtext_from_geocoder(location):
    #https://geocode-maps.yandex.ru/1.x/?format=json&geocode=Домодедово
    print location
    response = retry_request(
        "GET", "https://geocode-maps.yandex.ru/1.x/?format=json&geocode=" \
               +urllib2.quote(location+", Москва"))
    res_json = simplejson.loads(response.text)
    try:
        coords_line =  res_json["response"]['GeoObjectCollection']['featureMember'][0]['GeoObject']["Point"]["pos"]
        rtext = "%2C".join(coords_line.split(" ")[::-1])
    except:
        rtext = None
    return rtext




def make_yandex_url(params):
    # fromloc_rtext = DEFAULT_LOCATIONS_YANDEX_RTEXT.get(
    #     params.get("fromloc"),None)
    # toloc_rtext = DEFAULT_LOCATIONS_YANDEX_RTEXT.get(
    #     params.get("toloc"), "55.748070%2C37.536850")
    fromloc_rtext = get_rtext_from_geocoder(params.get("fromloc", 'Отель Novotel Москва Сити'))
    toloc_rtext = get_rtext_from_geocoder(params.get("toloc", "Аэропорт Шереметьево"))
    if fromloc_rtext is None or toloc_rtext is None:
        return "Неудалось построить маршрут"
    return "https://yandex.ru/maps/?rtext=" \
           +fromloc_rtext+"~"+toloc_rtext+"&rtt=mt"

def path_route():
    params = request.args
    response = c1_client.ActionResponse()
    if IS_DEBUG:
        response.messages.append("==debug==")
        response.messages.append("Params: "+str(params))
        response.messages.append("==response==")
    """
    try:
        response.messages.append(make_yandex_url(params))
    except:
        if IS_DEBUG:
            response.messages.append(tb = traceback.format_exc())
        else:
            response.messages.append("Что-т о пошдо не так")
    """
    return make_response(jsonify(response.to_dict()), 200)
