from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from line_generator import LineGenerator
from clipping_algorithm import ClippingAlgorithm
from graphics_view import GraphicsView

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Отсечение отрезков прямоугольным окном")
        self.setGeometry(100, 100, 800, 600)

        # Параметры прямоугольного окна для отсечения
        self.clip_window = (200, 150, 600, 450)  # (x_min, y_min, x_max, y_max)
        self.clip_window_visible = True

        # Генерация случайных отрезков
        self.line_generator = LineGenerator(num_lines=20)
        self.lines = self.line_generator.generate_lines()

        # Применение алгоритма отсечения
        self.clipper = ClippingAlgorithm(self.clip_window)
        self.clipped_lines = self.clipper.clip_lines(self.lines)

        # Настройка интерфейса
        layout = QVBoxLayout()
        self.graphics_view = GraphicsView(self.lines, self.clipped_lines, self.clip_window, self.clip_window_visible)
        layout.addWidget(self.graphics_view)

        # Кнопка для управления видимостью окна отсечения
        self.toggle_button = QPushButton("Скрыть окно отсечения")
        self.toggle_button.clicked.connect(self.toggle_clip_window)
        layout.addWidget(self.toggle_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def toggle_clip_window(self):
        """Переключение видимости окна отсечения."""
        self.clip_window_visible = not self.clip_window_visible
        self.graphics_view.set_clip_window_visible(self.clip_window_visible)
        self.toggle_button.setText("Показать окно отсечения" if not self.clip_window_visible else "Скрыть окно отсечения")
        self.graphics_view.update()
