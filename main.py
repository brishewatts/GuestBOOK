#!/usr/bin/env python
import os
import jinja2
import webapp2

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
        return self.render_template("hello.html")

class PosljiSporociloHandler(BaseHandler):
    def post(self):
        ime = self.request.get("ime")
        email = self.request.get ("email")
        sporocilo = self.request.get("sporocilo")

        if ime == "":
            ime = "unknown"

        if email == "":
            email = "not given"

        sporocilo = Sporocilo(ime=ime, email=email, message=sporocilo)
        sporocilo.put()

        return self.render_template("message.html")

class PrikaziSporociloHandler(BaseHandler):
    def get(self):
        all_messages = Sporocilo.query().order(Sporocilo.nastanek).fetch()

        messages = {"all_messages": all_messages}

        return self.render_template("prikazi_sporocila.html", messages)


class PosameznoSporocilo(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        message = {
            "sporocilo": sporocilo
        }

        return self.render_template("posamezno_sporocilo.html", message)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/message', PosljiSporociloHandler),
    webapp2.Route('/prikazi-sporocila', PrikaziSporociloHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
], debug=True)
