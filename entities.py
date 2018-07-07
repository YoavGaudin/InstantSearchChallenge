import sys

sys.path.append('C:\\Program Files (x86)\\Google\\google-cloud-sdk')


from google.appengine.ext import ndb


class Variable(ndb.Model):
    value = ndb.StringProperty()