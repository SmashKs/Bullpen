import json
from collections import namedtuple
from pprint import pprint as pp

import pyrebase
from pyrebase.pyrebase import Auth, Database, Firebase, Storage

from datapool.firebase import FIREBASE_CONFIGURATION

IMAGE_VERSION_1 = 'ImageVersion1'
IMAGE_VERSION_2 = 'ImageVersion2'


class FirebaseWrapper(object):
    @staticmethod
    def convert_dict_to_obj(object_name=None, data=None):
        """
        :param object_name: str
        :param data: dict
        :return: object
        """
        if not object_name:
            object_name = ''
        if not data:
            data = {}

        return namedtuple(object_name, data.keys())(*data.values())

    def __init__(self):
        self.__USER_CONFIG = FIREBASE_CONFIGURATION
        self.__user_config = None  # type: dict
        self.__firebase = None  # type: Firebase
        # *** We don't use this `auth` now.
        self.__firebase_auth = None  # type: Auth
        self.__firebase_database = None  # type: Database
        self.__firebase_storage = None  # type: Storage

    def _load_user_config(self):
        try:
            with open(self.__USER_CONFIG) as file:
                self.__user_config = json.loads(file.read())
        except FileNotFoundError as err:
            pp(err)
            self.__user_config = None

    def _obtain_each_objects(self):
        if self.__user_config:
            try:
                self.__firebase = pyrebase.initialize_app(self.__user_config)
            except FileNotFoundError as err:
                pp(err)
                self.__user_config = None

            # Get the firebase then assign each subjects.
            if self.__firebase:
                self.__firebase_auth = self.__firebase.auth()
                self.__firebase_database = self.__firebase.database()
                self.__firebase_storage = self.__firebase.storage()

    def _fetch_all_user_name(self, image_version=IMAGE_VERSION_2):  # type: (FirebaseWrapper, str) -> list
        name_list = []

        for name in self.__firebase_database.child(image_version).get().each():
            name_list.append(name.key())

        return name_list

    def __modified_variable(self, firebase_v2_data):
        pass

    def create(self):
        """
        @rtype: FirebaseWrapper
        """
        self._load_user_config()
        self._obtain_each_objects()

        return self

    def upload(self):
        if self.__firebase:
            self.__firebase = None

    def write_image_properties(self, author='', image_data=None, image_version=IMAGE_VERSION_2):
        """
        @type author: str
        @type image_data: dict
        @type image_version: str
        """

        if len(author) == 0:
            raise ValueError('The parameter author must have data.')

        if not isinstance(image_data, dict):
            raise TypeError('image_data should be a dict object.')

        self.__firebase_database.child(image_version).child(author).update(image_data)

    def read_image_properties(self, author=None, image_version=IMAGE_VERSION_2):
        root_node = self.__firebase_database.child(image_version)

        if author is not None:
            root_node = root_node.child(author)

        return root_node.get()


if __name__ == '__main__':
    f = FirebaseWrapper().create()
    # image = ImageDetailObj2(author='author',
    #                         title='test title',
    #                         url_list={111: 'https://www.google.com.tw',
    #                                   222: 'https://tw.yahoo.com.tw'},
    #                         tag_list={'google': 'https://www.google.com.tw',
    #                                   'yahoo': 'https://tw.yahoo.com'},
    #                         likes=12,
    #                         comments=100,
    #                         date=datetime.datetime.now())
    names = f._fetch_all_user_name()
    # for n in names:
    #     pp(f.read_image_properties(n).val())
    for val in f.read_image_properties(names[0]).val().values():  # type: dict
        # Change the key.
        val['date'] = val.pop('post date')
        if val.get('tag'):
            val['tag_list'] = val.pop('tag')
        if val.get('uri'):
            val['url_list'] = val.pop('uri')
        print(FirebaseWrapper.convert_dict_to_obj('ImageDataObj', val))
