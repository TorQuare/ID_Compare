__version__ = ''
__author__ = 'Patryk Bajgot'


from Engines.prepare_engine import EnumNames, ExtensionBuilder
from Engines.reading_file_engine import WriteToFile


class ConvertToIDs:

    sort_obj = object

    _keywords = ['HYPERLINK', 'https', 'invalid']
    _lp_list = []
    _hyperlinks_list = []
    _https_list = []
    _invalid_list = []
    _result_list = []

    def __init__(self, data: list):
        self._data_to_convert = data

    def start_conversion(self):
        self._sort_lists()
        self.sort_obj = SortIDsLists(self._lp_list, self._keywords)
        self._run_convert_methods()
        self.sort_obj.autorun()
        self._result_list = self.sort_obj.return_sorted_list()

    def return_ids_list(self):
        return self._result_list

    def _run_convert_methods(self):
        self._convert_hyperlinks()
        self._convert_links()
        self._check_invalid_len()

    def _sort_lists(self):
        for iterator in self._data_to_convert:
            if self._search_hyperlinks_keyword(iterator):
                self._lp_list.append(self._keywords[0])
                continue
            elif self._search_link_keyword(iterator):
                self._lp_list.append(self._keywords[1])
                continue
            else:
                self._invalid_list.append(iterator)
                self._lp_list.append(self._keywords[2])

    def _search_hyperlinks_keyword(self, data: str) -> bool:
        """
        Checks if given data should be added to hyperlink list.
        :param data: data to check
        :return: True if data should be added, False if not
        """
        keyword = self._keywords[0]
        if self._search_via_keyword(keyword, data):
            self._hyperlinks_list.append(data)
            return True
        return False

    def _convert_hyperlinks(self):
        """
        Calls all methods necessary to convert hyperlink into IDs.
        :return: Nothing
        """
        if len(self._hyperlinks_list) > 0:
            convert_obj = ConvertHyperlinksToIDs(self._hyperlinks_list)
            convert_obj.start_convert()
            self._hyperlinks_list = convert_obj.return_result()
            self.sort_obj.add_to_item_list(self._hyperlinks_list)
        else:
            self._insert_empty_to_sort()

    def _search_link_keyword(self, data: str) -> bool:
        """
        Checks if given data should be added to https list.
        :param data: data to check
        :return: True if data should be added, False if not
        """
        keyword = self._keywords[1]
        if self._search_via_keyword(keyword, data):
            self._https_list.append(data)
            return True
        return False

    def _convert_links(self):
        """
        Calls all methods necessary to convert link into IDs.
        :return: Nothing
        """
        if len(self._https_list) > 0:
            convert_obj = ConvertLinkToIDs(self._https_list)
            convert_obj.start_convert()
            self._https_list = convert_obj.return_result()
            self.sort_obj.add_to_item_list(self._https_list)
        else:
            self._insert_empty_to_sort()

    def _insert_empty_to_sort(self):
        """
        Adds empty value into sort_obj class variable.
        :return: Nothing
        """
        empty_value = 0
        self.sort_obj.add_to_item_list(empty_value)

    def _search_via_keyword(self, keyword: str, data: str) -> bool:
        """
        Checks if given keyword exists in given data.
        :param keyword: given keyword
        :param data: given data to check
        :return: True if keyword exists in data, False if not
        """
        for index in range(len(data)):
            if index + len(keyword) > len(data):
                break
            temp_list = self._return_temp_string_to_compare(index, keyword, data)
            if self._check_keyword_with_given_string(keyword, temp_list):
                return True
        return False

    @staticmethod
    def _return_temp_string_to_compare(current_index: int, keyword: str, data: str) -> str:
        """
        Converts given hyperlink / link into simple string at length of given keyword.
        :param current_index: current index
        :param keyword: current keyword
        :param data: data to search keyword
        :return: converted string
        """
        found_data = ''
        temp_list = []
        for inner_index in range(len(keyword)):
            temp_list.append(data[current_index + inner_index])
        return found_data.join(temp_list)

    @staticmethod
    def _check_keyword_with_given_string(keyword: str, data: str) -> bool:
        """
        Compare given data with keyword.
        :param keyword: searching keyword
        :param data: given data
        :return: True if keyword equals data, False if not
        """
        if keyword == data:
            return True
        return False

    def _check_invalid_len(self):
        """
        Checks if invalid list is empty, and add items to sort_obj variable.
        :return: Nothing
        """
        if len(self._invalid_list) > 0:
            self.sort_obj.add_to_item_list(self._invalid_list)
        else:
            self._insert_empty_to_sort()


class SortIDsLists:

    _item_list = []
    _result_list = []
    _indexes_list = []

    def __init__(self, lp_list: list, keywords: list):
        self._lp_list = lp_list
        self._keywords = keywords

    def add_to_item_list(self, data):
        """
        Appends items list by given data.
        :param data: data to expand items list
        :return: Nothing
        """
        self._item_list.append(data)

    def autorun(self):
        """
        Startup func.
        :return: Nothing
        """
        self._transfer_keyword_to_index()
        self._create_indexes_list()
        self._sort_via_keyword_index()

    def return_sorted_list(self):
        return self._result_list

    def _sort_via_keyword_index(self):
        """
        Sorts data via keyword correlated to item.
        :return: Nothing
        """
        for index in self._lp_list:
            self._result_list.append(self._item_list[index][self._indexes_list[index]])
            self._indexes_list[index] += 1

    def _create_indexes_list(self):
        """
        Expands indexes lista according to len of item_list in 1-D.
        :return: Nothing
        """
        for iterator in range(len(self._keywords)):
            self._indexes_list.append(0)

    def _transfer_keyword_to_index(self):
        """
        Transfers strings form lp_list into indexes of keyword lists.
        :return: Nothing
        """
        temp_list = []
        for iterator in self._lp_list:
            temp_list.append(self._compare_lp_to_keyword(iterator))
        self._lp_list = temp_list

    def _compare_lp_to_keyword(self, lp: str) -> int:
        """
        Compares given lp with keywords.
        :param lp: given lp
        :return: index of lp position in keyword list
        """
        for index in range(len(self._keywords)):
            if lp == self._keywords[index]:
                return index


class ConvertLinkToIDs:

    _mark = '/'
    _result_list = []

    def __init__(self, data: list):
        self._data = data

    def start_convert(self):
        """
        Startup func.
        :return: Nothing
        """
        self._result_list = self._split_link_into_id()

    def return_result(self):
        return self._result_list

    def _split_link_into_id(self) -> list:
        """
        Converts links into IDs by split data.
        :return: converted data
        """
        result = []
        for iterator in self._data:
            temp_list = iterator.split(self._mark)
            result.append(self._check_possible_of_convert_to_int(temp_list[len(temp_list) - 1]))
        return result

    @staticmethod
    def _check_possible_of_convert_to_int(data: str) -> str:
        """
        Checks if given data can be converted into int and returns data.
        :param data: given data to check
        :return: checked data
        """
        result = ''
        temp_list = []
        for iterator in data:
            try:
                temp_list.append(str(int(iterator)))
                continue
            except:
                continue
        return result.join(temp_list)


class ConvertHyperlinksToIDs:

    _mark = '"'
    _result_list = []

    def __init__(self, data: list):
        self._data = data

    def start_convert(self):
        """
        Startup func.
        :return: Nothing
        """
        to_convert = self._split_hyperlinks_into_link()
        convert_obj = ConvertLinkToIDs(to_convert)
        convert_obj.start_convert()
        self._result_list = convert_obj.return_result()

    def return_result(self):
        return self._result_list

    def _split_hyperlinks_into_link(self) -> list:
        """
        Converts hyperlinks into links by split data.
        :return: converted data
        """
        result = []
        for iterator in self._data:
            temp_list = iterator.split(self._mark)
            result.append(temp_list[1])
        return result


class ExtractLinksToNewFile:

    _result = []
    _found_targets = 0

    def __init__(self, data: list):
        self._filename = ExtensionBuilder.return_txt(EnumNames.LIST_OF_ID_FROM_LINKS_FILENAME)
        self._data = data

    def autorun(self):
        data = self._call_convert_class(self._data)
        WriteToFile.to_file(self._filename, data)
        self._found_targets = len(data)

    def return_found_targets_int(self):
        return self._found_targets

    @staticmethod
    def _call_convert_class(data: list) -> list:
        """
        Creates new obj and start convert data.
        :param data: given data to convert
        :return: converted data
        """
        convert_obj = ConvertToIDs(data)
        convert_obj.start_conversion()
        return convert_obj.return_ids_list()
