from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor, QBrush


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

        # 创建主布局
        self.main_layout = QtWidgets.QVBoxLayout(self)
        
        # 添加标题栏
        from views.components.title_bar import CustomTitleBar
        title_bar = CustomTitleBar('收件人设置', self)
        self.main_layout.addWidget(title_bar)

        # 创建收件人表格
        self.recipient_table = QtWidgets.QTableWidget()
        self.recipient_table.setRowCount(recipient_count)
        self.recipient_table.setColumnCount(1)
        self.recipient_table.setHorizontalHeaderLabels(['收件人'])
        self.recipient_table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.recipient_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.recipient_table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.recipient_table.horizontalHeader().setStretchLastSection(True)
        self.recipient_table.horizontalHeader().setSectionsClickable(False)
        self.recipient_table.verticalHeader().setSectionsClickable(False)
        self.recipient_table.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; color: white')
        self.recipient_table.setObjectName('recipient_table')
        self.main_layout.addWidget(self.recipient_table)

        # 添加按钮布局
        button_layout = QtWidgets.QHBoxLayout()
        self.add_recipient_button = QtWidgets.QPushButton('添加收件人')
        self.delete_recipient_button = QtWidgets.QPushButton('删除收件人')
        
        # 设置按钮样式
        button_style = """
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
        """
        self.add_recipient_button.setStyleSheet(button_style)
        self.delete_recipient_button.setStyleSheet(button_style)
        
        button_layout.addWidget(self.add_recipient_button)
        button_layout.addWidget(self.delete_recipient_button)
        self.main_layout.addLayout(button_layout)
        
        # 确认取消按钮
        dialog_buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        dialog_buttons.setStyleSheet(button_style)
        self.main_layout.addWidget(dialog_buttons)

        # 设置布局边距
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 连接按钮信号
        self.add_recipient_button.clicked.connect(self.add_recipient)
        self.delete_recipient_button.clicked.connect(self.delete_recipient)

    def load_recipients(self, receivers):
        """加载收件人列表到表格"""
        self.recipient_table.setRowCount(0)
        for receiver in receivers:
            row = self.recipient_table.rowCount()
            self.recipient_table.insertRow(row)
            self.recipient_table.setItem(row, 0, QtWidgets.QTableWidgetItem(receiver.get('email', '')))
    
    def get_recipients(self):
        """获取表格中的收件人列表"""
        recipients = []
        for row in range(self.recipient_table.rowCount()):
            email = self.recipient_table.item(row, 0)
            if email and email.text().strip():
                recipients.append({'email': email.text().strip()})
        return recipients
    
    def add_recipient(self):
        """添加一个新的收件人行"""
        row = self.recipient_table.rowCount()
        self.recipient_table.insertRow(row)
        self.recipient_table.setItem(row, 0, QtWidgets.QTableWidgetItem(''))
        
        # 选中新行并开始编辑
        self.recipient_table.selectRow(row)
        self.recipient_table.editItem(self.recipient_table.item(row, 0))
    
    def delete_recipient(self):
        """删除选中的收件人行"""
        selected_rows = self.recipient_table.selectionModel().selectedRows()
        
        # 如果没有选中行，则提示用户
        if not selected_rows:
            QtWidgets.QMessageBox.information(self, '提示', '请先选择要删除的收件人')
            return
        
        # 确认删除
        reply = QtWidgets.QMessageBox.question(
            self, '确认删除', 
            f'确定要删除选中的 {len(selected_rows)} 个收件人吗？',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        # 如果用户确认，则删除选中行
        if reply == QtWidgets.QMessageBox.Yes:
            # 从后向前删除，避免索引变化
            for index in sorted([i.row() for i in selected_rows], reverse=True):
                self.recipient_table.removeRow(index)

    def paintEvent(self, event):
        """绘制对话框背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制圆角矩形背景
        rect = self.rect()
        color = QColor(50, 50, 50)  # 深色背景
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)

    def mousePressEvent(self, event):
        """处理鼠标按下事件，用于拖动窗口"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件，用于拖动窗口"""
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()