import webapp2
from entities import Variable, RequestQueue
from google.appengine.ext import ndb
import json


def get_or_create_queue():
    key = ndb.Key('RequestQueue', 'request_queue')
    queue = key.get()
    if queue is None:
        queue = RequestQueue(id='request_queue', queue=json.dumps([]))
        queue.put()
    else:
        queue = key.get()

    return queue


def push_req(req):
    q = get_or_create_queue()
    q.push(req)


def pop_req():
    q = get_or_create_queue()
    return q.pop()


class GetHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name')
        key = ndb.Key('Variable', name)
        var = key.get()
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(getattr(var, 'value', None))


class SetHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name')
        value = self.request.get('value')
        key = ndb.Key('Variable', name)
        var = key.get()
        if var is None:
            var = Variable(id=name, value=value)
            previous_value = None
        else:
            previous_value = var.value
            var.value = value
        var.put()
        push_req((name, previous_value))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('')


class UnsetHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name')
        key = ndb.Key('Variable', name)
        var = key.get()
        key.delete()
        push_req((name, getattr(var, 'value', None)))
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('')


class NumEqualToHandler(webapp2.RequestHandler):
    def get(self):
        value = self.request.get('value')
        query = Variable.query(Variable.value == value)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(query.count())


class UndoHandler(webapp2.RequestHandler):
    def get(self):
        req = pop_req()
        print(req)
        if req is None:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.write('NO COMMANDS')
            return
        name, value = req
        if value is None:
            key = ndb.Key('Variable', name)
            key.delete()
        else:
            var = Variable(id=name, value=value)
            var.put()




class EndHandler(webapp2.RequestHandler):
    def get(self):
        Variable.query().map(lambda v: v.key.delete())
        RequestQueue.query().map(lambda v: v.key.delete())
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('')

