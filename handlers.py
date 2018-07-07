import webapp2
from entities import *


class GetHandler(webapp2.RequestHandler):
    def get(self, request):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write("GetHandler")
        # Variable()


class SetHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.__class__)


class UnsetHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.__class__)


class NumEqualToHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.__class__)


class UndoHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.__class__)


class EndHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(self.__class__)

