import sys

import qdarktheme
from PyQt5.QtWidgets import QApplication

from app.qapp import SynonymQtApp
from synonym_data_source import SynonymDataSource

""" 
To install 
----------

pip install PyQt5
pip install pyqtdarktheme
"""

if __name__ == "__main__":
    ds = SynonymDataSource("total_data.csv")
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarktheme.load_stylesheet())
    window = SynonymQtApp()
    window.init(ds, column="objet")
    window.show()
    sys.exit(app.exec_())
