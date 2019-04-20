#!/usr/bin/env python

from flask import url_for

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

# https://stackoverflow.com/questions/13317536/get-list-of-all-routes-defined-in-the-flask-app/19116758
def site_links(app):
    links = []
    for rule in app.url_map.iter_rules():
        print ("RULE:", rule)
        #if len(rule.defaults) >= len(rule.arguments):
        if has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return links

# https://stackoverflow.com/a/36033627
class PrefixMiddleware(object):
    def __init__(self, app, prefix=''):
        self.app = app
        self.prefix = prefix

    def __call__(self, environ, start_response):

        if environ['PATH_INFO'].startswith(self.prefix):
            environ['PATH_INFO'] = environ['PATH_INFO'][len(self.prefix):]
            environ['SCRIPT_NAME'] = self.prefix
            return self.app(environ, start_response)
        else:
            start_response('404', [('Content-Type', 'text/plain')])
            return ["This url does not belong to the app.".encode()]

