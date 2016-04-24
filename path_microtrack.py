# -*- coding: utf-8 -*-

from flask import render_template, jsonify, make_response
from flask import request
import libs.yandex_translate as ytr
import libs.chartfirst_client as c1_client
from libs.redis_cache import CacheService
import pprint


redis_db = {
    "tasks":{},
    "last_id":0
}

def path_microtrack_add():
    cache = CacheService()
    print "start get db"
    redis_db = cache.get_db()
    print "end get db"
    params = {key:rec for key, rec in request.args.items()}
    id = redis_db["last_id"]
    redis_db["last_id"] += 1
    params["original_lang"] = ytr.detect_lang(params["text"])
    params["en_text"] = ytr.translate(params["text"], params["original_lang"]+"-en")
    redis_db["tasks"][id] = params

    response = c1_client.ActionResponse()
    new_task_text = ytr.translate("Персонал оповещен, выполним в ближайшее время.\n\n  Номер вашей заявки ", params["original_lang"])
    response.messages.append(new_task_text+" id:"+str(id))

    print "start save"
    cache.save_db(redis_db)
    print "end save"
    return make_response(jsonify(response.to_dict()), 200)


def path_get_db():
    response = c1_client.ActionResponse()
    response.messages.append(pprint.pformat(redis_db))
    return make_response(jsonify(response.to_dict()), 200)
