from dataclasses import dataclass
from datetime import datetime


class ImageDetailBase:
    def __iter__(self):
        pass


@dataclass
class ImageDetailObj2(ImageDetailBase):
    title: str  # the title of this album
    author: str  # the owner of this album
    url_list: dict  # {id: photo url}
    tag_list: dict  # {tag string: tag url}
    likes: int  # the number of likes
    comments: int  # the number of comments
    date: datetime = datetime.now()  # timestamp

    def __iter__(self):
        yield 'author', self.author
        yield 'title', self.title
        yield 'uri', self.url_list
        yield 'tag', self.tag_list
        yield 'likes', self.likes
        yield 'comments', self.comments
        yield 'post date', self.date.strftime('%Y-%m-%d %H:%M')

    def __parameters_checker(self):
        if self.title is None:
            raise ValueError('The parameter title is invalid.')
        if self.author is None:
            raise ValueError('The parameter author is invalid.')
        if self.url_list is None or not isinstance(self.url_list, dict):
            raise ValueError('The parameter url_list is invalid.')
        if self.tag_list is None or not isinstance(self.tag_list, dict):
            raise ValueError('The parameter tag_list is invalid.')
        if self.likes is None:
            raise ValueError('The parameter likes is invalid.')
        if self.comments is None:
            raise ValueError('The parameter comments is invalid.')
        if self.date is None:
            raise ValueError('The parameter date is invalid.')


if __name__ == '__main__':
    pass
