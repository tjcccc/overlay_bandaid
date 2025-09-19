from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QCursor, QPaintEvent, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QMenu


class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        self._alpha = 0.2
        self._drag_pos = None

        self.setWindowFlag(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        self.menu = QMenu(self)
        quit_action = QAction("Quit", self.menu)
        quit_action.triggered.connect(QApplication.quit)
        self.menu.addAction(quit_action)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.resize(32, 16)

        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.show()

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        color = QColor(0, 0, 0)
        color.setAlpha(int(255 * self._alpha))
        painter.fillRect(self.rect(), color)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.setCursor(QCursor(Qt.CursorShape.ClosedHandCursor))
            wh = self.windowHandle()
            if wh is not None:
                wh.startSystemMove()
            e.accept()
        elif e.button() == Qt.MouseButton.RightButton:
            self.menu.popup(e.globalPosition().toPoint())
            e.accept()

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
            e.accept()


if __name__ == '__main__':
    import sys
    import os
    os.environ.setdefault("QC_QPA_PLATFORM", "wayland")
    app = QApplication(sys.argv)
    window = Overlay()
    sys.exit(app.exec())