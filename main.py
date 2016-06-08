#!/usr/bin/env python
import os
import jinja2
import webapp

from models import Sporocilo


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("conversation.html")

class PosljiSporociloHandler(BaseHandler):
    def post(self):
        usr_ime = self.request.get("ime")
        usr_email = self.request.get ("email")
        sporocilo = self.request.get("sporocilo")

        if usr_ime == "":
            usr_ime = "unknown"

        if usr_email == "":
            usr_email = "not given"

        sporocilo = Sporocilo(ime=usr_ime, email=usr_email, message=sporocilo)
        sporocilo.put()

        return self.render_template("message.html")

class PrikaziSporociloHandler(BaseHandler):
    def get(self):
        all_messages = Sporocilo.query().order(Sporocilo.nastanek).fetch()

        params = {"all_messages": all_messages}

        return self.render_template("seznam_sporocil.html", params=params)


class PosameznoSporocilo(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        params = {
            "sporocilo": sporocilo
        }

        return self.render_template("posamezno_sporocilo.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/message', PosljiSporociloHandler),
    webapp2.Route('/seznam-sporocil', PrikaziSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
], debug=True)
