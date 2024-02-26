import sys
from PyQt6 import QtGui
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QIcon
from PyQt6.QtCore import Qt, QSize
from collections import deque

class PaintApp(QWidget):
    def __init__(self):
        super().__init__()

        self.__layout = QHBoxLayout()
        self.__options_layout = QVBoxLayout()
        self.__screen_label = QLabel()

        self.__shapes = deque()
        self.__current_shape = None
        self.__drawing = False
        self.__last_x = None
        self.__last_y = None

        self.__selected_action = 'Pencil'
        self.__selected_color = 'black'
        self.__selected_pencil_width = 6

        self.setLayout(self.__layout)
        self.create_options_layout()
        self.set_drawing_screen()

        self.create_button('icons/brushW.png', lambda: self.set_selected_action('Pencil'))
        self.create_button('icons/eraserW.png', lambda: self.set_selected_action('Eraser'))
        self.create_button('icons/squareW.png', lambda: self.set_selected_action('Square'))
        self.create_button('icons/lineW.png', lambda: self.set_selected_action('Line'))
        self.create_button('icons/triangleW.png', lambda: self.set_selected_action('Triangle'))
        self.create_button('icons/circleW.png', lambda: self.set_selected_action('Circle'))
        self.create_button('icons/colorsW.png', lambda: self.set_selected_action('Colors'))
        self.create_button('icons/sizeW.png', self.toggle_size_combobox)
        
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.__options_layout.addItem(spacer)
        
        self.size_combobox = QComboBox()
        self.size_combobox.addItems(['2', '4', '6', '8', '10'])
        self.size_combobox.currentIndexChanged.connect(self.update_pencil_size)
        self.size_combobox.hide()  # Inicialmente oculta o combobox
        self.size_combobox.setStyleSheet("""
            QComboBox {
                background-color: #1f1f1f;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px;
                font-size: 15px;
                width: 100%;
            }
            
            QComboBox:hover {
                background-color: #555; 
            }
        """)
        
    def toggle_size_combobox(self):
        self.size_combobox.hide() if self.size_combobox.isVisible() else self.size_combobox.show()

    def update_pencil_size(self, index):
        size = self.size_combobox.itemText(index)
        self.__selected_pencil_width = int(size)
        self.toggle_size_combobox()  # Oculta o combobox após a seleção

    def pencil_action(self, current_x, current_y):
        if self.__last_x is None:
            self.__last_x = current_x
            self.__last_y = current_y
            return

        self.__current_shape = {
            'type': 'Line',
            'color': self.__selected_color,
            'width': self.__selected_pencil_width,
            'start_x': self.__last_x,
            'start_y': self.__last_y,
            'end_x': current_x,
            'end_y': current_y
        }

        self.__last_x = current_x
        self.__last_y = current_y

        self.__shapes.append(self.__current_shape.copy())

    def eraser_action(self, current_x, current_y):
        self.__selected_color = 'white'
        self.pencil_action(current_x, current_y)
        self.__selected_color = 'black'

    def draw_square(self, current_x, current_y):
        if self.__last_x is None:
            self.__last_x = current_x
            self.__last_y = current_y
            return

        possible_x = current_x - self.__last_x
        possible_y = current_y - self.__last_y

        if possible_x > 1 and possible_y > 1:
            new_width = max(possible_x, possible_y)
            new_x = int(current_x - possible_x / 2)
            new_y = int(current_y - possible_y / 2)

            self.__current_shape = {
                'type': 'Square',
                'color': self.__selected_color,
                'width': new_width,
                'x': new_x,
                'y': new_y
            }

    def draw_line(self, current_x, current_y):
        if self.__last_x is None:
            self.__last_x = current_x
            self.__last_y = current_y
            return

        self.__current_shape = {
            'type': 'Line',
            'color': self.__selected_color,
            'width': self.__selected_pencil_width,
            'start_x': self.__last_x,
            'start_y': self.__last_y,
            'end_x': current_x,
            'end_y': current_y
        }

    def draw(self, pen, painter, shape):
        pen.setColor(QColor(shape['color']))
        pen.setWidth(shape['width'])
        painter.setPen(pen)

        if shape['type'] == 'Square':
            painter.drawPoint(shape['x'], shape['y'])
        elif shape['type'] == 'Line':
            painter.drawLine(shape['start_x'], shape['start_y'], shape['end_x'], shape['end_y'])

    def paintEvent(self, event):
        self.set_drawing_screen()
        self.canvas = self.__screen_label.pixmap()
        painter = QPainter(self.canvas)
        pen = QPen()
        painter.setPen(pen)

        for shape in self.__shapes:
            self.draw(pen, painter, shape)

        if self.__drawing and self.__current_shape is not None:
            self.draw(pen, painter, self.__current_shape)

        self.__screen_label.setPixmap(self.canvas)
        painter.end()

    def mouseMoveEvent(self, event):
        current_x = int(event.position().x()) - 52
        current_y = int(event.position().y()) - 12

        self.__drawing = True

        if self.__selected_action == 'Pencil':
            self.pencil_action(current_x, current_y)
        elif self.__selected_action == 'Eraser':
            self.eraser_action(current_x, current_y)
        elif self.__selected_action == 'Square':
            self.draw_square(current_x, current_y)
        elif self.__selected_action == 'Rect':
            self.draw_line(current_x, current_y)
        elif self.__selected_action == 'Circle':
            pass
        elif self.__selected_action == 'Triangle':
            pass
        elif self.__selected_action == 'Rect':
            pass

        self.update()

    def mouseReleaseEvent(self, event):
        if self.__drawing:
            self.__last_x = None
            self.__last_y = None
            self.__drawing = False
            self.__shapes.append(self.__current_shape.copy())
            self.__current_shape = None
            self.update()

    def set_selected_action(self, name):
        self.__selected_action = name

    def set_drawing_screen(self):
        self.canvas = QPixmap(800, 700)
        self.canvas.fill(Qt.GlobalColor.white)
        self.__screen_label.setPixmap(self.canvas)
        self.__layout.addWidget(self.__screen_label)
        self.setStyleSheet("background-color: #3d3d3d;")

    def create_options_layout(self):
        self.__layout.addLayout(self.__options_layout)

    def create_button(self, icon_path, func):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setStyleSheet("""
            QPushButton {
                background-color: #1f1f1f;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px;
            }
            
            QPushButton:hover {
                background-color: #555; 
            }
        """)
        button.setIconSize(QSize(20, 20))
        button.clicked.connect(func)
        self.__options_layout.addWidget(button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PaintApp()
    window.show()
    sys.exit(app.exec())
