__version__ = '1.0'
__author__ = 'Patryk Bajgot'


import configparser

from Engines.prepare_engine import EnumNames, ExtensionBuilder, ExistCheckFile


class WindowConfig:

    add_extension = ExtensionBuilder()
    window_config_full_name = add_extension.return_ini(EnumNames.WINDOW_CONFIG_FILENAME)

    window_section_name = 'main_window'
    main_window_config = [
        ['title', 'ID_Compare'],
        ['geometry', '370x370'],
        ['position', '+300+300']
    ]

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.exist_check = ExistCheckFile()

    def create_basic_window_config(self):
        #TODO: poprawić na dict
        self.config.add_section(self.window_section_name)
        for iterator in range(len(self.main_window_config)):
            self.config.set(
                self.window_section_name,
                self.main_window_config[iterator][0],
                self.main_window_config[iterator][1]
            )
        window_config_file = open(self.window_config_full_name, 'w')
        self.config.write(window_config_file)
        window_config_file.close()


class WindowConfigReader(WindowConfig):

    _read = ''
    _title_setting = []
    _geometry_setting = []
    _position_setting = []

    def read_config(self):
        """
        Checks if config file exists. Loads data into class variables.
        :return: Nothing
        """
        self._check_config_exists()
        self._read = self.config.read(self.window_config_full_name)
        self._title_setting = self.main_window_config[0]
        self._geometry_setting = self.main_window_config[1]
        self._position_setting = self.main_window_config[2]

    def return_window_title(self) -> str:
        return self.config.get(self.window_section_name, self._title_setting[0])

    def return_window_geometry(self) -> str:
        return self.config.get(self.window_section_name, self._geometry_setting[0])

    def return_window_position(self) -> str:
        return self.config.get(self.window_section_name, self._position_setting[0])

    def return_window_height(self) -> int:
        result = self._split_geometry_settings()
        return int(result[0])

    def return_window_width(self) -> int:
        result = self._split_geometry_settings()
        return int(result[1])

    def _check_config_exists(self):
        """
        Calls create basic config if config does not exist.
        :return: Nothing
        """
        if not self.exist_check.check(self.window_config_full_name):
            self.create_basic_window_config()

    def _split_geometry_settings(self) -> list:
        """
        Splits geometry data to exclude height and width.
        :return: list with geometry data
        """
        return self.config.get(self.window_section_name, self._geometry_setting[0]).split('x')
