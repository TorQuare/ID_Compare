__version__ = ''
__author__ = 'Patryk Bajgot'

from Engines.id_compare_engine import IDCompare
from Engines.reading_file_engine import ReadEngineID
from Engines.prepare_engine import FinishConsole

try:
    reading = ReadEngineID()
    base_list = reading.read_check_list()
    list_to_compare = reading.read_compare_list()
    compare_no_skip = IDCompare(base_list, list_to_compare)
    compare_skip = IDCompare(base_list, list_to_compare, False)
    compare_no_skip.autorun()
    compare_skip.autorun()
    FinishConsole(False)
except Exception as e:
    print(e)
    FinishConsole(True)
