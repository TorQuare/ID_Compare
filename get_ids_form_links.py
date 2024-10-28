__version__ = ''
__author__ = 'Patryk Bajgot'

from Engines.json_id_engine import JsonToID
from Engines.reading_file_engine import ReadJsonDirectoryFiles
from Engines.prepare_engine import FinishConsole

try:
    json_dir_obj = ReadJsonDirectoryFiles()
    json_dir_obj.autorun()
    json_engine = JsonToID(json_dir_obj.return_json_file_list())
    json_engine.autorun()
    FinishConsole(False)
except Exception as e:
    print(e)
    FinishConsole(True)
