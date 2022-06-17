from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from app.utils import horizontal_layout, scroll_area, label
from synonym_data_source import SynonymDataSource


class SynonymQtApp(QMainWindow):
    class Entry:
        def __init__(self, column: str, word: str, tolerance: float, key: str):
            self.column = column
            self.word = word
            self.tolerance = tolerance
            self.key = key

    def __init__(self):
        super().__init__()
        self.width = 800
        self.height = 800
        self.datasource = None
        self.dictionary_keys: list = []
        self.checkboxes: dict = {}
        self.selected_dictionary: set | None = None
        self.dictionary_widgets: dict = {}
        self.grid = None
        self.setFixedSize(self.width, self.height)
        self.setWindowTitle("Syn Nonym")

    def init(self, datasource: SynonymDataSource = None, column: str = None):

        if datasource is None:
            self.__open_data_source_dialog()

        self.datasource = datasource
        self.dictionary_keys = []
        self.checkboxes = {}
        self.selected_dictionary = None
        self.dictionary_widgets = {}

        self.grid = QGridLayout()
        self.grid.setAlignment(Qt.AlignTop)
        w = QWidget()
        w.setStyleSheet("font-size: 20px")
        w.setLayout(self.grid)
        self.setCentralWidget(w)

        self.__init_search_configuration(column=column)
        self.__init_dictionary_layout()
        self.__init_export_layout()

    def __open_data_source_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(QFileDialog(), "Choose data source", "",
                                                   "CSV files (*.csv)")
        if file_name:
            if self.datasource is None or self.datasource.file_name != file_name:
                self.init(SynonymDataSource(file_name))

    def __init_search_configuration(self, column: str = None):
        data_source_name = QLineEdit()
        data_source_name.setText(self.datasource.file_name if self.datasource is not None else "")
        data_source_name.setEnabled(False)
        data_source_button = QPushButton("...")
        data_source_button.clicked.connect(lambda state: self.__open_data_source_dialog())

        self.grid.addLayout(horizontal_layout((label("Data source", width=170), 0),
                                              (data_source_name, 1),
                                              (data_source_button, 0)), 0, 0, 1, 2)

        column_combobox = QComboBox()
        if self.datasource is not None:
            column_combobox.addItems(self.datasource.columns)
            if column is not None and column in self.datasource.columns:
                column_combobox.setCurrentText(column)
        word_field = QLineEdit()
        self.grid.addLayout(horizontal_layout((label("Column", width=170), 0), (column_combobox, 1)), 1, 0, 1, 2)
        self.grid.addLayout(horizontal_layout((label("Word", width=170), 0), (word_field, 1)), 2, 0, 1, 2)

        tolerance_value = label("Tolerance (5)", width=170)
        tolerance_slider = QSlider(Qt.Horizontal)
        tolerance_slider.setMinimum(0)
        tolerance_slider.setMaximum(10)
        tolerance_slider.setValue(5)
        tolerance_slider.valueChanged.connect(
            lambda value: tolerance_value.setText("Tolerance (" + str(value) + ")"))
        self.grid.addLayout(
            horizontal_layout((tolerance_value, 0), (tolerance_slider, 1)),
            3, 0, 1, 2)

        search_button = QPushButton("Search")
        search_button.setFixedHeight(50)
        search_button.clicked.connect(
            lambda state, column=column_combobox, word_field=word_field, tolerance=tolerance_slider:
            self.__search_synonyms(column, word_field, tolerance))
        search_button.setEnabled(False)
        word_field.textChanged[str].connect(
            lambda: search_button.setEnabled(word_field.text() != "" and self.datasource is not None))

        self.grid.addWidget(search_button, 4, 0, 1, 2)

    def __init_dictionary_layout(self):
        self.dictionary_layout = QVBoxLayout()
        self.dictionary_layout.setAlignment(Qt.AlignTop)
        self.grid.addWidget(scroll_area(self.dictionary_layout, width=int(0.4 * self.width)), 5, 0)

        self.synonym_layout = QVBoxLayout()
        self.synonym_layout.setAlignment(Qt.AlignTop)
        self.synonym_layout.setSpacing(10)
        self.grid.addWidget(scroll_area(self.synonym_layout), 5, 1)

    def __init_export_layout(self):
        self.export_button = QPushButton("Export")
        self.export_button.setFixedHeight(50)
        self.export_button.clicked.connect(self.__choose_export_file)
        self.export_button.setEnabled(False)
        self.grid.addWidget(self.export_button, 6, 0, 1, 2)

    def __choose_export_file(self):
        file_name, _ = QFileDialog.getSaveFileName(QFileDialog(), "Choose file to export", "", "CSV files (*.csv)")
        if file_name:
            tmp = {entry.key: list(filter(lambda cb: cb.isChecked(), self.checkboxes[entry.key]))
                   for entry in self.dictionary_keys}
            self.datasource.export(file_name, [(entry.column, entry.word, entry.tolerance,
                                                list(map(lambda cb: cb.text(), tmp[entry.key])))
                                               for entry in
                                               self.dictionary_keys])

    def __search_synonyms(self, column: QComboBox, word_field: QLineEdit, tolerance: QSlider):
        self.__add_dictionary(column.currentText(), word_field.text(), tolerance.value())

    def __add_dictionary(self, column: str, word: str, tolerance: float):
        synonyms = self.datasource.search_synonyms(column, word, tolerance)
        key = self.__key(column, word, tolerance)
        if key in self.checkboxes:
            self.__update_dictionary(key, synonyms)
        else:
            entry = self.Entry(column, word, tolerance, key)
            self.dictionary_keys.append(entry)
            self.checkboxes[key] = [self.__check_box(s) for s in synonyms]
            w = QWidget()
            h = QHBoxLayout()
            w.setFixedHeight(50)
            w.setObjectName("" + key)
            h.addWidget(QLabel("[" + column + "] " + word + " (" + str(tolerance) + ")"), stretch=1)
            remove_button = QPushButton("X")
            remove_button.clicked.connect(lambda state: self.__remove_dictionary(entry))
            remove_button.setStyleSheet("background: red; color: white")
            h.addWidget(remove_button)
            w.setLayout(h)
            self.dictionary_layout.addWidget(w)
            self.dictionary_widgets[key] = w
            w.mouseReleaseEvent = lambda event, key=key: self.__select_dictionary(key)
            for cb in self.checkboxes[key]:
                self.synonym_layout.addWidget(cb)

            self.export_button.setEnabled(True)

        self.__select_dictionary(key)

    def __update_dictionary(self, key, synonyms):
        to_remove = list(filter(lambda cb: cb.text() not in synonyms, self.checkboxes[key]))
        current_synonyms = list(map(lambda cb: cb.text(), self.checkboxes[key]))
        to_add = list(filter(lambda syn: syn not in current_synonyms, synonyms))
        self.checkboxes[key] = list(filter(lambda cb: cb.text() in synonyms, self.checkboxes[key]))
        for cb in to_remove:
            cb.deleteLater()
        new_check_boxes = [self.__check_box(s) for s in to_add]
        self.checkboxes[key].extend(new_check_boxes)
        for cb in new_check_boxes:
            self.synonym_layout.addWidget(cb)

    def __select_dictionary(self, key: str):
        if self.selected_dictionary is not None:
            self.dictionary_widgets[self.selected_dictionary].setStyleSheet("")
        self.dictionary_widgets[key].setStyleSheet(
            "QWidget#" + key + " { background: #8ab4f7; border-radius: 5px }")
        for i in reversed(range(self.synonym_layout.count())):
            self.synonym_layout.itemAt(i).widget().hide()
        for cb in self.checkboxes[key]:
            cb.show()
        self.selected_dictionary = key

    def __remove_dictionary(self, entry: Entry):
        if entry.key == self.selected_dictionary:
            dict_index = self.dictionary_keys.index(entry)
            if dict_index > 0 and dict_index == (len(self.dictionary_keys) - 1):
                self.__select_dictionary(self.dictionary_keys[dict_index - 1].key)
            elif dict_index < len(self.dictionary_keys) - 1:
                self.__select_dictionary(self.dictionary_keys[dict_index + 1].key)

        self.dictionary_keys.remove(entry)
        self.export_button.setEnabled(len(self.dictionary_keys) > 0)

        for cb in self.checkboxes[entry.key]:
            cb.deleteLater()

        self.dictionary_widgets[entry.key].deleteLater()
        del self.checkboxes[entry.key]

    def __check_box(self, s: str) -> QCheckBox:
        cb = QCheckBox(s)
        cb.setParent(self.centralWidget())
        cb.setFixedHeight(30)
        return cb

    def __key(self, column: str, word: str, tolerance: float) -> str:
        return column + "-" + word + "-" + str(tolerance).replace('.', '')
