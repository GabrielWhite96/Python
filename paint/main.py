import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QAction, QMenu, QMenuBar, QColorDialog, QWidget, QInputDialog
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt

class PaintApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Paint Clone')
        self.drawing_mode = True

        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)
        
        self.pen_color = Qt.black
        
        self.create_buttons()
        
    def create_buttons(self):
        brush_button = QPushButton(self)
        brush_button.setIcon(QIcon('icons/brush.png'))  
        brush_button.clicked.connect(self.toggle_brush)
        brush_button.setGeometry(20, 20, 40, 40)
        
        color_button = QPushButton(self)
        color_button.setIcon(QIcon('icons/palette.png'))  
        color_button.clicked.connect(self.change_color)
        color_button.setGeometry(20, 80, 40, 40)

        size_button = QPushButton(self)
        size_button.setIcon(QIcon('icons/ruler.png'))  
        size_button.clicked.connect(self.change_size)
        size_button.setGeometry(20, 140, 40, 40)

        eraser_button = QPushButton(self)
        eraser_button.setIcon(QIcon('icons/eraser.png'))  
        eraser_button.clicked.connect(self.toggle_eraser)
        eraser_button.setGeometry(20, 200, 40, 40)
        
        clearAction = QPushButton(self)
        clearAction.setIcon(QIcon('icons/broom.png'))  
        clearAction.clicked.connect(self.canvas.clear)
        clearAction.setGeometry(20, 260, 40, 40)
        
        undo_button = QPushButton(self)
        undo_button.setIcon(QIcon('icons/undo.png'))
        undo_button.clicked.connect(self.canvas.undo)
        undo_button.setGeometry(20, 320, 40, 40)

        redo_button = QPushButton(self)
        redo_button.setIcon(QIcon('icons/redo.png'))
        redo_button.clicked.connect(self.canvas.redo)
        redo_button.setGeometry(20, 380, 40, 40)

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
        self.undo_stack = []
        self.redo_stack = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.canvas)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_point = event.pos()
            self.undo_stack.append(self.canvas.copy())

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
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.update()

    def set_color(self, color):
        self.pen.setColor(color)

    def set_size(self, size):
        self.brush_size = size

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.canvas = self.undo_stack[-1]
            self.update()

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack.pop())
            self.canvas = self.undo_stack[-1]
            self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PaintApp()
    window.show()
    sys.exit(app.exec_())