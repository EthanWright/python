"""
Paths
"""
import os

from sys import platform
from protected_constants import ProtectedPathConstants, AccountNames


class PathConstants(ProtectedPathConstants):

    MUSIC = 'Music'
    POST_ROCK = 'to_sort_post_rock'
    PROCESSING = 'z_processing'
    TXT = 'txt'
    NEW_SONGS = 'new_songs'
    NEW_ALBUMS = 'new_albums'
    NEEDS_METADATA = 'new_albums_needs_metadata'
    ORIGINAL_ALBUMS = 'original_albums'
    DUPES = 'dupes'

    PROGRAMMING = 'Programming'
    PYTHON = 'Python'
    FILE_SCRIPTS = 'file_scripts'
    MUSIC_SCRIPTS = 'music_scripts'


class PathConfig(object):
    file_structure = {
        PathConstants.MUSIC: {
            PathConstants.POST_ROCK: {},
            PathConstants.TXT: {},
            PathConstants.PROCESSING: {
                PathConstants.NEW_SONGS: {},
                PathConstants.NEEDS_METADATA: {},
                PathConstants.ORIGINAL_ALBUMS: {},
                PathConstants.NEW_ALBUMS: {},
            },
        },
        PathConstants.PROGRAMMING: {
            PathConstants.PYTHON: {
                PathConstants.FILE_SCRIPTS: {},
                PathConstants.MUSIC_SCRIPTS: {}
            }
        },
        PathConstants.VIDEOS: {},
    }

    linux_path_args = ['/', 'home', AccountNames.LINUX_ACCOUNT_NAME, 'Documents']
    LINUX_HOME_DIR = os.path.join(*linux_path_args)

    windows_path_args = ['C:', 'Users', AccountNames.WINDOWS_ACCOUNT_NAME, 'Documents']
    WINDOWS_HOME_DIR = os.path.join(*windows_path_args)

    # def get_linux_path(self):
    # def get_windows_path(self):


class PathDictionary(object):

    def __init__(self, config):
        self.dirs = {}
        self._parse_config(config, '')

    def get_dir(self, dir_name):
        return self.dirs.get(dir_name, '')

    def _parse_config(self, config, path_so_far):
        for dir_name, sub_config in config.items():
            new_path = os.path.join(path_so_far, dir_name)
            self.dirs[dir_name] = new_path
            self._parse_config(sub_config, new_path)


class PathGen(object):

    def __init__(self, config, root_path=''):
        self.path_dictionary = PathDictionary(config.file_structure)

        if not root_path:
            if platform == 'windows':
                root_path = config.WINDOWS_HOME_DIR
            elif platform == 'linux':
                root_path = config.LINUX_HOME_DIR

        self.root_path = root_path

    def __getattr__(self, attr):
        sub_dir_name = getattr(PathConstants, attr, attr)
        sub_dir = self.path_dictionary.get_dir(sub_dir_name)
        return os.path.join(self.root_path, sub_dir)

    @classmethod
    def gen_path_from_root(cls, root_path=''):
        return cls(root_path=root_path)


Paths = PathGen(PathConfig)


# TODO Delete tests
if __name__ == '__main__':
    p3 = PathGen.gen_path_from_root(root_path='')
    print('root_path.ROOT', p3.ROOT)
    print('root_path.MUSIC', p3.MUSIC)