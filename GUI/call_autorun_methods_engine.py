__version__ = ''
__author__ = 'Patryk Bajgot'

from Engines.id_compare_engine import IDCompare
from Engines.reading_file_engine import ReadEngineID, WriteToFile, ReadJsonDirectoryFiles
from Engines.json_id_engine import JsonToID
from Engines.link_extractor_engine import ExtractLinksToNewFile
from Engines.prepare_engine import PrepareFolder


class FirstRunAutorun:

    def __init__(self, prepare_readme: bool = False):
        self._prepare_readme = prepare_readme

    def autorun(self):
        """
        Startup func.
        :return: Nothing
        """
        try:
            PrepareFolder()
            create_files = WriteToFile()
            create_files.create_basic_files(self._prepare_readme)
            return True
        except Exception as e:
            raise Exception(e)


class CompareAutorun:

    found_targets = []
    _base_list = []
    _list_to_compare = []

    def __init__(self):
        self.reading = ReadEngineID()

    def compare_to_base(self) -> bool:
        """
        Startup func to compare data to base list.
        :return: True if all proces is correct, False if not
        """
        self._get_lists()
        return self._run_both_methods(self._base_list, self._list_to_compare)

    def base_to_compare(self) -> bool:
        """
        Startup func to compare base list to data.
        :return: True if all proces is correct, False if not
        """
        self._get_lists()
        return self._run_both_methods(self._list_to_compare, self._base_list)

    def return_found_targets(self):
        return self.found_targets

    def _get_lists(self):
        """
        Loads data to class variable from files.
        :return: Nothing
        """
        self._base_list = self.reading.read_check_list()
        self._list_to_compare = self.reading.read_compare_list()

    def _run_both_methods(self, base_list: list, list_to_compare: list) -> bool:
        """
        Calls all methods to compare given lists
        :param base_list: target to compare
        :param list_to_compare: data to compare
        :return: True if all process is done, False if there is any problem
        """
        try:
            compare_skip = IDCompare(base_list, list_to_compare)
            compare_no_skip = IDCompare(base_list, list_to_compare, False)
            compare_skip.autorun()
            compare_no_skip.autorun()
            self._collect_found_targets_int(
                compare_skip.return_int_not_found(),
                compare_skip.return_int_duplicates(),
                compare_no_skip.return_int_duplicates()
            )
            return True
        except:
            return False

    def _collect_found_targets_int(self, not_found: int, duplicates_skip: int, duplicates_no_skip: int):
        """
        Fill up class variable.
        :param not_found: number of not found ids
        :param duplicates_skip: number of duplicates ids
        :param duplicates_no_skip: number of all duplicates
        :return: Nothing
        """
        self.found_targets = [not_found, duplicates_skip, duplicates_no_skip]


class ExtractIDAutorun:

    _found_json_targets = 0
    _found_links_targets = 0
    _json_file_list = []
    _links_file_list = []

    def __init__(self):
        self.json_reading = ReadJsonDirectoryFiles()
        self.links_reading = ReadEngineID()

    def convert_json(self):
        """
        Startup func. Calls all methods to extract IDs form JSON file.
        :return: True if process is done, False if not
        """
        try:
            self._get_json_list()
            json_engine = JsonToID(self._json_file_list)
            json_engine.autorun()
            self._found_json_targets = len(json_engine.return_id())
            return True
        except:
            return False

    def convert_links(self):
        """
        Startup func. Calls all methods to extract IDs form links.
        :return: True if process is done, False if not
        """
        try:
            self._get_links_list()
            links_engine = ExtractLinksToNewFile(self._links_file_list)
            links_engine.autorun()
            self._found_links_targets = links_engine.return_found_targets_int()
            return True
        except:
            return False

    def return_int_found_json_targets(self):
        return self._found_json_targets

    def return_int_found_links_targets(self):
        return self._found_links_targets

    def _get_json_list(self):
        """
        Calls all methods to fill class variable by JSON data.
        :return: Nothing
        """
        self.json_reading.autorun()
        self._json_file_list = self.json_reading.return_json_file_list()

    def _get_links_list(self):
        """
        Calls all methods to fill class variable by links data.
        :return: Nothing
        """
        self._links_file_list = self.links_reading.read_check_list()
