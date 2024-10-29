from PyQt6.QtWidgets import QLabel, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QScrollArea, QLineEdit

import file_reader


class TeamsTab(QWidget):
    def __init__(self, dat26900: file_reader.Dat26900):
        super().__init__()
        self.team_idx = 0
        self.dat26900 = dat26900
        self.teams_tree_view = QTreeWidget()
        self.team_lines = []
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.teams = dat26900.get_team_profiles()

        self.setup_layout()
        self.reset()

    def setup_layout(self):
        left_vbox = QVBoxLayout()
        tree_scroll_area = QScrollArea()
        self.teams_tree_view.setHeaderHidden(True)
        tree_scroll_area.setWidget(self.teams_tree_view)
        tree_scroll_area.setWidgetResizable(True)
        left_vbox.addWidget(tree_scroll_area)
        tree_scroll_area.setMaximumWidth(175)
        self.layout.addLayout(left_vbox)

        for team in self.teams:
            team_item = QTreeWidgetItem([team['team_name'].decode('utf-8').strip('\x00')])
            self.teams_tree_view.addTopLevelItem(team_item)

        self.teams_tree_view.selectionModel().selectionChanged.connect(self.team_selected)

        right_vbox = QVBoxLayout()

        team_name_text_edit = QLineEdit()
        line1_text_edit = QLineEdit()
        line2_text_edit = QLineEdit()
        line3_text_edit = QLineEdit()
        line4_text_edit = QLineEdit()
        line5_text_edit = QLineEdit()
        line6_text_edit = QLineEdit()
        line7_text_edit = QLineEdit()
        line8_text_edit = QLineEdit()
        line9_text_edit = QLineEdit()

        self.team_lines = [team_name_text_edit, line1_text_edit, line2_text_edit, line3_text_edit, line4_text_edit,
                           line5_text_edit, line6_text_edit, line7_text_edit, line8_text_edit, line9_text_edit]

        for i, line in enumerate(self.team_lines):
            edit_hbox = QHBoxLayout()
            if i == 0:
                line.setMaxLength(0x29 - 1)
                edit_hbox.addWidget(QLabel("Team Name"))
            else:
                line.setMaxLength(0x33 - 1)
                edit_hbox.addWidget(QLabel(f"Line {i}"))
            edit_hbox.addWidget(line)
            right_vbox.addLayout(edit_hbox)
        self.layout.addLayout(right_vbox)

        button_hbox = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)
        button_hbox.addWidget(save_button)
        button_hbox.addWidget(reset_button)
        right_vbox.addLayout(button_hbox)

    def team_selected(self, selected):
        self.team_idx = selected.indexes()[0].row()
        self.reset()

    def reset(self):
        team = self.teams[self.team_idx]
        self.team_lines[0].setText(team['team_name'].decode('utf-8', errors='ignore').strip('\x00'))
        self.team_lines[1].setText(team['line1'].decode('utf-8', errors='ignore').strip('\x00'))
        self.team_lines[2].setText(team['line2'].decode('utf-8', errors='ignore').strip('\x00'))
        self.team_lines[3].setText(team['line3'].decode('utf-8', errors='ignore').strip('\x00'))
        self.team_lines[4].setText(team['line4'].decode('utf-8', errors='ignore').strip('\x00'))
        self.team_lines[5].setText(team['line5'].decode('utf-8', errors='ignore').strip('\x00'))
        self.team_lines[6].setText(team['line6'].decode('utf-8', errors='ignore').strip('\x00'))
        self.team_lines[7].setText(team['line7'].decode('utf-8', errors='ignore').strip('\x00'))
        self.team_lines[8].setText(team['line8'].decode('utf-8', errors='ignore').strip('\x00'))
        self.team_lines[9].setText(team['line9'].decode('utf-8', errors='ignore').strip('\x00'))

    def save(self):
        team = self.teams[self.team_idx]
        team['team_name'] = self.team_lines[0].text().encode('utf-8') + b'\x00'
        team['line1'] = self.team_lines[1].text().encode('utf-8') + b'\x00'
        team['line2'] = self.team_lines[2].text().encode('utf-8') + b'\x00'
        team['line3'] = self.team_lines[3].text().encode('utf-8') + b'\x00'
        team['line4'] = self.team_lines[4].text().encode('utf-8') + b'\x00'
        team['line5'] = self.team_lines[5].text().encode('utf-8') + b'\x00'
        team['line6'] = self.team_lines[6].text().encode('utf-8') + b'\x00'
        team['line7'] = self.team_lines[7].text().encode('utf-8') + b'\x00'
        team['line8'] = self.team_lines[8].text().encode('utf-8') + b'\x00'
        team['line9'] = self.team_lines[9].text().encode('utf-8') + b'\x00'
        self.dat26900.save_teams(self.teams)
        self.teams_tree_view.topLevelItem(self.team_idx).setText(0, team['team_name'].decode('utf-8').strip('\x00'))
