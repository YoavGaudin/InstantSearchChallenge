from google.appengine.ext import ndb
import json
import logging

class Variable(ndb.Model):
    value = ndb.StringProperty()


class RequestQueue(ndb.Model):
    queue = ndb.JsonProperty()

    def push(self, req):
        q = json.loads(self.queue)
        q.append(req)
        logging.info("A new request was pushed to the queue {}".format(q))
        self.queue = json.dumps(q)
        self.put()

    def pop(self):
        q = json.loads(self.queue)
        if not q:
            return None
        print(q)
        logging.info("About to pop a request from queue {}".format(q))
        req = q.pop()
        logging.info("Popped {}".format(req))
        self.queue = json.dumps(q)
        self.put()
        return req