from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter

from views.components.title_bar import CustomTitleBar


class MailRecipientsDialog(QtWidgets.QDialog):
    # 收件人设置界面
    def __init__(self):
        super().__init__()
        self.setWindowTitle('收件人设置')
        self.resize(500, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.setMinimumSize(QSize(300, 100))

        recipient_count = 5

        title_bar = CustomTitleBar('收件人设置', self)

        self.second_layout = QtWidgets.QVBoxLayout(self)

        recipient_table = QtWidgets.QTableWidget()
        recipient_table.setRowCount(recipient_count)
        recipient_table.setColumnCount(1)
        recipient_table.setHorizontalHeaderLabels(['收件人'])
        recipient_table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        recipient_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        recipient_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        recipient_table.horizontalHeader().setStretchLastSection(True)
        recipient_table.horizontalHeader().setSectionsClickable(False)
        recipient_table.verticalHeader().setSectionsClickable(False)
        recipient_table.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; color: white')

        self.button_layout = QtWidgets.QHBoxLayout(self)
        add_recipient_button = QtWidgets.QPushButton('添加收件人')
        delete_recipient_button = QtWidgets.QPushButton('删除收件人')
        add_recipient_button.setStyleSheet("""
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
        delete_recipient_button.setStyleSheet("""
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
        self.button_layout.addWidget(add_recipient_button)
        self.button_layout.addWidget(delete_recipient_button)

        self.recipient_layout = QtWidgets.QVBoxLayout()
        self.recipient_layout.addWidget(recipient_table)

        self.second_layout.addWidget(title_bar)
        self.second_layout.addWidget(recipient_table)
        self.second_layout.addLayout(self.button_layout)

        self.second_layout.setContentsMargins(20, 20, 20, 20)

        # 为表格设置对象名
        recipient_table.setObjectName('recipient_table')

    def load_recipients(self, receivers):
        table = self.findChild(QtWidgets.QTableWidget, 'recipient_table')
        if table:
            table.setRowCount(0)
            for receiver in receivers:
                row = table.rowCount()
                table.insertRow(row)
                table.setItem(row, 0, QtWidgets.QTableWidgetItem(receiver.get('email', '')))

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
