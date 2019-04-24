#!/usr/bin/env python

# starting from http://flask.pocoo.org/docs/1.0/quickstart/

from flask import Flask, session, redirect, url_for, escape, request, render_template, Response

import json

from sqlite import dbcreate, dblist, dbschema, dbtable, dbinsert, dbselect, dbtables, db_query, db_table_info
from sqlite import fullname # hack for now

from helpers import site_links, PrefixMiddleware

# temp hack
import sqlite3

# routing from nginx based on this prefix
prefix = "/sqlite"

app = Flask(__name__)
app.debug = True
app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=prefix)


# our top-level route
@app.route('/')
def app_home():
    return render_template('index.html')


# https://stackoverflow.com/questions/13317536/get-list-of-all-routes-defined-in-the-flask-app/19116758
@app.route("/site-map")
def site_map():
    return render_template("all_links.html", links=site_links(app))

@app.route('/db/<dbname>/table/<table>/', methods=['GET'])
def app_table_schema(dbname, table):
    title = "Schema for " + table
    columns, rows = db_table_info(dbname, table)
    return render_db_table(title, columns, rows)
    #return render_template("table_info.html", base=base, columns=columns, rows=rows, title=title)

@app.route('/db/<dbname>/dump', methods=['GET'])
def app_db_dump(dbname):
    def generate():
        # how to return from sqlite.py instead? (close after stream!)
        conn = sqlite3.connect(fullname(dbname))
        for line in conn.iterdump():
            yield line + "\n"
        conn.close()

    return Response(generate(), mimetype='text/sql')

@app.route('/db/<dbname>/', methods=['GET'])
def app_db_tables(dbname):
    return render_template("tables.html", dbname=dbname, tables=dbtables(dbname))

@app.route('/db/<dbname>', methods=['POST'])
def app_db_create(dbname):
    try:
        dbcreate(dbname)
        return "created db: " + dbname + "\n"
    except Exception as error:
        print("create name:{} error:{}", format(dbname, error))
        return "create name:{} error:{}\n", format(dbname, error)

@app.route('/db/', methods=['GET'])
def app_db_list():
    return render_template('db_list.html', dblist = dblist())
    #return "DB LIST: %s\n" % "\n".join(dblist()) + "\n"

    
@app.route('/db/<db>/create', methods=['POST'])
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


"""
@app.route('/db/<name>/table/<table>', methods=['GET'])
def app_db_select(name, table):
    return dbselect(name, table)
"""


@app.route('/db/<name>/insert', methods=['POST'])
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

def render_db_table(title, columns, rows):
    return render_template("basic_table.html", columns=columns, rows=rows, title=title)


#@app.route('/sqlite/static/<file>')
