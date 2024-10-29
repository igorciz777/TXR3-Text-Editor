from PyQt6.QtWidgets import QLabel, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QTextEdit

import file_reader


class ScrollingTab(QWidget):
    def __init__(self, dat26899: file_reader.Dat26899):
        super().__init__()
        self.text_idx = 0
        self.dat26899 = dat26899
        self.text_tree_view = QTreeWidget()
        self.text_lines = []
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.text_box = QTextEdit()

        self.scrolling_texts = dat26899.get_scrolling_text()

        self.setup_layout()
        self.reset()

    def setup_layout(self):
        left_vbox = QVBoxLayout()
        tree_scroll_area = QScrollArea()
        self.text_tree_view.setHeaderHidden(True)
        tree_scroll_area.setWidget(self.text_tree_view)
        tree_scroll_area.setWidgetResizable(True)
        left_vbox.addWidget(tree_scroll_area)
        tree_scroll_area.setMaximumWidth(175)
        self.layout.addLayout(left_vbox)

        for text in self.scrolling_texts:
            text_item = QTreeWidgetItem([text.decode('utf-8', errors='ignore').strip('\x00')])
            self.text_tree_view.addTopLevelItem(text_item)

        self.text_tree_view.selectionModel().selectionChanged.connect(self.text_selected)

        right_vbox = QVBoxLayout()
        label = QLabel("Text")
        right_vbox.addWidget(label)
        right_vbox.addWidget(self.text_box)

        button_hbox = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)
        button_hbox.addWidget(save_button)
        button_hbox.addWidget(reset_button)
        right_vbox.addLayout(button_hbox)

        self.layout.addLayout(right_vbox)

    def text_selected(self, selected):
        self.text_idx = selected.indexes()[0].row()
        self.reset()

    def reset(self):
        text = self.scrolling_texts[self.text_idx]
        self.text_box.setText(text.decode('utf-8', errors='ignore').strip('\x00'))

    def save(self):
        text = self.text_box.toPlainText().encode('utf-8') + b'\x00'
        self.scrolling_texts[self.text_idx] = text

        self.dat26899.save_scroll_text(self.scrolling_texts)

        self.text_tree_view.topLevelItem(self.text_idx).setText(0, text.decode('utf-8', errors='ignore').strip('\x00'))
        self.reset()
