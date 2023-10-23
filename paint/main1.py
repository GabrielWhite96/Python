import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QColorDialog, QWidget, QInputDialog
from PyQt5.QtGui import QPainter, QPen, QPixmap, QIcon
from PyQt5.QtCore import Qt

class PaintApp(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.button_info = [
            {"icon_path": 'icons/brush.png', "click_function": self.toggle_brush, "x": 20, "y": 20, "width": 40, "height": 40},
            {"icon_path": 'icons/palette.png', "click_function": self.change_color, "x": 20, "y": 80, "width": 40, "height": 40},
            {"icon_path": 'icons/ruler.png', "click_function": self.change_size, "x": 20, "y": 140, "width": 40, "height": 40},
            {"icon_path": 'icons/eraser.png', "click_function": self.toggle_eraser, "x": 20, "y": 200, "width": 40, "height": 40},
            {"icon_path": 'icons/broom.png', "click_function": self.canvas.clear, "x": 20, "y": 260, "width": 40, "height": 40}
        ]

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Paint Clone')
        self.drawing_mode = True

        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)
        
        self.pen_color = Qt.black
        
        for info in self.button_info:
            self.create_button(info["icon_path"], info["click_function"], info["x"], info["y"], info["width"], info["height"])
    
    def create_button(self, icon_path, click_function, x, y, width, height):
        button = QPushButton(self)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(click_function)
        button.setGeometry(x, y, width, height)
        return button

    def change_color(self):
        self.pen_color = QColorDialog.getColor()
        if self.pen_color.isValid():
            self.canvas.set_color(self.pen_color)

    def change_size(self):
        size, ok = QInputDialog.getInt(self, 'Brush Size', 'Enter brush size:')
        if ok:
            self.canvas.set_size(size)

    def toggle_eraser(self):
        self.drawing_mode = False

    def toggle_brush(self):
        self.drawing_mode = True
        self.canvas.set_color(self.pen_color)

class Canvas(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setGeometry(0, 0, parent.width(), parent.height())
        self.canvas = QPixmap(self.size())
        self.canvas.fill(Qt.white)
        self.last_point = None
        self.pen = QPen()
        self.pen.setColor(Qt.black)
        self.pen.setWidth(2)
        self.brush_size = 2

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.canvas)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) and self.last_point:
            painter = QPainter(self.canvas)
            painter.setPen(self.pen)
            painter.setBrush(self.pen.color())
            if self.parent().drawing_mode:
                painter.drawEllipse(event.pos(), self.brush_size, self.brush_size)
            else:
                self.pen.setColor(Qt.white)
                painter.drawEllipse(event.pos(), self.brush_size, self.brush_size)
            self.update()
            self.last_point = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = None

    def clear(self):
        self.canvas.fill(Qt.white)
        self.update()

    def set_color(self, color):
        self.pen.setColor(color)

    def set_size(self, size):
        self.brush_size = size

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PaintApp()
    window.show()
    sys.exit(app.exec_())
