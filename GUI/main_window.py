__version__ = ''
__author__ = 'Patryk Bajgot'


import os
import subprocess
from tkinter import *
from GUI.call_autorun_methods_engine import *
from Engines.prepare_engine import EnumPath, EnumNames
from Engines.config_reader import WindowConfigReader


class MainWindowConfig:

    _geometry = ''
    _position = ''
    _title = ''
    _status_string = 'Wait'
    _quick_compare_window_on = False
    _window_height = 0
    _window_width = 0
    _links_int = 0
    _not_found_int = 0
    _duplicates_skip_int = 0
    _duplicates_no_skip_int = 0
    _empty_list_for_targets_found = [0, 0, 0]
    _found_targets_list_int = []

    def __init__(self):
        self.config = WindowConfigReader()

    def read_window_config(self):
        """
        Loads window configuration from config file.
        :return: Nothing
        """
        self.config.read_config()
        self._geometry = self.config.return_window_geometry()
        self._title = self.config.return_window_title()
        self._position = self.config.return_window_position()
        self._window_height = self.config.return_window_height()
        self._window_width = self.config.return_window_width()


class FoundTargetsLabelInMainWindow(MainWindowConfig):

    def split_target_list(self, data: list):
        """
        Calls all methods to change class variables.
        :param data: given data
        :return: Nothing
        """
        self._not_found_int_update(data[0])
        self._duplicates_skip_int_update(data[1])
        self._duplicates_no_skip_int_update(data[2])

    def found_links_int_update(self, value: int):
        """
        Change class variable into given value.
        :param value: given value
        :return: Nothing
        """
        self._links_int = value

    def _not_found_int_update(self, value: int):
        """
        Change class variable into given value.
        :param value: given value
        :return: Nothing
        """
        self._not_found_int = value

    def _duplicates_skip_int_update(self, value: int):
        """
        Change class variable into given value.
        :param value: given value
        :return: Nothing
        """
        self._duplicates_skip_int = value

    def _duplicates_no_skip_int_update(self, value: int):
        """
        Change class variable into given value.
        :param value: given value
        :return: Nothing
        """
        self._duplicates_no_skip_int = value


class StatusLabelInMainWindow(MainWindowConfig):

    def select_correct_status(self, result: bool):
        """
        Calls methods to set status label.
        :param result: selects which status should be set
        :return: Nothing
        """
        if result:
            self._status_done()
        else:
            self._status_failed()

    def status_unable_to_open_file(self):
        """
        Sets status label
        :return: Nothing
        """
        self._status_string = 'Unable to open file'

    def _status_done(self):
        """
        Sets status label
        :return: Nothing
        """
        self._status_string = "Done"

    def _status_failed(self):
        """
        Sets status label
        :return: Nothing
        """
        self._status_string = "Failed"


class AutorunEngines(MainWindowConfig):

    label_engine = StatusLabelInMainWindow()

    def change_status_to_open_file_exception(self):
        """
        Changes status label to error value.
        :return: Nothing
        """
        self.label_engine.status_unable_to_open_file()

    def first_run(self):
        """
        Creates class obj and calls first run func.
        :return: Nothing
        """
        first_run_obj = AutorunFirstRun()
        self._modify_labels_in_window(first_run_obj.run(), self._empty_list_for_targets_found)

    def compare_to_base(self):
        """
        Creates class obj and calls compare func.
        :return: Nothing
        """
        compare_obj = AutorunCompare()
        self._modify_labels_in_window(compare_obj.compare_to_base(), compare_obj.return_found_targets())

    def base_to_compare(self):
        """
        Creates class obj and calls compare func.
        :return: Nothing
        """
        compare_obj = AutorunCompare()
        self._modify_labels_in_window(compare_obj.base_to_compare(), compare_obj.return_found_targets())

    def extract_json(self):
        """
        Creates class obj and calls extract func.
        :return: Nothing
        """
        extract = AutorunExtractID()
        self._modify_labels_in_window(extract.extract_json(), extract.return_json_found_targets_int(), False)

    def extract_links(self):
        """
        Creates class obj and calls extract func.
        :return: Nothing
        """
        extract = AutorunExtractID()
        self._modify_labels_in_window(extract.extract_links(), extract.return_links_found_targets_int(), False)

    def _modify_labels_in_window(self, result: bool, targets, modify_duplicates: bool = True):
        """
        Calls func to change status label for selected by result settings.
        :param result: True if status should be set to 'Done', False if not
        :param targets: list or int with found IDs
        :param modify_duplicates: selects which label should be changed
        :return: Nothing
        """
        self.label_engine.select_correct_status(result)
        if result:
            targets_engine = FoundTargetsLabelInMainWindow()
            if modify_duplicates:
                targets_engine.split_target_list(targets)
            else:
                targets_engine.found_links_int_update(targets)


class AutorunFirstRun:

    def __init__(self):
        self.prepare_obj = FirstRunAutorun()

    def run(self):
        """
        Startup func.
        :return: True if everything is ok or exception on fail.
        """
        return self.prepare_obj.autorun()


class OpenFiles:

    def __init__(self):
        app_name = 'notepad.exe '
        self.base_list_command = app_name + os.path.join(EnumPath.LOCAL_PATH, EnumNames.CHECK_LIST_FILENAME)
        self.list_to_compare_command = app_name + os.path.join(EnumPath.LOCAL_PATH, EnumNames.TO_COMPARE_FILENAME)
        self.duplicates_skip_command = app_name + os.path.join(
            EnumPath.LOCAL_PATH,
            EnumNames.LIST_OF_DUPLICATES_WITH_SKIP_FILENAME
        )
        self.duplicates_command = app_name + os.path.join(EnumPath.LOCAL_PATH, EnumNames.LIST_OF_DUPLICATES_FILENAME)
        self.not_found_command = app_name + os.path.join(EnumPath.LOCAL_PATH, EnumNames.LIST_OF_NOT_FOUND_FILENAME)
        self.ids_json_command = app_name + os.path.join(EnumPath.LOCAL_PATH, EnumNames.LIST_OF_ID_FROM_JSON_FILENAME)
        self.ids_links_command = app_name + os.path.join(EnumPath.LOCAL_PATH, EnumNames.LIST_OF_ID_FROM_LINKS_FILENAME)

    def open_base_list(self):
        return self._open_file(self.base_list_command)

    def open_list_to_compare(self):
        return self._open_file(self.list_to_compare_command)

    def open_duplicates_skip(self):
        return self._open_file(self.duplicates_skip_command)

    def open_duplicates(self):
        return self._open_file(self.duplicates_command)

    def open_not_found(self):
        return self._open_file(self.not_found_command)

    def open_ids_json(self):
        return self._open_file(self.ids_json_command)

    def open_ids_links(self):
        return self._open_file(self.ids_links_command)

    def open_directory(self):
        return self._open_file('explorer.exe ' + EnumPath.LOCAL_PATH)

    @staticmethod
    def _open_file(command: str, shell_on=False):
        """
        Tries to run given command.
        :param command: command
        :param shell_on: shell setting
        :return: True if command works correctly, False if not
        """
        try:
            subprocess.Popen(command, shell=shell_on)
            return True
        except:
            return False


class AutorunExtractID:

    def __init__(self):
        self.extract = ExtractIDAutorun()

    def extract_json(self):
        return self.extract.convert_json()

    def return_json_found_targets_int(self):
        return self.extract.return_int_found_json_targets()

    def extract_links(self):
        return self.extract.convert_links()

    def return_links_found_targets_int(self):
        return self.extract.return_int_found_links_targets()


class AutorunCompare:

    def __init__(self):
        self.compare = CompareAutorun()

    def compare_to_base(self):
        return self.compare.compare_to_base()

    def base_to_compare(self):
        return self.compare.base_to_compare()

    def return_found_targets(self):
        return self.compare.return_found_targets()


class MainWindowGUI(MainWindowConfig):

    def main_window(self):

        main_window = Tk()
        main_window.title(self._title)

        if not self._quick_compare_window_on:
            main_window.geometry(self._geometry + self._position)
            main_window.minsize(self._window_height, self._window_height)
            main_window.maxsize(self._window_height, self._window_height)

        def window_compare_to_base(self):
            AutorunEngines.compare_to_base(self)
            change_status_labels(self)
            change_found(self)

        def window_base_to_compare(self):
            AutorunEngines.base_to_compare(self)
            change_status_labels(self)
            change_found(self)

        def window_extract_json(self):
            AutorunEngines.extract_json(self)
            change_status_labels(self)
            change_found(self)

        def window_extract_links(self):
            AutorunEngines.extract_links(self)
            change_status_labels(self)
            change_found(self)

        def window_open_base_list(self):
            open_obj = OpenFiles()
            open_obj.open_base_list()

        def window_open_list_to_compare(self):
            open_obj = OpenFiles()
            open_obj.open_list_to_compare()

        def window_open_duplicates_skip(self):
            open_obj = OpenFiles()
            open_obj.open_duplicates_skip()

        def window_open_duplicates(self):
            open_obj = OpenFiles()
            open_obj.open_duplicates()

        def window_open_not_found(self):
            open_obj = OpenFiles()
            open_obj.open_not_found()

        def window_open_ids_json(self):
            open_obj = OpenFiles()
            open_obj.open_ids_json()

        def window_open_ids_links(self):
            open_obj = OpenFiles()
            open_obj.open_ids_links()

        def window_open_directory(self):
            open_obj = OpenFiles()
            open_obj.open_directory()

        def window_first_run(self):
            AutorunEngines.first_run(self)
            change_status_labels(self)

        def change_status_labels(self):
            status_label.config(text='Status: ' + self._status_string)

        def change_found(self):
            try:
                not_found_label.config(text='Not found: ' + str(self._not_found_int))
                duplicates_label.config(text='Duplicates found: ' + str(self._duplicates_skip_int))
                all_duplicates_label.config(text='All duplicates found: ' + str(self._duplicates_no_skip_int))
            except:
                fail_string = 'Fatal error'
                not_found_label.config(text='Not found: ' + fail_string)
                duplicates_label.config(text='Duplicates found: ' + fail_string)
                all_duplicates_label.config(text='All duplicates found: ' + fail_string)

        def change_found_id(self):
            try:
                found_links_label.config(text='Links found: ' + str(self._links_int))
            except:
                found_links_label.config(text='Links found: Fatal error')


        main_frame = Frame(main_window).pack()

        compare_to_base_btn = Button(main_frame, text='Compare > Base', width=15)
        compare_to_base_btn.place(x=10, y=10)
        compare_to_base_btn.bind('<Button-1>', window_compare_to_base)

        base_to_compare_btn = Button(main_frame, text='Base > Compare', width=15)
        base_to_compare_btn.place(x=10, y=50)
        base_to_compare_btn.bind('<Button-1>', window_base_to_compare)

        get_id_form_json_btn = Button(main_frame, text='IDs from JSON', width=15)
        get_id_form_json_btn.place(x=10, y=90)
        get_id_form_json_btn.bind('<Button-1>', window_extract_json)

        get_id_from_links_btn = Button(main_frame, text='IDs from links', width=15)
        get_id_from_links_btn.place(x=10, y=130)
        get_id_from_links_btn.bind('<Button-1>', window_extract_links)

        show_base_list_btn = Button(main_frame, text='Show base list', width=15)
        show_base_list_btn.place(x=10, y=170)
        show_base_list_btn.bind('<Button-1>', window_open_base_list)

        show_compare_list_btn = Button(main_frame, text='Show compare list', width=15)
        show_compare_list_btn.place(x=165, y=170)
        show_compare_list_btn.bind('<Button-1>', window_open_list_to_compare)

        show_duplicates_skip = Button(main_frame, text='Duplicates', width=13)
        show_duplicates_skip.place(x=10, y=210)
        show_duplicates_skip.bind('<Button-1>', window_open_duplicates_skip)

        show_duplicates_list = Button(main_frame, text='All duplicates', width=13)
        show_duplicates_list.place(x=112, y=210)
        show_duplicates_list.bind('<Button-1>', window_open_duplicates)

        show_not_found_list = Button(main_frame, text='Not Found', width=13)
        show_not_found_list.place(x=213, y=210)
        show_not_found_list.bind('<Button-1>', window_open_not_found)

        show_found_ids_json = Button(main_frame, text='IDs JSON', width=20)
        show_found_ids_json.place(x=10, y=250)
        show_found_ids_json.bind('<Button-1>', window_open_ids_json)

        show_found_ids_links = Button(main_frame, text='IDs links', width=20)
        show_found_ids_links.place(x=165, y=250)
        show_found_ids_links.bind('<Button-1>', window_open_ids_links)

        show_file_explorer_btn = Button(main_frame, text='Show in explorer', width=42)
        show_file_explorer_btn.place(x=10, y=290)
        show_file_explorer_btn.bind('<Button-1>', window_open_directory)

        first_run_btn = Button(main_frame, text='FIRST RUN', width=42, bg='#b6b6b6')
        first_run_btn.place(x=10, y=330)
        first_run_btn.bind('<Button-1>', window_first_run)

        status_label = Label(main_frame, text='Status: ' + self._status_string)
        status_label.place(x=165, y=10)

        not_found_label = Label(main_frame, text='Not found: ' + str(self._not_found_int))
        not_found_label.place(x=165, y=40)

        duplicates_label = Label(main_frame, text='Duplicates found: ' + str(self._duplicates_skip_int))
        duplicates_label.place(x=165, y=70)

        all_duplicates_label = Label(main_frame, text='All duplicates found: ' + str(self._duplicates_no_skip_int))
        all_duplicates_label.place(x=165, y=100)

        found_links_label = Label(main_frame, text='Links found: ' + str(self._links_int))
        found_links_label.place(x=165, y=130)

        main_window.mainloop()
