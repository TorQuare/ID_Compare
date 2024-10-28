__version__ = ''
__author__ = 'Patryk Bajgot'


from Engines.prepare_engine import EnumNames
from Engines.reading_file_engine import WriteToFile


class JsonToID:

    _id_list = []
    _link_str = '"Link"'

    def __init__(self, filenames_list: list):
        self.write_file_obj = WriteToFile()
        self.target_filename = EnumNames.LIST_OF_ID_FROM_JSON_FILENAME
        self._filenames_list = filenames_list

    def autorun(self):
        """
        Startup func.
        :return: Nothing or raise exception if there is no JSON IDs in given files.
        """
        links_list = self._create_links_list(self._filenames_list)
        if len(links_list) > 0:
            self._id_list = self._convert_to_ids(links_list)
            self._to_file()
        else:
            raise Exception('There is no ID in given JSON file.')

    def return_id(self):
        return self._id_list

    def _create_links_list(self, filenames: list) -> list:
        """
        Converts data from given filenames into links list.
        :param filenames: filenames to collect data
        :return: list with found links
        """
        links_list = []
        for filename in filenames:
            full_file_list = self._read_file(filename)
            links_list.append(self._found_links(full_file_list))
        return self._merge_lists_in_links_list(links_list)

    @staticmethod
    def _convert_to_ids(data: list) -> list:
        """
        Converts given links list into id list
        :param data: given data with links
        :return: list with ids
        """
        result = []
        for iterator in data:
            try:
                temp_list = iterator.split('/')
                temp_int_list = temp_list[len(temp_list) - 1].split('"')
                result.append(temp_int_list[0])
            except Exception as e:
                raise Exception(f'Incorrect link in given file{e}')
        return result

    @staticmethod
    def _read_file(filename: str) -> list:
        """
        Loads data from given file.
        :param filename: filename to read
        :return: list with loaded data
        """
        with open(filename, 'r') as file:
            result = file.read().split(',')
        return result

    def _found_links(self, data: list) -> list:
        """
        Returns list with found links.
        :param data: given data
        :return: list with links
        """
        result = []
        for iterator in data:
            try:
                temp_list = iterator.split(':')
                if temp_list[0] == self._link_str:
                    result.append(iterator)
            except:
                continue
        return result

    @staticmethod
    def _merge_lists_in_links_list(links_list: list) -> list:
        """
        Merge all data from files saved in 3-D lists into one 1-D list and returns those list.
        :param links_list: list of all links found in JSON files
        :return: 1-D list with links
        """
        if len(links_list) > 0:
            result = []
            for iterator in links_list:
                for second_iterator in iterator:
                    result.append(second_iterator)
            return result
        else:
            return links_list

    def _to_file(self):
        """
        Calls method to save file.
        :return: Nothing
        """
        self.write_file_obj.to_file(self.target_filename, self._id_list)
