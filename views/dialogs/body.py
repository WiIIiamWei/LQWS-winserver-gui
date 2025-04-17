from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPainter, QColor, QBrush

from views.components.title_bar import CustomTitleBar


class MailBodyDialog(QtWidgets.QDialog):
    """邮件正文设置界面"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('邮件正文设置')
        self.resize(500, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)

        self.setMinimumSize(QSize(300, 100))

        # 创建主布局
        self.main_layout = QtWidgets.QVBoxLayout(self)
        
        # 添加标题栏
        title_bar = CustomTitleBar('邮件正文设置', self)
        self.main_layout.addWidget(title_bar)
        
        # 添加正文编辑器
        self.mail_body_text = QtWidgets.QTextEdit()
        self.mail_body_text.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; color: white')
        self.mail_body_text.setObjectName('mail_body_text')
        self.mail_body_text.setPlaceholderText('在此输入邮件正文内容...')
        self.main_layout.addWidget(self.mail_body_text)
        
        # 添加说明标签
        self.hint_label = QtWidgets.QLabel(
            '提示：您可以使用{字段名}作为占位符，发送邮件时会自动替换为实际数据。'
        )
        self.hint_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt; color: #cccccc;')
        self.hint_label.setWordWrap(True)
        self.main_layout.addWidget(self.hint_label)
        
        # 添加按钮布局
        self.button_layout = QtWidgets.QHBoxLayout()
        
        # 创建确认取消按钮
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
        
        self.ok_button = QtWidgets.QPushButton('确定')
        self.ok_button.setStyleSheet(button_style)
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QtWidgets.QPushButton('取消')
        self.cancel_button.setStyleSheet(button_style)
        self.cancel_button.clicked.connect(self.reject)
        
        self.button_layout.addWidget(self.ok_button)
        self.button_layout.addWidget(self.cancel_button)
        
        self.main_layout.addLayout(self.button_layout)
        
        # 设置布局边距
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        
        # 存储正文格式数据
        self.format_data = {}

    def load_body(self, format_dict):
        """从格式字典加载正文内容"""
        if not isinstance(format_dict, dict):
            format_dict = {}
            
        self.format_data = format_dict.copy()
        content = format_dict.get('content', '')
        self.mail_body_text.setText(content)
        
        # 如果有标题，显示在额外字段中
        if 'title' in format_dict:
            # 这里可以添加标题输入框，如果需要
            pass

    def get_body(self):
        """获取正文内容并返回格式字典"""
        # 获取当前文本内容
        content = self.mail_body_text.toPlainText()
        
        # 更新格式数据
        self.format_data['content'] = content
        
        # 如果需要添加其他格式相关的设置，可以在这里添加
        
        return self.format_data

    def paintEvent(self, event):
        """绘制对话框背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制圆角矩形背景
        rect = self.rect()
        color = QColor(50, 50, 50)  # 设置深色背景
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