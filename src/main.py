import sys

import rivals_tab
import teams_tab
import cars_tab
import bad_tab
import scrolling_tab
import file_reader

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QTabWidget
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

        self.title_label = QLabel("Open TXR3 Text Data Files")
        self.title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.subtitle_label = QLabel("Select 26899.dat and 26900.dat files.\n"
                                     "You can extract them with GUT Archive Tools")
        self.subtitle_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dat1_label = QLabel("26899.dat")
        self.dat2_label = QLabel("26900.dat")
        self.dat1_field = QLineEdit()
        self.dat2_field = QLineEdit()
        self.dat1_button = QPushButton("Browse...")
        self.dat2_button = QPushButton("Browse...")
        self.accept_button = QPushButton("OK")
        self.accept_button.setEnabled(False)

        self.dat1_layout = QHBoxLayout()
        self.dat2_layout = QHBoxLayout()
        self.dat1_layout.addWidget(self.dat1_label)
        self.dat1_layout.addWidget(self.dat1_field)
        self.dat1_layout.addWidget(self.dat1_button)
        self.dat2_layout.addWidget(self.dat2_label)
        self.dat2_layout.addWidget(self.dat2_field)
        self.dat2_layout.addWidget(self.dat2_button)

        self.dat1_button.clicked.connect(lambda: self.open_file_dialog(self.dat1_field))
        self.dat2_button.clicked.connect(lambda: self.open_file_dialog(self.dat2_field))
        self.dat1_field.textChanged.connect(self.check_fields)
        self.dat2_field.textChanged.connect(self.check_fields)
        self.accept_button.clicked.connect(self.accept)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.title_label)
        self.layout().addWidget(self.subtitle_label)
        self.layout().addLayout(self.dat1_layout)
        self.layout().addLayout(self.dat2_layout)
        self.layout().addWidget(self.accept_button)

    def open_file_dialog(self, dat_field):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open .dat file', '', 'DAT Files (*.dat)')
        dat_field.setText(file_name)

    def check_fields(self):
        if self.dat1_field.text() and self.dat2_field.text():
            self.accept_button.setEnabled(True)
        else:
            self.accept_button.setEnabled(False)

    def closeEvent(self, a0: QtGui.QCloseEvent):
        sys.exit(0)

    def accept(self):
        global var_teams_tab, var_rivals_tab, var_cars_tab, var_bad_tab, var_scrolling_tab
        dat26899 = file_reader.Dat26899(self.dat1_field.text())
        dat26900 = file_reader.Dat26900(self.dat2_field.text())
        var_teams_tab = teams_tab.TeamsTab(dat26900)
        var_rivals_tab = rivals_tab.RivalsTab(dat26899, dat26900)
        var_cars_tab = cars_tab.CarsTab(dat26899)
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

        self.setLayout(QVBoxLayout())

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
            QtCore.QUrl("https://github.com/igorciz777")))  # todo

        about_action = help_menu.addAction("About")
        # todo about dialog

        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)


def run_app():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    run_app()
