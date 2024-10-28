__version__ = ''
__author__ = 'Patryk Bajgot'


from Engines.prepare_engine import EnumPath
from Engines.reading_file_engine import WriteToFile
from Engines.link_extractor_engine import ConvertToIDs


class IDCompare:

    _duplicates_int = 0
    _not_found_int = 0

    def __init__(self, base_list: list, list_to_compare: list, skip_first_found_value: bool = True):
        self.write_file_obj = WriteToFile()
        self._base_list = base_list
        self._list_to_compare = list_to_compare
        self._skip_first_found_value = skip_first_found_value

    def autorun(self):
        """
        Startup func.
        :return: Nothing
        """
        base_list = self._call_conversion_class(self._base_list)
        list_to_compare = self._call_conversion_class(self._list_to_compare)
        duplicates = self._start_compare(base_list, list_to_compare, self._skip_first_found_value)
        not_found = self._not_found(base_list, list_to_compare)
        self._duplicates_int = len(duplicates)
        self._not_found_int = len(not_found)
        self._to_file(duplicates, self._skip_first_found_value, True)
        self._to_file(not_found, False, False)

    def return_int_duplicates(self):
        return self._duplicates_int

    def return_int_not_found(self):
        return self._not_found_int

    @staticmethod
    def _call_conversion_class(data: list) -> list:
        """
        Creates new obj and start convert data.
        :param data: given data to convert
        :return: converted data
        """
        convert_obj = ConvertToIDs(data)
        convert_obj.start_conversion()
        result = convert_obj.return_ids_list()
        del convert_obj
        return result

    def _start_compare(self, base_list: list, list_to_compare: list, skip_duplicates: bool) -> list:
        """
        Compare given lists.
        :param base_list: check list
        :param list_to_compare: list with searching values
        :param skip_duplicates: used for select of saving data
        :return: compare result
        """
        result = []
        for iterator in base_list:
            if self._second_compare_iteration(result, iterator, list_to_compare, skip_duplicates):
                result.append(iterator)
        return result

    def _second_compare_iteration(
            self,
            duplicates_found: list,
            data: str,
            base_list: list,
            skip_duplicates: bool
    ) -> bool:
        """
        Checks if given data should be added to duplicates list.
        :param duplicates_found: actually found duplicates
        :param data: given data
        :param base_list: list with searching values
        :param skip_duplicates: used for select of saving data
        :return: True if data should be added, False if not
        """
        for iterator in base_list:
            if self._add_or_decline_string(duplicates_found, data, iterator, skip_duplicates):
                return True
        return False

    def _add_or_decline_string(
            self,
            duplicates_found: list,
            data: str,
            compare_data: str,
            skip_duplicates: bool
    ) -> bool:
        """
        Checking that given two strings are equal.
        :param duplicates_found: actually found duplicates
        :param data: given data
        :param compare_data: list with searching values
        :param skip_duplicates: used for select of saving data
        :return: True if strings are equal, False if not
        """
        if data == compare_data:
            if not skip_duplicates:
                return True
            if not self._duplicate_into_duplicates(duplicates_found, compare_data):
                return True
        return False

    @staticmethod
    def _duplicate_into_duplicates(duplicates_found: list, compare_data: str) -> bool:
        """
        Checking that given data are in duplicates list.
        :param duplicates_found: duplicates list
        :param compare_data: data to check
        :return: True if data is in list, False if not
        """
        for iterator in duplicates_found:
            if compare_data == iterator:
                return True
        return False

    def _not_found(self, base_list: list, list_to_compare: list) -> list:
        """
        Checks which IDs are not in given list.
        :param base_list: check list
        :param list_to_compare: list to compare
        :return: list with not found IDs
        """
        result = []
        for iterator in list_to_compare:
            found_flag = False
            for compare_iterator in base_list:
                if iterator == compare_iterator:
                    found_flag = True
                    break
            if not found_flag:
                if self._duplicate_into_duplicates(result, iterator):
                    result.append(iterator)
        return result

    def _to_file(self, data: list, skip_first_found_value: bool, duplicates_bool: bool):
        """
        Saves given data to correct files.
        :param data: data to save
        :param skip_first_found_value: used to select final filename
        :param duplicates_bool: used to select which file will be saved
        :return: Nothing
        """
        if duplicates_bool:
            if skip_first_found_value:
                filename = EnumPath.LIST_OF_DUPLICATES_WITH_SKIP_PATH
            else:
                filename = EnumPath.LIST_OF_DUPLICATES_PATH
        else:
            filename = EnumPath.LIST_OF_NOT_FOUND_PATH
        self.write_file_obj.to_file(filename, data)
