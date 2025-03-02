from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton, QColorDialog, QLabel, QSlider

import file_reader


class RivalDataWidget(QWidget):
    def __init__(self,
                 dat26899: file_reader.Dat26899):
        super().__init__()
        self.window_color = QColor(0, 0, 0, 0)
        self.body_color_2 = QColor(0, 0, 0, 0)
        self.body_color_1 = QColor(0, 0, 0, 0)
        self.dat26899 = dat26899

        self.car_models = dat26899.get_car_models()
        self.car_models_enum = {}
        for i, model in enumerate(self.car_models):
            self.car_models_enum[i] = model['brand'].decode('utf-8', errors='ignore').strip('\x00') + ' ' + \
                                      model['model'].decode('utf-8', errors='ignore').strip('\x00') + ' ' + \
                                      model['chassis'].decode('utf-8', errors='ignore').strip('\x00') + ' ' + \
                                      model['spec'].decode('utf-8', errors='ignore').strip('\x00')

        self.data_fields = [
            'car_id',
            'engine', 'engine_swap', 'muffler', 'cooling', 'transmission', 'clutch',
            'suspension', 'brake', 'reinforce', 'weight_down',
            'front_bumper', 'front_bumper_material', 'bonnet', 'bonnet_material', 'grill', 'grill_material',
            'overfender', 'overfender_material', 'sideskirt', 'sideskirt_material',
            'rear_bumper', 'rear_bumper_material', 'rear_spoiler', 'rear_spoiler_material', 'mirror', 'mirror_material',
            'front_light_design',
            'front_light_eyeline', 'front_light_eyeline_material', 'front_light_color',
            'tail_light_eyeline', 'tail_light_eyeline_material', 'tail_light_color',
            'winker', 'horn', 'numberplate', 'meter',
            'front_wheel_size', 'front_wheel',
            'rear_wheel_size', 'rear_wheel', 'front_tire', 'rear_tire'
        ]

        self.body_color_1_fields = ['body_color_1_r', 'body_color_1_g', 'body_color_1_b']
        self.body_color_2_fields = ['body_color_2_r', 'body_color_2_g', 'body_color_2_b']
        self.window_color_fields = ['window_color_r', 'window_color_g', 'window_color_b', 'window_color_alpha']

        self.engine_swaps_enum = {
            0x00: 'None',
            0x01: 'L4 NA',
            0x02: 'L6 NA',
            0x03: 'V6 NA',
            0x04: 'V8 NA',
            0x05: 'RE NA',
            0x06: 'L4 TURBO',
            0x07: 'L6 TURBO',
            0x08: 'V6 TURBO',
            0x09: 'V8 TURBO',
            0x0A: 'F4 TURBO',
            0x0B: 'F6 TURBO',
            0x0C: 'RE TURBO'
        }

        self.materials_enum = {
            0x00: 'FRP',
            0x01: 'Urethane',
            0x02: 'D-Carbon Natural',
            0x03: 'D-Carbon Colored'
        }

        self.tires_enum = {
            0x00: 'Normal',
            0x01: 'HG',
            0x02: 'S'
        }

        self.wheel_size_enum = {
            0x00: 'Normal',
            0x01: '+1 Inch',
            0x02: '+2 Inch'
        }

        self.wheels_enum = {
            0x00: 'Normal',
            0x01: '5ZIGEN Type 1',
            0x02: '5ZIGEN Type 2',
            0x03: '5ZIGEN Type 3',
            0x04: '5ZIGEN Type 4',
            0x05: '5ZIGEN Type 5',
            0x06: 'Enkei Type 1',
            0x07: 'Enkei Type 2',
            0x08: 'Enkei Type 3',
            0x09: 'Enkei Type 4',
            0x0A: 'Enkei Type 5',
            0x0B: 'First Type 1',
            0x0C: 'First Type 2',
            0x0D: 'First Type 3',
            0x0E: 'First Type 4',
            0x0F: 'First Type 5',
            0x10: 'Hart Type 1',
            0x11: 'Hart Type 2',
            0x12: 'Hart Type 3',
            0x13: 'Hart Type 4',
            0x14: 'Hart Type 5',
            0x15: 'Riverside Type 1',
            0x16: 'Riverside Type 2',
            0x17: 'Riverside Type 3',
            0x18: 'Riverside Type 4',
            0x19: 'Riverside Type 5',
            0x1A: 'Weds Type 1',
            0x1B: 'Weds Type 2',
            0x1C: 'Weds Type 3',
            0x1D: 'Weds Type 4',
            0x1E: 'Weds Type 5',
            0x1F: 'WORK Type 1',
            0x20: 'WORK Type 2',
            0x21: 'WORK Type 3',
            0x22: 'WORK Type 4',
            0x23: 'WORK Type 5',
            0x24: 'Yokohama Type 1',
            0x25: 'Yokohama Type 2',
            0x26: 'Yokohama Type 3',
            0x27: 'Yokohama Type 4',
            0x28: 'Yokohama Type 5'
        }

        self.levels_to_9 = {  # engine
            0x00: 'Stock',
            0x01: 'Level 1',
            0x02: 'Level 2',
            0x03: 'Level 3',
            0x04: 'Level 4',
            0x05: 'Level 5',
            0x06: 'Level 6',
            0x07: 'Level 7',
            0x08: 'Level 8',
            0x09: 'Level 9'
        }

        self.levels_to_5 = {  # muffler, cooldown, clutch, brake, reinforce, weight_down
            0x00: 'Stock',
            0x01: 'Level 1',
            0x02: 'Level 2',
            0x03: 'Level 3',
            0x04: 'Level 4',
            0x05: 'Level 5'
        }

        self.levels_to_3 = {  # transmission, suspension
            0x00: 'Stock',
            0x01: 'Level 1',
            0x02: 'Level 2',
            0x03: 'Level 3'
        }

        self.types_enum_with_off = {  # rear spoiler
            0x00: 'Stock',
            0x01: 'Type 1',
            0x02: 'Type 2',
            0x03: 'Type 3',
            0x04: 'Type 4',
            0x05: 'Type 5',
            0x06: 'Off'
        }

        self.types_enum_licence_plate = {
            0x00: 'Stock',
            0x01: 'Type 1',
            0x02: 'Type 2',
            0x03: 'Type 3',
            0x04: 'Type 4',
            0x05: 'Off'
        }

        self.types_enum = {
            0x00: 'Stock',
            0x01: 'Type 1',
            0x02: 'Type 2',
            0x03: 'Type 3',
            0x04: 'Type 4',
            0x05: 'Type 5'
        }

        self.data_lines = {field: QComboBox() for field in self.data_fields}
        self.color_buttons = {
            'body_color_1': QPushButton("Select Body Color 1"),
            'body_color_2': QPushButton("Select Body Color 2"),
            'window_color': QPushButton("Select Window Color")
        }
        self.color_previews = {
            'body_color_1': QLabel(),
            'body_color_2': QLabel(),
            'window_color': QLabel()
        }

        layout = QVBoxLayout()
        row_layout = QHBoxLayout()
        for i, field in enumerate(self.data_fields):
            if i > 0 and i % 3 == 0:
                layout.addLayout(row_layout)
                row_layout = QHBoxLayout()
            hbox = QVBoxLayout()
            hbox.addWidget(QLabel(field.replace('_', ' ').title() + ":"))
            hbox.addWidget(self.data_lines[field])
            row_layout.addLayout(hbox)
        layout.addLayout(row_layout)

        for color_field, button in self.color_buttons.items():
            color_layout = QHBoxLayout()
            button.clicked.connect(lambda _, cf=color_field: self.open_color_dialog(cf))
            color_layout.addWidget(button)
            color_layout.addWidget(self.color_previews[color_field])
            layout.addLayout(color_layout)

        self.body_reflection_slider = QSlider()
        self.body_reflection_slider.setMinimum(0)
        self.body_reflection_slider.setMaximum(255)
        self.body_reflection_slider.setOrientation(Qt.Orientation.Horizontal)

        layout.addWidget(QLabel("Body Reflection:"))
        layout.addWidget(self.body_reflection_slider)

        self.setLayout(layout)

        self.populate_comboboxes()

    def populate_comboboxes(self):
        for field, combobox in self.data_lines.items():
            if field in ['engine']:
                for key, value in self.levels_to_9.items():
                    combobox.addItem(value, key)
            elif field in ['muffler', 'cooling', 'clutch', 'brake', 'reinforce', 'weight_down']:
                for key, value in self.levels_to_5.items():
                    combobox.addItem(value, key)
            elif field in ['transmission', 'suspension']:
                for key, value in self.levels_to_3.items():
                    combobox.addItem(value, key)
            elif field == 'engine_swap':
                for key, value in self.engine_swaps_enum.items():
                    combobox.addItem(value, key)
            elif field in ['front_bumper', 'bonnet', 'grill', 'mirror', 'overfender', 'sideskirt',
                           'rear_bumper', 'horn', 'meter', 'front_light_eyeline', 'front_light_color',
                           'tail_light_eyeline', 'tail_light_color', 'winker', 'front_light_design']:
                for key, value in self.types_enum.items():
                    combobox.addItem(value, key)
            elif field == 'rear_spoiler':
                for key, value in self.types_enum_with_off.items():
                    combobox.addItem(value, key)
            elif field in ['front_bumper_material', 'bonnet_material', 'grill_material', 'mirror_material',
                           'overfender_material', 'sideskirt_material', 'rear_bumper_material',
                           'rear_spoiler_material', 'front_light_eyeline_material', 'tail_light_eyeline_material']:
                for key, value in self.materials_enum.items():
                    combobox.addItem(value, key)
            elif field in ['front_tire', 'rear_tire']:
                for key, value in self.tires_enum.items():
                    combobox.addItem(value, key)
            elif field in ['front_wheel_size', 'rear_wheel_size']:
                for key, value in self.wheel_size_enum.items():
                    combobox.addItem(value, key)
            elif field in ['front_wheel', 'rear_wheel']:
                for key, value in self.wheels_enum.items():
                    combobox.addItem(value, key)
            elif field in ['numberplate']:
                for key, value in self.types_enum_licence_plate.items():
                    combobox.addItem(value, key)
            elif field == 'car_id':
                for key, value in self.car_models_enum.items():
                    combobox.addItem(value, key)
            else:
                for i in range(256):
                    combobox.addItem(str(i), i)

    def open_color_dialog(self, color_field):
        color = QColorDialog.getColor()
        if color.isValid():
            if color_field == 'body_color_1':
                self.body_color_1 = color
            elif color_field == 'body_color_2':
                self.body_color_2 = color
            elif color_field == 'window_color':
                self.window_color = color
            self.update_color_preview(color_field)

    def update_color_preview(self, color_field):
        color = getattr(self, color_field)
        pixmap = QPixmap(20, 20)
        pixmap.fill(color)
        self.color_previews[color_field].setPixmap(pixmap)

    def reset(self, rival):
        for field in self.data_fields:
            self.data_lines[field].setCurrentIndex(rival[field])
        self.body_color_1 = QColor(rival['body_color_1_r'], rival['body_color_1_g'], rival['body_color_1_b'])
        self.body_color_2 = QColor(rival['body_color_2_r'], rival['body_color_2_g'], rival['body_color_2_b'])
        self.window_color = QColor(rival['window_color_r'], rival['window_color_g'], rival['window_color_b'],
                                   rival['window_color_alpha'])
        self.update_color_preview('body_color_1')
        self.update_color_preview('body_color_2')
        self.update_color_preview('window_color')

        self.body_reflection_slider.setValue(rival['body_reflection'])

    def save(self, rival):
        for field in self.data_fields:
            rival[field] = self.data_lines[field].currentData()
        rival['body_color_1_r'] = self.body_color_1.red()
        rival['body_color_1_g'] = self.body_color_1.green()
        rival['body_color_1_b'] = self.body_color_1.blue()
        rival['body_color_2_r'] = self.body_color_2.red()
        rival['body_color_2_g'] = self.body_color_2.green()
        rival['body_color_2_b'] = self.body_color_2.blue()
        rival['window_color_r'] = self.window_color.red()
        rival['window_color_g'] = self.window_color.green()
        rival['window_color_b'] = self.window_color.blue()
        rival['window_color_alpha'] = self.window_color.alpha()
        rival['body_reflection'] = self.body_reflection_slider.value()
