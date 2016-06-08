from google.appengine.ext import ndb


class Sporocilo(ndb.Model):
    ime = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.StringProperty()
    nastanek = ndb.DateTimeProperty(auto_now_add=True)