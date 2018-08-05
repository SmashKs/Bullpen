from pprint import pprint as pp

from datapool.firebase.FirebaseWrapper import FirebaseWrapper


class FetcherImageVer2:
    def __init__(self, firebase_wrapper):
        self.__wrapper = firebase_wrapper  # type: FirebaseWrapper
        self.__users = {}  # type: dict

    def get(self):
        name_list = self.__wrapper.fetch_all_user_name()

        for name in name_list:
            albums = []
            for val in self.__wrapper.read_image_properties(name).val().values():
                self._fix_key(val)
                albums.append(FirebaseWrapper.convert_dict_to_obj('ImageDataObj', val))

            self.__users[name] = albums

        return self.__users

    def _fix_key(self, data):
        # Change the key.
        data['date'] = data.pop('post date')

        if data.get('tag'):
            data['tag_list'] = data.pop('tag')
        if data.get('uri'):
            data['url_list'] = data.pop('uri')


if __name__ == '__main__':
    wrapper = FirebaseWrapper().create()
    fetcher = FetcherImageVer2(wrapper).get()
    pp(fetcher)
