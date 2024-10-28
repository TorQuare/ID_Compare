__version__ = ''
__author__ = 'Patryk Bajgot'

from Engines.link_extractor_engine import ExtractLinksToNewFile
from Engines.reading_file_engine import ReadEngineID
from Engines.prepare_engine import FinishConsole

try:
    reading = ReadEngineID()
    extract = ExtractLinksToNewFile(reading.read_check_list())
    extract.autorun()
    FinishConsole(False)
except Exception as e:
    print(e)
    FinishConsole(True)
