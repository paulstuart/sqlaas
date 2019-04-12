#!/usr/bin/env python

# starting from http://flask.pocoo.org/docs/1.0/quickstart/

from flask import Flask, session, redirect, url_for, escape, request

import json

from sqlite import dbcreate, dblist, dbschema, dbtable, dbinsert, dbselect

app = Flask(__name__)

base = "/sqlite/v1"

@app.route('/')
def hello_world():
    return 'hey now.'

@app.route(base + '/db/create/<name>', methods=['POST'])
def app_db_create(name):
    try:
        dbcreate(name)
        return "created db: " + name + "\n"
    except Exception as error:
        print("create name:{} error:{}", format(name, error))
        return "create name:{} error:{}\n", format(name, error)

@app.route(base + '/db/list', methods=['GET'])
def app_db_list():
    return "DB LIST HERE: %s\n" % "\n".join(dblist()) + "\n"

@app.route(base + '/db/<name>/schema', methods=['GET'])
def app_db_schema(name):
    try:
        return "schemed:\n" + "\n".join(dbschema(name)) + "\n"
    except:
        raise
    return "should never see this, ok?"
    
@app.route(base + '/db/<db>/create', methods=['POST'])
def app_db_create_table(db):
    try:
        data = request.get_data(as_text=True, cache=False)
        print("gonna create table for:" + request.path)
        print("create table DDL:" + data)
        dbtable(db, data)
        print("done wit table")
        return "created table on db: {}\n".format(db)
    except Exception as error:
        print("create table error:", error)
        return "error:{} data:{}\n".format(error, data)


@app.route(base + '/db/<name>/table/<table>', methods=['GET'])
def app_db_select(name, table):
    return dbselect(name, table)


@app.route(base + '/db/<name>/insert', methods=['POST'])
def app_db_insert(name):
    print("insert db:", name, "our type:", request.content_type)
    if request.content_type == 'application/json':
        try:
            print("j good?")
            j = request.get_json(cache=False)
            dbinsert(name, j['query'], j['values'])
            return "inserted\n"
        except Exception as error:
            print("JDATA:", request.data)
            print("json error:", error)
            raise
    else:
        return "whelp, unsupported content type: '{0}'\n".format(request.content_type)





def leftovers():
    """from db create toss after verifying worthless"""
    if request.content_type == 'application/sql':
        try:
            d = request.get_data(cache=False)
            print("given:", d)
        except Exception as error:
            print("mmm error:", error)

    if request.content_type == 'application/json':
        try:
            j = request.get_json(cache=False)
            #j = request.get_data(cache=False, as_text=True)
            #print("got j name: %s" % j['name'])
            resp = "hey: %s" % (j)
            print("BODY:", resp)
            return "JSON:" + resp + "\n"
        except Exception as error:
            print("ah error:", error)

    return "thanks\n"
