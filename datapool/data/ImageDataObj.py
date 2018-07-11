from datetime import datetime


class ImageDetailBase:
    def __iter__(self):
        pass


class ImageDetailObj2(ImageDetailBase):
    def __init__(self,
                 title='',
                 author='',
                 url_list=None,
                 tag_list=None,
                 likes=0,
                 comments=0,
                 date=datetime.now()):
        """
        @type title: str
        @type author: str
        @type url_list: dict
        @type tag_list: dict
        @type likes: int
        @type comments: int
        @type date: datetime

        :param title: the title of this album
        :param author: the owner of this album
        :param url_list: {id: photo url}
        :param tag_list: {tag string: tag url}
        :param likes: the number of likes
        :param comments: the number of comments
        :param date: timestamp
        """

        self.__title = title
        self.__author = author
        self.__url_list = url_list
        self.__tag_list = tag_list
        self.__likes = likes
        self.__comments = comments
        self.__date = date

    def __iter__(self):
        yield 'author', self.__author
        yield 'title', self.__title
        yield 'uri', self.__url_list
        yield 'tag', self.__tag_list
        yield 'likes', self.__likes
        yield 'comments', self.__comments
        yield 'post date', self.__date.strftime('%Y-%m-%d %H:%M')

    def __parameters_checker(self):
        if self.__title is None:
            raise ValueError('The parameter title is invalid.')
        if self.__author is None:
            raise ValueError('The parameter author is invalid.')
        if self.__url_list is None or not isinstance(self.__url_list, dict):
            raise ValueError('The parameter url_list is invalid.')
        if self.__tag_list is None or not isinstance(self.__tag_list, dict):
            raise ValueError('The parameter tag_list is invalid.')
        if self.__likes is None:
            raise ValueError('The parameter likes is invalid.')
        if self.__comments is None:
            raise ValueError('The parameter comments is invalid.')
        if self.__date is None:
            raise ValueError('The parameter date is invalid.')


if __name__ == '__main__':
    pass
