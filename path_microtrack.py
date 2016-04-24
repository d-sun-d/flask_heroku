# -*- coding: utf-8 -*-

from flask import render_template, jsonify, make_response
from flask import request
import libs.yandex_translate as ytr
import libs.chartfirst_client as c1_client
from libs.redis_cache import CacheService, REDIS_DB_TEMPLATE
import pprint



def path_microtrack_add():
    cache = CacheService()
    print "start get db"
    redis_db = cache.get_db()
    print "end get db"
    params = {key:rec for key, rec in request.args.items()}
    id = redis_db["last_id"]
    redis_db["last_id"] += 1
    params["state"] = "new"
    params["original_lang"] = ytr.detect_lang(params["text"])
    params["en_text"] = ytr.translate(params["text"], params["original_lang"]+"-en")
    redis_db["tasks"][id] = params

    response = c1_client.ActionResponse()
    new_task_text = ytr.translate("Персонал оповещен, выполним в ближайшее время.\n\n  Номер вашей заявки ", params["original_lang"])
    response.messages.append(new_task_text+" id:"+str(id))

    if params["category"] == "service":
        staff_text = ytr.translate(params["text"], params["original_lang"]+"-tg")
        c1_client.send_push(
            "StaffAccorDemoBot",
            ["N: "+str(id) +"\nRoom:"+str(params.get("room"))+"\n\n"+ staff_text], keybord=[["Done"]])

        reception_text = ytr.translate(params["text"], params["original_lang"]+"-en")
        c1_client.send_push(
            "ReceptionAccorDemoBot",
            ["N: "+str(id) +"\nRoom:"+str(params.get("room"))+"\n\nEN: "+\
             reception_text + "\n\nORIG-LANG: "+params["original_lang"]+"\nORIG: "+\
             params["text"] ])

    if params["category"] == "reception":
        reception_text = ytr.translate(params["text"], params["original_lang"]+"-en")
        c1_client.send_push(
            "ReceptionAccorDemoBot",
            ["N: "+str(id) +"\nRoom:"+str(params.get("room"))+"\n\nEN: "+\
             reception_text + "\n\nORIG-LANG: "+params["original_lang"]+"\nORIG: "+\
             params["text"] ])


    print "start save"
    cache.save_db(redis_db)
    print "end save"
    return make_response(jsonify(response.to_dict()), 200)

def path_microtask_change_state():
    params = {key:rec for key, rec in request.args.items()}
    cache = CacheService()
    redis_db = cache.get_db()
    task_info = redis_db["tasks"].get(params["taskid"])
    response = c1_client.ActionResponse()
    if task_info is None:
        response.messages.append("No microtask with id="+params["taskid"])
    elif params["newstate"] == "done":
        c1_client.send_push(
            "ReceptionAccorDemoBot",
            ["Task "+params["taskid"]+" done"])
        text = u"Ваша заявка id="+params["taskid"]+u" решена.\n\n"+\
                                           u"Если Ваша проблема решена не полностью, отправьте /help"+params["taskid"]
        client_result_text = ytr.translate(text, "ru-"+task_info["original_lang"])
        c1_client.send_push(
            "AccorDemoIntro",
            [client_result_text],
            task_info.get("id", 1298445)
        )
        response.messages.append("Ok")
        task_info["state"] = params["newstate"]
        cache.save_db(redis_db)
    else:
        response.messages.append("Not impemented new state actions")

    return make_response(jsonify(response.to_dict()), 200)


def path_get_db():
    cache = CacheService()
    redis_db = cache.get_db()
    response = c1_client.ActionResponse()
    response.messages.append(pprint.pformat(redis_db))
    return make_response(jsonify(response.to_dict()), 200)
