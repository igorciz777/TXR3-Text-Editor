from PyQt6.QtWidgets import QLabel, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QLineEdit

import file_reader


class BadTab(QWidget):
    def __init__(self, dat26899: file_reader.Dat26899):
        super().__init__()
        self.bad_idx = 0
        self.bad_file = 0
        self.dat26899 = dat26899
        self.bad_tree_view = QTreeWidget()
        self.bad_lines = []
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.bad_1 = dat26899.get_bad_names(0)
        self.bad_2 = dat26899.get_bad_names(1)

        self.setup_layout()
        self.reset()

    def setup_layout(self):
        left_vbox = QVBoxLayout()
        tree_scroll_area = QScrollArea()
        self.bad_tree_view.setHeaderHidden(True)
        tree_scroll_area.setWidget(self.bad_tree_view)
        tree_scroll_area.setWidgetResizable(True)
        left_vbox.addWidget(tree_scroll_area)
        tree_scroll_area.setMaximumWidth(175)
        self.layout.addLayout(left_vbox)

        self.bad_tree_view.addTopLevelItem(QTreeWidgetItem(["B.A.D. Names 1"]))
        self.bad_tree_view.addTopLevelItem(QTreeWidgetItem(["B.A.D. Names 2"]))

        for bad in self.bad_1:
            bad_item = QTreeWidgetItem([bad['name0'].decode('utf-8', errors='ignore').strip('\x00')])
            self.bad_tree_view.topLevelItem(0).addChild(bad_item)

        for bad in self.bad_2:
            bad_item = QTreeWidgetItem([bad['name0'].decode('utf-8', errors='ignore').strip('\x00')])
            self.bad_tree_view.topLevelItem(1).addChild(bad_item)

        self.bad_tree_view.selectionModel().selectionChanged.connect(self.bad_selected)

        right_vbox = QVBoxLayout()

        value_text_edit = QLineEdit()
        value_text_edit.setEnabled(False)
        bad_name0_text_edit = QLineEdit()
        bad_name0_text_edit.setMaxLength(0x12 - 1)
        bad_name1_text_edit = QLineEdit()
        bad_name1_text_edit.setMaxLength(0x12 - 1)
        self.bad_lines = [value_text_edit, bad_name0_text_edit, bad_name1_text_edit]

        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Value:"))
        edit_hbox.addWidget(value_text_edit)
        right_vbox.addLayout(edit_hbox)

        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("B.A.D. Name 1:"))
        edit_hbox.addWidget(bad_name0_text_edit)
        edit_hbox.addWidget(QLabel("B.A.D. Name 2:"))
        edit_hbox.addWidget(bad_name1_text_edit)
        right_vbox.addLayout(edit_hbox)

        button_hbox = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)
        button_hbox.addWidget(save_button)
        button_hbox.addWidget(reset_button)
        right_vbox.addLayout(button_hbox)

        self.layout.addLayout(right_vbox)

    def bad_selected(self, selected):
        if selected.indexes()[0].parent().row() == -1:
            # file
            pass
        else:
            # bad
            self.bad_idx = selected.indexes()[0].row()
            self.bad_file = selected.indexes()[0].parent().row()
            self.reset()

    def reset(self):
        bad = None
        if self.bad_file == 0:
            bad = self.bad_1[self.bad_idx]
        elif self.bad_file == 1:
            bad = self.bad_2[self.bad_idx]
        self.bad_lines[0].setText(str(bad['value']))
        self.bad_lines[1].setText(bad['name0'].decode('utf-8', errors='ignore').strip('\x00'))
        self.bad_lines[2].setText(bad['name1'].decode('utf-8', errors='ignore').strip('\x00'))

    def save(self):
        bad = None
        if self.bad_file == 0:
            bad = self.bad_1[self.bad_idx]
        elif self.bad_file == 1:
            bad = self.bad_2[self.bad_idx]
        bad['name0'] = self.bad_lines[1].text().encode('utf-8') + b'\x00'
        bad['name1'] = self.bad_lines[2].text().encode('utf-8') + b'\x00'

        if self.bad_file == 0:
            self.dat26899.save_bad_names(self.bad_file, self.bad_1)
        else:
            self.dat26899.save_bad_names(self.bad_file, self.bad_2)

        self.bad_tree_view.topLevelItem(self.bad_file).child(self.bad_idx).setText(0, self.bad_lines[1].text())

        self.reset()
