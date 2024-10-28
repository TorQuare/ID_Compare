__version__ = ''
__author__ = 'Patryk Bajgot'

from enum import Enum
import os
import shutil


class EnumNames:

    # Extensions:
    EXTENSION_MARK = '.'
    JSON_EXTENSION = 'json'
    TXT_EXTENSION = 'txt'
    INI_EXTENSION = 'ini'
    README_EXTENSION = 'md'

    # Dictionary names:
    DUPLICATES_DIR_NAME = 'Duplicates'
    NOT_FOUND_DIR_NAME = 'NotFound'
    JSON_DIR_NAME = 'JSON_Directory'

    # Files names:
    README_FILENAME = 'README'
    WINDOW_CONFIG_FILENAME = 'window_config'
    TO_COMPARE_FILENAME = 'list_to_compare'
    CHECK_LIST_FILENAME = 'base_list'
    LIST_OF_DUPLICATES_FILENAME = 'list_of_duplicates'
    LIST_OF_DUPLICATES_WITH_SKIP_FILENAME = 'list_of_duplicates_with_skip'
    LIST_OF_NOT_FOUND_FILENAME = 'list_of_not_found'
    LIST_OF_ID_FROM_JSON_FILENAME = 'ID_list'
    LIST_OF_ID_FROM_LINKS_FILENAME = 'ID_from_links'


class EnumPath:

    LOCAL_PATH = os.getcwd()
    TXT_EXTENSION = EnumNames.EXTENSION_MARK + EnumNames.TXT_EXTENSION

    # Path to directories:
    DUPLICATES_FOLDER_PATH = os.path.join(LOCAL_PATH, EnumNames.DUPLICATES_DIR_NAME)
    NOT_FOUND_FOLDER_PATH = os.path.join(LOCAL_PATH, EnumNames.NOT_FOUND_DIR_NAME)
    JSON_FOLDER_PATH = os.path.join(LOCAL_PATH, EnumNames.JSON_DIR_NAME)

    # Path to files in directories:
    LIST_OF_DUPLICATES_PATH = os.path.join(
        DUPLICATES_FOLDER_PATH,
        EnumNames.LIST_OF_DUPLICATES_FILENAME + TXT_EXTENSION
    )
    LIST_OF_DUPLICATES_WITH_SKIP_PATH = os.path.join(
        DUPLICATES_FOLDER_PATH,
        EnumNames.LIST_OF_DUPLICATES_WITH_SKIP_FILENAME + TXT_EXTENSION
    )
    LIST_OF_NOT_FOUND_PATH = os.path.join(
        NOT_FOUND_FOLDER_PATH,
        EnumNames.LIST_OF_NOT_FOUND_FILENAME + TXT_EXTENSION
    )
    LIST_OF_ID_FROM_JSON_PATH = os.path.join(
        JSON_FOLDER_PATH,
        EnumNames.LIST_OF_ID_FROM_JSON_FILENAME + TXT_EXTENSION
    )


class ExtensionBuilder:

    @staticmethod
    def return_txt(filename: str) -> str:
        """
        Add extension into given filename
        :param filename: given filename
        :return: given filename with extension
        """
        return str(filename) + EnumNames.EXTENSION_MARK + EnumNames.TXT_EXTENSION

    @staticmethod
    def return_json(filename: str) -> str:
        """
        Add extension into given filename
        :param filename: given filename
        :return: given filename with extension
        """
        return str(filename) + EnumNames.EXTENSION_MARK + EnumNames.JSON_EXTENSION

    @staticmethod
    def return_ini(filename: str) -> str:
        """
        Add extension into given filename
        :param filename: given filename
        :return: given filename with extension
        """
        return str(filename) + EnumNames.EXTENSION_MARK + EnumNames.INI_EXTENSION

    @staticmethod
    def return_readme(filename: str) -> str:
        """
        Add extension into given filename
        :param filename: given filename
        :return: given filename with extension
        """
        return str(filename) + EnumNames.EXTENSION_MARK + EnumNames.README_EXTENSION


class FinishConsole:

    def __init__(self, except_bool: bool):
        if except_bool:
            self._except_message()
        else:
            self._finish_message()

    @staticmethod
    def _except_message():
        """
        Stops console and returns exception message.
        :return: Nothing
        """
        print('Need to debug or invalid value in lists!')
        os.system('pause >NULL')
        return 0

    @staticmethod
    def _finish_message():
        """
        Stops console and returns done message.
        :return: Nothing
        """
        print('Done')
        os.system('pause >NULL')
        return 0


class PrepareFolder:

    def __init__(self):
        self.create_folder(EnumPath.DUPLICATES_FOLDER_PATH)
        self.create_folder(EnumPath.NOT_FOUND_FOLDER_PATH)
        self.create_folder(EnumPath.JSON_FOLDER_PATH)

    @staticmethod
    def create_folder(path: str):
        """
        Creates folder in given path.
        :param path: path to new folder
        :return: Nothing
        """
        try:
            shutil.rmtree(path)
            os.mkdir(path)
        except:
            os.mkdir(path)


class ExistCheckFile:

    @staticmethod
    def check(filename: str) -> bool:
        """
        Tries to open given filename and returns True if file exists.
        :param filename: file to open
        :return: True if file exists, False if not
        """
        try:
            file = open(filename, 'r')
            file.close()
            return True
        except:
            return False
