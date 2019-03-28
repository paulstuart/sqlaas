

from flask import Flask, session, redirect, url_for, escape, request

import json

#import sqlite3
from sqlite import dbcreate, dblist, dbschema, dbtable, dbinsert, dbselect

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

base = "/sqlite/v1"

#@app.route(base + '/db/create')
@app.route(base + '/db/create/<name>', methods=['POST'])
def app_db_create(name):
    try:
        dbcreate(name)
        return "created: " + name
    except:
        raise
    
    #print("do create")
    #return "okay\n"
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
            print("got j name: %s" % j['name'])
            resp = "hey: %s" % (j)
            print("BODY:", resp)
            return "JSON:" + resp + "\n"
        except Exception as error:
            print("ah error:", error)

    return "thanks\n"
    #return 'Hello, World!'


@app.route(base + '/db/list', methods=['GET'])
def app_db_list():
    return "HERE: %s\n" % "\n".join(dblist())

@app.route(base + '/db/<name>/schema', methods=['GET'])
def app_db_schema(name):
    try:
        return "schemed:\n" + "\n".join(dbschema(name))
    except:
        raise
    
@app.route(base + '/db/<db>/table/<table>', methods=['POST'])
def app_db_create_table(db, table):

    try:
        data = request.data.decode("utf-8") #get_data(cache=False)
        print("do table")
        dbtable(db, table, data)
        print("done table")
        return "created: {0}.{1}".format(db, table)
    except Exception as error:
        print("crap error:", error)
        print("crap data:", data)
        return "erp, unsupported content type: '{0}'".format(request.content_type)

    return "sorry, unsupported content type: '{0}'".format(request.content_type)


@app.route(base + '/db/<name>/table/<table>', methods=['GET'])
def app_db_select(name, table):
    return dbselect(name, table)


@app.route(base + '/db/<name>/insert/<table>', methods=['POST'])
def app_db_insert(name, table):
    print("insert table:", table)   
    print("our type:", request.content_type)
    if request.content_type == 'application/json':
        try:
            print("j good?")
            j = request.get_json(cache=False)
            #j=j = request.data.decode("utf-8") #get_data(cache=False)
            #jj = json.loads(j)
            #print("jj:",jj)

            #j = request.get_data(cache=False, as_text=True)
            #data = request.data.decode("utf-8") #get_data(cache=False)
            print( "j data:" , j)
            #print("got j name: %s" % j['name'])
            resp = "hey: %s" % (j)
            print("BODY:", resp)
            print("query:", j['query'])
            print("values:", j['values'])
            #return "JSON:" + resp + "\n"
            answer = dbinsert(name, j['query'], j['values'])
            print("answer:", answer)
        except Exception as error:
            print("JDATA:", request.data)
            print("json error:", error)
            raise

    return "thanks\n"
