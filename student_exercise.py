# Average speed Calculator
from PyQt6.QtWidgets import *
import sys


class AvgSpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Average Speed Calculator")
        grid = QGridLayout()

        distance_label = QLabel("Distance:")
        self.distance_line_edit = QLineEdit()

        self.combobox1 = QComboBox()
        self.combobox1.addItem("Kilometre")
        self.combobox1.addItem("Miles")

        time = QLabel("Time (hours):")
        self.time_line_edit = QLineEdit()

        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)
        self.result_label = QLabel("")

        grid.addWidget(distance_label, 0, 0)
        grid.addWidget(self.distance_line_edit, 0, 1)
        grid.addWidget(self.combobox1, 0, 3)
        grid.addWidget(time, 1, 0)
        grid.addWidget(self.time_line_edit, 1, 1)
        grid.addWidget(calculate_button, 2, 1)
        grid.addWidget(self.result_label, 3, 0, 1, 3)

        self.setLayout(grid)

    def calculate(self):
        distance = float(self.distance_line_edit.text())
        time = float(self.time_line_edit.text())
        speed = distance/time

        if self.combobox1.currentText() == "Kilometre":
            speed = round(speed, 2)
            unit = "km/h"
        if self.combobox1.currentText() == "Miles":
            speed = round(speed * 0.621, 2)
            unit = 'mph'

        self.result_label.setText(f"Average Speed: {speed} {unit}")


app = QApplication(sys.argv)
speed_calculator = AvgSpeedCalculator()
speed_calculator.show()
sys.exit(app.exec())