# coding=utf8

"""
    zl2pdf.zl2pdf
    ~~~~~~~~~~~~~

    The core worker.

    Usage::

        >>> from zl2pdf.zl2pdf import Zl2PDF
        >>> zl2pdf = Zl2PDF(slug, pool_size=15)
        >>> zl2pdf.run()
"""

import os
import sys
import time
import subprocess

import gevent
import requests
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all(thread=False, select=False)
from jinja2 import Environment, FileSystemLoader

from . import charset
from .models import Column, Post
from .logger import logger
from .zhapis import *
from .exceptions import *


class Zl2PDF(object):

    def __init__(self, slug, pool_size=20):  # default pool size: 20
        self.slug = slug
        self.column = Column(slug=self.slug)
        self.posts = []
        self.pool_size = pool_size
        self.out = self.slug + '.pdf'  # output filename
        self.cmd = ['wkhtmltopdf',
                         '-',
                         # '--quiet',  # Be less verbose
                         '--page-size',  # Set paper size to: A4
                         'A4',
                         '--outline',
                         '--outline-depth',  # Set the depth of the outline
                         '2',
                         self.out]
        self.html = None
        self.lib_path = os.path.normpath(
            os.path.abspath(os.path.dirname(__file__)))
        self.static_path = os.path.normpath(os.path.join(self.lib_path, 'static'))

    def load_column(self):
        '''load column information from zhihu.com..'''

        logger.info(self.load_column.__doc__)

        uri = load_column_api(self.slug)

        try:
            r = requests.get(uri)
        except RequestException, e:
            logger.error(str(e))
            sys.exit(1)

        if r.status_code != 200:  # 404, 403 .. Not OK
            logger.error('Response status code not 200: %r' % r.status_code)
            sys.exit(1)

        # status: 200

        data = r.json()

        self.column.name = data.get('name')
        self.column.description = data.get('description')
        self.column.posts_count = data.get('postsCount')
        logger.success('column information load: name: %s, description: %s, posts: %d' % (
            self.column.name, self.column.description, self.column.posts_count
        ))

    def load_posts_list(self):
        '''load posts list from this column'''

        logger.info(self.load_posts_list.__doc__)

        uri = load_posts_api(self.slug)
        params = {'limit': self.column.posts_count, 'offset': 0}

        try:
            r = requests.get(uri, params=params)
        except RequestException, e:
            logger.error(str(e))
            sys.exit(1)

        if r.status_code != 200:  # 404, 403 .. Not OK
            logger.error('Response status code not 200: %r' % r.status_code)
            sys.exit(1)

        # status: 200

        data = r.json()
        self.posts = [Post(
            urltoken=item.get('slug'),
            published_at=load_datetime(item.get('publishedTime'))
        ) for item in data]

        # Ask: Need us sort by time? No

        logger.success('posts list load')

    def load_single_post(self, post):  # urltoken: int

        urltoken = post.urltoken

        assert post.urltoken  # should not empty

        uri = load_post_api(self.slug, urltoken)

        try:
            r = requests.get(uri)
        except RequestException, e:
            logger.warn(str(e)+ ', urltoken: %d' % urltoken)
            pass  # skip troubled post
        else:
            if r.status_code != 200:
                logger.warn('Response status code not 200: %r, urltoken: %d' % (r.status_code, urltoken))
            else:
                data = r.json()
                post.content = data.get('content')
                post.title = data.get('title')
                post.title_pic = data.get('titleImage')
                post.author = data.get('author').get('name')
                logger.info('ok, title: %s, urltoken: %d' % (post.title, post.urltoken))

    def load_posts(self):
        """load each post from zhihu.com.."""
        logger.info(self.load_posts.__doc__)

        assert self.posts

        pool = Pool(size=self.pool_size)

        for post in self.posts:
            pool.spawn(self.load_single_post, post)

        pool.join()

        logger.success('all posts load')

    def render(self):
        """render posts with template"""
        logger.info(self.render.__doc__)
        env = Environment(loader=FileSystemLoader(self.static_path))
        template = env.get_template('pdf.html')
        self.html = template.render(static_path=self.static_path,
                                    posts=self.posts,
                                    column=self.column)
        logger.success('rendered')

    def run(self):
        start_time = time.time()
        logger.info("started. short url: %s, pool size: %d, output: %s" % (self.slug, self.pool_size, self.out))
        self.load_column()
        self.load_posts_list()
        self.load_posts()
        self.render()
        logger.info('Generate pdf with wkhtmltopdf:')
        proc = subprocess.Popen(self.cmd, stdin=subprocess.PIPE,
                                stdout=sys.stdout, stderr=sys.stderr)
        stdout, stderr = proc.communicate(input=self.html.encode(charset))
        logger.success('Generated to %s in %.3f seconds' % (self.out, time.time() - start_time))
