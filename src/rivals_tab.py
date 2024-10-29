from PyQt6.QtWidgets import QWidget, QTreeWidget, QVBoxLayout, QScrollArea, QHBoxLayout, QTreeWidgetItem, QTabWidget
from PyQt6.QtWidgets import QLineEdit, QLabel, QPushButton

import file_reader


class RivalsTab(QWidget):
    def __init__(self, dat26899: file_reader.Dat26899, dat26900: file_reader.Dat26900):
        super().__init__()
        self.rival_idx = 0
        self.region_idx = 0
        self.dat26899 = dat26899
        self.dat26900 = dat26900
        self.rivals_tree_view = QTreeWidget()

        self.teams = dat26900.get_team_profiles()
        self.tokyo_rivals_struct = dat26899.get_tokyo_rivals()
        self.osaka_rivals_struct = dat26899.get_osaka_rivals()
        self.nagoya_rivals_struct = dat26899.get_nagoya_rivals()
        self.tokyo_rivals_profiles = dat26900.get_tokyo_rivals()
        self.osaka_rivals_profiles = dat26900.get_osaka_rivals()
        self.nagoya_rivals_profiles = dat26900.get_nagoya_rivals()

        self.rival_lines = []

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setup_layout()
        self.reset()

    def setup_layout(self):
        left_vbox = QVBoxLayout()
        tree_scroll_area = QScrollArea()
        self.rivals_tree_view.setHeaderHidden(True)
        tree_scroll_area.setWidget(self.rivals_tree_view)
        tree_scroll_area.setWidgetResizable(True)
        left_vbox.addWidget(tree_scroll_area)
        tree_scroll_area.setMaximumWidth(275)
        self.layout.addLayout(left_vbox)

        self.rivals_tree_view.addTopLevelItem(QTreeWidgetItem(["Tokyo Rivals"]))
        self.rivals_tree_view.addTopLevelItem(QTreeWidgetItem(["Osaka Rivals"]))
        self.rivals_tree_view.addTopLevelItem(QTreeWidgetItem(["Nagoya Rivals"]))

        for tokyo_rival in self.tokyo_rivals_struct:
            rival_item = QTreeWidgetItem([tokyo_rival['nickname_1'].decode('utf-8', errors='ignore').strip('\x00')
                                          + tokyo_rival['nickname_2'].decode('utf-8', errors='ignore').strip('\x00')])

            self.rivals_tree_view.topLevelItem(0).addChild(rival_item)

        for osaka_rival in self.osaka_rivals_struct:
            rival_item = QTreeWidgetItem([osaka_rival['nickname_1'].decode('utf-8', errors='ignore').strip('\x00')
                                          + osaka_rival['nickname_2'].decode('utf-8', errors='ignore').strip('\x00')])

            self.rivals_tree_view.topLevelItem(1).addChild(rival_item)

        for nagoya_rival in self.nagoya_rivals_struct:
            rival_item = QTreeWidgetItem([nagoya_rival['nickname_1'].decode('utf-8', errors='ignore').strip('\x00')
                                          + nagoya_rival['nickname_2'].decode('utf-8', errors='ignore').strip('\x00')])

            self.rivals_tree_view.topLevelItem(2).addChild(rival_item)

        self.rivals_tree_view.selectionModel().selectionChanged.connect(self.rival_selected)

        right_vbox = QVBoxLayout()
        self.layout.addLayout(right_vbox)

        rival_tabs = QTabWidget()
        right_vbox.addWidget(rival_tabs)

        rival_id_text = QLineEdit()
        rival_team_text = QLineEdit()
        rival_nickname_1_text_edit = QLineEdit()
        rival_nickname_2_text_edit = QLineEdit()
        rival_name_text_edit = QLineEdit()
        rival_job_text_edit = QLineEdit()
        rival_career_text_edit = QLineEdit()
        rival_motto_text_edit = QLineEdit()
        rival_profile2_line1 = QLineEdit()
        rival_profile2_line2 = QLineEdit()
        rival_profile2_line3 = QLineEdit()
        rival_profile2_line4 = QLineEdit()
        rival_profile2_line5 = QLineEdit()
        rival_profile3_line1 = QLineEdit()
        rival_profile3_line2 = QLineEdit()
        rival_profile3_line3 = QLineEdit()
        rival_profile3_line4 = QLineEdit()
        rival_profile3_line5 = QLineEdit()

        self.rival_lines = [rival_id_text, rival_team_text, rival_nickname_1_text_edit, rival_nickname_2_text_edit,
                            rival_name_text_edit, rival_job_text_edit, rival_career_text_edit, rival_motto_text_edit,
                            rival_profile2_line1, rival_profile2_line2, rival_profile2_line3, rival_profile2_line4,
                            rival_profile2_line5, rival_profile3_line1, rival_profile3_line2, rival_profile3_line3,
                            rival_profile3_line4, rival_profile3_line5]

        self.rival_lines[0].setEnabled(False)
        self.rival_lines[1].setEnabled(False)
        self.rival_lines[2].setMaxLength(0x12 - 1)
        self.rival_lines[3].setMaxLength(0x10 - 1)
        self.rival_lines[4].setMaxLength(0x23 - 1)
        self.rival_lines[5].setMaxLength(0x3d - 1)
        self.rival_lines[6].setMaxLength(0x0b - 1)
        for line in self.rival_lines[7:]:
            line.setMaxLength(0x51 - 1)

        rival_tabs.addTab(self.profile1(), "Profile 1")
        rival_tabs.addTab(self.profile2(), "Profile 2")
        rival_tabs.addTab(self.profile3(), "Profile 3")

        button_hbox = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)
        button_hbox.addWidget(save_button)
        button_hbox.addWidget(reset_button)
        right_vbox.addLayout(button_hbox)

    def profile1(self):
        widget = QWidget()
        layout = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Rival ID:"))
        hbox.addWidget(self.rival_lines[0])
        hbox.addWidget(QLabel("Team:"))
        hbox.addWidget(self.rival_lines[1])
        layout.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Nickname:"))
        hbox.addWidget(self.rival_lines[2])
        hbox.addWidget(self.rival_lines[3])
        layout.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Name:"))
        hbox.addWidget(self.rival_lines[4])
        layout.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Job:"))
        hbox.addWidget(self.rival_lines[5])
        hbox.addWidget(QLabel("Career:"))
        hbox.addWidget(self.rival_lines[6])
        layout.addLayout(hbox)
        hbox = QHBoxLayout()
        hbox.addWidget(QLabel("Motto:"))
        hbox.addWidget(self.rival_lines[7])
        layout.addLayout(hbox)
        widget.setLayout(layout)

        return widget

    def profile2(self):
        widget = QWidget()
        layout = QVBoxLayout()
        for i, line in enumerate(self.rival_lines[8:13]):
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel("Line {}: ".format(i + 1)))
            hbox.addWidget(line)
            layout.addLayout(hbox)
        widget.setLayout(layout)
        return widget

    def profile3(self):
        widget = QWidget()
        layout = QVBoxLayout()
        for i, line in enumerate(self.rival_lines[13:]):
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel("Line {}: ".format(i + 1)))
            hbox.addWidget(line)
            layout.addLayout(hbox)
        widget.setLayout(layout)
        return widget

    def rival_selected(self, selected):
        # check if parent exists - if not, it's a region
        if selected.indexes()[0].parent().row() == -1:
            # region
            pass
        else:
            # rival
            self.rival_idx = selected.indexes()[0].row()
            self.region_idx = selected.indexes()[0].parent().row()
            self.reset()

    def reset(self):
        rival = None
        profile = None
        if self.region_idx == 0:
            rival = self.tokyo_rivals_struct[self.rival_idx]
            profile = self.tokyo_rivals_profiles[self.rival_idx]
        elif self.region_idx == 1:
            rival = self.osaka_rivals_struct[self.rival_idx]
            profile = self.osaka_rivals_profiles[self.rival_idx]
        elif self.region_idx == 2:
            rival = self.nagoya_rivals_struct[self.rival_idx]
            profile = self.nagoya_rivals_profiles[self.rival_idx]

        team = self.teams[rival['team_id']]

        self.rival_lines[0].setText(str(rival['rival_id'] + 1))
        self.rival_lines[1].setText(team['team_name'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[2].setText(rival['nickname_1'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[3].setText(rival['nickname_2'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[4].setText(profile['name'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[5].setText(profile['job'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[6].setText(profile['career'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[7].setText(profile['motto'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[8].setText(profile['p2_line1'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[9].setText(profile['p2_line2'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[10].setText(profile['p2_line3'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[11].setText(profile['p2_line4'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[12].setText(profile['p2_line5'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[13].setText(profile['p3_line1'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[14].setText(profile['p3_line2'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[15].setText(profile['p3_line3'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[16].setText(profile['p3_line4'].decode('utf-8', errors='ignore').strip('\x00'))
        self.rival_lines[17].setText(profile['p3_line5'].decode('utf-8', errors='ignore').strip('\x00'))

    def save(self):
        rival = None
        profile = None
        if self.region_idx == 0:
            rival = self.tokyo_rivals_struct[self.rival_idx]
            profile = self.tokyo_rivals_profiles[self.rival_idx]
        elif self.region_idx == 1:
            rival = self.osaka_rivals_struct[self.rival_idx]
            profile = self.osaka_rivals_profiles[self.rival_idx]
        elif self.region_idx == 2:
            rival = self.nagoya_rivals_struct[self.rival_idx]
            profile = self.nagoya_rivals_profiles[self.rival_idx]

        rival['nickname_1'] = self.rival_lines[2].text().encode('utf-8') + b'\x00'
        rival['nickname_2'] = self.rival_lines[3].text().encode('utf-8') + b'\x00'
        profile['name'] = self.rival_lines[4].text().encode('utf-8') + b'\x00'
        profile['job'] = self.rival_lines[5].text().encode('utf-8') + b'\x00'
        profile['career'] = self.rival_lines[6].text().encode('utf-8') + b'\x00'
        profile['motto'] = self.rival_lines[7].text().encode('utf-8') + b'\x00'
        profile['p2_line1'] = self.rival_lines[8].text().encode('utf-8') + b'\x00'
        profile['p2_line2'] = self.rival_lines[9].text().encode('utf-8') + b'\x00'
        profile['p2_line3'] = self.rival_lines[10].text().encode('utf-8') + b'\x00'
        profile['p2_line4'] = self.rival_lines[11].text().encode('utf-8') + b'\x00'
        profile['p2_line5'] = self.rival_lines[12].text().encode('utf-8') + b'\x00'
        profile['p3_line1'] = self.rival_lines[13].text().encode('utf-8') + b'\x00'
        profile['p3_line2'] = self.rival_lines[14].text().encode('utf-8') + b'\x00'
        profile['p3_line3'] = self.rival_lines[15].text().encode('utf-8') + b'\x00'
        profile['p3_line4'] = self.rival_lines[16].text().encode('utf-8') + b'\x00'
        profile['p3_line5'] = self.rival_lines[17].text().encode('utf-8') + b'\x00'

        if self.region_idx == 0:
            self.dat26899.save_rivals(self.region_idx, self.tokyo_rivals_struct)
            self.dat26900.save_rivals(self.region_idx, self.tokyo_rivals_profiles)
        elif self.region_idx == 1:
            self.dat26899.save_rivals(self.region_idx, self.osaka_rivals_struct)
            self.dat26900.save_rivals(self.region_idx, self.osaka_rivals_profiles)
        elif self.region_idx == 2:
            self.dat26899.save_rivals(self.region_idx, self.nagoya_rivals_struct)
            self.dat26900.save_rivals(self.region_idx, self.nagoya_rivals_profiles)

        self.rivals_tree_view.topLevelItem(self.region_idx).child(self.rival_idx)\
            .setText(0, self.rival_lines[2].text() + self.rival_lines[3].text())

