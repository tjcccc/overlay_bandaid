from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QCursor, QPaintEvent, QAction
from PyQt6.QtWidgets import QApplication, QWidget, QMenu


class Overlay(QWidget):
    def __init__(self):
        super().__init__()

        # self._alpha = 0.5
        self._drag_pos = None
        self._inside = False

        self.setWindowFlag(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating, True)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.default_opacity = 0.5
        self.hidden_opacity = 0
        self.opacity = self.default_opacity

        self.fade_after_ms = 3000
        self._hide_timer = QTimer(self)
        self._hide_timer.setSingleShot(True)
        self._hide_timer.timeout.connect(self._hide_now)

        self.menu = QMenu(self)
        quit_action = QAction("Quit", self.menu)
        quit_action.triggered.connect(QApplication.quit)
        self.menu.addAction(quit_action)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.resize(64, 32)

        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        self.show()


    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)
        color = QColor(0, 0, 0)
        # color.setAlpha(int(255 * self._alpha))
        color.setAlphaF(self.opacity)
        painter.fillRect(self.rect(), color)


    def enterEvent(self, _):
        self._inside = True
        if self._hide_timer.isActive():
            self._hide_timer.stop()
        if self.opacity != self.default_opacity:
            self.opacity = self.default_opacity
            self.update()


    def leaveEvent(self, _):
        self._inside = False
        if not self._hide_timer.isActive():
            self._hide_timer.start(self.fade_after_ms)


    def _hide_now(self):
        if not self._inside:
            if self.opacity != self.hidden_opacity:
                self.opacity = self.hidden_opacity
                self.update()


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


    def keyPressEvent(self, event):
        event.ignore()


    def keyReleaseEvent(self, event):
        event.ignore()

if __name__ == '__main__':
    import sys
    import os
    os.environ.setdefault("QC_QPA_PLATFORM", "wayland")
    app = QApplication(sys.argv)
    window = Overlay()
    sys.exit(app.exec())