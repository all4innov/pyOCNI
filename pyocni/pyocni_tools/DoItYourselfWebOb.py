# All rights reserved
# Work extracted from webob.org website
# thttp://docs.webob.org/en/latest/do-it-yourself.html

import re
import sys
from webob import Request, Response
from webob import exc

import eventlet
from eventlet import wsgi

var_regex = re.compile(r'''
     \{        # The exact character "{"
     (\w+)       # The variable name (restricted to a-z, 0-9, _)
      (?::([^}]+))? # The optional :regex part
     \}          # The exact character "}"
     ''', re.VERBOSE)


def template_to_regex(template):
    regex = ''
    last_pos = 0
    for match in var_regex.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex


def load_controller(string):
    module_name, func_name = string.split(':', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    func = getattr(module, func_name)
    return func


class Router(object):
    def __init__(self):
        self.routes = []

    def add_route(self, template, controller, **vars):
        if isinstance(controller, basestring):
            controller = load_controller(controller)
        self.routes.append((re.compile(template_to_regex(template)),
                            controller,
                            vars))

    def __call__(self, environ, start_response):
        req = Request(environ)
        for regex, controller, vars in self.routes:
            match = regex.match(req.path_info)
            if match:
                req.urlvars = match.groupdict()
                req.urlvars.update(vars)
                return controller(environ, start_response)
        return exc.HTTPNotFound()(environ, start_response)


def controller(func):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            resp = func(req, **req.urlvars)
        except exc.HTTPException, e:
            resp = e
        if isinstance(resp, basestring):
            resp = Response(body=resp)
        return resp(environ, start_response)

    return replacement


def rest_controller(cls):
    def replacement(environ, start_response):
        req = Request(environ)
        try:
            instance = cls(req, **req.urlvars)
            action = req.urlvars.get('action')
            if action:
                action += '_' + req.method.lower()
            else:
                action = req.method.lower()
            try:
                method = getattr(instance, action)
            except AttributeError:
                raise exc.HTTPNotFound("No action %s" % action)
            resp = method()
            if isinstance(resp, basestring):
                resp = Response(body=resp)
        except exc.HTTPException, e:
            resp = e
        return resp(environ, start_response)

    return replacement

if __name__ == '__main__':
    #================================================================================
    @controller
    def hello(req):
        if req.method == 'POST':
            return 'Hello from POST %s!' % req.params['name']
        elif req.method == 'GET':
            return '''<form method="POST">
                 You're name: <input type="text" name="name">
                 <input type="submit">
                 </form>'''

    hello_world = Router()
    hello_world.add_route('/', controller=hello)

    req = Request.blank('/')
    resp = req.get_response(hello_world)
    print (resp)

    req.method = 'POST'
    req.body = 'name=Houssem'
    resp = req.get_response(hello_world)
    print (resp)
    #================================================================================

    print ('================================================================================')

    #================================================================================
    class Hello(object):
        def __init__(self, req):
            self.request = req

        def post(self):
            return 'Hello from POST %s!' % self.request.params['name']

        def get(self):
            return 'Hello from GET'

        def put(self):
            return 'Hello from PUT %s!' % self.request.params['name']

        def delete(self):
            return 'Hello from DELETE'

    class Hello2(object):
        def __init__(self, req, a):
            self.a = a
            self.request = req

        def post(self):
            print self.request.body
            return 'Hello2 from POST %s!' % self.request. params

        def get(self):
            return 'Hello2 from GET: 33333333 ' + str(self.a)

        def put(self):
            return 'Hello2 from PUT %s!' % self.request.params['name']

        def delete(self):
            return 'Hello2 from DELETE'

    hello = rest_controller(Hello)
    hello2 = rest_controller(Hello2)

    hello_world = Router()
    hello_world.add_route('/', controller=hello)
    hello_world.add_route('/{a:bb}/', controller=hello2)

    req = Request.blank('/a/')
    req.body = 'name=Houssem'
    resp = req.get_response(hello_world)
    print (resp)

    req.method = 'POST'
    resp = req.get_response(hello_world)
    print (resp)

    req.method = 'GET'
    resp = req.get_response(hello_world)
    print (resp)

    req.method = 'PUT'
    resp = req.get_response(hello_world)
    print (resp)

    req.method = 'DELETE'
    resp = req.get_response(hello_world)
    print (resp)

    # =======================================================================

    class ocni_server(object):
        """

        Represent the main occi REST server

        """

        def run_server(self):
            """

            to run the server

            """
            wsgi.server(eventlet.listen(('', 8090)), hello_world)

            pass

    ocni_server_instance = ocni_server()
    ocni_server_instance.run_server()
