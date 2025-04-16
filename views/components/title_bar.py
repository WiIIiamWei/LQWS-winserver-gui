from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent


class CustomTitleBar(QtWidgets.QWidget):
    # 标题栏
    def __init__(self, word, parent=None):
        super().__init__(parent)

        self.setFixedHeight(30)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.titleLabel = QtWidgets.QLabel(word)
        self.titleLabel.setStyleSheet("color: white; font-size: 15pt; font-weight: bold;")
        self.minimizeButton = QtWidgets.QPushButton("")
        self.minimizeButton.setFixedSize(30, 30)
        self.minimizeButton.setStyleSheet(
            "QPushButton{border-image:url('./images/min.png');background:#363636;border-radius:10px;}"  # 29c941
            "QPushButton:hover{background:#1ac033;}"
        )
        self.minimizeButton.clicked.connect(self.minimize)

        self.maximizeButton = QtWidgets.QPushButton("")
        self.maximizeButton.setFixedSize(30, 30)
        self.maximizeButton.setStyleSheet(
            "QPushButton{border-image:url('./images/max.png');background:#363636;border-radius:10px;}"
            "QPushButton:hover{background:#ecae27;}"
        )
        self.maximizeButton.clicked.connect(self.maximize_restore)

        self.closeButton = QtWidgets.QPushButton("")
        self.closeButton.setFixedSize(30, 30)
        self.closeButton.setStyleSheet(
            "QPushButton{border-image:url('./images/close.png');background:#363636;border-radius:10px;}"
            "QPushButton:hover{background:#eb4845;}"
        )
        self.closeButton.clicked.connect(self.close)

        layout.addWidget(self.titleLabel)
        layout.addStretch()
        layout.addWidget(self.minimizeButton)
        layout.addWidget(self.maximizeButton)
        layout.addWidget(self.closeButton)

        self.setLayout(layout)
        self.start = None
        self.pressing = False

    def minimize(self):
        # 界面最小化
        self.window().showMinimized()

    def maximize_restore(self):
        # 界面最大化
        if self.window().isMaximized():
            self.window().showNormal()
        else:
            self.window().showMaximized()

    def close(self):
        # 关闭界面
        self.window().close()

    def mousePressEvent(self, event: QMouseEvent):
        # 光标按下处理
        if event.button() == Qt.LeftButton:
            self.start = event.globalPos()
            self.pressing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        # 光标移动处理
        if self.pressing:
            self.window().move(self.window().pos() + event.globalPos() - self.start)
            self.start = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        # 光标松开处理
        self.pressing = False
