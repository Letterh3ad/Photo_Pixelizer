import sys
import cv2
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QStackedWidget, QWidget, QVBoxLayout, QCheckBox, QLabel, QHBoxLayout, QSpinBox
from Pixelizer_Engine.Pixel_Methods import pixelate_frame_realtime

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Pixelation Tool")
        self.setGeometry(100, 100, 800, 600)

        self.camera = cv2.VideoCapture(0)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        main_page = QWidget()
        main_layout = QVBoxLayout()

        voronoi_button = QPushButton("Voronoi Pixelation")
        voronoi_button.clicked.connect(self.show_voronoi_page)

        pixelate_button = QPushButton("Standard Pixelation")
        pixelate_button.clicked.connect(self.show_pixelate_page)

        main_layout.addWidget(voronoi_button)
        main_layout.addWidget(pixelate_button)
        main_page.setLayout(main_layout)

        self.voronoi_page = QWidget()
        voronoi_layout = QVBoxLayout()
        voronoi_layout.addWidget(QPushButton("Back to Main", clicked=self.show_main_page))
        self.voronoi_page.setLayout(voronoi_layout)

        self.pixelate_page = QWidget()
        pixelate_layout = QVBoxLayout()

        self.realtime_checkbox = QCheckBox("Realtime Image")
        self.realtime_checkbox.stateChanged.connect(self.toggle_realtime)

        self.block_size_spinbox = QSpinBox()
        self.block_size_spinbox.setRange(2, 100)
        self.block_size_spinbox.setValue(32)
        self.block_size_spinbox.setPrefix("Block Size: ")

        self.video_layout = QHBoxLayout()

        self.original_video_label = QLabel()
        self.pixelated_video_label = QLabel()

        self.video_layout.addWidget(self.original_video_label)
        self.video_layout.addWidget(self.pixelated_video_label)

        pixelate_button = QPushButton("Pixelate Image")
        back_button = QPushButton("Back to Main", clicked=self.show_main_page)

        pixelate_layout.addWidget(self.realtime_checkbox)
        pixelate_layout.addWidget(self.block_size_spinbox)
        pixelate_layout.addLayout(self.video_layout)
        pixelate_layout.addWidget(pixelate_button)
        pixelate_layout.addWidget(back_button)

        self.pixelate_page.setLayout(pixelate_layout)

        self.stacked_widget.addWidget(main_page)
        self.stacked_widget.addWidget(self.voronoi_page)
        self.stacked_widget.addWidget(self.pixelate_page)

        self.stacked_widget.setCurrentWidget(main_page)

    def show_main_page(self):
        self.timer.stop()
        self.stacked_widget.setCurrentIndex(0)

    def show_voronoi_page(self):
        self.timer.stop()
        self.stacked_widget.setCurrentWidget(self.voronoi_page)

    def show_pixelate_page(self):
        self.stacked_widget.setCurrentWidget(self.pixelate_page)

    def toggle_realtime(self):
        if self.realtime_checkbox.isChecked():
            self.timer.start(30)
        else:
            self.timer.stop()
            self.original_video_label.clear()
            self.pixelated_video_label.clear()

    def update_frames(self):
        ret, frame = self.camera.read()
        if not ret:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame_rgb.shape
        step = channel * width

        original_image = QImage(frame_rgb.data, width, height, step, QImage.Format_RGB888)
        self.original_video_label.setPixmap(QPixmap.fromImage(original_image))

        block_size = self.block_size_spinbox.value()
        pixelated_frame = pixelate_frame_realtime(frame_rgb, block_size)
        pixelated_image = QImage(pixelated_frame.data, width, height, step, QImage.Format_RGB888)
        self.pixelated_video_label.setPixmap(QPixmap.fromImage(pixelated_image))

    def closeEvent(self, event):
        self.timer.stop()
        self.camera.release()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
