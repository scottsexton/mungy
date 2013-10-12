#!/usr/bin/env python
import os
import sqlite3

from PIL import Image as PILImage

import settings
import strategies


class DBManager(object):
    operator = {'eq': '=',
                'ne': '<>',
                'gt': '>',
                'gte': '>=',
                'lt': '<',
                'lte': '<=',
               }

    def __init__(self, database='oo_proj.db'):
        self.conn = sqlite3.connect(database)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def initialize_db(self):
        try:
            self.query(ImageORM.schema)
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

    def query(self, sql, bind_vars=None):
        print "QUERY:",sql
        if bind_vars is not None:
            print "VARS:",bind_vars
            return self.cur.execute(sql,bind_vars)
        return self.cur.execute(sql)

    def filter(self, **kwargs):
        sql = "SELECT * FROM "+self.__class__.table
        where = []
        for key, value in kwargs.items():
            if value:
                if '__' in key:
                    field, operator = key.split('__')[:2]
                else:
                    field, operator = (key,'=')
                where.append("%s %s '%s'" % (field, operator, kwargs[key]))
        if len(where) > 0:
            sql += ' WHERE '+' AND '.join(where)
        print "FILTER:",sql
        return self.cur.execute(sql)

    def save(self, obj):
        columns = []
        values = []
        for field in self.__class__.fields:
            value = getattr(obj, field, None)
            if value:
                columns.append(field)
                values.append(value)
        qs = ['?']*len(columns)
        sql = 'INSERT OR REPLACE INTO %s (%s) VALUES (%s)' % (self.__class__.table, ','.join(columns), ','.join(qs))
        self.query(sql, values)

    def delete(self, obj):
        sql = 'DELETE FROM %s WHERE id = ?' % self.__class__.table
        self.query(sql, str(obj.id))

    def __del__(self):
        self.conn.commit()
        self.conn.close()


class ImageORM(DBManager):
    table = 'images'
    fields = ('id', 'filename', 'pub_date')
    schema = "CREATE TABLE images(id INTEGER PRIMARY KEY, filename TEXT NOT NULL UNIQUE, created DATETIME DEFAULT CURRENT_TIMESTAMP)"

    def images(self, filename=None):
        return [ImageFactory.new_image(**dict(zip(image_record.keys(), image_record))) for image_record in self.filter(filename=filename)]

    def get_random(self, not_in=None):
        sql = "SELECT id, filename FROM images"
        bind_vars = None
        if not_in and len(not_in) > 0:
            bind_vars = [str(i) for i in not_in]
            qs = ['?']*len(not_in)
            sql += ' WHERE id NOT IN (%s)' % ','.join(qs)
        sql += " ORDER BY RANDOM() LIMIT 1"
        return [ImageFactory.new_image(**dict(zip(image_record.keys(), image_record))) for image_record in self.query(sql, bind_vars)][0]

    def save(self, image):
        super(ImageORM, self).save(image)

    def delete(self, image):
        super(ImageORM, self).delete(image)


class ImageFactory(object):
    @classmethod
    def new_image(cls, **kwargs):
        image = Image()
        for field in ImageORM.fields:
            if field in kwargs:
                setattr(image, field, kwargs[field])
        return image

    @classmethod
    def new_image_munge(cls, *args, **kwargs):
        munge = ImageMunge(**kwargs)
        for img in args:
            munge.add(img)
        return munge


class Image(object):
    def __init__(self, id=None, filename=None):
        self.id = id
        self.filename = filename

    @property
    def fullpath(self):
        return os.path.join(settings.IMAGE_DIR, self.filename)

    @property
    def file_data(self):
        return PILImage.open(self.fullpath)

    def resize(self, height, width):
        img_file = self.file_data
        img_file = img_file.resize((height, width), PILImage.ANTIALIAS)
        img_file.save(self.fullpath)

    def delete(self):
        try:
            os.remove(self.fullpath)
        except OSError:
            pass
        if self.id is not None:
            ImageORM().delete(self)

    def mode(self, img_type):
        img_file = self.file_data
        if img_file.mode != 'RGBA':
            fixed_type = PILImage.new('RGBA', img_file.size)
            fixed_type.paste(img_file)
            fixed_type.save(self.fullpath)

    def save(self):
        ImageORM().save(self)


class ImageMunge(Image):
    def __init__(self, id=None, filename=None):
        self.members = []
        super(ImageMunge, self).__init__(id, filename)

    def add(self, image):
        if len(self.members) >= 2:
            raise ValueError("ImageMunge can only contain two Images")
        self.members.append(image)

    def remove(self, image):
        self.members.remove(image)

    def munge(self, strategy):
        if len(self.members) < 2:
            raise ValueError('Munge requires two images')
        strategy = getattr(strategies, strategy)()
        manip_image = strategy.manip(self.members[0], self.members[1], self.filename)
        manip_image = ImageFactory.new_image(filename=self.filename)
        manip_image.save()
        return manip_image
