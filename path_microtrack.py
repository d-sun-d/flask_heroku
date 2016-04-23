from flask import render_template, jsonify, make_response
from flask import request
import libs.yandex_translate as ytr
import libs.chartfirst_client as c1_client
import pprint

LOCAL_DB = {
    "tasks":{},
    "last_id":0
}


def path_microtrack_add():
    params = {key:rec for key, rec in request.args.items()}
    id = LOCAL_DB["last_id"]
    LOCAL_DB["last_id"] += 1
    params["original_lang"] = ytr.detect_lang(params["text"])
    params["en_text"] = ytr.translate(params["text"], params["original_lang"]+"-en")
    LOCAL_DB[id] = params

    response = c1_client.ActionResponse()
    new_task_text = ytr.translate("New task", params["original_lang"])
    response.messages.append(new_task_text+" id:"+str(id))

    return make_response(jsonify(response.to_dict()), 200)


def path_get_db():
    response = c1_client.ActionResponse()
    response.messages.append(pprint.pformat(LOCAL_DB))
    return make_response(jsonify(response.to_dict()), 200)
