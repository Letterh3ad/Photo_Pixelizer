from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QDial, QWidget, QLabel
from PySide6.QtCore import Qt

class ControlWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control Panel")
        self.setFixedSize(300, 300)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QVBoxLayout()

        # Dial and button layout
        dial_button_layout = QHBoxLayout()
        self.dial = QDial()
        self.dial.setRange(0, 100)
        self.dial.valueChanged.connect(self.dial_value_changed)
        self.dial_label = QLabel("Dial: 0")
        self.dial_label.setAlignment(Qt.AlignCenter)
        
        dial_button_layout.addWidget(self.dial)
        dial_button_layout.addWidget(self.dial_label)

        self.dial_button = QPushButton("Snap")
        self.dial_button.clicked.connect(self.dial_button_clicked)
        dial_button_layout.addWidget(self.dial_button)

        main_layout.addLayout(dial_button_layout)

        # Button grid layout (Up, Down, Left, Right)
        button_layout = QVBoxLayout()

        up_button = QPushButton("Up")
        up_button.clicked.connect(lambda: self.button_clicked("Up"))
        button_layout.addWidget(up_button, alignment=Qt.AlignHCenter)

        middle_layout = QHBoxLayout()
        Backwards_button = QPushButton("Backwards")
        Backwards_button.clicked.connect(lambda: self.button_clicked("Backwards"))
        middle_layout.addWidget(Backwards_button, alignment=Qt.AlignLeft)

        Forwards_button = QPushButton("Forwards")
        Forwards_button.clicked.connect(lambda: self.button_clicked("Forwards"))
        middle_layout.addWidget(Forwards_button, alignment=Qt.AlignRight)

        button_layout.addLayout(middle_layout)

        down_button = QPushButton("Down")
        down_button.clicked.connect(lambda: self.button_clicked("Down"))
        button_layout.addWidget(down_button, alignment=Qt.AlignHCenter)

        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)

    def button_clicked(self, button_name):
        print(button_name)

    def dial_value_changed(self):
        value = self.dial.value()
        self.dial_label.setText(f"Dial: {value}")
        print(f"Dial Value: {value}")

    def dial_button_clicked(self):
        print("Snap")

if __name__ == "__main__":
    app = QApplication([])
    window = ControlWindow()
    window.show()
    app.exec()
