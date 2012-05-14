# still a FAILED WORK :(
import routes
from routes import Mapper
from routes.middleware import RoutesMiddleware
import eventlet

from eventlet import wsgi
import webob
from webob import Request, Response
from webob import exc


class ocni_server(object):
    """

    Represent the main occi REST server

    """

    class Application(object):
        """Test application to call from router."""

        def __call__(self, environ, start_response):
            start_response("200", [])
            return ['Router result']

    class Router(object):
        """Test router."""

        def _dispatch(self, req):
            """Dispatch the request to the appropriate controller.

            Called by self._router after matching the incoming request to a route
            and putting the information into req.environ.  Either returns 404
            or the routed WSGI app's response.

            """
            match = req.environ['wsgiorg.routing_args'][1]
            if not match:
                return webob.exc.HTTPNotFound()
            app = match['controller']
            return app

        def application(self, env, start_response):
            start_response('200 OK', [('Content-Type', 'text/plain')])
            return ['Hello, Houssem!\r\n']

        def __init__(self):
            mapper = routes.Mapper()
            mapper.connect("/", controller=self.application)
            self._router = routes.middleware.RoutesMiddleware(self._dispatch, mapper)

        #    def application(self, env, start_response):
        #        map = Mapper()
        #        map.connect("/", controller=self.Hello)#, action="post")#, conditions=dict(method=["GET"]))
        #
        #        self.Hello = RoutesMiddleware(self.Hello, map)
        #
        #        req = Request.blank('/')
        #        req.body = 'name=Houssem'
        #        resp = req.get_response(self.Hello)
        #        print (resp)
        #        return resp
        #
        #    class Hello(object):
        #        def __init__(self, req):
        #            self.request = req
        #
        #        def post(self):
        #            return 'Hello from POST %s!' % self.request.params['name']
        #
        #        def get(self):
        #            return 'Hello from GET'
        #
        #        def put(self):
        #            return 'Hello from PUT %s!' % self.request.params['name']
        #
        #        def delete(self):
        #            return 'Hello from DELETE'

    class Hello2(object):
        def __init__(self, req, action):
            self.a = action
            self.request = req

        def post(self):
            return 'Hello2 from POST %s!' % self.request.params['name']

        def get(self):
            return 'Hello2 from GET: 33333333 ' + str(self.a)

        def put(self):
            return 'Hello2 from PUT %s!' % self.request.params['name']

        def delete(self):
            return 'Hello2 from DELETE'

    from routes import Mapper

    map = Mapper()
    map.connect(None, "/error/{action}/", controller="Hello2")
    from routes.middleware import RoutesMiddleware

    app = RoutesMiddleware(Application, map)

    def run_server(self):
        """

        to run the server

        """

        #result = webob.Request.blank('/').get_response(self.Router())
        #print result

        eventlet.wsgi.server(eventlet.listen(('', 8090)), self.app)
        pass


#req2 = Request.blank('/')
#req2.body = 'name=Houssem'
#resp2 = req2.get_response()
#print (resp2)
if __name__ == '__main__':
    ocni_server_instance = ocni_server()
    ocni_server_instance.run_server()
