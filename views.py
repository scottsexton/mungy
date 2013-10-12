#!/usr/bin/env python
import re
from urllib import quote

from bottle import (redirect, template)

from models import (ImageFactory, ImageORM)


class HomeView(object):
    def __init__(self):
        self.template = 'home'

    def render_GET(self, images):
        return template(self.template, images=images)


class MungeView():
    def __init__(self):
        self.template = 'munge'

    def render_POST(self, form):
        if form['image1'] == '' or form['image2'] == '':
            msg = quote("This form requires all fields.")
            redirect('/error?msg='+msg)
        orm = ImageORM()
        image1 = orm.images(filename=form['image1'])[0]
        image2 = orm.images(filename=form['image2'])[0]
        algorithm = form['algorithm']
        munge_name = "%s-%s-%s.png" % (algorithm.lower(), re.sub(r'\.png$', '', form['image1']), re.sub(r'\.png$', '', form['image2']))
        munger = ImageFactory.new_image_munge(image1, image2, filename=munge_name)
        munged_img = munger.munge(algorithm)
        return template(self.template, munge=munger)


class UploadView(object):
    def render_POST(self, form, data):
        if data and data.file:
            filename = re.sub(r'\.\w{3,4}$', '.png', data.filename, flags=re.IGNORECASE)
            new_img = ImageFactory.new_image(filename=filename)
            with open(new_img.fullpath, 'wb') as file_data:
                file_data.write(data.file.read())
            new_img.resize(300,300)
            new_img.mode('png')
            new_img.save()
        redirect('/')


class ErrorView(object):
    def __init__(self):
        self.template = 'error'

    def render(self, query):
        msg = query.get('msg', '')
        return template(self.template, message=msg)
