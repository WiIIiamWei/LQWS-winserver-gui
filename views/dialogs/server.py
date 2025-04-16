from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter


class StartDialog(QtWidgets.QDialog):
    # 服务器运行界面
    def __init__(self):
        super().__init__()
        self.setWindowTitle('服务器运行')
        self.resize(500, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.setMinimumSize(QSize(300, 100))

        self.second_layout = QtWidgets.QVBoxLayout(self)

        log_display = QtWidgets.QTextEdit()
        log_display.setReadOnly(True)
        log_display.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; color: white')

        button_layout = QtWidgets.QHBoxLayout(self)
        restart_button = QtWidgets.QPushButton('重启服务器')
        stop_button = QtWidgets.QPushButton('停止服务器')  # 红色
        restart_button.setStyleSheet("""
            QPushButton {
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            color: white;
            }
            QPushButton:hover {
            background:#366ecc;
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
        """)
        stop_button.setStyleSheet("""
            QPushButton {
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            color: white;
            }
            QPushButton:hover {
            background:#eb4845;
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
        """)
        stop_button.clicked.connect(self.close)

        button_layout.addWidget(restart_button)
        button_layout.addWidget(stop_button)

        self.second_layout.addWidget(log_display)
        self.second_layout.addLayout(button_layout)

        self.second_layout.setContentsMargins(20, 20, 20, 20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the rounded rectangle background
        rect = self.rect()
        # color = QColor(255, 255, 255)  # Set the desired background color
        # painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
