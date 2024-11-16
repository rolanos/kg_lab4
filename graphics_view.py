from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QCursor
from PyQt5.QtCore import Qt, QRect, QPoint

class GraphicsView(QWidget):
    def __init__(self, lines, clipped_lines, clip_window, clip_window_visible=True):
        super().__init__()
        self.lines = lines
        self.clipped_lines = clipped_lines
        self.clip_window = QRect(*clip_window)  # Используем QRect для окна отсечения
        self.clip_window_visible = clip_window_visible
        self.dragging = False
        self.resizing = False
        self.resize_direction = None  # Направление изменения размера
        self.resize_margin = 10  # Ширина области захвата для изменения размера

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Выбираем цвет для всех отрезков в зависимости от видимости окна отсечения
        if self.clip_window_visible:
            # Синие линии для всех отрезков, зеленое окно, красные отсеченные отрезки
            pen = QPen(QColor(0, 0, 255), 2)
            painter.setPen(pen)
            for line in self.lines:
                x1, y1 = int(line[0][0]), int(line[0][1])
                x2, y2 = int(line[1][0]), int(line[1][1])
                painter.drawLine(x1, y1, x2, y2)

            # Отрисовка окна отсечения
            pen = QPen(QColor(0, 255, 0), 2, Qt.DashLine)
            painter.setPen(pen)
            painter.drawRect(self.clip_window)

            # Красные линии для отсеченных отрезков
            pen = QPen(QColor(255, 0, 0), 2)
            painter.setPen(pen)
            for line in self.clipped_lines:
                x1, y1 = int(line[0][0]), int(line[0][1])
                x2, y2 = int(line[1][0]), int(line[1][1])
                painter.drawLine(x1, y1, x2, y2)
        else:
            pen = QPen(QColor(0, 0, 255), 2)
            painter.setPen(pen)
            for line in self.lines:
                x1, y1 = int(line[0][0]), int(line[0][1])
                x2, y2 = int(line[1][0]), int(line[1][1])
                painter.drawLine(x1, y1, x2, y2)

    def set_clip_window_visible(self, visible):
        """Установка видимости окна отсечения."""
        self.clip_window_visible = visible
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.clip_window_visible:
            # Определяем направление изменения размера по позиции курсора
            if self.is_on_resize_corner(event.pos()):
                self.resizing = True
                self.resize_direction = "corner"
            elif self.is_on_resize_edge(event.pos()):
                self.resizing = True
            elif self.clip_window.contains(event.pos()):
                # Начинаем перетаскивание окна
                self.dragging = True
                self.drag_start = event.pos() - self.clip_window.topLeft()
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragging:
            # Перемещение окна отсечения
            self.clip_window.moveTopLeft(event.pos() - self.drag_start)
            self.update()
        elif self.resizing:
            # Изменение размера окна
            self.resize_clip_window(event.pos())
            self.update()
        elif self.clip_window_visible:
            # Обновляем курсор в зависимости от позиции
            if self.is_on_resize_corner(event.pos()):
                self.setCursor(QCursor(Qt.SizeFDiagCursor))
            elif self.is_on_resize_edge(event.pos()):
                self.setCursor(QCursor(Qt.SizeHorCursor if self.resize_direction in ["left", "right"] else Qt.SizeVerCursor))
            elif self.clip_window.contains(event.pos()):
                self.setCursor(QCursor(Qt.OpenHandCursor))
            else:
                self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.resizing = False
        self.resize_direction = None
        self.setCursor(QCursor(Qt.ArrowCursor))
        self.update_clipped_lines()  # Пересчитываем отсеченные линии после изменения размера или перемещения
        self.update()

    def is_on_resize_corner(self, pos):
        """Проверка, находится ли курсор в углу для изменения размера"""
        corner_area = QRect(self.clip_window.bottomRight() - QPoint(self.resize_margin, self.resize_margin),
                            self.clip_window.bottomRight())
        return corner_area.contains(pos)

    def is_on_resize_edge(self, pos):
        """Определение стороны окна отсечения для изменения размера"""
        if abs(pos.x() - self.clip_window.left()) < self.resize_margin:
            self.resize_direction = "left"
            return True
        elif abs(pos.x() - self.clip_window.right()) < self.resize_margin:
            self.resize_direction = "right"
            return True
        elif abs(pos.y() - self.clip_window.top()) < self.resize_margin:
            self.resize_direction = "top"
            return True
        elif abs(pos.y() - self.clip_window.bottom()) < self.resize_margin:
            self.resize_direction = "bottom"
            return True
        return False

    def resize_clip_window(self, pos):
        """Изменение размера окна в зависимости от направления"""
        if self.resize_direction == "left":
            self.clip_window.setLeft(pos.x())
        elif self.resize_direction == "right":
            self.clip_window.setRight(pos.x())
        elif self.resize_direction == "top":
            self.clip_window.setTop(pos.y())
        elif self.resize_direction == "bottom":
            self.clip_window.setBottom(pos.y())
        elif self.resize_direction == "corner":
            self.clip_window.setBottomRight(pos)

    def update_clipped_lines(self):
        """Обновляем список отсеченных отрезков, перерисовывая с новым окном"""
        from clipping_algorithm import ClippingAlgorithm  # Импорт внутри, чтобы избежать циклических зависимостей
        clipper = ClippingAlgorithm((self.clip_window.left(), self.clip_window.top(),
                                     self.clip_window.right(), self.clip_window.bottom()))
        self.clipped_lines = clipper.clip_lines(self.lines)
