__version__ = ''
__author__ = 'Patryk Bajgot'

from GUI.main_window import MainWindowGUI

window = MainWindowGUI()
window.read_window_config()
window.main_window()
