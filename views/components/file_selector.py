from PySide6 import QtWidgets
from PySide6.QtCore import Signal, QObject


class FileSelector(QObject):
    """文件选择器组件"""
    file_selected = Signal(str)  # 文件选择信号
    
    def __init__(self):
        super().__init__()
        # 创建布局
        self.layout = QtWidgets.QHBoxLayout()
        
        # 创建标签、输入框和按钮
        self.tip_label = QtWidgets.QLabel('配置文件路径：')
        self.tip_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        
        self.config_path = QtWidgets.QLineEdit()
        self.config_path.setPlaceholderText('输入文件路径')
        self.config_path.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; ')
        self.config_path.setObjectName('config_path')
        
        self.file_select_button = QtWidgets.QPushButton('选择...')
        self.file_select_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        
        # 添加到布局
        self.layout.addWidget(self.tip_label)
        self.layout.addWidget(self.config_path)
        self.layout.addWidget(self.file_select_button)
        
        # 连接信号
        self.file_select_button.clicked.connect(self.select_file)
    
    def get_layout(self):
        """获取布局"""
        return self.layout
    
    def get_file_path(self):
        """获取文件路径"""
        return self.config_path.text()
    
    def set_file_path(self, path):
        """设置文件路径"""
        self.config_path.setText(path)
    
    def select_file(self):
        """打开文件选择对话框"""
        file_path = QtWidgets.QFileDialog.getOpenFileName(
            None, '选择文件', './', 'JSON Files (*.json)')
        if file_path[0]:
            self.config_path.setText(file_path[0])
            self.file_selected.emit(file_path[0])