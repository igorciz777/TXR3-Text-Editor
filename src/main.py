import os
import sys

import rivals_tab
import teams_tab
import cars_tab
import bad_tab
import scrolling_tab
import file_reader

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QTabWidget, QMessageBox
from PyQt6.QtWidgets import QStyle, QVBoxLayout, QDialog, QFileDialog, QWidget, QHBoxLayout

var_teams_tab = None
var_rivals_tab = None
var_cars_tab = None
var_bad_tab = None
var_scrolling_tab = None


class StartupDialog(QDialog):
    def __init__(self, icon):
        super().__init__()
        self.mainWidget = QWidget()
        self.setWindowTitle("TXR3 Text Editor")
        self.setWindowIcon(icon)
        self.setGeometry(100, 100, 600, 200)

        self.title_label = QLabel("TXR3 Text Editor")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;"
                                       "color:  #2e2e2e;background-color: #bababa;")
        self.subtitle_label = QLabel("Select required data files either manually or through a folder scan.\n"
                                     "You can extract them from BUILD.DAT using GUT Archive Tools")
        self.subtitle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.bin_26679_field = QLineEdit()
        self.bin_26680_field = QLineEdit()
        self.bin_26681_field = QLineEdit()
        self.bin_26682_field = QLineEdit()
        self.dat_26899_field = QLineEdit()
        self.dat_26900_field = QLineEdit()

        self.browse_folder_button = QPushButton("Scan Folder")
        self.accept_button = QPushButton("OK")
        self.accept_button.setEnabled(False)

        self.accept_button.clicked.connect(self.accept)
        self.browse_folder_button.clicked.connect(self.browse_folder)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.title_label)
        self.layout().addWidget(self.subtitle_label)
        self.layout().addLayout(self.make_filebrowse_layout("00026679.bin", self.bin_26679_field))
        self.layout().addLayout(self.make_filebrowse_layout("00026680.bin", self.bin_26680_field))
        self.layout().addLayout(self.make_filebrowse_layout("00026681.bin", self.bin_26681_field))
        self.layout().addLayout(self.make_filebrowse_layout("00026682.bin", self.bin_26682_field))
        self.layout().addLayout(self.make_filebrowse_layout("00026899.dat", self.dat_26899_field))
        self.layout().addLayout(self.make_filebrowse_layout("00026900.dat", self.dat_26900_field))
        self.layout().addWidget(self.browse_folder_button)
        self.layout().addWidget(self.accept_button)

        made_by = QLabel("Made by: igorciz777")
        made_by.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(made_by)

    def open_file_dialog(self, field, dat=True):
        if dat:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Open .dat file', '', 'DAT Files (*.dat)')
        else:
            file_name, _ = QFileDialog.getOpenFileName(self, 'Open .bin file', '', 'BIN Files (*.bin)')
        field.setText(file_name)

    def check_fields(self):
        if (self.bin_26679_field.text() and self.bin_26680_field.text() and self.bin_26681_field.text()
                and self.bin_26682_field.text() and self.dat_26899_field.text() and self.dat_26900_field.text()):
            self.accept_button.setEnabled(True)
        else:
            self.accept_button.setEnabled(False)

    def make_filebrowse_layout(self, filename, field):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(filename))
        field.textChanged.connect(self.check_fields)
        layout.addWidget(field)
        button = QPushButton("Browse")
        if filename.endswith(".dat"):
            button.clicked.connect(lambda: self.open_file_dialog(field, True))
        else:
            button.clicked.connect(lambda: self.open_file_dialog(field, False))
        layout.addWidget(button)

        return layout

    def closeEvent(self, a0: QtGui.QCloseEvent):
        sys.exit(0)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder_path:
            bin_26679_path = None
            bin_26680_path = None
            bin_26681_path = None
            bin_26682_path = None
            dat_26899_path = None
            dat_26900_path = None
            for file in os.listdir(folder_path):
                # print(file)
                if file == "00026679.bin":
                    bin_26679_path = os.path.join(folder_path, file)
                elif file == "00026680.bin":
                    bin_26680_path = os.path.join(folder_path, file)
                elif file == "00026681.bin":
                    bin_26681_path = os.path.join(folder_path, file)
                elif file == "00026682.bin":
                    bin_26682_path = os.path.join(folder_path, file)
                elif file == "00026899.dat":
                    dat_26899_path = os.path.join(folder_path, file)
                elif file == "00026900.dat":
                    dat_26900_path = os.path.join(folder_path, file)
            if (bin_26679_path and bin_26680_path and bin_26681_path and bin_26682_path
                    and dat_26899_path and dat_26900_path):
                self.bin_26679_field.setText(bin_26679_path)
                self.bin_26680_field.setText(bin_26680_path)
                self.bin_26681_field.setText(bin_26681_path)
                self.bin_26682_field.setText(bin_26682_path)
                self.dat_26899_field.setText(dat_26899_path)
                self.dat_26900_field.setText(dat_26900_path)
                self.accept_button.setEnabled(True)
            else:
                QMessageBox.critical(self, "Error", "Selected folder does not contain required files")
                self.accept_button.setEnabled(False)

    def accept(self):
        global var_teams_tab, var_rivals_tab, var_cars_tab, var_bad_tab, var_scrolling_tab
        bin26679 = file_reader.Bin26679(self.bin_26679_field.text())
        bin26680 = file_reader.Bin26680(self.bin_26680_field.text())
        bin26681 = file_reader.Bin26681(self.bin_26681_field.text())
        bin26682 = file_reader.Bin26682(self.bin_26682_field.text())
        dat26899 = file_reader.Dat26899(self.dat_26899_field.text())
        dat26900 = file_reader.Dat26900(self.dat_26900_field.text())
        var_teams_tab = teams_tab.TeamsTab(dat26900)
        var_rivals_tab = rivals_tab.RivalsTab(bin26680, bin26681, bin26682, dat26899, dat26900)
        var_cars_tab = cars_tab.CarsTab(bin26679, dat26899)
        var_bad_tab = bad_tab.BadTab(dat26899)
        var_scrolling_tab = scrolling_tab.ScrollingTab(dat26899)
        super().accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu_bar = self.menuBar()
        self.status_bar = self.statusBar()
        self.setWindowTitle("TXR3 Text Editor")
        pixmap = QStyle.StandardPixmap.SP_FileDialogContentsView
        icon = self.style().standardIcon(pixmap)

        self.tab_widget = QTabWidget()

        self.setCentralWidget(self.tab_widget)
        self.setWindowIcon(icon)
        self.setGeometry(100, 100, 800, 600)

        self.startup_dialog = StartupDialog(icon)
        self.startup_dialog.exec()
        if self.startup_dialog.result() == QDialog.DialogCode.Accepted:
            self.tab_widget.addTab(var_teams_tab, "Teams")
            self.tab_widget.addTab(var_rivals_tab, "Rivals")
            self.tab_widget.addTab(var_cars_tab, "Cars")
            self.tab_widget.addTab(var_bad_tab, "B.A.D.")
            self.tab_widget.addTab(var_scrolling_tab, "Other")

        self.menu_bar_setup()

    def menu_bar_setup(self):
        file_menu = self.menu_bar.addMenu("File")
        help_menu = self.menu_bar.addMenu("Help")

        git_wiki_action = help_menu.addAction("How to use")
        git_wiki_action.triggered.connect(lambda: QtGui.QDesktopServices.openUrl(
            QtCore.QUrl("https://github.com/igorciz777/TXR3-Text-Editor/wiki")))

        about_action = help_menu.addAction("About")
        about_action.triggered.connect(lambda: QMessageBox.about(self, "About",
                                                                 "TXR3 Text Editor\n"
                                                                 "Made by: igorciz777\n"
                                                                 "Version: 1.2\n"
                                                                 "GitHub: github.com/igorciz777/TXR3-Text-Editor"))

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)


def run_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_app()
