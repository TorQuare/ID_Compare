__version__ = ''
__author__ = 'Patryk Bajgot'

import os
from Engines.prepare_engine import EnumNames, EnumPath, ExtensionBuilder


class WriteToFile:

    def __init__(self):
        self.to_compare_full_filename = ExtensionBuilder.return_txt(EnumNames.TO_COMPARE_FILENAME)
        self.check_list_full_filename = ExtensionBuilder.return_txt(EnumNames.CHECK_LIST_FILENAME)
        self.readme_full_filename = ExtensionBuilder.return_readme(EnumNames.README_FILENAME)

    def create_basic_files(self, create_readme: bool = False):
        """
        Creates necessary empty files.
        :param create_readme: set to True if README.MD should be created
        :return: Nothing
        """
        creation_list = [self.to_compare_full_filename, self.check_list_full_filename]
        if create_readme:
            creation_list.append(self.readme_full_filename)
        for data in creation_list:
            file = open(data, 'w')
            file.close()

    @staticmethod
    def to_file(filename: str, data: list):
        """
        Saves given data into given file.
        :param filename: target filename
        :param data: data to save
        :return: Nothing
        """
        index = 0
        with open(filename, 'w') as file:
            for record in data:
                if index == len(data) - 1:
                    file.write(str(record))
                else:
                    file.write(str(record) + ', ')
                index += 1
            file.write('\n\n\nList:\n')
            for record in data:
                file.write(str(record) + '\n')


class ReadEngineID(WriteToFile):

    def read_compare_list(self) -> list:
        """
        Calls method to read data from list_to_compare.txt.
        :return: list with read data
        """
        return self._read_data(self.to_compare_full_filename)

    def read_check_list(self) -> list:
        """
        Calls method to read data from list_to_check.txt.
        :return: list with read data
        """
        return self._read_data(self.check_list_full_filename)

    def _check_reading_method(self, filename: str) -> list:
        """
        Selects and calls method to read data from given file/
        :param filename: file to read
        :return: list with read data
        """
        empty_line = self._check_lines(filename)
        if empty_line:
            result = self._read_single_line(filename)
        else:
            result = self._read_multiline(filename)
        return result

    def _read_data(self, filename: str) -> list:
        """
        Calls methods to read data from file.
        :param filename: file to read
        :return: list with read data
        """
        result = self._check_reading_method(filename)
        EmptyFilesChecker(result)
        return result

    def _read_single_line(self, filename: str) -> list:
        """
        Read IDs form single line
        :param filename: file with data
        :return: loaded IDs
        """
        with open(filename, 'r') as file:
            result = file.read().split(', ')
        result = self._last_check(result, False)
        return result

    def _read_multiline(self, filename: str) -> list:
        """
        Read IDs form multiline
        :param filename: file with data
        :return: loaded IDs
        """
        result = []
        with open(filename, 'r') as file:
            for data in file:
                record = self._last_check(data, True)
                if len(record) > 0:
                    result.append(record)
        return result

    @staticmethod
    def _last_check(data, single_data_bool: bool):
        """
        Converts given data to data without whitespace.
        :param data: list or string with loaded record/s
        :param single_data_bool: True if there is only one ID in given data.
        :return:
        """
        if single_data_bool:
            last_index = data
        else:
            last_index = data[len(data) - 1]
        temp_data = last_index.split('\n')
        if single_data_bool:
            data = temp_data[0]
        else:
            data.remove(last_index)
            data.append(temp_data[0])
        return data

    @staticmethod
    def _check_lines(filename: str) -> bool:
        """
        Check if first lines are empty.
        :param filename: file to check
        :return: True if there are empty lines, False if not
        """
        with open(filename, 'r') as file:
            for iterator in range(5):
                line = file.readline()
                if iterator > 0:
                    if len(line) > 0:
                        return False
        return True


class ReadJsonDirectoryFiles:

    def __init__(self):
        self.json_filename = ''
        self.json_filename_list = []
        self.file_flag = False

    def autorun(self):
        self._check_json_local_dir()
        self._check_file_exists()

    def return_json_file_list(self) -> list:
        """
        Returns found JSON files list.
        :return: list of JSON files or raise exception
        """
        if self.file_flag:
            json_full_filenames_list = []
            for iterator in self.json_filename_list:
                json_full_filenames_list.append(os.path.join(EnumPath.JSON_FOLDER_PATH, iterator))
            return json_full_filenames_list
        else:
            raise Exception('No JSON file in directory')

    def _check_json_local_dir(self):
        """
        Calls methods to collect JSON files from JSON directory.
        :return: Nothing
        """
        dir_list = os.listdir(EnumPath.JSON_FOLDER_PATH)
        self._get_filename(dir_list)

    def _get_filename(self, dir_list: list):
        """
        Found and send to class variable all JSON filenames.
        :param dir_list: filenames from given directory
        :return: Nothing
        """
        for iterator in dir_list:
            try:
                temp_list = iterator.split('.')
                if temp_list[len(temp_list) - 1] == EnumNames.JSON_EXTENSION:
                    self.json_filename_list.append(iterator)
            except:
                continue

    def _check_file_exists(self):
        """
        Checks if any JSON file exists.
        :return: Nothing or raise exception if there is no JSON files
        """
        if len(self.json_filename_list) > 0:
            self.file_flag = True
        else:
            print('No JSON file in directory')
            raise Exception('No JSON file in directory')


class EmptyFilesChecker:

    _empty_line_mark_list = ['', '\n', ' ']

    def __init__(self, data: list):
        if len(data) <= 0:
            self._is_empty()
        else:
            for iterator in self._empty_line_mark_list:
                if data[0] == iterator:
                    self._is_empty()
            self._not_empty()

    @staticmethod
    def _not_empty():
        return True

    @staticmethod
    def _is_empty():
        print('One or more of given lists are empty!')
        raise Exception('One or more of given lists are empty!')
