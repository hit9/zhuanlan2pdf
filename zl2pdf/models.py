# coding=utf8

"""
    zl2pdf.models
    ~~~~~~~~~~~~~

    ZhuanLan models
"""


class Post(object):
    '''zhuanlan.zhihu.com/{{column.slug}}/{{self.urltoken}}'''

    def __init__(self,
                 title=None,
                 author=None,
                 published_at=None,  # datetime object
                 title_pic=None,  # title Image URL
                 urltoken=None, # string, i.e. '19637432'
                 content=None,
                 ):

        self.urltoken = urltoken
        self.title = title
        self.author = author
        self.published_at = published_at
        self.title_pic = title_pic
        self.content = content


class Column(object):
    '''zhuanlan.zhihu.com/{{self.slug}}'''

    def __init__(self,
                 slug=None,  # string, column' short url name
                 name=None,
                 description=None
                 ):
        self.name = name
        self.description = description
        self.posts_count = 0
