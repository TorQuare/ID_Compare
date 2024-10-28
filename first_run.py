__version__ = ''
__author__ = 'Patryk Bajgot'

from Engines.reading_file_engine import WriteToFile
from Engines.prepare_engine import PrepareFolder, FinishConsole
from Engines.config_reader import WindowConfig

try:
    create_window_config = WindowConfig()
    create_window_config.create_basic_window_config()
    folder_creation = PrepareFolder()
    create_files = WriteToFile()
    create_files.create_basic_files()
    FinishConsole(False)
except Exception as e:
    print(e)
    FinishConsole(True)
