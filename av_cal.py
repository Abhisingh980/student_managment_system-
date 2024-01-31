import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QComboBox, QPushButton


def get_value(s):
    if s in "miles":
        pass
    elif s in "kilometer":
        pass


class AvgCalculate(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("average speed calculator")
        self.select_value = None
        grid = QGridLayout()

        distance = QLabel("Speed")
        self.dis_text_box = QLineEdit(self)

        time = QLabel("Time(hr)")
        self.time_txt_box = QLineEdit(self)

        convert_button = QPushButton("calculate")
        convert_button.clicked.connect(self.calculate)

        self.result = QLabel()

        combox = QComboBox()
        combox.addItems(["miles", "kilometer"])
        combox.currentTextChanged.connect(self.select_box)

        grid.addWidget(distance, 0, 0)
        grid.addWidget(self.dis_text_box, 0, 1)
        grid.addWidget(time, 1, 0)
        grid.addWidget(self.time_txt_box, 1, 1)
        grid.addWidget(combox, 0, 2)
        grid.addWidget(convert_button, 2, 1)
        grid.addWidget(self.result, 3, 0, 1, 2)

        self.setLayout(grid)

    def select_box(self, select_value):
        self.select_value = select_value
        print(self.select_value)

    def calculate(self):
        distance = int(self.dis_text_box.text())
        time = int(self.time_txt_box.text())
        print(self.select_value)
        if self.select_value == None:
            self.result.setText(f"select the ...")
        elif self.select_value in "miles":
            miles_value = distance / 1.609
            avg = miles_value / time
            self.result.setText(f"Avg is {round(avg,2)} miles/hr")
        elif self.select_value in "kilometer":
            avg = distance / time
            self.result.setText(f"avg is {avg} Km/hr")


app = QApplication(sys.argv)
app_speed_avg = AvgCalculate()
app_speed_avg.show()
sys.exit(app.exec())
