from PyQt6.QtWidgets import QLineEdit, QPushButton, QLabel, QTextEdit
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTreeWidget, QVBoxLayout, QScrollArea, QTreeWidgetItem

import file_reader


class CarsTab(QWidget):
    def __init__(self,
                 bin26679: file_reader.Bin26679,
                 dat26899: file_reader.Dat26899):
        super().__init__()
        self.car_idx = 0
        self.description_idx = 0
        self.bin26679 = bin26679
        self.dat26899 = dat26899
        self.cars_tree_view = QTreeWidget()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.cars = dat26899.get_car_models()
        self.car_descriptions = dat26899.get_scrolling_text(True)
        self.car_lines = []
        self.drivetrain_types = ['4WD', 'FF', 'FR', 'MR', 'RR']
        self.engine_types = ['F4', 'F6', 'L3', 'L4', 'L6', 'RE', 'V6', 'V8', 'V10', 'V12']

        self.setup_layout()
        self.reset()

    def setup_layout(self):
        left_vbox = QVBoxLayout()
        tree_scroll_area = QScrollArea()
        self.cars_tree_view.setHeaderHidden(True)
        tree_scroll_area.setWidget(self.cars_tree_view)
        tree_scroll_area.setWidgetResizable(True)
        left_vbox.addWidget(tree_scroll_area)
        tree_scroll_area.setMaximumWidth(250)
        self.layout.addLayout(left_vbox)

        for car in self.cars:
            car_item = QTreeWidgetItem([car['model'].decode('utf-8', errors='ignore').strip('\x00') +
                                        ' ' + car['chassis'].decode('utf-8', errors='ignore').strip('\x00')])
            self.cars_tree_view.addTopLevelItem(car_item)

        self.cars_tree_view.selectionModel().selectionChanged.connect(self.car_selected)

        right_vbox = QVBoxLayout()

        brand_text_edit = QLineEdit()
        model_text_edit = QLineEdit()
        chassis_text_edit = QLineEdit()
        spec_text_edit = QLineEdit()
        drivetrain_text_edit = QLineEdit()
        weight_text_edit = QLineEdit()
        displacement_text_edit = QLineEdit()
        engine_text_edit = QLineEdit()
        power_text_edit = QLineEdit()
        flavor_text_edit = QTextEdit()

        self.car_lines = [brand_text_edit, model_text_edit, chassis_text_edit, spec_text_edit, drivetrain_text_edit,
                          weight_text_edit, displacement_text_edit, engine_text_edit, power_text_edit, flavor_text_edit]

        brand_text_edit.setMaxLength(0x14 - 1)
        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Brand"))
        edit_hbox.addWidget(brand_text_edit)
        right_vbox.addLayout(edit_hbox)

        model_text_edit.setMaxLength(0x20 - 1)
        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Model"))
        edit_hbox.addWidget(model_text_edit)
        right_vbox.addLayout(edit_hbox)

        chassis_text_edit.setMaxLength(0x0c - 1)
        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Chassis"))
        edit_hbox.addWidget(chassis_text_edit)
        right_vbox.addLayout(edit_hbox)

        spec_text_edit.setMaxLength(0x28 - 1)
        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Spec"))
        edit_hbox.addWidget(spec_text_edit)
        right_vbox.addLayout(edit_hbox)

        drivetrain_text_edit.setEnabled(False)
        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Drivetrain"))
        edit_hbox.addWidget(drivetrain_text_edit)
        right_vbox.addLayout(edit_hbox)

        weight_text_edit.setEnabled(False)
        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Weight"))
        edit_hbox.addWidget(weight_text_edit)
        right_vbox.addLayout(edit_hbox)

        displacement_text_edit.setEnabled(False)
        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Displacement"))
        edit_hbox.addWidget(displacement_text_edit)
        right_vbox.addLayout(edit_hbox)

        engine_text_edit.setEnabled(False)
        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Engine"))
        edit_hbox.addWidget(engine_text_edit)
        right_vbox.addLayout(edit_hbox)

        power_text_edit.setEnabled(False)
        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Power"))
        edit_hbox.addWidget(power_text_edit)
        right_vbox.addLayout(edit_hbox)

        edit_hbox = QHBoxLayout()
        edit_hbox.addWidget(QLabel("Description"))
        right_vbox.addLayout(edit_hbox)
        right_vbox.addWidget(flavor_text_edit)

        dsc_max_length = 0x709 - 1
        flavor_text_edit.textChanged.connect(lambda: file_reader.check_max_length(flavor_text_edit, dsc_max_length))

        button_hbox = QHBoxLayout()
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset)
        button_hbox.addWidget(save_button)
        button_hbox.addWidget(reset_button)
        right_vbox.addLayout(button_hbox)

        self.layout.addLayout(right_vbox)
        self.reset()

    def car_selected(self):
        self.car_idx = self.cars_tree_view.selectedIndexes()[0].row()
        self.description_idx = self.car_idx
        if 48 <= self.car_idx <= 59:  # Vitz misalignment fix
            self.description_idx += 1
        if self.car_idx == 79:
            self.description_idx = 48

        if self.car_idx >= 80:  # Dummy car misalignment fix
            self.description_idx -= 2

        if self.car_idx >= 116:  # 0 car misalignment fix
            self.description_idx -= 1

        if self.car_idx == 59 or self.car_idx == 116 or self.car_idx == 80:
            self.car_lines[9].setEnabled(False)
        else:
            self.car_lines[9].setEnabled(True)
        # print(self.car_idx, self.description_idx)
        self.reset()

    def reset(self):
        car = self.cars[self.car_idx]
        description = self.car_descriptions[self.description_idx]
        self.car_lines[0].setText(car['brand'].decode('utf-8', errors='ignore').strip('\x00'))
        self.car_lines[1].setText(car['model'].decode('utf-8', errors='ignore').strip('\x00'))
        self.car_lines[2].setText(car['chassis'].decode('utf-8', errors='ignore').strip('\x00'))
        self.car_lines[3].setText(car['spec'].decode('utf-8', errors='ignore').strip('\x00'))
        self.car_lines[4].setText(self.drivetrain_types[car['drivetrain']])
        self.car_lines[5].setText(str(car['weight']) + 'kg')
        if car['rotor_count'] > 0:
            self.car_lines[6].setText(str(car['displacement']) + 'x' + str(car['rotor_count']) + 'cc')
        else:
            self.car_lines[6].setText(str(car['displacement']) + 'cc')

        self.car_lines[7].setText(self.engine_types[car['engine_type']])
        self.car_lines[8].setText(str(car['power']) + 'PS')
        self.car_lines[9].setText(description.decode('utf-8', errors='ignore').strip('\x00'))

    def save(self):
        car = self.cars[self.car_idx]
        car['brand'] = self.car_lines[0].text().encode('utf-8') + b'\x00'
        car['model'] = self.car_lines[1].text().encode('utf-8') + b'\x00'
        car['chassis'] = self.car_lines[2].text().encode('utf-8') + b'\x00'
        car['spec'] = self.car_lines[3].text().encode('utf-8') + b'\x00'

        if self.car_idx != 59 and self.car_idx != 116 and self.car_idx != 80:
            self.car_descriptions[self.description_idx] = self.car_lines[9].toPlainText().encode('utf-8') + b'\x00'

        self.bin26679.save_car_models(self.cars)
        self.dat26899.save_car_models(self.cars, self.car_descriptions)

        self.cars_tree_view.currentItem().setText(0, car['model'].decode('utf-8', errors='ignore').strip('\x00') +
                                                  ' ' + car['chassis'].decode('utf-8', errors='ignore').strip('\x00'))
