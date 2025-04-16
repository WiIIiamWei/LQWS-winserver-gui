from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter

from views.components.title_bar import CustomTitleBar


class MailBodyDialog(QtWidgets.QDialog):
    # 邮件正文设置界面
    def __init__(self):
        super().__init__()
        self.setWindowTitle('邮件正文设置')
        self.resize(500, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.setMinimumSize(QSize(300, 100))

        title_bar = CustomTitleBar('邮件正文设置', self)

        self.second_layout = QtWidgets.QVBoxLayout(self)

        self.button_layout = QtWidgets.QHBoxLayout(self)
        alert_bridge_name_button = QtWidgets.QPushButton('桥梁名称')
        alert_test_point_button = QtWidgets.QPushButton('测试点')
        alert_level_button = QtWidgets.QPushButton('警报等级')
        alert_data_button = QtWidgets.QPushButton('警报数据')
        alert_bridge_name_button.setStyleSheet("""
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
        alert_test_point_button.setStyleSheet("""
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
        alert_level_button.setStyleSheet("""
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
        alert_data_button.setStyleSheet("""
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
        self.button_layout.addWidget(alert_bridge_name_button)
        self.button_layout.addWidget(alert_test_point_button)
        self.button_layout.addWidget(alert_level_button)
        self.button_layout.addWidget(alert_data_button)

        mail_body_text = QtWidgets.QTextEdit()
        mail_body_text.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; color: white')

        save_button = QtWidgets.QPushButton('保存')
        save_button.setStyleSheet("""
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

        self.second_layout.addWidget(title_bar)
        self.second_layout.addWidget(mail_body_text)
        self.second_layout.addLayout(self.button_layout)
        self.second_layout.addWidget(save_button)

        self.second_layout.setContentsMargins(20, 20, 20, 20)

        mail_body_text.setObjectName('mail_body_text')

    def load_body(self, format_dict):
        text_edit = self.findChild(QtWidgets.QTextEdit, 'mail_body_text')
        if text_edit:
            content = format_dict.get('content', '')
            text_edit.setText(content)

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
