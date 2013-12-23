# coding=utf8

"""
    zl2pdf.zhapis
    ~~~~~~~~~~~~~

    zhuanlan.zhihu.com's **PUBLIC** GET http apis.
"""

from datetime import datetime

LOAD_COLUMN_URI_PATTERN = 'http://zhuanlan.zhihu.com/api/columns/{slug}'
LOAD_POSTS_URI_PATTERN = 'http://zhuanlan.zhihu.com/api/columns/{slug}/posts'
LOAD_POST_URI_PATTERN = 'http://zhuanlan.zhihu.com/api/columns/{slug}/posts/{urltoken}'

DATETIME_FORMATTER = '%Y-%m-%dT%H:%M:%S'


def load_column_api(slug):
    """load column information.
    sample::

        >>> api_uri = load_column_api(slug)
        >>> requests.get(api_uri)"""
    return LOAD_COLUMN_URI_PATTERN.format(slug=slug)


def load_posts_api(slug):
    """load multiple posts.
    sample::

        >>> api_uri = load_posts_api(slug)
        >>> requests.get(api_uri, params={'limit': 10, 'offset': 0})"""
    return LOAD_POSTS_URI_PATTERN.format(slug=slug)  # py version >= 2.6


def load_post_api(slug, urltoken):
    """load single post.
    sample::

        >>> api_uri = load_post_api(slug, urltoken)
        >>> requests.get(api_ur)"""
    return LOAD_POST_URI_PATTERN.format(slug=slug, urltoken=urltoken)


def load_datetime(time_str):
    """'2013-11-16T21:22:10+08:00' => datetime.datetime(2013, 11, 16, 21, 22, 10)"""
    return datetime.strptime(time_str[:19], DATETIME_FORMATTER)
