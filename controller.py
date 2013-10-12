#!/usr/bin/env python
import bottle

import models
import os.path
import settings
import views


class Server(object):
    def __init__(self, init_db=False):
        self.app = bottle.Bottle()
        Routes.setup_routing(self.app)
        if init_db:
            models.DBManager().initialize_db()


class ImageDeletor(object):
    @classmethod
    def delete(cls, filename=None):
        if filename:
            img = models.ImageORM().images(filename=filename)[0]
            img.delete()
        else:
            for img in models.ImageORM().images():
                img.delete()


class Routes(object):
    @staticmethod
    def setup_routing(app):
        bottle.TEMPLATE_PATH = ['./templates/']

        @app.get('/css/<filename:path>')
        def send_js(filename):
            return bottle.static_file(filename, root=settings.STYLE_DIR)

        @app.get('/js/<filename:path>')
        def send_js(filename):
            return bottle.static_file(filename, root=settings.SCRIPT_DIR)

        @app.get('/<filename:re:favicon\.ico>')
        @app.get('/images/<filename:path>')
        def send_image(filename):
            return bottle.static_file(filename, root=settings.IMAGE_DIR)

        @app.delete('/images')
        @app.delete('/images/<filename:path>')
        def delete_image(filename=None):
            ImageDeletor.delete(filename)
            bottle.redirect('/')

        @app.post('/images')
        def new_image():
            return views.UploadView().render_POST(bottle.request.forms, bottle.request.files.new_upload)

        @app.post('/munge')
        def munge():
            return views.MungeView().render_POST(bottle.request.forms)

        @app.get('/')
        def index():
            image_manager = models.ImageORM()
            return views.HomeView().render_GET(images=image_manager.images())

        @app.get('/error')
        def uh_oh():
            return views.ErrorView().render(bottle.request.query)


if __name__ == '__main__':
    server = Server(init_db=not os.path.isfile('oo_proj.db'))
    server.app.run(host='localhost', port=8080, debug=True)
